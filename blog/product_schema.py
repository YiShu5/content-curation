"""Shared product schema for topics and score dimensions."""

import json
from pathlib import Path


ROOT = Path(__file__).parent.parent
SCHEMA_PATH = ROOT / "config" / "product_schema.json"


def _load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


_SCHEMA = _load_schema()
TOPICS = list(_SCHEMA["topics"])
UNKNOWN_TOPIC = str(_SCHEMA.get("unknown_topic") or "其他")
SCORE_DIMENSIONS = list(_SCHEMA["score_dimensions"])


def normalize_topic(value):
    topic = str(value or "").strip()
    return topic if topic in TOPICS else UNKNOWN_TOPIC
