"""Public daily-edition route tests.

Run: blog/.venv/bin/python blog/test_daily_routes.py
"""

import json
import sys
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

import app as app_module
from app import app
from daily_issues import DailyIssueStore
import today_signal


LA = ZoneInfo("America/Los_Angeles")


def source(source_id="source-1", status="readable"):
    return {
        "source_id": source_id,
        "title": f"来源 {source_id}",
        "url": f"https://example.com/{source_id}",
        "canonical_url": f"https://example.com/{source_id}",
        "publisher": "测试媒体",
        "publisher_key": "test-publisher",
        "published_at": "2026-07-11T08:00:00-07:00",
        "is_primary": True,
        "verification_status": status,
    }


def topic(title, topic_id="topic-1", rank=1):
    return {
        "topic_id": topic_id,
        "rank": rank,
        "category": "AI 前沿",
        "title": title,
        "what_happened": f"{title}的事件摘要。",
        "discussion_focus": ["产品影响", "行业反应"],
        "why_ranked": f"{title}可能影响下一步判断。",
        "sources": [source()],
    }


def attention(title="正在升温的讨论"):
    row = topic(title, topic_id="attention-1", rank=1)
    row["attention_status"] = "rising"
    return row


def publish_fixture(store, issue_date, title):
    return store.publish(
        issue_date,
        [topic(title)],
        [attention()],
        now=datetime.fromisoformat(f"{issue_date}T09:00:00-07:00"),
    )


def publish_and_revise_fixture(store, issue_date, before, after):
    first = publish_fixture(store, issue_date, before)
    return store.revise(
        issue_date,
        [topic(after)],
        [attention()],
        expected_revision=first["revision"],
        now=datetime.fromisoformat(f"{issue_date}T10:00:00-07:00"),
    )


def corrupt_current_issue(store, issue_date):
    store._issue_path(issue_date).write_text("{broken", encoding="utf-8")


@contextmanager
def issue_client(now="2026-07-11T09:00:00-07:00"):
    old_config = {
        key: app.config.get(key)
        for key in ("DAILY_ISSUES_DIR", "PUBLIC_BASE_URL", "BLOG_TIMEZONE", "TESTING")
    }
    original_signal_cache = today_signal.SIGNAL_CACHE
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        try:
            app.config.update(
                DAILY_ISSUES_DIR=str(root / "daily-issues"),
                PUBLIC_BASE_URL="https://noise.example",
                BLOG_TIMEZONE="America/Los_Angeles",
                TESTING=True,
            )
            today_signal.SIGNAL_CACHE = root / "today-signal.json"
            store = DailyIssueStore(Path(app.config["DAILY_ISSUES_DIR"]), app.config["BLOG_TIMEZONE"])
            archive_fixture = [{
                "id": "library-1",
                "title": "深度内容样本",
                "topic": "AI 前沿",
                "score_verdict": "必读",
                "cover_url": "",
                "platform": "YouTube",
                "creator": "作者",
                "pub_date": "2026-07-10",
                "duration": 20,
                "guests": "",
                "summary": "摘要",
                "link": "https://example.com/library",
                "score_total": 90,
                "scores": {},
                "key_quotes": [],
                "core_ideas": [],
                "key_insights": "",
                "why_watch": "",
            }]
            fixed_now = datetime.fromisoformat(now).astimezone(LA)
            with patch.object(app_module, "load_archive_records", return_value=archive_fixture), patch.object(
                app_module, "_local_now", return_value=fixed_now, create=True
            ):
                yield app.test_client(), store, root
        finally:
            today_signal.SIGNAL_CACHE = original_signal_cache
            app.config.update(old_config)


def test_home_uses_latest_published_issue_not_signal_cache():
    with issue_client() as (client, store, _):
        publish_fixture(store, "2026-07-10", "旧主题")
        publish_fixture(store, "2026-07-11", "最新主题")
        response = client.get("/")
        html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "最新主题" in html
    assert "旧主题" not in html
    assert "AI HOT" not in html
    assert "加入首页判断" not in html
    assert "先不加" not in html


def test_dated_issue_is_stable_and_uses_historical_wording():
    with issue_client() as (client, store, _):
        publish_fixture(store, "2026-07-10", "固定主题")
        response = client.get("/daily/2026-07-10")
        html = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "这一天，哪些讨论值得知道？" in html
    assert '<link rel="canonical" href="https://noise.example/daily/2026-07-10">' in html
    assert "<title>降噪｜2026-07-10 值得知道的讨论</title>" in html
    assert '<meta name="description" content="固定主题可能影响下一步判断。">' in html
    assert '<meta property="og:url" content="https://noise.example/daily/2026-07-10">' in html
    assert 'content="https://noise.example/"' not in html


def test_archive_is_descending_and_unknown_date_is_404():
    with issue_client() as (client, store, _):
        publish_fixture(store, "2026-07-10", "十号")
        publish_fixture(store, "2026-07-11", "十一号")
        html = client.get("/daily").get_data(as_text=True)
        invalid = client.get("/daily/2026-02-30")
        absent = client.get("/daily/2026-07-09")
    assert html.index("2026-07-11") < html.index("2026-07-10")
    assert invalid.status_code == 404
    assert absent.status_code == 404


def test_no_published_issue_keeps_deep_library_available():
    with issue_client() as (client, _store, _):
        html = client.get("/").get_data(as_text=True)
    assert "还没有发布第一期" in html
    assert 'id="deep-library"' in html


def test_old_latest_is_labeled_and_published_snapshot_does_not_drift():
    with issue_client(now="2026-07-12T09:00:00-07:00") as (client, store, root):
        publish_fixture(store, "2026-07-11", "稳定主题")
        first = client.get("/").get_data(as_text=True)
        today_signal.SIGNAL_CACHE.write_text(
            json.dumps({"signals": [{"title": "不应该上首页的新主题"}]}),
            encoding="utf-8",
        )
        second = client.get("/").get_data(as_text=True)
    assert "最新一期 · 2026.07.11" in second
    assert "这一天，哪些讨论值得知道？" in second
    assert "稳定主题" in first and "稳定主题" in second
    assert "不应该上首页的新主题" not in second


def test_home_falls_back_to_archived_revision_when_current_json_is_corrupt():
    with issue_client() as (client, store, _):
        publish_and_revise_fixture(store, "2026-07-11", "修订前", "修订后")
        corrupt_current_issue(store, "2026-07-11")
        html = client.get("/").get_data(as_text=True)
    assert "修订前" in html
    assert "修订后" not in html


def test_unrecoverable_dated_issue_is_friendly_503_not_404():
    with issue_client() as (client, store, _):
        publish_fixture(store, "2026-07-11", "已损坏")
        corrupt_current_issue(store, "2026-07-11")
        response = client.get("/daily/2026-07-11")
        html = response.get_data(as_text=True)
    assert response.status_code == 503
    assert "这期简报暂时无法读取" in html
    assert "DailyIssueCorrupt" not in html


def test_only_corrupt_first_issue_is_not_misreported_as_never_published():
    with issue_client() as (client, store, _):
        publish_fixture(store, "2026-07-11", "唯一一期")
        corrupt_current_issue(store, "2026-07-11")
        html = client.get("/").get_data(as_text=True)
    assert "最新一期暂时无法读取" in html
    assert "还没有发布第一期" not in html
    assert 'id="deep-library"' in html


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print(f"✓ {test.__name__}")
    print("\n全部通过 ✅")
