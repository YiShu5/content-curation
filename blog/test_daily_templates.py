"""Public daily template tests.

Run: blog/.venv/bin/python blog/test_daily_templates.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from flask import render_template

from app import app


def source(source_id="source-1", publisher="Official", status="readable"):
    return {
        "source_id": source_id,
        "title": f"Source {source_id}",
        "url": f"https://example.com/{source_id}",
        "canonical_url": f"https://example.com/{source_id}",
        "publisher": publisher,
        "publisher_key": publisher.lower(),
        "published_at": "2026-07-11T08:00:00-07:00",
        "is_primary": True,
        "verification_status": status,
    }


def issue_fixture(topic_count=3, source_count=2, attention=None):
    topics = []
    for rank in range(1, topic_count + 1):
        sources = [source(f"source-{rank}-{i}") for i in range(1, source_count + 1)]
        topics.append({
            "topic_id": f"topic-{rank}",
            "rank": rank,
            "category": "AI 前沿",
            "title": f"值得知道的讨论 {rank}",
            "what_happened": "这是事件的准确摘要。",
            "discussion_focus": ["产品影响", "行业反应", "后续变化"],
            "why_ranked": "它可能影响下一步判断。",
            "sources": sources,
            "independent_source_count": source_count,
        })
    return {
        "issue_date": "2026-07-11",
        "issue_number": 7,
        "revision": 1,
        "revised_at": "2026-07-11T09:00:00-07:00",
        "topics": topics,
        "attention": [] if attention is None else attention,
    }


def render_brief(issue, *, is_home=True, is_current_day=True):
    with app.test_request_context("/"):
        return render_template(
            "_daily_brief.html", issue=issue,
            is_home=is_home, is_current_day=is_current_day,
        )


def test_three_topics_render_one_lead_and_two_side_cards():
    html = render_brief(issue_fixture(topic_count=3))
    assert 'class="daily-topic-grid daily-topic-count-3"' in html
    assert html.count('class="daily-topic ') == 3
    assert "daily-topic-rank-1" in html
    assert "daily-topic-rank-2" in html
    assert "daily-topic-rank-3" in html
    assert "2 个相关来源已合并" in html
    assert "2026.07.11" in html


def test_single_source_does_not_claim_sources_were_merged():
    html = render_brief(issue_fixture(topic_count=1, source_count=1))
    assert "相关来源已合并" not in html
    assert "Official" in html


def test_public_template_contains_no_management_payload():
    html = render_brief(issue_fixture(topic_count=3))
    assert "发布今日" not in html
    assert "修订本期" not in html
    assert "data-candidates" not in html
    assert "加入首页判断" not in html


def test_one_and_two_topic_states_do_not_render_phantom_slots():
    one = render_brief(issue_fixture(topic_count=1, attention=[]))
    assert "daily-topic-count-1" in one
    assert one.count('class="daily-topic ') == 1
    assert "今天仅有 1 个主题达到标准" in one
    assert "daily-attention" not in one
    two = render_brief(issue_fixture(topic_count=2, attention=[]))
    assert "daily-topic-count-2" in two
    assert two.count('class="daily-topic ') == 2
    assert "daily-topic-rank-3" not in two
    assert "今天仅有 2 个主题达到标准" in two


def test_unavailable_source_is_plain_text_and_attention_is_minimal():
    attention = issue_fixture(topic_count=1, source_count=1)["topics"]
    attention[0]["attention_status"] = "rising"
    issue = issue_fixture(topic_count=1, attention=attention)
    issue["topics"][0]["sources"][0]["verification_status"] = "unavailable"
    html = render_brief(issue)
    assert "讨论上升中" in html
    assert "来源暂不可访问" in html
    attention_html = html.split("daily-attention", 1)[1]
    assert "<details" not in attention_html


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"OK: {len(tests)} daily template tests passed")
