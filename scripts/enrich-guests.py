#!/usr/bin/env python3
"""
嘉宾信息增强 - 从已有的深度摘要为每位嘉宾生成「身份头衔 + 背景 + 本期角色」

读取 archive/*/metadata.json（需 rewrite_complete 且有 guests），调用 DeepSeek
基于 deep_summary + key_insights 生成结构化 guest_info，写回 metadata.json。

- 幂等：已有 guest_info 时跳过，除非传 --force
- 强约束：只能基于摘要，不得编造摘要中没有的具体头衔（未知则留空/写参与讨论）

用法:
  .venv/bin/python scripts/enrich-guests.py [--force] [archive_dir ...]
"""
import json
import os
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).parent.parent

# 加载 config/.env
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / "config" / ".env")
except ImportError:
    pass

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("OPENAI_MODEL", "deepseek-chat")

PROMPT = """你是中文内容编辑。下面是一期节目/视频的信息，请为每位嘉宾生成结构化介绍。

【严格要求】
1. 所有输出字段（title/bio/relevance）必须用**简体中文**，无论摘要原文是中文还是英文，一律翻译成中文表达；专有名词（公司名/产品名）可保留英文。
2. 只能基于给定的「标题」和「深度摘要」来写，绝对不要编造摘要中无法推断的具体头衔、公司、履历。
3. 如果摘要里看不出某位嘉宾的明确身份，title 留空字符串，bio 用一句中性描述（如"本期节目嘉宾"）。
4. relevance 必须紧扣这期内容——这位嘉宾在本期主要谈了什么、扮演什么角色，1-2 句。
5. name 保留给定的嘉宾名；若是知名人物且有通用中文名，可用中文名（如 Jensen Huang→黄仁勋）。
6. 只输出 JSON，格式：{"guests":[{"name":"","title":"","bio":"","relevance":""}, ...]}

【视频标题】
{title}

【嘉宾名单】
{guests}

【深度摘要】
{summary}
"""


def gen_guest_info(title, guests, summary):
    content = (PROMPT
               .replace("{title}", title or "")
               .replace("{guests}", "、".join(guests))
               .replace("{summary}", (summary or "")[:4000]))
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": content}],
            "response_format": {"type": "json_object"},
            "temperature": 0.3,
        },
        timeout=120,
    )
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"]
    data = json.loads(raw)
    out = data.get("guests", [])
    # 规范化字段
    cleaned = []
    for g in out:
        if not isinstance(g, dict):
            continue
        cleaned.append({
            "name": (g.get("name") or "").strip(),
            "title": (g.get("title") or "").strip(),
            "bio": (g.get("bio") or "").strip(),
            "relevance": (g.get("relevance") or "").strip(),
        })
    return cleaned


def main():
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv

    if not API_KEY:
        print("[ERROR] 未配置 OPENAI_API_KEY")
        sys.exit(1)

    if args:
        metas = [Path(a) / "metadata.json" for a in args]
    else:
        metas = sorted((PROJECT_ROOT / "archive").glob("*/metadata.json"))

    done = skipped = failed = 0
    for mp in metas:
        if not mp.exists():
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        guests = m.get("guests") or []
        if not m.get("rewrite_complete") or not guests:
            continue
        if m.get("guest_info") and not force:
            skipped += 1
            continue
        title = m.get("chinese_title") or m.get("title") or ""
        summary = m.get("deep_summary") or ""
        if m.get("key_insights"):
            summary = summary + "\n\n" + m["key_insights"]
        try:
            print(f"  [嘉宾] {title[:30]} ← {guests}")
            info = gen_guest_info(title, guests, summary)
            m["guest_info"] = info
            mp.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
            for g in info:
                print(f"      · {g['name']}｜{g['title'] or '(无头衔)'}")
            done += 1
        except Exception as e:
            print(f"      [WARN] 失败: {e}")
            failed += 1

    print(f"\n完成: 生成 {done}，跳过 {skipped}，失败 {failed}")


if __name__ == "__main__":
    main()
