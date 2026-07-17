#!/usr/bin/env python3
"""
重算评分 - 按新评分体系（洞察原创50 / 信源质量25 / 故事可读25）给已归档内容打分

- 题材（是否 AI）不进评分，用 topic 标签区分
- 基于已有 deep_summary + key_insights 打分，不重跑整条流水线
- 首次运行把旧评分备份到 scores_v1，可回退
- 写回 scores / score_total / score_verdict

用法:
  .venv/bin/python scripts/rescore.py [--force] [archive_dir ...]
"""
import json
import sys
from pathlib import Path

from _common import chat_json, iter_metadata, require_api_key

PROMPT = """你是严格的中文内容评审。请对下面这期内容打分。

【核心原则】评分只衡量"内容本身有多值得花时间"，**与题材无关**。一个顶级的投资或游戏访谈完全可以拿满分；一个全程讲 AI 但空洞的视频应该低分。不要因为是不是 AI 而拔高或压低。

【三个维度，满分 100】

1. insight 洞察原创（0-50，最重要）：认知增量。是否有范式级/反直觉/重新定义概念的洞察，而非常识复述。
   43-50 范式级且论证扎实｜33-42 多个非显然洞察｜23-32 有一两个亮点但整体常规｜12-22 偏常识｜0-11 几乎无增量

2. source 信源质量（0-25）：信息的稀缺性与一手性。嘉宾是否该领域当事人/权威、是否亲历的一手经验。
   只根据内容体现的信息判断，不靠外部知识臆测，不因"名气大"给高分，看一手性与稀缺性。
   21-25 顶级一手｜14-20 可靠一手｜7-13 多为二手观点｜0-6 来源弱/泛泛

3. storytelling 故事可读（0-25）：叙事质量、案例张力、可读性。
   21-25 极佳｜14-20 良好｜7-13 一般｜0-6 弱

total = 三者之和。verdict 按 total：≥90 必读｜75-89 强烈推荐｜60-74 推荐｜45-59 一般｜<45 可跳过。

每个维度给 1-2 句具体 reason，不能写空话。只输出 JSON：
{"insight":{"score":0,"reason":""},"source":{"score":0,"reason":""},"storytelling":{"score":0,"reason":""},"total":0,"verdict":""}

==== 内容信息 ====
标题：{title}
嘉宾：{guests}

深度摘要 + 关键洞察：
{body}
"""

# 维度上限与评级阈值单源于 config/product_schema.json（与 rewrite.js 共用）
_SCHEMA = json.loads(
    (Path(__file__).resolve().parent.parent / "config" / "product_schema.json")
    .read_text(encoding="utf-8"))
DIMENSIONS = [(d["key"], d["max"]) for d in _SCHEMA["score_dimensions"]]
VERDICTS = [(t["min"], t["label"]) for t in _SCHEMA["verdict_thresholds"]]


def verdict_of(total):
    for thr, label in VERDICTS:
        if total >= thr:
            return label
    return "可跳过"


def rescore(title, guests, body):
    content = (PROMPT
               .replace("{title}", title or "")
               .replace("{guests}", "、".join(guests) if guests else "（无具名嘉宾）")
               .replace("{body}", (body or "")[:6000]))
    d = chat_json(content, temperature=0.2)

    def dim(key, cap):
        o = d.get(key) or {}
        try:
            sc = max(0, min(int(o.get("score", 0)), cap))
        except (TypeError, ValueError):
            sc = 0
        return {"score": sc, "reason": (o.get("reason") or "").strip()}

    dims = {key: dim(key, cap) for key, cap in DIMENSIONS}
    total = sum(v["score"] for v in dims.values())
    return {**dims, "total": total, "verdict": verdict_of(total)}


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    dirs = [a for a in argv if not a.startswith("--")]

    require_api_key()
    metas = iter_metadata(dirs)

    done = skipped = failed = 0
    for mp in metas:
        if not mp.exists():
            continue
        m = json.loads(mp.read_text(encoding="utf-8"))
        if not m.get("rewrite_complete"):
            continue
        # 已是新体系（有 insight 维度）且非强制 → 跳过
        if isinstance(m.get("scores"), dict) and "insight" in m["scores"] and not force:
            skipped += 1
            continue
        body = (m.get("deep_summary") or "")
        if m.get("key_insights"):
            body += "\n\n" + m["key_insights"]
        if not body.strip():
            skipped += 1
            continue
        title = m.get("chinese_title") or m.get("title") or ""
        try:
            new = rescore(title, m.get("guests") or [], body)
            # 首次备份旧评分
            if "scores_v1" not in m and isinstance(m.get("scores"), dict):
                m["scores_v1"] = m["scores"]
                m["score_total_v1"] = m.get("score_total")
            m["scores"] = new
            m["score_total"] = new["total"]
            m["score_verdict"] = new["verdict"]
            mp.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
            old = m.get("score_total_v1")
            print(f"  [评分] {title[:26]:<28} {str(old):>4} → {new['total']:>3} "
                  f"({new['verdict']})  洞察{new['insight']['score']}/信源{new['source']['score']}/故事{new['storytelling']['score']}")
            done += 1
        except Exception as e:
            print(f"  [WARN] {title[:26]} 失败: {e}")
            failed += 1

    print(f"\n完成: 重算 {done}，跳过 {skipped}，失败 {failed}")


if __name__ == "__main__":
    main()
