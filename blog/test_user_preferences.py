"""User preference behavior-learning tests.

Run: blog/.venv/bin/python blog/test_user_preferences.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import user_preferences as prefs


def test_behavior_summary_covers_frontend_events():
    old_path = prefs.CLICK_LOG
    profile = {
        "learning": {
            "enabled": True,
            "days": 90,
            "event_weights": {
                "card": 0.3,
                "open_attention": 0.5,
                "open_news": 0.5,
                "watch_video": 1.0,
                "open_breaking": 1.5,
                "open_local": 1.5,
                "promote_attention": 2.0,
                "deep_library": 3.0,
            },
        }
    }
    with tempfile.TemporaryDirectory() as td:
        prefs.CLICK_LOG = Path(td) / "clicks.log"
        prefs.CLICK_LOG.write_text(
            "\n".join([
                '{"ts":"2026-07-07 08:31:00","kind":"card","slot":"library","source":"archive"}',
                '{"ts":"2026-07-07 08:32:00","kind":"open_attention","slot":"attention","source":"AI HOT"}',
                '{"ts":"2026-07-07 08:33:00","kind":"promote_attention","slot":"attention","source":"AI HOT"}',
                '{"ts":"2026-07-07 08:34:00","kind":"dismiss_attention","slot":"attention","source":"AI HOT"}',
            ]),
            encoding="utf-8",
        )
        summary = prefs.behavior_summary(profile)
    prefs.CLICK_LOG = old_path
    assert summary["events_considered"] == 3
    assert summary["slot_weights"]["attention"] == 2.5
    assert summary["slot_weights"]["library"] == 0.3
    print("✓ behavior weights cover frontend positive events")


def test_config_preferences_include_actual_positive_events():
    profile = prefs.load_profile()
    weights = (profile.get("learning") or {}).get("event_weights") or {}
    for key in ["card", "open_attention", "open_news", "watch_video", "open_breaking", "open_local", "open_origin", "share_card", "promote_attention", "deep_library"]:
        assert float(weights.get(key, 0)) > 0, key
    assert float(weights.get("dismiss_attention", 0) or 0) == 0
    print("✓ config preferences include actual positive events")


if __name__ == "__main__":
    test_behavior_summary_covers_frontend_events()
    test_config_preferences_include_actual_positive_events()
    print("\n全部通过 ✅")
