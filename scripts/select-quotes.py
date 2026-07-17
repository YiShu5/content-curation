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
import sys

from _common import chat_json, iter_metadata, require_api_key

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
    data = chat_json(content, temperature=0.2)
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

    require_api_key()
    metas = iter_metadata(dirs)

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
            # key_quotes_source 与 key_quotes 必须等长同序（rewrite 的配对承诺），精选后同步重排
            origin_sources = m.get("key_quotes_source_all") or m.get("key_quotes_source") or []
            if origin_sources and len(origin_sources) == len(source):
                m.setdefault("key_quotes_source_all", origin_sources)
                m["key_quotes_source"] = [origin_sources[source.index(q)] for q in picked]
            mp.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"  [金句] {title[:28]}：{len(source)} → {len(picked)} 条")
            done += 1
        except Exception as e:
            print(f"  [WARN] {title[:28]} 失败: {e}")
            failed += 1

    print(f"\n完成: 精选 {done}，跳过 {skipped}，失败 {failed}")


if __name__ == "__main__":
    main()
