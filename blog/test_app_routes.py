"""Flask route smoke tests.

Run: blog/.venv/bin/python blog/test_app_routes.py
"""

import sys
from tempfile import TemporaryDirectory
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import app
import today_signal


def test_homepage_renders():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "降噪" in resp.get_data(as_text=True)
    print("✓ homepage renders")


def test_homepage_shows_missing_signal_state_when_cache_absent():
    original_cache = today_signal.SIGNAL_CACHE
    try:
        with TemporaryDirectory() as tmp:
            today_signal.SIGNAL_CACHE = Path(tmp) / "missing-today-signal.json"
            client = app.test_client()
            resp = client.get("/")
            html = resp.get_data(as_text=True)
    finally:
        today_signal.SIGNAL_CACHE = original_cache

    assert resp.status_code == 200
    assert "今日 AI 判断" in html
    assert "未生成" in html
    assert "还没有生成今日判断" in html
    print("✓ missing signal cache renders homepage state")


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


if __name__ == "__main__":
    test_homepage_renders()
    test_homepage_shows_missing_signal_state_when_cache_absent()
    test_detail_related_prefers_cover_url()
    print("\n全部通过 ✅")
