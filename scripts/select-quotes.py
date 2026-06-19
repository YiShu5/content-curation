#!/usr/bin/env python3
"""
金句精选 - 让 DeepSeek 从已有金句中挑出最精华的 N 条（默认 3）

- 通过返回「序号」选择，原句文字保持不变（不改写）
- 备份原始金句到 key_quotes_all，幂等且可回退
- 选出的 N 条按重要性排序写回 key_quotes

用法:
  .venv/bin/python scripts/select-quotes.py [--n 3] [--force] [archive_dir ...]
"""
import json
import os
import sys
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).parent.parent
try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / "config" / ".env")
except ImportError:
    pass

API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("OPENAI_MODEL", "deepseek-chat")

PROMPT = """你是中文内容编辑。下面是一期节目《{title}》提炼出的若干条金句。
请从中挑选出**最精华、最有代表性、最能引发思考**的 {n} 条。

【要求】
1. 只做挑选，不要改写任何文字。
2. 通过序号选择，按你认为的重要性从高到低排序。
3. 只输出 JSON，格式：{{"indices":[序号, 序号, ...]}}（序号基于下面列表的编号）。

金句列表：
{quotes}
"""


def select(title, quotes, n):
    numbered = "\n".join(f"{i+1}. {q}" for i, q in enumerate(quotes))
    content = (PROMPT
               .replace("{title}", title or "")
               .replace("{n}", str(n))
               .replace("{quotes}", numbered))
    resp = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": content}],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        },
        timeout=120,
    )
    resp.raise_for_status()
    data = json.loads(resp.json()["choices"][0]["message"]["content"])
    idx = data.get("indices", [])
    picked = []
    for i in idx:
        if isinstance(i, int) and 1 <= i <= len(quotes) and quotes[i - 1] not in picked:
            picked.append(quotes[i - 1])
    return picked[:n]


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    n = 3
    if "--n" in argv:
        n = int(argv[argv.index("--n") + 1])
    dirs = [a for a in argv if not a.startswith("--") and a != str(n)]

    if not API_KEY:
        print("[ERROR] 未配置 OPENAI_API_KEY")
        sys.exit(1)

    metas = ([Path(d) / "metadata.json" for d in dirs] if dirs
             else sorted((PROJECT_ROOT / "archive").glob("*/metadata.json")))

    done = skipped = failed = 0
    for mp in metas:
        if not mp.exists():
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        # 原始金句来源：优先备份字段，保证可重复执行
        source = m.get("key_quotes_all") or m.get("key_quotes") or []
        if not m.get("rewrite_complete") or not source:
            continue
        if len(source) <= n and not force:
            skipped += 1
            continue
        if m.get("key_quotes_all") and len(m.get("key_quotes", [])) == n and not force:
            skipped += 1
            continue
        title = m.get("chinese_title") or m.get("title") or ""
        try:
            picked = select(title, source, n)
            if not picked:
                raise RuntimeError("未返回有效序号")
            m.setdefault("key_quotes_all", source)
            m["key_quotes"] = picked
            mp.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  [金句] {title[:28]}：{len(source)} → {len(picked)} 条")
            done += 1
        except Exception as e:
            print(f"  [WARN] {title[:28]} 失败: {e}")
            failed += 1

    print(f"\n完成: 精选 {done}，跳过 {skipped}，失败 {failed}")


if __name__ == "__main__":
    main()
