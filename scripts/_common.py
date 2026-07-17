"""scripts 公共工具：环境配置 + DeepSeek 调用 + archive 遍历。

被 rescore.py / enrich-guests.py / select-quotes.py 复用，统一三者重复的脚手架。
（直接 `python scripts/xxx.py` 运行时，scripts/ 会自动进 sys.path，故可 `from _common import ...`）
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).parent.parent
ARCHIVE_ROOT = PROJECT_ROOT / "archive"
LLM_LOG = PROJECT_ROOT / "blog" / "data" / "llm_calls.jsonl"


def log_llm_call(record):
    """LLM 调用观测日志（与 blog/today_signal.py、scripts/rewrite.js 同一 jsonl）。
    日志写入失败绝不影响主流程。"""
    try:
        LLM_LOG.parent.mkdir(parents=True, exist_ok=True)
        with LLM_LOG.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass

# 加载 config/.env
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / "config" / ".env")
except ImportError:
    pass

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("OPENAI_MODEL", "deepseek-chat")


def require_api_key():
    """未配置 key 时打印错误并退出（三个脚本统一行为）"""
    if not API_KEY:
        print("[ERROR] 未配置 OPENAI_API_KEY")
        sys.exit(1)


def chat_json(prompt, temperature=0.3, timeout=120, caller=None):
    """调用 DeepSeek（OpenAI 兼容）chat 接口，强制 JSON 输出，返回解析后的 dict。"""
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "caller": caller or Path(sys.argv[0]).stem or "scripts",
        "model": MODEL,
        "temperature": temperature,
        "prompt_chars": len(prompt),
    }
    start = time.time()
    try:
        resp = requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "response_format": {"type": "json_object"},
                "temperature": temperature,
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        payload = resp.json()
        content = payload["choices"][0]["message"]["content"]
        usage = payload.get("usage") or {}
        record.update(
            ms=int((time.time() - start) * 1000),
            completion_chars=len(content),
            prompt_tokens=usage.get("prompt_tokens"),
            completion_tokens=usage.get("completion_tokens"),
        )
        return json.loads(content)
    except Exception as exc:
        record.update(ms=int((time.time() - start) * 1000), error=str(exc)[:200])
        raise
    finally:
        log_llm_call(record)


def iter_metadata(dirs=None):
    """要处理的 metadata.json 路径列表：给定 dirs 用 dirs，否则扫描 archive/*。"""
    if dirs:
        return [Path(d) / "metadata.json" for d in dirs]
    return sorted(ARCHIVE_ROOT.glob("*/metadata.json"))
