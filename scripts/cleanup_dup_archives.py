#!/usr/bin/env python3
"""清理 archive 里同一内容 id 的重复目录（历史上因日期/标题漂移重复抓出来的）。

用法:
  blog/.venv/bin/python scripts/cleanup_dup_archives.py            # dry-run，只打印清单
  blog/.venv/bin/python scripts/cleanup_dup_archives.py --apply    # 执行移动

每组重复只保留一份：优先 rewrite_complete=True，其次后处理字段
（scores/scores_v1/key_quotes/key_quotes_all/guest_info/core_ideas/deep_summary）
最全，并列时目录名最新。其余目录**移动**到 archive/_duplicates_quarantine/，
绝不删除——转录是付费资产，archive 被 gitignore、没有 git 兜底。
"""

import argparse
import json
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
ARCHIVE_DIR = PROJECT_ROOT / "archive"
QUARANTINE_NAME = "_duplicates_quarantine"

# 越靠后的处理阶段字段越说明这份归档「更完整」
RICHNESS_FIELDS = ("scores", "scores_v1", "key_quotes", "key_quotes_all",
                   "guest_info", "core_ideas", "deep_summary")

# 保留者优先级与 fetch.resolve_archive_dir 的复用优先级同源
# （rewrite_complete 优先、目录名最新兜底），此处额外考虑：
# - feishu_synced/feishu_doc_synced：sync-feishu*.js 只新建不更新，
#   保留未同步份会让下次 sync 制造飞书重复记录（CLAUDE.md 的坑）
# - richness：后处理字段更全的份


def _keeper_key(entry):
    d, meta = entry
    return (
        bool(meta.get("rewrite_complete")),
        bool(meta.get("feishu_synced")) or bool(meta.get("feishu_doc_synced")),
        _richness(meta),
        d.name,
    )


def _load_meta(d: Path):
    try:
        return json.loads((d / "metadata.json").read_text(encoding="utf-8"))
    except Exception:
        return None


def _richness(meta: dict) -> int:
    return sum(1 for f in RICHNESS_FIELDS if meta.get(f))


def collect_groups(archive_root: Path) -> dict:
    """按 metadata 的 id 分组（单层扫描，不进隔离区）。返回 {id: [(dir, meta), ...]}"""
    groups = {}
    for d in sorted(archive_root.iterdir()):
        if not d.is_dir() or d.name == QUARANTINE_NAME:
            continue
        meta = _load_meta(d)
        if meta is None:
            print(f"[跳过] 无有效 metadata.json: {d.name}")
            continue
        rid = str(meta.get("id") or "")
        if not rid:
            print(f"[跳过] metadata 无 id: {d.name}")
            continue
        groups.setdefault(rid, []).append((d, meta))
    return groups


def plan_cleanup(archive_root: Path):
    """返回 (保留清单, 移动清单)：[(id, dir)], [(id, dir)]"""
    keep, move = [], []
    for rid, entries in collect_groups(archive_root).items():
        if len(entries) == 1:
            continue
        entries.sort(key=_keeper_key, reverse=True)
        keep.append((rid, entries[0][0]))
        move.extend((rid, d) for d, _ in entries[1:])
    return keep, move


def quarantine_target(quarantine: Path, name: str) -> Path:
    """隔离区同名目录已存在（二次运行）时加序号后缀，绝不覆盖。"""
    target = quarantine / name
    n = 2
    while target.exists():
        target = quarantine / f"{name}-{n}"
        n += 1
    return target


def main():
    parser = argparse.ArgumentParser(description="按 id 去重 archive 目录（默认 dry-run）")
    parser.add_argument("--apply", action="store_true", help="真正执行移动（默认只打印清单）")
    parser.add_argument("--archive", default=str(ARCHIVE_DIR), help="archive 根目录（测试用）")
    args = parser.parse_args()

    archive_root = Path(args.archive)
    if not archive_root.is_dir():
        raise SystemExit(f"archive 目录不存在: {archive_root}")

    keep, move = plan_cleanup(archive_root)
    if not move:
        print("没有发现重复目录，无需清理。")
        return

    print(f"\n发现 {len(keep)} 组重复，共 {len(move)} 个冗余目录：\n")
    for rid, kd in keep:
        print(f"[保留] {rid}: {kd.name}")
        for mid, md in move:
            if mid == rid:
                print(f"    [移动] {md.name}")

    if not args.apply:
        print(f"\ndry-run 结束（未动任何文件）。确认无误后加 --apply 执行移动到 "
              f"{archive_root / QUARANTINE_NAME}/。")
        return

    quarantine = archive_root / QUARANTINE_NAME
    quarantine.mkdir(exist_ok=True)
    for _, md in move:
        target = quarantine_target(quarantine, md.name)
        shutil.move(str(md), str(target))
        print(f"[已移动] {md.name} -> {target.relative_to(archive_root)}")
    print(f"\n完成：{len(move)} 个目录已移入隔离区（未删除任何文件）。")


if __name__ == "__main__":
    main()
