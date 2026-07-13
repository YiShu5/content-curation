"""金句卡参数化 CLI（make_quote_shots.py）的离线测试。

运行：blog/.venv/bin/python blog/test_quote_card.py
约束：绝不触网、绝不写真实 archive/ blog/data/ docs/ ——全部走 tempfile +
monkeypatch 模块常量，try/finally 还原。

覆盖 code-review 修复：.part 不算缓存 / --no-part 移除 / raw 帧缓存键含定位句+shift /
旧产物不掩盖失败 / argparse 用法错误退出码 1 / embed 失败退出码 7 /
record_id 与 --dir 互斥 / --text 模式 --index 越界 / --locate 定位展示解耦 /
normalize_quote 委托 today_signal。
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

RID = "vidABC123xy"


# ── 工具 ────────────────────────────────────────────────────────────────────
def _write_meta(root, dirname, **overrides):
    d = Path(root) / dirname
    d.mkdir(parents=True, exist_ok=True)
    meta = {
        "id": RID,
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


def _raw(out_dir, i, locate_text, shift=2.0):
    """按实现的缓存键规则算 raw 帧路径（键 = 定位句哈希 + shift）。"""
    return Path(out_dir) / mqs.raw_frame_name(RID, i, locate_text, shift)


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


def test_normalize_quote_delegates_to_today_signal():
    """normalize_quote 不再逐字拷贝：优先 T.quote_text 公共别名，缺失降级 _quote_text。"""
    had = hasattr(mqs.T, "quote_text")
    saved = getattr(mqs.T, "quote_text", None)
    try:
        mqs.T.quote_text = lambda item: "DELEGATED:" + str(item)
        assert mqs.normalize_quote("原文") == "DELEGATED:原文"
    finally:
        if had:
            mqs.T.quote_text = saved
        else:
            delattr(mqs.T, "quote_text")
    # 别名缺失时降级到 _quote_text（行为同旧实现）
    if not hasattr(mqs.T, "quote_text"):
        assert mqs.normalize_quote("“兜底”") == "兜底"
    print("✓ normalize_quote 委托 today_signal（quote_text 别名 → _quote_text 降级）")


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


def test_dir_and_record_id_mutually_exclusive():
    code = None
    with contextlib.redirect_stderr(io.StringIO()) as buf:
        try:
            mqs.main(["someid", "--dir", "/tmp/whatever"])
        except SystemExit as e:
            code = _exit_code(e)
    assert code == mqs.EXIT_USAGE, code
    assert "二选一" in buf.getvalue()
    print("✓ record_id 与 --dir 同时给出明确报错（不再静默偏向 --dir）")


# ── 管线打桩 ────────────────────────────────────────────────────────────────
class _Stub:
    """替换模块内下载/抽帧/Chrome/定位函数，fake 写文件并计数。"""

    def __init__(self):
        self.calls = {"yt": 0, "ffmpeg": 0, "chrome": 0, "locate": 0}
        self.locate_texts = []  # locate_quote 实际收到的定位句
        self.html_seen = []     # Chrome 渲染时的 HTML 内容
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
            self.html_seen.append(Path(html_path).read_text(encoding="utf-8"))
            Path(out_png).write_bytes(b"fake-card")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        def fake_locate(archive_dir, text):
            self.calls["locate"] += 1
            self.locate_texts.append(text)
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
            for i, q in ((0, "第一句金句"), (1, "第二句金句")):
                assert _raw(out, i, q).exists()  # raw 键含定位句哈希 + s2.0
                assert (out / f"shot-vidABC123xy-{i}.png").exists()
                assert not (out / f"shot-vidABC123xy-{i}.html").exists()  # 渲染后清理
            assert stub.calls["yt"] == 1, stub.calls   # 同记录多金句只下载一次
            assert stub.calls["ffmpeg"] == 2
            assert stub.calls["locate"] == 2

            # 第二次：raw 帧 + 整片全走缓存，不再下载/定位/抽帧；成品必重渲染
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
    print("✓ 管线打桩：产物命名 / 下载只一次 / --force 重抽 / 0 字节重下 / 成品必重渲染")


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
            # --text 也做定位句（归一化后），raw 键随之计算
            assert stub.locate_texts == ["覆盖的文案"]
            assert _raw(out, 0, "覆盖的文案").exists()
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ --dir / --text / --name / --role 覆盖")


def test_locate_decouples_from_display_text():
    """--locate 只管语义定位，展示文案仍走 --text；raw 键按实际定位句计算。"""
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

            mqs.main(["--dir", str(d), "--text", "中文展示文案",
                      "--locate", "moving from the age of scaling",
                      "--out", str(out)])
            # 定位用英文句，展示用中文文案
            assert stub.locate_texts == ["moving from the age of scaling"]
            assert any("中文展示文案" in h for h in stub.html_seen)
            assert not any("moving from the age" in h for h in stub.html_seen)
            # raw 缓存键按实际定位句（而非展示文案）计算
            assert _raw(out, 0, "moving from the age of scaling").exists()
            assert not _raw(out, 0, "中文展示文案").exists()
            assert (out / "shot-vidABC123xy-0.png").exists()

            # --locate 为空白（归一化后空）→ 报错
            code = None
            with contextlib.redirect_stderr(io.StringIO()) as buf:
                try:
                    mqs.main(["--dir", str(d), "--text", "文案",
                              "--locate", "“”", "--out", str(out)])
                except SystemExit as e:
                    code = _exit_code(e)
            assert code == mqs.EXIT_USAGE, code
            assert "--locate" in buf.getvalue()
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ --locate 定位与 --text 展示解耦（含空 --locate 报错）")


def test_raw_cache_key_varies_with_locate_and_shift():
    """改 --shift / 换 --text 定位句 → 新缓存键重新抽帧；同键第二次才复用。"""
    # 纯函数层：键随定位句/shift 变化且稳定
    n_base = mqs.raw_frame_name("r", 0, "a", 2.0)
    assert n_base == mqs.raw_frame_name("r", 0, "a", 2)  # 2 与 2.0 同键
    assert n_base != mqs.raw_frame_name("r", 0, "b", 2.0)   # 定位句变 → 新键
    assert n_base != mqs.raw_frame_name("r", 0, "a", 2.5)   # shift 变 → 新键
    assert n_base != mqs.raw_frame_name("r", 1, "a", 2.0)   # 序号变 → 新键
    assert n_base.startswith("raw-r-0-") and n_base.endswith("-s2.0.png")

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

            mqs.main(["vidABC123xy", "--index", "0", "--out", str(out)])
            assert stub.calls["ffmpeg"] == 1
            assert _raw(out, 0, "第一句金句", 2.0).exists()

            # 改 --shift → 不加 --force 也重新定位+抽帧（旧键不再被静默复用）
            mqs.main(["vidABC123xy", "--index", "0", "--shift", "5",
                      "--out", str(out)])
            assert stub.calls["ffmpeg"] == 2, stub.calls
            assert _raw(out, 0, "第一句金句", 5.0).exists()

            # 换 --text 定位句 → 新键重抽
            mqs.main(["--dir", str(d), "--text", "换一句定位句", "--out", str(out)])
            assert stub.calls["ffmpeg"] == 3, stub.calls
            assert _raw(out, 0, "换一句定位句").exists()

            # 同参数再跑 → 同键复用，不再抽帧（成品仍重渲染）
            chrome_before = stub.calls["chrome"]
            mqs.main(["--dir", str(d), "--text", "换一句定位句", "--out", str(out)])
            assert stub.calls["ffmpeg"] == 3, stub.calls
            assert stub.calls["chrome"] == chrome_before + 1
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ raw 缓存键含定位句+shift：改 --shift/--text 自动走新键，同键复用")


def test_stale_outputs_do_not_mask_failure():
    """抽帧/渲染失败时：旧产物先被 unlink，returncode+exists 双条件判定，不留假成功。"""
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
            out.mkdir(parents=True)
            stub.install()

            # a) Chrome 失败（returncode=1 且写出了残缺文件）：
            #    预置的旧成品不得掩盖失败，退出码 5，产物被清掉
            stale_shot = out / "shot-vidABC123xy-0.png"
            stale_shot.write_bytes(b"stale-old-card")

            def chrome_fail(html_path, out_png):
                Path(out_png).write_bytes(b"broken-half-render")  # 有文件但 rc!=0
                return SimpleNamespace(returncode=1, stdout="", stderr="chrome boom")

            mqs._run_chrome = chrome_fail
            code = None
            with contextlib.redirect_stderr(io.StringIO()) as buf:
                try:
                    mqs.main(["vidABC123xy", "--index", "0", "--out", str(out)])
                except SystemExit as e:
                    code = _exit_code(e)
            assert code == mqs.EXIT_RENDER, code
            assert "RENDER_FAIL" in buf.getvalue() and "chrome boom" in buf.getvalue()
            assert not stale_shot.exists()  # 旧成品/半成品都不留
            assert (out / "shot-vidABC123xy-0.html").exists()  # html 留着排查

            # b) 成功路径：旧成品内容被真正覆盖（成品每次重渲染，不吃缓存）
            def chrome_ok(html_path, out_png):
                Path(out_png).write_bytes(b"fake-card")
                return SimpleNamespace(returncode=0, stdout="", stderr="")

            mqs._run_chrome = chrome_ok
            stale_shot.write_bytes(b"stale-old-card")
            mqs.main(["vidABC123xy", "--index", "0", "--out", str(out)])
            assert stale_shot.read_bytes() == b"fake-card"

            # c) ffmpeg 失败（rc=1 无产物）：--force 下预置旧 raw 帧被清、退出码 4
            raw0 = _raw(out, 0, "第一句金句")
            assert raw0.exists()

            def ffmpeg_fail(video, at, out_p):
                return SimpleNamespace(returncode=1, stdout="", stderr="ffmpeg boom")

            mqs._run_ffmpeg = ffmpeg_fail
            code = None
            with contextlib.redirect_stderr(io.StringIO()) as buf:
                try:
                    mqs.main(["vidABC123xy", "--index", "0", "--force",
                              "--out", str(out)])
                except SystemExit as e:
                    code = _exit_code(e)
            assert code == mqs.EXIT_FRAME, code
            assert "FRAME_FAIL" in buf.getvalue() and "ffmpeg boom" in buf.getvalue()
            assert not raw0.exists()  # 旧 raw 不得再冒充有效缓存
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ 旧产物不掩盖失败：先 unlink + returncode/exists 双条件 + stderr 尾部")


# ── 下载缓存（.part 排除 / --no-part 移除）─────────────────────────────────
def test_part_file_not_treated_as_cache():
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            mqs.VIDEO_CACHE_DIR.mkdir(parents=True)
            # 中断残留：非零字节 .part 不算有效缓存，也不删（留给 yt-dlp 续传）
            part = mqs.VIDEO_CACHE_DIR / "vidABC123xy.mp4.part"
            part.write_bytes(b"partial-download-bytes")
            assert mqs.find_cached_video("vidABC123xy") is None
            assert part.exists()

            # 完整文件仍正常命中
            full = mqs.VIDEO_CACHE_DIR / "vidABC123xy.mp4"
            full.write_bytes(b"full-video")
            assert mqs.find_cached_video("vidABC123xy") == full
            full.unlink()

            # 走整条管线：只有 .part 时必须触发重下
            d, meta = _write_meta(mqs.ARCHIVE_ROOT, "20240101-demo")
            _write_transcript(d, with_ts=True)
            stub.install()
            mqs.main(["vidABC123xy", "--index", "0", "--out", str(root / "cards")])
            assert stub.calls["yt"] == 1, stub.calls
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ .part 残留不算缓存（不误删、命中完整文件、管线触发重下）")


def test_yt_dlp_uses_default_part_files():
    """_run_yt_dlp 不再传 --no-part：默认 .part 临时文件 + 完成后改名，可续传。"""
    saved_run, saved_which = mqs.subprocess.run, mqs.shutil.which
    captured = {}
    try:
        mqs.shutil.which = lambda *a, **k: "/fake/bin/yt-dlp"

        def fake_run(cmd, **kw):
            captured["cmd"] = list(cmd)
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        mqs.subprocess.run = fake_run
        mqs._run_yt_dlp("https://youtu.be/x", "/tmp/x.%(ext)s")
        cmd = captured["cmd"]
        assert "--no-part" not in cmd, cmd
        assert cmd[0] == "/fake/bin/yt-dlp" and cmd[-1] == "https://youtu.be/x"
        assert "-o" in cmd
    finally:
        mqs.subprocess.run, mqs.shutil.which = saved_run, saved_which
    print("✓ yt-dlp 不再带 --no-part（中断可续传，残留是 .part 不会毒缓存）")


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


def test_argparse_usage_error_exits_1_not_2():
    """argparse 用法错误必须走 EXIT_USAGE=1，不得占用 2（2=转录无时间戳）。"""
    for argv in (["--shift", "abc"],          # 类型错误
                 ["--bogus-flag"],            # 未知参数
                 ["a", "b"]):                 # 多余位置参数
        code = None
        with contextlib.redirect_stderr(io.StringIO()) as buf:
            try:
                mqs.main(argv)
            except SystemExit as e:
                code = _exit_code(e)
        assert code == mqs.EXIT_USAGE == 1, (argv, code)
        assert code != mqs.EXIT_NO_TIMESTAMP
        assert "错误" in buf.getvalue()
    print("✓ argparse 用法错误退出码 1（不与 2=无时间戳撞车）")


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


def test_text_mode_index_bounds():
    """--text 模式的 --index 也要满足 0 <= i < max(len(key_quotes), 1)。"""
    old_root, old_cache = mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR
    stub = _Stub()
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            mqs.ARCHIVE_ROOT = root / "archive"
            mqs.VIDEO_CACHE_DIR = root / "video_cache"
            d, meta = _write_meta(mqs.ARCHIVE_ROOT, "20240101-demo")  # 2 条金句
            _write_transcript(d, with_ts=True)
            out = root / "cards"
            stub.install()

            # 越界/负数 → EXIT_USAGE，不产出 raw-...--1.png 之类
            for bad in ("2", "5", "-1"):
                code = None
                with contextlib.redirect_stderr(io.StringIO()) as buf:
                    try:
                        mqs.main(["--dir", str(d), "--text", "文案",
                                  "--index", bad, "--out", str(out)])
                    except SystemExit as e:
                        code = _exit_code(e)
                assert code == mqs.EXIT_USAGE, (bad, code)
                assert "越界" in buf.getvalue()
            assert stub.calls == {"yt": 0, "ffmpeg": 0, "chrome": 0, "locate": 0}
            assert not list(out.glob("raw-*")) if out.exists() else True

            # 合法上界：--index 1（共 2 条）可用
            mqs.main(["--dir", str(d), "--text", "文案", "--index", "1",
                      "--out", str(out)])
            assert (out / "shot-vidABC123xy-1.png").exists()

            # key_quotes 为空时 --text 仍允许序号 0（max(len,1)=1），1 则越界
            d2, _ = _write_meta(mqs.ARCHIVE_ROOT, "20240102-noquotes",
                                id="vidNoQuotes", key_quotes=[],
                                url="https://youtu.be/vidNoQuotes")
            _write_transcript(d2, with_ts=True)
            mqs.main(["--dir", str(d2), "--text", "文案", "--out", str(out)])
            assert (out / "shot-vidNoQuotes-0.png").exists()
            code = None
            with contextlib.redirect_stderr(io.StringIO()):
                try:
                    mqs.main(["--dir", str(d2), "--text", "文案",
                              "--index", "1", "--out", str(out)])
                except SystemExit as e:
                    code = _exit_code(e)
            assert code == mqs.EXIT_USAGE, code
    finally:
        stub.restore()
        mqs.ARCHIVE_ROOT, mqs.VIDEO_CACHE_DIR = old_root, old_cache
    print("✓ --text 模式 --index 越界校验（含 key_quotes 为空只许 0）")


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


def test_embed_failure_exits_7():
    """embed_query 失败不裸 traceback：简洁中文报错（含原因）+ EXIT_EMBED=7。"""
    saved = mqs.embeddings.embed_query

    def boom(query):
        raise RuntimeError("Missing ZHIPU_API_KEY")

    try:
        mqs.embeddings.embed_query = boom
        code = None
        with contextlib.redirect_stderr(io.StringIO()) as buf:
            try:
                mqs.locate_quote("/tmp/nonexistent-archive", "任意金句")
            except SystemExit as e:
                code = _exit_code(e)
        assert code == mqs.EXIT_EMBED == 7, code
        msg = buf.getvalue()
        assert "向量化失败" in msg          # 简洁中文错误
        assert "Missing ZHIPU_API_KEY" in msg  # 带原因
        assert "Traceback" not in msg
    finally:
        mqs.embeddings.embed_query = saved
    print("✓ embed_query 失败 → 中文报错 + 退出码 7（不裸 traceback）")


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
    test_normalize_quote_delegates_to_today_signal()
    test_resolve_record_dir()
    test_main_errors_when_record_missing()
    test_dir_and_record_id_mutually_exclusive()
    test_pipeline_stubbed()
    test_pipeline_text_and_dir_overrides()
    test_locate_decouples_from_display_text()
    test_raw_cache_key_varies_with_locate_and_shift()
    test_stale_outputs_do_not_mask_failure()
    test_part_file_not_treated_as_cache()
    test_yt_dlp_uses_default_part_files()
    test_fail_fast_non_youtube_before_download()
    test_fail_fast_no_timestamp_exit_2()
    test_argparse_usage_error_exits_1_not_2()
    test_fail_fast_index_out_of_range()
    test_text_mode_index_bounds()
    test_strict_aborts_on_low_score()
    test_embed_failure_exits_7()
    test_require_tool_missing_hint()
    print("\n全部通过 ✅")
