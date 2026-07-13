"""Administrator route tests. Run: blog/.venv/bin/python blog/test_admin_routes.py"""

import json
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app import app


def configured_client():
    app.config.update(TESTING=True, SECRET_KEY="test-secret", BLOG_ADMIN_PASSWORD="correct horse")
    return app.test_client()


def source(source_id="real"):
    return {"source_id": source_id, "title": "Official", "url": "https://official.ai/release",
            "canonical_url": "https://official.ai/release", "publisher": "Official",
            "publisher_key": "official.ai", "published_at": "", "is_primary": True,
            "verification_status": "readable"}


def topic(topic_id="topic-a", rank=1):
    return {"topic_id": topic_id, "rank": rank, "category": "AI", "title": "A",
            "what_happened": "A happened.", "discussion_focus": [], "why_ranked": "A matters.",
            "sources": [source(topic_id + "-source")], "independent_source_count": 1}


def cache(date="2026-07-11"):
    return {"freshness": {"status": "fresh"}, "daily_draft": {
        "schema_version": 1, "draft_date": date, "generated_at": date + " 09:00",
        "topics": [topic()], "candidates": [topic("topic-b", 0)],
        "attention": [topic("topic-c", 0) | {"attention_status": "rising"}],
    }}


def admin_client(tmp):
    app.config.update(TESTING=True, SECRET_KEY="test-secret", BLOG_ADMIN_PASSWORD="correct horse",
                      BLOG_TIMEZONE="America/Los_Angeles", DAILY_ISSUES_DIR=str(Path(tmp) / "issues"),
                      DAILY_EDITOR_LOG=str(Path(tmp) / "events.jsonl"))
    client = app.test_client()
    with client.session_transaction() as session:
        session["daily_admin"] = True
        session["admin_csrf"] = "known-token"
    return client


def test_anonymous_admin_routes_are_rejected():
    client = configured_client()
    with patch("ingest_jobs.start_job") as start_job, patch("ingest_jobs.get_job") as get_job, patch("today_signal.read_signal_cache") as read_cache:
        assert client.post("/ingest", json={"url": "https://youtube.com/watch?v=x"}).status_code == 401
        assert client.get("/ingest/status?job_id=x").status_code == 401
        assert client.post("/signal/attention", json={"action": "dismiss", "item_id": "x"}).status_code == 401
        assert client.get("/admin/daily/draft?date=2026-07-11").status_code == 401
        for action in ("preview", "publish", "revise"):
            assert client.post(f"/admin/daily/2026-07-11/{action}", json={}).status_code == 401
        start_job.assert_not_called()
        get_job.assert_not_called()
        read_cache.assert_not_called()


def test_login_uses_csrf_and_creates_admin_session():
    client = configured_client()
    page = client.get("/admin/login")
    assert page.status_code == 200
    assert page.headers["Cache-Control"] == "no-store"
    with client.session_transaction() as session:
        token = session["admin_csrf"]
    assert client.post("/admin/login", data={"password": "wrong", "csrf_token": token}).status_code == 401
    assert client.post("/admin/login", data={"password": "correct horse", "csrf_token": token}).status_code == 302
    with client.session_transaction() as session:
        assert session["daily_admin"] is True


def test_admin_posts_require_csrf_but_track_stays_public():
    client = configured_client()
    with client.session_transaction() as session:
        session["daily_admin"] = True
        session["admin_csrf"] = "known-token"
    assert client.post("/ingest", json={}).status_code == 403
    assert client.post("/signal/attention", json={}).status_code == 403
    assert client.post("/admin/logout").status_code == 403
    for action in ("preview", "publish", "revise"):
        assert client.post(f"/admin/daily/2026-07-11/{action}", json={}).status_code == 403
    assert client.post("/admin/logout", headers={"X-CSRF-Token": "known-token"}).status_code == 302
    assert configured_client().post("/track", json={"kind": "test"}).status_code == 204


def test_admin_mutations_proceed_with_known_csrf_and_admin_html_is_not_cached():
    client = configured_client()
    with client.session_transaction() as session:
        session["daily_admin"] = True
        session["admin_csrf"] = "known-token"
    with patch("ingest_jobs.start_job", return_value={"status": "queued", "job_id": "job-1"}) as start_job:
        response = client.post(
            "/ingest",
            json={"url": "https://youtube.com/watch?v=x"},
            headers={"X-CSRF-Token": "known-token"},
        )
        assert response.status_code == 200
        start_job.assert_called_once()
    with patch("today_signal.read_signal_cache", return_value={"signals": [], "attention": []}), patch("today_signal.dismiss_attention_item", return_value=({"signals": [], "attention": []}, False)) as dismiss:
        response = client.post(
            "/signal/attention",
            json={"action": "dismiss", "item_id": "x"},
            headers={"X-CSRF-Token": "known-token"},
        )
        assert response.status_code == 200
        dismiss.assert_called_once()
    page = client.get("/")
    assert b"known-token" not in page.data
    assert page.headers["Cache-Control"] == "no-store"


def test_draft_preview_publish_duplicate_and_audit():
    with TemporaryDirectory() as tmp:
        client = admin_client(tmp)
        now = datetime.fromisoformat("2026-07-11T09:30:00-07:00")
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value=cache()):
            draft = client.get("/admin/daily/draft?date=2026-07-11")
            assert draft.status_code == 200
            assert draft.get_json()["draft"]["topics"][0]["topic_id"] == "topic-a"
            preview = client.post("/admin/daily/2026-07-11/preview",
                headers={"X-CSRF-Token": "known-token"},
                json={"preview_surface": "home", "topics": [{"topic_id": "topic-a"}]})
            assert preview.status_code == 200 and "今天" in preview.get_json()["html"]
            assert not (Path(tmp) / "issues" / "2026-07-11.json").exists()
            dated = client.post("/admin/daily/2026-07-11/preview",
                headers={"X-CSRF-Token": "known-token"},
                json={"preview_surface": "dated", "topics": [{"topic_id": "topic-a"}]})
            assert dated.status_code == 200 and "这一天" in dated.get_json()["html"]
            assert client.post("/admin/daily/2026-07-11/preview", headers={"X-CSRF-Token": "known-token"},
                json={"preview_surface": "evil", "topics": [{"topic_id": "topic-a"}]}).status_code == 400
            published = client.post("/admin/daily/2026-07-11/publish",
                headers={"X-CSRF-Token": "known-token"},
                json={"topics": [{"topic_id": "topic-a", "title": "人工标题"}]})
            assert published.status_code == 201
            assert published.get_json()["issue"]["topics"][0]["title"] == "人工标题"
            assert published.get_json()["issue"]["topics"][0]["sources"][0]["url"] == "https://official.ai/release"
            assert "draft" not in published.get_json()
            duplicate = client.post("/admin/daily/2026-07-11/publish",
                headers={"X-CSRF-Token": "known-token"}, json={"topics": [{"topic_id": "topic-a"}]})
            assert duplicate.status_code == 409 and duplicate.get_json()["code"] == "already_published"
        event = json.loads((Path(tmp) / "events.jsonl").read_text(encoding="utf-8").splitlines()[0])
        assert event["ts"] == "2026-07-11T09:30:00-07:00" and event["kind"] == "publish"


def test_publish_validation_and_revision_conflict():
    with TemporaryDirectory() as tmp:
        client = admin_client(tmp)
        headers = {"X-CSRF-Token": "known-token"}
        now = datetime.fromisoformat("2026-07-11T09:30:00-07:00")
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value=cache()):
            assert client.get("/admin/daily/draft?date=not-a-date").status_code == 400
            assert client.post("/admin/daily/not-a-date/publish", headers=headers,
                               json={"topics": [{"topic_id": "topic-a"}]}).status_code == 400
            assert client.post("/admin/daily/2026-07-10/publish", headers=headers,
                               json={"topics": [{"topic_id": "topic-a"}]}).status_code == 409
            assert client.post("/admin/daily/2026-07-11/publish", headers=headers,
                               json={"topics": []}).status_code == 400
            assert client.post("/admin/daily/2026-07-11/publish", headers=headers,
                               json={"topics": [{"topic_id": "topic-a"}]}).status_code == 201
            assert client.post("/admin/daily/2026-07-11/revise", headers=headers,
                               json={"topics": [{"topic_id": "topic-a"}]}).status_code == 400
            revised = client.post("/admin/daily/2026-07-11/revise", headers=headers,
                json={"expected_revision": 1, "topics": [{"topic_id": "topic-a", "title": "R2"}]})
            assert revised.status_code == 200 and revised.get_json()["issue"]["revision"] == 2
            conflict = client.post("/admin/daily/2026-07-11/revise", headers=headers,
                json={"expected_revision": 1, "topics": [{"topic_id": "topic-a"}]})
            assert conflict.status_code == 409 and conflict.get_json()["code"] == "revision_conflict"


def test_editor_rejects_non_object_json_and_reports_audit_failure_after_commit():
    with TemporaryDirectory() as tmp:
        client = admin_client(tmp)
        headers = {"X-CSRF-Token": "known-token"}
        now = datetime.fromisoformat("2026-07-11T09:30:00-07:00")
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value=cache()):
            for payload in (["topic-a"], "topic-a", 7, True):
                response = client.post(
                    "/admin/daily/2026-07-11/publish",
                    headers=headers,
                    json=payload,
                )
                assert response.status_code == 400
            with patch("daily_editor.append_editor_event", side_effect=OSError("disk full")):
                response = client.post(
                    "/admin/daily/2026-07-11/publish",
                    headers=headers,
                    json={"topics": [{"topic_id": "topic-a"}]},
                )
            assert response.status_code == 201
            assert response.get_json()["status"] == "ok"
            assert response.get_json()["audit_status"] == "failed"
            assert (Path(tmp) / "issues" / "2026-07-11.json").exists()


def test_missing_cache_blocks_first_publish_but_not_stored_revision():
    with TemporaryDirectory() as tmp:
        client = admin_client(tmp); headers = {"X-CSRF-Token": "known-token"}
        now = datetime.fromisoformat("2026-07-11T09:30:00-07:00")
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value={}):
            assert client.get("/admin/daily/draft?date=2026-07-11").status_code == 409
            assert client.post("/admin/daily/2026-07-11/publish", headers=headers,
                json={"topics": [{"topic_id": "topic-a"}]}).status_code == 409
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value=cache()):
            assert client.post("/admin/daily/2026-07-11/publish", headers=headers,
                               json={"topics": [{"topic_id": "topic-a"}]}).status_code == 201
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value={}):
            response = client.get("/admin/daily/draft?date=2026-07-11")
            assert response.status_code == 200
            assert response.get_json()["draft"]["topics"][0]["topic_id"] == "topic-a"
            assert client.post("/admin/daily/2026-07-11/revise", headers=headers,
                json={"expected_revision": 1, "topics": [{"topic_id": "topic-a"}]}).status_code == 200


def test_historical_revision_ignores_unrelated_today_cache():
    with TemporaryDirectory() as tmp:
        client = admin_client(tmp); headers = {"X-CSRF-Token": "known-token"}
        then = datetime.fromisoformat("2026-07-10T09:30:00-07:00")
        with patch("app._local_now", return_value=then), patch("today_signal.read_signal_cache", return_value=cache("2026-07-10")):
            assert client.post("/admin/daily/2026-07-10/publish", headers=headers,
                json={"topics": [{"topic_id": "topic-a"}]}).status_code == 201
        today = datetime.fromisoformat("2026-07-11T09:30:00-07:00")
        unrelated = cache(); unrelated["daily_draft"]["topics"] = [topic("unrelated")]
        with patch("app._local_now", return_value=today), patch("today_signal.read_signal_cache", return_value=unrelated):
            draft = client.get("/admin/daily/draft?date=2026-07-10")
            assert draft.status_code == 200
            groups = draft.get_json()["draft"]
            ids = [row["topic_id"] for group in ("topics", "candidates", "attention") for row in groups[group]]
            assert ids == list(dict.fromkeys(ids)) and "unrelated" not in ids
            assert client.post("/admin/daily/2026-07-10/revise", headers=headers,
                json={"expected_revision": 1, "topics": [{"topic_id": "topic-a"}]}).status_code == 200


def test_corrupt_current_with_public_fallback_disables_admin_writes():
    with TemporaryDirectory() as tmp:
        client = admin_client(tmp); headers = {"X-CSRF-Token": "known-token"}
        now = datetime.fromisoformat("2026-07-11T09:30:00-07:00")
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value=cache()):
            assert client.post("/admin/daily/2026-07-11/publish", headers=headers,
                json={"topics": [{"topic_id": "topic-a"}]}).status_code == 201
            assert client.post("/admin/daily/2026-07-11/revise", headers=headers,
                json={"expected_revision": 1, "topics": [{"topic_id": "topic-a", "title": "R2"}]}).status_code == 200
        current = Path(tmp) / "issues" / "2026-07-11.json"
        current.write_text("{broken", encoding="utf-8")
        before = current.read_bytes()
        with patch("app._local_now", return_value=now), patch("today_signal.read_signal_cache", return_value=cache()):
            assert client.get("/daily/2026-07-11").status_code == 200
            draft = client.get("/admin/daily/draft?date=2026-07-11")
            assert draft.status_code == 503 and draft.get_json()["code"] == "storage_corrupt"
            revised = client.post("/admin/daily/2026-07-11/revise", headers=headers,
                json={"expected_revision": 2, "topics": [{"topic_id": "topic-a"}]})
            assert revised.status_code == 503 and revised.get_json()["code"] == "storage_corrupt"
            page = client.get("/daily/2026-07-11")
            assert page.status_code == 200
        assert current.read_bytes() == before


if __name__ == "__main__":
    test_anonymous_admin_routes_are_rejected()
    test_login_uses_csrf_and_creates_admin_session()
    test_admin_posts_require_csrf_but_track_stays_public()
    test_admin_mutations_proceed_with_known_csrf_and_admin_html_is_not_cached()
    test_draft_preview_publish_duplicate_and_audit()
    test_publish_validation_and_revision_conflict()
    test_editor_rejects_non_object_json_and_reports_audit_failure_after_commit()
    test_missing_cache_blocks_first_publish_but_not_stored_revision()
    test_historical_revision_ignores_unrelated_today_cache()
    test_corrupt_current_with_public_fallback_disables_admin_writes()
    print("全部通过 ✅")
