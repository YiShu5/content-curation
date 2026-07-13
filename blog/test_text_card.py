"""Text quote card tests (module + route).

Run: blog/.venv/bin/python blog/test_text_card.py
"""

import sys
import tempfile
from types import SimpleNamespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import text_card
import app as app_module
from app import app


def test_text_card_html_escapes_and_footer():
    h = text_card.text_card_html('注入<b>&"测试', "某人<x>", "头衔&", "标题<t>", "YouTube")
    assert "注入&lt;b&gt;&amp;&quot;测试" in h
    assert "某人&lt;x&gt;" in h
    assert "头衔&amp;" in h
    assert "《标题&lt;t&gt;》 · YouTube · 降噪 NoiseFilter" in h
    assert "<b>&" not in h.split("<style>")[1].split("</style>")[0]  # style 区无注入
    print("✓ text_card_html 全字段转义 + 脚注")


def test_text_card_html_font_size_and_optional_fields():
    short = text_card.text_card_html("短句", "人", "", "", "")
    assert "font-size:60px" in short
    assert "《" not in short.split("class=ft")[1]  # 无标题不渲染书名号
    long = text_card.text_card_html("长" * 60, "人", "", "T", "P")
    assert "font-size:36px" in long
    assert "— <b>人</b>" in short  # 无头衔只署名
    print("✓ 字号阶梯与可选字段")


def test_render_text_card_success_and_failure():
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "card.png"

        def fake_chrome_ok(html_path, out_png, chrome_path=None, timeout=None, size=None):
            Path(out_png).write_bytes(b"PNG")
            return SimpleNamespace(returncode=0, stderr="")

        old = text_card.run_chrome_screenshot
        try:
            text_card.run_chrome_screenshot = fake_chrome_ok
            ok, msg = text_card.render_text_card("金句", "人", "", "T", "P", out)
            assert ok and out.exists()
            assert not out.with_suffix(".html").exists(), "成功后应清理临时 html"

            # 失败：rc 非 0 → 半成品被清、html 留存排查
            def fake_chrome_fail(html_path, out_png, chrome_path=None, timeout=None, size=None):
                Path(out_png).write_bytes(b"broken")
                return SimpleNamespace(returncode=1, stderr="chrome boom")

            text_card.run_chrome_screenshot = fake_chrome_fail
            ok, msg = text_card.render_text_card("金句", "人", "", "T", "P", out)
            assert not ok and "chrome boom" in msg
            assert not out.exists(), "失败时不得留下半成品"
            assert out.with_suffix(".html").exists(), "失败时 html 留存排查"

            # Chrome 缺失 → (False, msg) 不抛
            def fake_chrome_missing(*a, **kw):
                raise FileNotFoundError("未找到 Chrome")

            text_card.run_chrome_screenshot = fake_chrome_missing
            ok, msg = text_card.render_text_card("金句", "人", "", "T", "P", out)
            assert not ok and "Chrome" in msg
        finally:
            text_card.run_chrome_screenshot = old
    print("✓ render_text_card 成功/失败/Chrome 缺失三态")


_ARTICLE = {
    "id": "vidabc10001",
    "title": "测试内容",
    "platform": "YouTube",
    "creator": "频道",
    "guests": "嘉宾甲、嘉宾乙",
    "guest_info": [{"name": "嘉宾甲", "title": "首席科学家"}],
    "key_quotes": ["第一条金句。", "第二条金句。"],
}


def test_quote_card_route_renders_and_caches():
    old_records = app_module.load_archive_records
    old_render = text_card.render_text_card
    calls = []
    try:
        with tempfile.TemporaryDirectory() as td:
            app_module.load_archive_records = lambda: [dict(_ARTICLE)]

            def fake_render(text, name, role, title, platform, out_png):
                calls.append((text, name, role))
                Path(out_png).parent.mkdir(parents=True, exist_ok=True)
                Path(out_png).write_bytes(b"PNG")
                return True, ""

            text_card.render_text_card = fake_render
            # 把缓存目录指到 tmp：monkeypatch app 模块的 __file__ 定位基准不可行，
            # 直接清理真实缓存键风险大——改为拦截 send_file 前的路径生成不现实，
            # 因此用真实 data/quote_cards 但用测试专属 record_id，测后清理。
            client = app.test_client()
            r1 = client.get("/article/vidabc10001/quote-card.png?i=0")
            assert r1.status_code == 200, r1.status_code
            assert len(calls) == 1
            assert calls[0][1] == "嘉宾甲" and calls[0][2] == "首席科学家"
            # 第二次命中缓存，不再渲染
            r2 = client.get("/article/vidabc10001/quote-card.png?i=0")
            assert r2.status_code == 200 and len(calls) == 1

            # 越界/非法 index、未知记录 → 404
            assert client.get("/article/vidabc10001/quote-card.png?i=9").status_code == 404
            assert client.get("/article/vidabc10001/quote-card.png?i=x").status_code == 404
            assert client.get("/article/nobody/quote-card.png?i=0").status_code == 404
    finally:
        app_module.load_archive_records = old_records
        text_card.render_text_card = old_render
        for p in (Path(__file__).parent / "data" / "quote_cards").glob("textcard-vidabc10001-*"):
            p.unlink()
    print("✓ 金句卡路由：渲染/缓存命中/404 边界")


def test_quote_card_route_render_failure_503():
    old_records = app_module.load_archive_records
    old_render = text_card.render_text_card
    try:
        app_module.load_archive_records = lambda: [dict(_ARTICLE)]
        text_card.render_text_card = lambda *a: (False, "chrome missing")
        client = app.test_client()
        assert client.get("/article/vidabc10001/quote-card.png?i=1").status_code == 503
    finally:
        app_module.load_archive_records = old_records
        text_card.render_text_card = old_render
    print("✓ 渲染失败返回 503")


def test_detail_page_renders_card_button():
    from flask import render_template
    article = dict(_ARTICLE)
    article.update({"cover_url": "", "topic": "AI 前沿", "pub_date": "2026-07-11",
                    "duration": 60, "link": "https://example.com", "score_total": None,
                    "summary_md": "正文", "summary": "正文", "why_watch": "",
                    "key_insights": ""})
    with app.test_request_context("/article/vidabc10001"):
        html = render_template("detail.html", article=article, related=[])
    assert 'data-card-url="/article/vidabc10001/quote-card.png?i=0"' in html
    assert 'data-byline="嘉宾甲 · 首席科学家"' in html
    assert 'id="qc-modal"' in html
    assert "share_card" in html  # 埋点 kind 已接
    print("✓ 详情页渲染金句卡按钮与弹层")


_PAYLOAD = {
    "generated_at": "2099-01-01 08:30",
    "breaking": {"title": "大新闻<b>", "summary": "总结&", "action": "本周应该测试"},
    "signals": [
        {"slot_label": "C 端增长", "title": "标题一", "summary": "总结一", "why": "理由一"},
        {"slot_label": "行业趋势", "title": "标题二<i>", "summary": "总结二", "why": ""},
    ],
}


def test_daily_card_html_content_and_escape():
    h = text_card.daily_card_html(_PAYLOAD)
    assert "2099-01-01" in h
    assert "大新闻&lt;b&gt;" in h and "总结&amp;" in h
    assert "本周应该测试" in h            # breaking 行动章
    assert "C 端增长" in h and "标题一" in h and "理由一" in h
    assert "标题二&lt;i&gt;" in h
    assert h.count("为什么值得看") == 1   # 空 why 不渲染该块
    # 无 breaking / 无信号的降级
    h2 = text_card.daily_card_html({"generated_at": "2099-01-02", "signals": []})
    assert "顶级大新闻" not in h2 and "今日无入选判断" in h2
    print("✓ daily_card_html 内容/转义/空分支")


def test_render_daily_card_uses_wide_size():
    sizes = []

    def fake_chrome(html_path, out_png, chrome_path=None, timeout=None, size=None):
        sizes.append(size)
        Path(out_png).write_bytes(b"PNG")
        return SimpleNamespace(returncode=0, stderr="")

    old = text_card.run_chrome_screenshot
    try:
        text_card.run_chrome_screenshot = fake_chrome
        with tempfile.TemporaryDirectory() as td:
            ok, _ = text_card.render_daily_card(_PAYLOAD, Path(td) / "d.png")
            assert ok and sizes == [(1920, 1080)]
    finally:
        text_card.run_chrome_screenshot = old
    print("✓ render_daily_card 走 1920×1080")


def test_signal_card_route():
    import today_signal
    old_read = today_signal.read_signal_cache
    old_render = text_card.render_daily_card
    calls = []
    try:
        today_signal.read_signal_cache = lambda: dict(_PAYLOAD)

        def fake_render(payload, out_png, date_str=""):
            calls.append(date_str)
            Path(out_png).parent.mkdir(parents=True, exist_ok=True)
            Path(out_png).write_bytes(b"PNG")
            return True, ""

        text_card.render_daily_card = fake_render
        client = app.test_client()
        assert client.get("/signal-card.png").status_code == 200
        assert calls == ["2099-01-01"]
        assert client.get("/signal-card.png").status_code == 200
        assert len(calls) == 1, "同一 generated_at 命中缓存不重渲染"

        # promote 改了 signals（generated_at 不变）→ 缓存键变化，必须重渲染
        promoted = dict(_PAYLOAD)
        promoted["signals"] = _PAYLOAD["signals"] + [
            {"slot_label": "热议", "title": "手动加入", "summary": "s", "item_id": "manual1"}]
        today_signal.read_signal_cache = lambda: promoted
        assert client.get("/signal-card.png").status_code == 200
        assert len(calls) == 2, "promote 后不得复用旧卡"

        # 空缓存 → 404；渲染失败 → 503
        today_signal.read_signal_cache = lambda: None
        assert client.get("/signal-card.png").status_code == 404
        today_signal.read_signal_cache = lambda: {"generated_at": "2099-09-09",
                                                  "signals": [{"title": "x"}]}
        text_card.render_daily_card = lambda *a, **kw: (False, "no chrome")
        assert client.get("/signal-card.png").status_code == 503
    finally:
        today_signal.read_signal_cache = old_read
        text_card.render_daily_card = old_render
        for payload in (dict(_PAYLOAD), promoted):
            key = app_module._daily_card_key(payload)
            p = Path(__file__).parent / "data" / "quote_cards" / f"dailycard-{key}.png"
            p.unlink(missing_ok=True)
    print("✓ /signal-card.png 路由：渲染/缓存/promote失效/404/503")


def test_signals_template_renders_share_button():
    from flask import render_template
    with app.test_request_context("/"):
        html = render_template("_signals.html", breaking=_PAYLOAD["breaking"],
                               signals=_PAYLOAD["signals"], attention=[],
                               signal_meta={"window_hours": 48,
                                            "generated_at": "2099-01-01 08:30"})
    assert 'id="signalsShareBtn"' in html
    assert 'id="sc-copy-data"' in html and "标题一" in html
    assert 'id="sc-modal"' in html
    # 无信号无 breaking：按钮与弹层都不渲染
    with app.test_request_context("/"):
        html2 = render_template("_signals.html", breaking=None, signals=[],
                                attention=[], signal_meta={"window_hours": 48})
    assert 'id="signalsShareBtn"' not in html2
    print("✓ 信号面板分享按钮渲染与空态")


if __name__ == "__main__":
    test_text_card_html_escapes_and_footer()
    test_text_card_html_font_size_and_optional_fields()
    test_render_text_card_success_and_failure()
    test_quote_card_route_renders_and_caches()
    test_quote_card_route_render_failure_503()
    test_detail_page_renders_card_button()
    test_daily_card_html_content_and_escape()
    test_render_daily_card_uses_wide_size()
    test_signal_card_route()
    test_signals_template_renders_share_button()
    print("\n全部通过 ✅")
