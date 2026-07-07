"""单用户偏好配置与透明的行为权重。

不使用 Agent Memory：偏好来自可编辑的 config/preferences.json，以及
用户明确产生的点击/入库事件。没有操作不视为负反馈。
"""

import json
import time
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).parent.parent
PROFILE_PATH = ROOT / "config" / "preferences.json"
CLICK_LOG = Path(__file__).parent / "data" / "clicks.log"


def load_profile():
    """读取产品偏好；配置缺失时返回空结构，避免阻断每日任务。"""
    try:
        return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _parse_ts(value):
    try:
        return time.mktime(time.strptime(value, "%Y-%m-%d %H:%M:%S"))
    except (TypeError, ValueError):
        return 0


def behavior_summary(profile=None):
    """汇总最近一段时间的正向行为，供编辑排序使用。

    单次未点击的含义不明确，所以只累计显式正向动作，不生成负反馈。
    """
    profile = profile or load_profile()
    learning = profile.get("learning") or {}
    if not learning.get("enabled", True) or not CLICK_LOG.exists():
        return {"events_considered": 0, "slot_weights": {}, "source_weights": {}}

    days = int(learning.get("days") or 90)
    weights = learning.get("event_weights") or {}
    cutoff = time.time() - days * 86400
    slot_weights = defaultdict(float)
    source_weights = defaultdict(float)
    considered = 0

    try:
        lines = CLICK_LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        lines = []

    for line in lines[-2000:]:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if _parse_ts(event.get("ts")) < cutoff:
            continue
        weight = float(weights.get(event.get("kind"), 0) or 0)
        if weight <= 0:
            continue
        considered += 1
        slot = str(event.get("slot") or "").strip()
        source = str(event.get("source") or "").strip()
        if slot:
            slot_weights[slot] += weight
        if source:
            source_weights[source] += weight

    def _rounded(mapping):
        return {
            key: round(value, 1)
            for key, value in sorted(
                mapping.items(), key=lambda item: item[1], reverse=True)
        }

    return {
        "events_considered": considered,
        "slot_weights": _rounded(slot_weights),
        "source_weights": _rounded(source_weights),
    }


def prompt_context(profile=None):
    """生成简短、稳定的用户上下文，避免把完整日志塞给模型。"""
    profile = profile or load_profile()
    user = profile.get("user") or {}
    rules = profile.get("editorial_rules") or {}
    learning = behavior_summary(profile)
    return json.dumps({
        "role": user.get("role", "AI 产品经理"),
        "current_product": user.get("current_product", ""),
        "current_problem": user.get("current_problem", ""),
        "market": user.get("market", "全球市场"),
        "trend_horizon": user.get("trend_horizon", "未来 1–3 个月"),
        "prefer": rules.get("prefer", []),
        "reject": rules.get("reject", []),
        "observed_behavior": learning,
    }, ensure_ascii=False)
