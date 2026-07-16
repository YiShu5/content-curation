#!/usr/bin/env python3
"""盘中热度新高监控：轮询 AI HOT，刷新当日最高讨论度的新条目即时推送飞书。

用法：blog/.venv/bin/python blog/hot_watch.py [--dry-run]
配合 cron 每 30 分钟一轮（对齐上游 30 分钟缓存 TTL）。

与每日简报刻意不做跨系统去重：本监控给即时性（指向原始信源），
简报给沉淀观点（有闸门有加工），同一事件出现两次是互补而非重复。

退出码：0 正常（含播种/无事发生）；1 发送失败（已记 pending 下轮重试）；
        2 上游拉取失败（状态不动）。
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

ROOT = Path(__file__).resolve().parent.parent

# config.Config 在导入时读环境变量，dotenv 必须先于它加载
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / "config" / ".env")
except ImportError:
    pass

from config import Config  # noqa: E402
from today_signal import fetch_aihot  # noqa: E402

STATE_PATH = Path(__file__).resolve().parent / "data" / "hot_watch_state.json"

# 入围下限：只有「≥此分 且 刷新当日最高分」的新条目才推送（相对触发，抗分数尺度漂移；
# 2026-07 实测 AI HOT 48h 内最高仅 83 分，绝对高阈值会让监控永远不触发）
THRESHOLD = int(os.getenv("HOT_WATCH_THRESHOLD", "78"))
WINDOW_HOURS = int(os.getenv("HOT_WATCH_WINDOW_HOURS", "6"))
QUIET_HOURS = os.getenv("HOT_WATCH_QUIET", "")  # 如 "23-8"；空 = 全天实时
MAX_PER_MSG = int(os.getenv("HOT_WATCH_MAX_PER_MSG", "5"))
MAX_ATTEMPTS = int(os.getenv("HOT_WATCH_MAX_ATTEMPTS", "3"))
STATE_TTL_HOURS = int(os.getenv("HOT_WATCH_STATE_TTL_HOURS", "72"))


def item_key(item):
    """与 today_signal 同款去重键：sha1(url or title) 前 12 位。"""
    basis = str(item.get("url") or item.get("title") or "")
    return hashlib.sha1(basis.encode("utf-8")).hexdigest()[:12]


def load_state(path=STATE_PATH):
    """读状态；缺失/损坏/结构异常返回 None（触发静默播种，绝不洪水重发）。"""
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        print("[hot-watch] 状态文件损坏，将重新播种", file=sys.stderr)
        return None
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), dict):
        print("[hot-watch] 状态文件结构异常，将重新播种", file=sys.stderr)
        return None
    return payload


def save_state(state, path=STATE_PATH):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", dir=path.parent, suffix=".tmp", delete=False, encoding="utf-8"
        ) as handle:
            temp_path = Path(handle.name)
            json.dump(state, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        temp_path = None
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def is_quiet(now_local, quiet_spec=QUIET_HOURS):
    """解析 '23-8' 式跨零点区间；[start:00, end:00) 内为安静时段。"""
    spec = (quiet_spec or "").strip()
    if not spec:
        return False
    try:
        start_text, end_text = spec.split("-", 1)
        start, end = int(start_text), int(end_text)
    except ValueError:
        return False
    if start == end:
        return False
    hour = now_local.hour
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end


def prune_state(state, now, ttl_hours=STATE_TTL_HOURS):
    cutoff = now - timedelta(hours=ttl_hours)
    kept = {}
    for key, row in state.get("items", {}).items():
        latest = None
        for stamp in (row.get("first_over_at"), row.get("notified_at")):
            if not stamp:
                continue
            try:
                parsed = datetime.fromisoformat(stamp)
            except (TypeError, ValueError):
                continue
            if latest is None or parsed > latest:
                latest = parsed
        try:
            fresh = latest is None or latest >= cutoff
        except TypeError:
            fresh = True
        if fresh:
            kept[key] = row
    state["items"] = kept
    return state


def _safe_score(item):
    try:
        return int(item.get("score") or 0)
    except (TypeError, ValueError):
        return 0


def _champion_score(state, today):
    champ = state.get("champion") or {}
    if champ.get("date") != today:
        return 0
    try:
        return int(champ.get("score") or 0)
    except (TypeError, ValueError):
        return 0


def collect_pending(items, state, now, threshold=THRESHOLD):
    """当日冠军规则：「score ≥ 下限 且 刷新当日最高分」的新条目入库为 pending。

    - 冠军分按 Asia/Shanghai 自然日重置（跨零点后首条 ≥下限 的即当选）
    - 已见条目（key 在 state）分数后涨只静默抬高冠军线，不重推
    - 未当选的条目绝不入库——它日后真成了当日新高仍会触发
    - 当选条目字段全量快照进 state，滑出抓取窗口后重试仍能发出
    """
    today = now.date().isoformat()
    best = _champion_score(state, today)

    # 已通知过的新闻分数继续涨：抬线不重推，防止随后的次高分新条目冒充"新高"
    for item in items:
        score = _safe_score(item)
        if score >= threshold and item_key(item) in state["items"] and score > best:
            best = score

    champion_item = None
    for item in items:
        score = _safe_score(item)
        if score < threshold or score <= best:
            continue
        if item_key(item) in state["items"]:
            continue
        if champion_item is None or score > _safe_score(champion_item):
            champion_item = item

    if champion_item is not None:
        best = _safe_score(champion_item)
        state["items"][item_key(champion_item)] = {
            "title": str(champion_item.get("title") or "")[:120],
            "url": str(champion_item.get("url") or ""),
            "source": str(champion_item.get("source") or ""),
            "summary": str(champion_item.get("summary") or "")[:200],
            "score": best,
            "status": "pending",
            "first_over_at": now.isoformat(timespec="seconds"),
            "attempts": 0,
        }

    if best > 0:
        state["champion"] = {"date": today, "score": best}
    return state


def _detected_note(row, now):
    """检测时间与发送时间差超过 45 分钟时标注（夜间补报/重试补发的场景）。"""
    stamp = row.get("first_over_at")
    if not stamp:
        return ""
    try:
        first = datetime.fromisoformat(stamp)
        if now - first <= timedelta(minutes=45):
            return ""
        return f" · {first.strftime('%H:%M')} 检测"
    except (TypeError, ValueError):
        return ""


def _item_lines(row, now, number=None):
    prefix = f"{number}. " if number else ""
    indent = "   " if number else ""
    source = f" · {row['source']}" if row.get("source") else ""
    lines = [f"{prefix}{row['title']}（热度 {row['score']}{source}{_detected_note(row, now)}）"]
    summary = (row.get("summary") or "").strip()
    if summary:
        lines.append(f"{indent}{summary[:60]}")
    if row.get("url"):
        lines.append(f"{indent}{row['url']}")
    return lines


def format_message(batch, now_local, max_items=MAX_PER_MSG):
    header_time = now_local.strftime("%m-%d %H:%M")
    lines = []
    if len(batch) == 1:
        lines.append(f"🔥 盘中热度新高 {header_time}")
        lines.extend(_item_lines(batch[0], now_local))
    else:
        lines.append(f"🔥 盘中热度新高 {header_time}（{len(batch)} 条）")
        for index, row in enumerate(batch[:max_items], 1):
            lines.extend(_item_lines(row, now_local, number=index))
        rest = batch[max_items:]
        if rest:
            titles = " / ".join((row.get("title") or "")[:20] for row in rest)
            lines.append(f"另有 {len(rest)} 条超阈值：{titles}")
    return "\n".join(lines)


def send_feishu(text):
    script = ROOT / "scripts" / "notify-feishu.sh"
    result = subprocess.run([str(script), text], capture_output=True, text=True)
    if result.returncode != 0:
        if result.stderr:
            sys.stderr.write(result.stderr)
        return False
    return True


def run_once(*, fetch=None, send=None, now=None, state_path=STATE_PATH,
             threshold=THRESHOLD, quiet_spec=QUIET_HOURS,
             window_hours=WINDOW_HOURS, max_attempts=MAX_ATTEMPTS,
             max_per_msg=MAX_PER_MSG, ttl_hours=STATE_TTL_HOURS,
             dry_run=False):
    fetch = fetch or fetch_aihot
    send = send or send_feishu
    now = now or datetime.now(ZoneInfo(Config.BLOG_TIMEZONE))

    try:
        items = fetch(window_hours) or []
    except Exception as exc:
        print(f"[hot-watch] AI HOT 拉取失败：{exc}", file=sys.stderr)
        return 2

    state = load_state(state_path)
    if state is None:
        state = {
            "version": 1,
            "seeded_at": now.isoformat(timespec="seconds"),
            "items": {},
        }
        collect_pending(items, state, now, threshold)
        for row in state["items"].values():
            row["status"] = "seeded"
        save_state(state, state_path)
        champ = (state.get("champion") or {}).get("score", "无")
        print(f"[hot-watch] 首次运行：播种完成（当日冠军 {champ} 分），不通知")
        return 0

    collect_pending(items, state, now, threshold)
    prune_state(state, now, ttl_hours)

    if is_quiet(now, quiet_spec):
        save_state(state, state_path)
        pending = sum(1 for row in state["items"].values() if row.get("status") == "pending")
        print(f"[hot-watch] 安静时段，积攒 {pending} 条待补报")
        return 0

    batch_keys = [
        key for key, row in state["items"].items()
        if row.get("status") == "pending" and int(row.get("attempts") or 0) < max_attempts
    ]
    if not batch_keys:
        save_state(state, state_path)
        print("[hot-watch] 本轮无新巨热点")
        return 0

    batch_keys.sort(key=lambda key: -int(state["items"][key].get("score") or 0))
    batch = [state["items"][key] for key in batch_keys]
    text = format_message(batch, now, max_per_msg)

    if dry_run:
        save_state(state, state_path)
        print(f"[hot-watch] --dry-run 待发 {len(batch)} 条，消息预览：\n{text}")
        return 0

    if send(text):
        stamp = now.isoformat(timespec="seconds")
        for key in batch_keys:
            row = state["items"][key]
            row["status"] = "notified"
            row["notified_at"] = stamp
            row["attempts"] = int(row.get("attempts") or 0) + 1
        save_state(state, state_path)
        print(f"[hot-watch] 已推送 {len(batch_keys)} 条巨热点")
        return 0

    for key in batch_keys:
        row = state["items"][key]
        row["attempts"] = int(row.get("attempts") or 0) + 1
        if row["attempts"] >= max_attempts:
            row["status"] = "gave_up"
            print(f"[hot-watch] 重试 {row['attempts']} 次仍失败，放弃：{row['title']}", file=sys.stderr)
    save_state(state, state_path)
    print("[hot-watch] 发送失败，pending 保留待下轮重试", file=sys.stderr)
    return 1


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    return run_once(dry_run="--dry-run" in args)


if __name__ == "__main__":
    sys.exit(main())
