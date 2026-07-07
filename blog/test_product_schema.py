"""Shared product schema tests.

Run: blog/.venv/bin/python blog/test_product_schema.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import product_schema as schema


def test_topics_include_ai_frontier_and_unknown_falls_back():
    assert schema.TOPICS == [
        "AI 前沿", "AI 编程", "AI 产品", "AI 创业",
        "AI 商业", "投资", "个人效率", "其他",
    ]
    assert schema.normalize_topic("AI 前沿") == "AI 前沿"
    assert schema.normalize_topic(" 不存在的话题 ") == "其他"
    assert schema.normalize_topic("") == "其他"
    print("✓ topics schema")


def test_score_dimensions_are_current_three_axis():
    assert schema.SCORE_DIMENSIONS == [
        {"key": "insight", "label": "洞察原创", "max": 50},
        {"key": "source", "label": "信源质量", "max": 25},
        {"key": "storytelling", "label": "故事可读", "max": 25},
    ]
    print("✓ score dimensions schema")


if __name__ == "__main__":
    test_topics_include_ai_frontier_and_unknown_falls_back()
    test_score_dimensions_are_current_three_axis()
    print("\n全部通过 ✅")
