"""Administrator route tests. Run: blog/.venv/bin/python blog/test_admin_routes.py"""

from unittest.mock import patch

from app import app


def configured_client():
    app.config.update(TESTING=True, SECRET_KEY="test-secret", BLOG_ADMIN_PASSWORD="correct horse")
    return app.test_client()


def test_anonymous_admin_routes_are_rejected():
    client = configured_client()
    with patch("ingest_jobs.start_job") as start_job, patch("ingest_jobs.get_job") as get_job, patch("today_signal.read_signal_cache") as read_cache:
        assert client.post("/ingest", json={"url": "https://youtube.com/watch?v=x"}).status_code == 401
        assert client.get("/ingest/status?job_id=x").status_code == 401
        assert client.post("/signal/attention", json={"action": "dismiss", "item_id": "x"}).status_code == 401
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


if __name__ == "__main__":
    test_anonymous_admin_routes_are_rejected()
    test_login_uses_csrf_and_creates_admin_session()
    test_admin_posts_require_csrf_but_track_stays_public()
    test_admin_mutations_proceed_with_known_csrf_and_admin_html_is_not_cached()
    print("全部通过 ✅")
