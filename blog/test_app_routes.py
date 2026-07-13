"""Flask route smoke tests.

Run: blog/.venv/bin/python blog/test_app_routes.py
"""

import sys
from datetime import datetime
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

import app as app_module
from app import app
import today_signal


def test_homepage_renders():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "降噪" in resp.get_data(as_text=True)
    print("✓ homepage renders")


def test_homepage_without_published_issue_keeps_deep_library():
    original_dir = app.config["DAILY_ISSUES_DIR"]
    try:
        with TemporaryDirectory() as tmp:
            app.config["DAILY_ISSUES_DIR"] = str(Path(tmp) / "daily-issues")
            with patch.object(app_module, "load_archive_records", return_value=[]), patch.object(
                app_module,
                "_local_now",
                return_value=datetime(2026, 7, 11, 9, tzinfo=ZoneInfo("America/Los_Angeles")),
            ):
                client = app.test_client()
                resp = client.get("/")
                html = resp.get_data(as_text=True)
    finally:
        app.config["DAILY_ISSUES_DIR"] = original_dir

    assert resp.status_code == 200
    assert "还没有发布第一期" in html
    assert 'id="deep-library"' in html
    assert "今日 AI 判断" not in html
    print("✓ no published issue keeps deep library")


def test_detail_related_prefers_cover_url():
    from flask import render_template
    article = {
        "id": "a",
        "title": "主文章",
        "cover_url": "",
        "topic": "AI 前沿",
        "creator": "作者",
        "pub_date": "2026-07-07",
        "duration": 60,
        "link": "https://example.com",
        "platform": "YouTube",
        "score_total": None,
        "guest_info": [],
        "guests": "",
        "key_quotes": [],
        "summary_md": "正文",
        "summary": "正文",
        "why_watch": "",
        "key_insights": "",
    }
    related = [{
        "id": "b",
        "title": "相关文章",
        "cover_url": "/cover-local/archive-dir",
        "platform": "YouTube",
        "topic": "AI 前沿",
        "score": 88,
    }]
    with app.test_request_context("/article/a"):
        html = render_template("detail.html", article=article, related=related)
    assert 'src="/cover-local/archive-dir"' in html
    print("✓ detail related prefers cover_url")


def test_ingest_status_passes_through_record_id():
    """API 契约：/ingest/status 原样透传 job dict（含 record_id），app.py 零改动的前提。"""
    import json as _json
    import ingest_jobs as jobs
    old_path = jobs.JOBS_PATH
    try:
        with TemporaryDirectory() as tmp:
            jobs.JOBS_PATH = Path(tmp) / "jobs.json"
            jobs.JOBS_PATH.write_text(_json.dumps({
                "yt:abcdefghijk": {
                    "job_id": "yt:abcdefghijk",
                    "status": "done",
                    "record_id": "abcdefghijk",
                    "message": "已加入深度库",
                }
            }), encoding="utf-8")
            app.config.update(
                SECRET_KEY="test-secret",
                BLOG_ADMIN_PASSWORD="test-password",
            )
            client = app.test_client()
            with client.session_transaction() as session:
                session["daily_admin"] = True
                session["admin_csrf"] = "test-csrf"
            resp = client.get("/ingest/status?job_id=yt:abcdefghijk")
            assert resp.status_code == 200
            assert resp.get_json()["record_id"] == "abcdefghijk"
    finally:
        jobs.JOBS_PATH = old_path
    print("✓ ingest status passes through record_id")


def test_detail_quote_anchor():
    from flask import render_template
    quotes = [
        "“带首尾引号的金句会被归一化。”",
        {"text": "第二条金句，内容不同。", "speaker": "某嘉宾"},
        "第三条金句，hash 必须彼此不同。",
    ]
    article = {
        "id": "a",
        "title": "主文章",
        "cover_url": "",
        "topic": "AI 前沿",
        "creator": "作者",
        "pub_date": "2026-07-07",
        "duration": 60,
        "link": "https://example.com",
        "platform": "YouTube",
        "score_total": None,
        "guest_info": [],
        "guests": "",
        "key_quotes": quotes,
        "summary_md": "正文",
        "summary": "正文",
        "why_watch": "",
        "key_insights": "",
    }
    with app.test_request_context("/article/a"):
        html = render_template("detail.html", article=article, related=[])

    anchors = [app_module._quote_anchor(q) for q in quotes]
    for a in anchors:
        assert a.startswith("q-") and len(a) == 10
        assert f'id="{a}"' in html
    assert len(set(anchors)) == 3          # 不同金句 hash 必不同
    assert 'id="key-quotes"' in html       # 降级滚动的目标锚点
    assert "/^#q-/" in html                # 降级 JS 已注入
    # dict 形态金句展示正文而非 Python repr
    assert "第二条金句，内容不同。" in html
    assert "{&#39;text&#39;" not in html and "{'text'" not in html
    # 归一化幂等：带引号与去引号文本 hash 一致；dict 形态与字符串一致
    assert app_module._quote_anchor("“带首尾引号的金句会被归一化。”") == \
        app_module._quote_anchor("带首尾引号的金句会被归一化。")
    assert app_module._quote_anchor({"text": "第二条金句，内容不同。"}) == \
        app_module._quote_anchor("第二条金句，内容不同。")
    assert app_module._quote_anchor("") == ""
    print("✓ detail quote anchors stable across quoting and dict forms")


def test_missing_attention_promote_does_not_write_positive_log():
    original_cache = today_signal.SIGNAL_CACHE
    original_app_file = app_module.__file__
    try:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            today_signal.SIGNAL_CACHE = tmp_path / "today_signal.json"
            today_signal.SIGNAL_CACHE.write_text(
                '{"generated_at":"2026-07-07 08:31","signals":[],"attention":[]}',
                encoding="utf-8",
            )
            app_module.__file__ = str(tmp_path / "app.py")

            client = app.test_client()
            app.config.update(SECRET_KEY="test-secret", BLOG_ADMIN_PASSWORD="test-password")
            with client.session_transaction() as session:
                session["daily_admin"] = True
                session["admin_csrf"] = "test-csrf"
            resp = client.post(
                "/signal/attention",
                headers={"X-CSRF-Token": "test-csrf"},
                json={
                    "action": "promote",
                    "item_id": "missing",
                    "label": "不存在的热议",
                    "href": "https://example.com/missing",
                    "source": "AI HOT",
                },
            )
            log_path = tmp_path / "data" / "clicks.log"
            log_exists = log_path.exists()
    finally:
        app_module.__file__ = original_app_file
        today_signal.SIGNAL_CACHE = original_cache

    assert resp.status_code == 200
    assert resp.get_json()["status"] == "not_found"
    assert not log_exists
    print("✓ missing promote does not create positive behavior log")


if __name__ == "__main__":
    test_homepage_renders()
    test_homepage_without_published_issue_keeps_deep_library()
    test_detail_related_prefers_cover_url()
    test_ingest_status_passes_through_record_id()
    test_detail_quote_anchor()
    test_missing_attention_promote_does_not_write_positive_log()
    print("\n全部通过 ✅")
