"""scripts 公共工具：环境配置 + DeepSeek 调用 + archive 遍历。

被 rescore.py / enrich-guests.py / select-quotes.py 复用，统一三者重复的脚手架。
（直接 `python scripts/xxx.py` 运行时，scripts/ 会自动进 sys.path，故可 `from _common import ...`）
"""
import json
import os
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).parent.parent
ARCHIVE_ROOT = PROJECT_ROOT / "archive"

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


def chat_json(prompt, temperature=0.3, timeout=120):
    """调用 DeepSeek（OpenAI 兼容）chat 接口，强制 JSON 输出，返回解析后的 dict。"""
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
    return json.loads(resp.json()["choices"][0]["message"]["content"])


def iter_metadata(dirs=None):
    """要处理的 metadata.json 路径列表：给定 dirs 用 dirs，否则扫描 archive/*。"""
    if dirs:
        return [Path(d) / "metadata.json" for d in dirs]
    return sorted(ARCHIVE_ROOT.glob("*/metadata.json"))
