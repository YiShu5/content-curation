import hmac
import secrets
from functools import wraps

from flask import abort, current_app, jsonify, request, session


def is_admin():
    return session.get("daily_admin") is True


def csrf_token():
    token = session.get("admin_csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        session["admin_csrf"] = token
    return token


def login_admin(password):
    expected = str(current_app.config.get("BLOG_ADMIN_PASSWORD") or "")
    valid = bool(expected) and hmac.compare_digest(str(password or ""), expected)
    if valid:
        session.clear()
        session["daily_admin"] = True
        session["admin_csrf"] = secrets.token_urlsafe(32)
    return valid


def logout_admin():
    session.clear()


def validate_csrf():
    supplied = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token") or ""
    expected = session.get("admin_csrf") or ""
    if not expected or not hmac.compare_digest(str(supplied), str(expected)):
        abort(403)


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not is_admin():
            return jsonify({"status": "unauthorized"}), 401
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            validate_csrf()
        return view(*args, **kwargs)
    return wrapped
