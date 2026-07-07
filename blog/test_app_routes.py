"""Flask route smoke tests.

Run: blog/.venv/bin/python blog/test_app_routes.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app import app


def test_homepage_renders():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert "降噪" in resp.get_data(as_text=True)
    print("✓ homepage renders")


if __name__ == "__main__":
    test_homepage_renders()
    print("\n全部通过 ✅")
