"""Fetch archive dedup & cleanup script tests.

Run: blog/.venv/bin/python blog/test_fetch_dedup.py
"""

import hashlib
import json
import sys
import tempfile
from types import SimpleNamespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# fetch.py 顶层 import 根 .venv 才有的库；测试只跑纯函数与打桩路径，全部桩掉。
for _missing in ("yt_dlp", "yaml", "feedparser"):
    sys.modules.setdefault(_missing, SimpleNamespace())

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
import fetch
import cleanup_dup_archives as cleanup


def _suffix(item_id):
    return hashlib.sha1(item_id.encode("utf-8")).hexdigest()[:8]


def _write_dir(root, name, meta=None, transcript=None):
    d = root / name
    d.mkdir(parents=True, exist_ok=True)
    if meta is not None:
        (d / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    if transcript is not None:
        (d / "transcript.md").write_text(transcript, encoding="utf-8")
    return d


def _item(item_id="vidabc10001", platform="youtube", upload_date="20260101"):
    return fetch.VideoItem(
        id=item_id,
        url=f"https://www.youtube.com/watch?v={item_id}",
        title="测试视频",
        uploader="测试频道",
        platform=platform,
        upload_date=upload_date,
        duration=1200,
        thumbnail_url="",
        description="",
    )


VALID_TRANSCRIPT = """---
source_url: "https://www.youtube.com/watch?v=vidabc10001"
platform: youtube
transcript_source: whisper-local
---

[00:00:01] 这是一段已经付费/耗时换来的真实转录正文。
"""


def test_resolve_prefers_rewrite_complete():
    rid = "vidabc10001"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _write_dir(root, f"20260701-旧标题-{_suffix(rid)}",
                   {"id": rid, "rewrite_complete": True})
        _write_dir(root, f"20260709-新标题A-{_suffix(rid)}",
                   {"id": rid, "rewrite_complete": False})
        _write_dir(root, f"20260710-新标题B-{_suffix(rid)}",
                   {"id": rid, "rewrite_complete": False})
        got = fetch.resolve_archive_dir(root, rid)
        assert got is not None and got.name.startswith("20260701"), got
    print("✓ resolve 优先 rewrite_complete 的目录")


def test_resolve_all_stubs_picks_newest():
    rid = "vidabc10001"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _write_dir(root, f"20260708-标题-{_suffix(rid)}", {"id": rid, "rewrite_complete": False})
        _write_dir(root, f"20260710-标题-{_suffix(rid)}", {"id": rid, "rewrite_complete": False})
        got = fetch.resolve_archive_dir(root, rid)
        assert got is not None and got.name.startswith("20260710"), got
    print("✓ resolve 全 stub 时取目录名最新")


def test_resolve_no_hit_and_empty_id():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        assert fetch.resolve_archive_dir(root, "vidabc10001") is None
        _write_dir(root, f"20260710-别人-{_suffix('othervideo0')}",
                   {"id": "othervideo0", "rewrite_complete": True})
        assert fetch.resolve_archive_dir(root, "vidabc10001") is None
        assert fetch.resolve_archive_dir(root, "") is None
    print("✓ resolve 无命中/空 id 返回 None")


def test_resolve_suffix_collision_guarded_by_id_check():
    rid = "vidabc10001"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # 目录名后缀恰好等于 rid 的 sha1 前 8 位，但 metadata 里是另一个 id
        _write_dir(root, f"20260710-撞车-{_suffix(rid)}",
                   {"id": "different000", "rewrite_complete": True})
        assert fetch.resolve_archive_dir(root, rid) is None
    print("✓ resolve 后缀撞车被 metadata id 校验拦截")


def test_resolve_skips_corrupt_metadata():
    rid = "vidabc10001"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        bad = root / f"20260710-坏的-{_suffix(rid)}"
        bad.mkdir()
        (bad / "metadata.json").write_text("{not json", encoding="utf-8")
        assert fetch.resolve_archive_dir(root, rid) is None
        _write_dir(root, f"20260709-好的-{_suffix(rid)}", {"id": rid, "rewrite_complete": True})
        got = fetch.resolve_archive_dir(root, rid)
        assert got is not None and got.name.startswith("20260709"), got
    print("✓ resolve 跳过损坏 metadata")


def test_read_existing_transcript():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        d = _write_dir(root, "x", transcript=VALID_TRANSCRIPT)
        body, source = fetch.read_existing_transcript(d)
        assert body.startswith("[00:00:01]") and source == "whisper-local", (body[:30], source)

        d2 = _write_dir(root, "y", transcript="---\ntranscript_source: none\n---\n\n[转录获取失败: x]")
        assert fetch.read_existing_transcript(d2) == ("", "")
        d3 = _write_dir(root, "z", transcript="---\ntranscript_source: bibigpt\n---\n\n[无可用转录]")
        assert fetch.read_existing_transcript(d3) == ("", "")
        d4 = _write_dir(root, "w")  # 无 transcript.md
        assert fetch.read_existing_transcript(d4) == ("", "")
    print("✓ read_existing_transcript 识别有效正文与失败标记")


class _ForbiddenCall(BaseException):
    """继承 BaseException：穿透 process_item 转录链自身的 except Exception，
    被禁函数（尤其付费 BibiGPT）一旦触达立即在测试层炸出。"""


def _forbid(name):
    def _boom(*a, **kw):
        raise _ForbiddenCall(f"{name} 不应被调用")
    return _boom


def test_process_item_reuses_complete_dir_without_transcription():
    rid = "vidabc10001"
    old = {k: getattr(fetch, k) for k in (
        "ARCHIVE_DIR", "get_transcript_baoyu", "get_transcript_ytapi",
        "get_transcript_whisper", "get_transcript_bibigpt", "download_thumbnail")}
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fetch.ARCHIVE_DIR = root
            _write_dir(root, f"20260701-完整-{_suffix(rid)}",
                       {"id": rid, "rewrite_complete": True}, VALID_TRANSCRIPT)
            for fn in ("get_transcript_baoyu", "get_transcript_ytapi",
                       "get_transcript_whisper", "get_transcript_bibigpt",
                       "download_thumbnail"):
                setattr(fetch, fn, _forbid(fn))
            assert fetch.process_item(_item(rid)) is True
    finally:
        for k, v in old.items():
            setattr(fetch, k, v)
    print("✓ 复用 complete 目录直接跳过，不触任何转录")


def test_process_item_reused_stub_survives_rewrite_failure():
    """spec 硬约束：rmtree 只删本次新建目录；复用目录失败后原样保留、转录字节不变。"""
    rid = "vidabc10001"
    old = {k: getattr(fetch, k) for k in (
        "ARCHIVE_DIR", "subprocess", "get_transcript_baoyu", "get_transcript_ytapi",
        "get_transcript_whisper", "get_transcript_bibigpt", "download_thumbnail")}
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fetch.ARCHIVE_DIR = root
            stub = _write_dir(root, f"20260708-旧stub-{_suffix(rid)}",
                              {"id": rid, "rewrite_complete": False}, VALID_TRANSCRIPT)
            before = (stub / "transcript.md").read_bytes()
            # 有有效转录 → 整条转录链必须不被触碰（含付费 BibiGPT）
            for fn in ("get_transcript_baoyu", "get_transcript_ytapi",
                       "get_transcript_whisper", "get_transcript_bibigpt"):
                setattr(fetch, fn, _forbid(fn))
            fetch.download_thumbnail = lambda url, dest: False
            fetch.subprocess = SimpleNamespace(run=lambda *a, **kw: SimpleNamespace(
                returncode=1, stdout="", stderr="rewrite boom"))

            assert fetch.process_item(_item(rid)) is False
            assert stub.exists(), "复用目录不得被 rmtree"
            assert (stub / "transcript.md").read_bytes() == before, "转录必须字节不变"
    finally:
        for k, v in old.items():
            setattr(fetch, k, v)
    print("✓ 复用目录在 rewrite 失败后原样保留（rmtree 保护）")


def test_process_item_new_dir_still_cleaned_on_no_transcript():
    rid = "vidabc10001"
    old = {k: getattr(fetch, k) for k in (
        "ARCHIVE_DIR", "get_transcript_baoyu", "get_transcript_ytapi",
        "get_transcript_whisper", "get_transcript_bibigpt", "download_thumbnail")}

    def _fail(*a, **kw):
        raise RuntimeError("转录失败")

    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            fetch.ARCHIVE_DIR = root
            for fn in ("get_transcript_baoyu", "get_transcript_ytapi",
                       "get_transcript_whisper", "get_transcript_bibigpt"):
                setattr(fetch, fn, _fail)
            fetch.download_thumbnail = lambda url, dest: False

            assert fetch.process_item(_item(rid)) is None
            assert list(root.iterdir()) == [], "本次新建的空壳目录应被清理"
    finally:
        for k, v in old.items():
            setattr(fetch, k, v)
    print("✓ 新建目录无转录时仍被清理（旧行为保留）")


def test_cleanup_plan_and_dry_run():
    rid_a, rid_b = "vidaaa00001", "vidbbb00002"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _write_dir(root, f"20260701-A完整-{_suffix(rid_a)}",
                   {"id": rid_a, "rewrite_complete": True, "scores": {"x": 1},
                    "key_quotes": ["q"], "guest_info": [{"name": "g"}]})
        _write_dir(root, f"20260710-Astub-{_suffix(rid_a)}",
                   {"id": rid_a, "rewrite_complete": False})
        # 同组两份都 complete：保留后处理字段更全的那份（目录名更旧也该赢）
        _write_dir(root, f"20260702-B富-{_suffix(rid_b)}",
                   {"id": rid_b, "rewrite_complete": True, "scores": {"x": 1},
                    "scores_v1": {"y": 1}, "key_quotes_all": ["q"], "guest_info": [{}]})
        _write_dir(root, f"20260709-B穷-{_suffix(rid_b)}",
                   {"id": rid_b, "rewrite_complete": True})
        _write_dir(root, "20260703-单独一条-abcd1234", {"id": "solo0000001"})
        (root / "无metadata裸目录").mkdir()

        snapshot = sorted(p.name for p in root.iterdir())
        keep, move = cleanup.plan_cleanup(root)
        keep_names = {d.name for _, d in keep}
        move_names = {d.name for _, d in move}
        assert f"20260701-A完整-{_suffix(rid_a)}" in keep_names
        assert f"20260710-Astub-{_suffix(rid_a)}" in move_names
        assert f"20260702-B富-{_suffix(rid_b)}" in keep_names
        assert f"20260709-B穷-{_suffix(rid_b)}" in move_names
        assert "20260703-单独一条-abcd1234" not in keep_names | move_names

        # dry-run（默认）不动任何文件
        old_argv = sys.argv
        try:
            sys.argv = ["cleanup", "--archive", str(root)]
            cleanup.main()
        finally:
            sys.argv = old_argv
        assert sorted(p.name for p in root.iterdir()) == snapshot, "dry-run 不得动文件"
    print("✓ cleanup 分组/保留判定正确，dry-run 零改动")


def test_cleanup_apply_moves_to_quarantine_without_overwrite():
    rid = "vidaaa00001"
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        keep_dir = f"20260701-完整-{_suffix(rid)}"
        dup_dir = f"20260710-stub-{_suffix(rid)}"
        _write_dir(root, keep_dir, {"id": rid, "rewrite_complete": True, "scores": {"x": 1}})
        _write_dir(root, dup_dir, {"id": rid, "rewrite_complete": False}, VALID_TRANSCRIPT)
        # 二次运行场景：隔离区里已有同名目录
        (root / cleanup.QUARANTINE_NAME / dup_dir).mkdir(parents=True)

        old_argv = sys.argv
        try:
            sys.argv = ["cleanup", "--archive", str(root), "--apply"]
            cleanup.main()
        finally:
            sys.argv = old_argv

        assert (root / keep_dir).exists()
        assert not (root / dup_dir).exists()
        moved = root / cleanup.QUARANTINE_NAME / f"{dup_dir}-2"
        assert moved.exists(), "同名冲突应加序号后缀而非覆盖"
        assert (moved / "transcript.md").exists(), "移动必须保全文件"

        # 隔离区对所有单层读取链路不可见
        assert fetch.resolve_archive_dir(root, rid) == root / keep_dir
        visible = {p.parent.name for p in root.glob("*/metadata.json")}
        assert cleanup.QUARANTINE_NAME not in visible
        assert not any(cleanup.QUARANTINE_NAME in str(p) for p in root.glob("*/metadata.json"))
    print("✓ cleanup --apply 移动进隔离区，二次运行不覆盖，读取链路免疫")


if __name__ == "__main__":
    test_resolve_prefers_rewrite_complete()
    test_resolve_all_stubs_picks_newest()
    test_resolve_no_hit_and_empty_id()
    test_resolve_suffix_collision_guarded_by_id_check()
    test_resolve_skips_corrupt_metadata()
    test_read_existing_transcript()
    test_process_item_reuses_complete_dir_without_transcription()
    test_process_item_reused_stub_survives_rewrite_failure()
    test_process_item_new_dir_still_cleaned_on_no_transcript()
    test_cleanup_plan_and_dry_run()
    test_cleanup_apply_moves_to_quarantine_without_overwrite()
    print("\n全部通过 ✅")
