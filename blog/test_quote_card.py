"""金句卡参数化 CLI（make_quote_shots.py）的离线测试。

运行：blog/.venv/bin/python blog/test_quote_card.py
约束：绝不触网、绝不写真实 archive/ blog/data/ docs/ ——全部走 tempfile +
monkeypatch 模块常量，try/finally 还原。
"""

import contextlib
import io
import json
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).parent))

import make_quote_shots as mqs


# ── 工具 ────────────────────────────────────────────────────────────────────
def _write_meta(root, dirname, **overrides):
    d = Path(root) / dirname
    d.mkdir(parents=True, exist_ok=True)
    meta = {
        "id": "vidABC123xy",
        "url": "https://www.youtube.com/watch?v=vidABC123xy",
        "platform": "youtube",
        "uploader": "Some Channel",
        "guests": ["测试嘉宾"],
        "guest_info": [{"name": "测试嘉宾", "title": "测试头衔"}],
        "rewrite_complete": True,
        "key_quotes": ["第一句金句", "第二句金句"],
    }
    meta.update(overrides)
    (d / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False),
                                     encoding="utf-8")
    return d, meta


def _write_transcript(d, with_ts=True):
    body = "[00:01:00] 大家好，这是转录。\n[00:02:30] 我们正从规模化时代进入研究时代。\n" \
        if with_ts else "大家好，这是没有时间戳的转录。\n"
    (Path(d) / "transcript.md").write_text(body, encoding="utf-8")


def _exit_code(e):
    return e.code if isinstance(e.code, int) else 1


# ── font_size_for 边界 ──────────────────────────────────────────────────────
def test_font_size_boundaries():
    assert mqs.font_size_for("字" * 22) == 60
    assert mqs.font_size_for("字" * 23) == 50
    assert mqs.font_size_for("字" * 36) == 50
    assert mqs.font_size_for("字" * 37) == 42
    assert mqs.font_size_for("字" * 54) == 42
    assert mqs.font_size_for("字" * 55) == 36
    assert mqs.font_size_for("") == 60
    print("✓ font_size_for 边界（22/23/36/37/54/55）")


# ── 署名降级链 ──────────────────────────────────────────────────────────────
def test_attribution_chain():
    # 1) guest_info 完整
    meta = {"guest_info": [{"name": "Geoffrey Hinton",
                            "title": "深度学习之父、图灵奖得主、诺奖得主"}],
            "guests": ["别人"], "uploader": "CBS"}
    assert mqs.resolve_attribution(meta) == ("Geoffrey Hinton", "深度学习之父")

    # 2) guest_info 为 null + guests 是 list
    meta = {"guest_info": None, "guests": ["Ilya Sutskever", "第二人"],
            "uploader": "Dwarkesh"}
    assert mqs.resolve_attribution(meta) == ("Ilya Sutskever", "")

    # 3) guests 是字符串 '甲、乙'
    meta = {"guest_info": None, "guests": "甲、乙", "uploader": "频道"}
    assert mqs.resolve_attribution(meta) == ("甲", "")

    # 4) 全空剩 uploader
    meta = {"guest_info": None, "guests": [], "uploader": "Big Think"}
    assert mqs.resolve_attribution(meta) == ("Big Think", "")

    # guest_info=[] 空列表不得 IndexError
    meta = {"guest_info": [], "guests": None, "uploader": "频道"}
    assert mqs.resolve_attribution(meta) == ("频道", "")

    # guests list 里有空串要跳过
    meta = {"guest_info": [], "guests": ["", "  ", "真嘉宾"], "uploader": "频道"}
    assert mqs.resolve_attribution(meta) == ("真嘉宾", "")

    # 超长 title 截断约 20 字
    meta = {"guest_info": [{"name": "张三", "title": "超" * 50}], "uploader": "x"}
    name, role = mqs.resolve_attribution(meta)
    assert name == "张三" and role == "超" * 20 and len(role) == 20

    # 显式覆盖优先
    assert mqs.resolve_attribution(meta, "李四", "自定义头衔") == ("李四", "自定义头衔")
    print("✓ 署名降级链（guest_info → guests → uploader，含空列表/截断/覆盖）")


def test_attribution_omits_role_when_empty():
    out = mqs.overlay_html("/tmp/x.png", "金句", "Big Think", "")
    assert "— <b>Big Think</b>" in out
    assert "·" not in out  # 无头衔时只渲染「— 人名」
    out2 = mqs.overlay_html("/tmp/x.png", "金句", "张三", "头衔")
    assert "— <b>张三</b> · 头衔" in out2
    print("✓ 无头衔时署名只渲染人名")


# ── 金句归一化与 HTML ───────────────────────────────────────────────────────
def test_quote_normalization_and_html():
    # 带中文引号 strip 后模板加「」，不出现双重引号
    text = mqs.normalize_quote("“我们得到的是互联网的幽灵”")
    assert text == "我们得到的是互联网的幽灵"
    out = mqs.overlay_html("/tmp/x.png", text, "Karpathy", "OpenAI 创始成员")
    assert "「我们得到的是互联网的幽灵」" in out
    assert "“" not in out and "”" not in out

    # 英文引号与空白
    assert mqs.normalize_quote('  "hello"  ') == "hello"

    # dict 形态取 text 键
    assert mqs.normalize_quote({"text": "结构化金句"}) == "结构化金句"
    assert mqs.normalize_quote({"quote": "备用键"}) == "备用键"
    assert mqs.normalize_quote(None) == ""

    # 含 <&" 的金句被 HTML 转义（防注入）
    out = mqs.overlay_html("/tmp/x.png", 'a<b&"c', "名<字", "头&衔")
    assert "a&lt;b&amp;&quot;c" in out
    assert 'a<b&"c' not in out
    assert "名&lt;字" in out and "头&amp;衔" in out

    # 字号来自 font_size_for
    assert f"font-size:{mqs.font_size_for('短句')}px" in \
        mqs.overlay_html("/tmp/x.png", "短句", "n", "")
    assert "text-wrap:balance" in out
    print("✓ 金句归一化 + 「」 + HTML 转义")


# ── record_id → 目录解析 ────────────────────────────────────────────────────
def test_resolve_record_dir():
    old_root = mqs.ARCHIVE_ROOT
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "archive"
            mqs.ARCHIVE_ROOT = root
            # 同 id 三目录：最新是 stub、中间 complete、最旧 complete
            _write_meta(root, "20240303-newest-stub", rewrite_complete=False)
            _write_meta(root, "20240202-complete")
            _write_meta(root, "20240101-old-complete")
            # 干扰项：另一个 id + 一个损坏 metadata
            _write_meta(root, "20240404-other", id="otherid9999")
            broken = root / "20240505-broken"
            broken.mkdir(parents=True)
            (broken / "metadata.json").write_text("{not json", encoding="utf-8")

            d, meta = mqs.resolve_record_dir("vidABC123xy")
            assert d is not None and d.name == "20240202-complete", d
            assert meta["id"] == "vidABC123xy"

            d2, m2 = mqs.resolve_record_dir("不存在的id")
            assert d2 is None and m2 is None
    finally:
        mqs.ARCHIVE_ROOT = old_root
    print("✓ record 解析：倒序 + 只认 rewrite_complete + id 相等；解析不到返回 None")


def test_main_errors_when_record_missing():
    old_root = mqs.ARCHIVE_ROOT
    try:
        with tempfile.TemporaryDirectory() as td:
            mqs.ARCHIVE_ROOT = Path(td) / "archive"
            code = None
            with contextlib.redirect_stderr(io.StringIO()) as buf:
                try:
                    mqs.main(["nope-id", "--out", str(Path(td) / "out")])
                except SystemExit as e:
                    code = _exit_code(e)
            assert code == mqs.EXIT_USAGE, code
            assert "nope-id" in buf.getvalue()
    finally:
        mqs.ARCHIVE_ROOT = old_root
    print("✓ 解析不到 record_id 明确报错退出")


# ── 管线打桩 ────────────────────────────────────────────────────────────────
class _Stub:
    """替换模块内下载/抽帧/Chrome/定位函数，fake 写文件并计数。"""

    def __init__(self):
        self.calls = {"yt": 0, "ffmpeg": 0, "chrome": 0, "locate": 0}
        self.saved = {}

    def install(self):
        self.saved = {
            "_run_yt_dlp": mqs._run_yt_dlp,
            "_run_ffmpeg": mqs._run_ffmpeg,
            "_run_chrome": mqs._run_chrome,
            "locate_quote": mqs.locate_quote,
        }

        def fake_yt(url, out_tmpl):
            self.calls["yt"] += 1
            p = Path(out_tmpl.replace("%(ext)s", "mp4"))
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(b"fake-video-bytes")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        def fake_ffmpeg(video, at, out):
            self.calls["ffmpeg"] += 1
            assert Path(video).stat().st_size > 0  # 必须已有有效整片
            Path(out).write_bytes(b"fake-frame")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        def fake_chrome(html_path, out_png):
            self.calls["chrome"] += 1
            assert Path(html_path).exists()
            Path(out_png).write_bytes(b"fake-card")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        def fake_locate(archive_dir, text):
            self.calls["locate"] += 1
            return (150, "片段……", 0.87)

        mqs._run_yt_dlp = fake_yt
        mqs._run_ffmpeg = fake_ffmpeg
        mqs._run_chrome = fake_chrome
        mqs.locate_quote = fake_locate

    def restore(self):
        for k, v in self.saved.items():
            setattr(mqs, k, v)


def test_pipeline_stubbed():
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            d, meta = _write_meta(mqs.ARCHIVE_ROOT, "20240101-demo")
            _write_transcript(d, with_ts=True)
            out = root / "cards"
            stub.install()

            # 第一次：两条金句 → 定位 2 次、下载 1 次、抽帧 2 次、渲染 2 次
            mqs.main(["vidABC123xy", "--out", str(out)])
            for i in (0, 1):
                assert (out / f"raw-vidABC123xy-{i}.png").exists()
                assert (out / f"shot-vidABC123xy-{i}.png").exists()
                assert not (out / f"shot-vidABC123xy-{i}.html").exists()  # 渲染后清理
            assert stub.calls["yt"] == 1, stub.calls   # 同记录多金句只下载一次
            assert stub.calls["ffmpeg"] == 2
            assert stub.calls["locate"] == 2

            # 第二次：raw 帧 + 整片全走缓存，不再下载/定位/抽帧，只重渲染
            mqs.main(["vidABC123xy", "--out", str(out)])
            assert stub.calls["yt"] == 1, stub.calls
            assert stub.calls["ffmpeg"] == 2
            assert stub.calls["locate"] == 2
            assert stub.calls["chrome"] == 4

            # --force：重定位重抽帧，但整片缓存仍命中（yt 不再调）
            mqs.main(["vidABC123xy", "--out", str(out), "--force", "--index", "0"])
            assert stub.calls["yt"] == 1, stub.calls
            assert stub.calls["ffmpeg"] == 3
            assert stub.calls["locate"] == 3

            # 0 字节缓存视为无效 → 触发重下
            cached = mqs.VIDEO_CACHE_DIR / "vidABC123xy.mp4"
            cached.write_bytes(b"")
            mqs.main(["vidABC123xy", "--out", str(out), "--force", "--index", "1"])
            assert stub.calls["yt"] == 2, stub.calls
            assert cached.stat().st_size > 0  # 重下后缓存有效
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ 管线打桩：产物命名 / 下载只一次 / --force 重抽 / 0 字节重下")


def test_pipeline_text_and_dir_overrides():
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            d, meta = _write_meta(mqs.ARCHIVE_ROOT, "20240101-demo")
            _write_transcript(d, with_ts=True)
            out = root / "cards"
            stub.install()

            # --dir + --text + --name/--role：只出一张卡（序号缺省 0）
            mqs.main(["--dir", str(d), "--text", "“覆盖的文案”",
                      "--name", "自定义人", "--role", "自定义头衔",
                      "--out", str(out)])
            assert (out / "shot-vidABC123xy-0.png").exists()
            assert not (out / "shot-vidABC123xy-1.png").exists()
            assert stub.calls["yt"] == 1 and stub.calls["ffmpeg"] == 1
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ --dir / --text / --name / --role 覆盖")


# ── fail-fast ───────────────────────────────────────────────────────────────
def test_fail_fast_non_youtube_before_download():
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            d, meta = _write_meta(
                mqs.ARCHIVE_ROOT, "20240101-xhs",
                url="https://www.xiaohongshu.com/explore/abc123")
            _write_transcript(d, with_ts=True)
            stub.install()

            code = None
            with contextlib.redirect_stderr(io.StringIO()) as buf:
                try:
                    mqs.main(["vidABC123xy", "--out", str(root / "out")])
                except SystemExit as e:
                    code = _exit_code(e)
            assert code == mqs.EXIT_USAGE, code
            assert "YouTube" in buf.getvalue()
            # 在任何下载/定位之前退出
            assert stub.calls == {"yt": 0, "ffmpeg": 0, "chrome": 0, "locate": 0}

            # url 为 None / 空串不得 AttributeError
            for bad in (None, ""):
                _write_meta(mqs.ARCHIVE_ROOT, "20240101-xhs", url=bad)
                code = None
                with contextlib.redirect_stderr(io.StringIO()):
                    try:
                        mqs.main(["vidABC123xy", "--out", str(root / "out")])
                    except SystemExit as e:
                        code = _exit_code(e)
                assert code == mqs.EXIT_USAGE, (bad, code)
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ 非 YouTube url 在任何下载前退出（None/空串安全）")


def test_fail_fast_no_timestamp_exit_2():
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            d, meta = _write_meta(mqs.ARCHIVE_ROOT, "20240101-nots")
            _write_transcript(d, with_ts=False)
            stub.install()

            code = None
            with contextlib.redirect_stderr(io.StringIO()):
                try:
                    mqs.main(["vidABC123xy", "--out", str(root / "out")])
                except SystemExit as e:
                    code = _exit_code(e)
            assert code == 2, code  # 沿用旧脚本退出码语义
            # 无时间戳在 embed/下载之前就退出
            assert stub.calls["locate"] == 0 and stub.calls["yt"] == 0
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ transcript 无时间戳退出码 2（且不触发 embed/下载）")


def test_fail_fast_index_out_of_range():
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            d, meta = _write_meta(mqs.ARCHIVE_ROOT, "20240101-demo")
            _write_transcript(d, with_ts=True)
            stub.install()

            for bad in ("5", "0,5", "-1", "abc"):
                code = None
                with contextlib.redirect_stderr(io.StringIO()) as buf:
                    try:
                        mqs.main(["vidABC123xy", "--index", bad,
                                  "--out", str(root / "out")])
                    except SystemExit as e:
                        code = _exit_code(e)
                assert code == mqs.EXIT_USAGE, (bad, code)
            assert stub.calls["yt"] == 0
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ --index 越界/非法明确报错")


def test_strict_aborts_on_low_score():
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            d, meta = _write_meta(mqs.ARCHIVE_ROOT, "20240101-demo")
            _write_transcript(d, with_ts=True)
            stub.install()
            saved_locate = mqs.locate_quote
            mqs.locate_quote = lambda ad, t: (100, "弱匹配片段", 0.10)
            try:
                # 默认：低分只警告，仍产出
                out = root / "cards"
                with contextlib.redirect_stderr(io.StringIO()) as buf:
                    mqs.main(["vidABC123xy", "--index", "0", "--out", str(out)])
                assert (out / "shot-vidABC123xy-0.png").exists()
                assert "警告" in buf.getvalue()
                # --strict：中止
                code = None
                with contextlib.redirect_stderr(io.StringIO()):
                    try:
                        mqs.main(["vidABC123xy", "--index", "1", "--strict",
                                  "--out", str(out)])
                    except SystemExit as e:
                        code = _exit_code(e)
                assert code == mqs.EXIT_STRICT, code
                assert not (out / "shot-vidABC123xy-1.png").exists()
            finally:
                mqs.locate_quote = saved_locate
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ 匹配分 <0.35 默认警告 / --strict 中止")


def test_require_tool_missing_hint():
    saved_which = mqs.shutil.which
    try:
        mqs.shutil.which = lambda *a, **k: None
        code = None
        with contextlib.redirect_stderr(io.StringIO()) as buf:
            try:
                mqs.require_tool("yt-dlp", "可在根 .venv 安装：.venv/bin/pip install yt-dlp")
            except SystemExit as e:
                code = _exit_code(e)
        assert code == mqs.EXIT_USAGE, code
        msg = buf.getvalue()
        assert "yt-dlp" in msg and "安装" in msg  # 报错含安装提示
    finally:
        mqs.shutil.which = saved_which
    print("✓ shutil.which 返回 None 时报错含安装提示")


if __name__ == "__main__":
    test_font_size_boundaries()
    test_attribution_chain()
    test_attribution_omits_role_when_empty()
    test_quote_normalization_and_html()
    test_resolve_record_dir()
    test_main_errors_when_record_missing()
    test_pipeline_stubbed()
    test_pipeline_text_and_dir_overrides()
    test_fail_fast_non_youtube_before_download()
    test_fail_fast_no_timestamp_exit_2()
    test_fail_fast_index_out_of_range()
    test_strict_aborts_on_low_score()
    test_require_tool_missing_hint()
    print("\n全部通过 ✅")
