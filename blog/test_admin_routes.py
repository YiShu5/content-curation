"""Administrator route tests. Run: blog/.venv/bin/python blog/test_admin_routes.py"""

from app import app


def configured_client():
    app.config.update(TESTING=True, SECRET_KEY="test-secret", BLOG_ADMIN_PASSWORD="correct horse")
    return app.test_client()


def test_anonymous_admin_routes_are_rejected():
    client = configured_client()
    assert client.post("/ingest", json={"url": "https://youtube.com/watch?v=x"}).status_code == 401
    assert client.get("/ingest/status?job_id=x").status_code == 401
    assert client.post("/signal/attention", json={"action": "dismiss", "item_id": "x"}).status_code == 401


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


if __name__ == "__main__":
    test_anonymous_admin_routes_are_rejected()
    test_login_uses_csrf_and_creates_admin_session()
    test_admin_posts_require_csrf_but_track_stays_public()
    print("全部通过 ✅")
