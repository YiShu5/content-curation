"""原文读取与缓存：Trafilatura 主路径，Jina Reader 兜底。

Jina Reader 路由改编自 Agent-Reach 的 ``channels/web.py``：
https://github.com/Panniantong/Agent-Reach/blob/e825f6740d24c6c315c3b0dc41907e6c87ff39a5/agent_reach/channels/web.py

Agent-Reach 的 MIT 许可说明见项目根目录 THIRD_PARTY_NOTICES.md。
Trafilatura 为 Apache-2.0 依赖：https://github.com/adbar/trafilatura
"""

import hashlib
import json
import time
from pathlib import Path

import requests


DATA_DIR = Path(__file__).parent / "data" / "source_cache"
CACHE_TTL = 7 * 86400
MIN_TEXT_CHARS = 240
MAX_TEXT_CHARS = 6000
_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
)


def _cache_path(url):
    key = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return DATA_DIR / f"{key}.json"


def _read_cache(url):
    path = _cache_path(url)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - float(data.get("fetched_at") or 0) <= CACHE_TTL:
            return data
    except (OSError, ValueError, json.JSONDecodeError):
        pass
    return None


def _write_cache(url, result):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "url": url,
        "fetched_at": time.time(),
        **result,
    }
    _cache_path(url).write_text(
        json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def _read_trafilatura(url):
    import trafilatura

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return ""
    return trafilatura.extract(
        downloaded,
        output_format="txt",
        include_comments=False,
        include_tables=False,
        favor_precision=True,
    ) or ""


def _read_jina(url):
    response = requests.get(
        f"https://r.jina.ai/{url}",
        headers={"User-Agent": _UA, "Accept": "text/plain"},
        timeout=30,
    )
    response.raise_for_status()
    return response.text


def read_original(url):
    """读取原始链接，返回 text/method/readable；任何失败都降级为空结果。"""
    if not str(url or "").startswith(("http://", "https://")):
        return {"text": "", "method": "invalid", "readable": False}
    cached = _read_cache(url)
    if cached is not None:
        return cached

    errors = []
    for method, reader in (("trafilatura", _read_trafilatura), ("jina", _read_jina)):
        try:
            text = " ".join((reader(url) or "").split()).strip()
            if len(text) >= MIN_TEXT_CHARS:
                return _write_cache(url, {
                    "text": text[:MAX_TEXT_CHARS],
                    "method": method,
                    "readable": True,
                })
        except Exception as exc:  # 原文核验失败不能拖垮整份日报
            errors.append(f"{method}:{type(exc).__name__}")

    return _write_cache(url, {
        "text": "",
        "method": "failed",
        "readable": False,
        "errors": errors,
    })
