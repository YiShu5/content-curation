"""今日必读延伸视频推荐的离线测试。

运行：blog/.venv/bin/python blog/test_today_signal.py
"""

import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import today_signal as ts
import user_preferences as prefs
from tool_probe import probe_command


def _candidate(video_id, *, duration=1800, title="候选", channel="Example"):
    return {
        "id": video_id,
        "title": title,
        "duration": duration,
        "channel": channel,
        "description": "解释热点背后的机制、案例和产品决策。",
        "upload_date": "20260701",
        "view_count": 1000,
        "url": f"https://www.youtube.com/watch?v={video_id}",
    }


def test_probe():
    assert probe_command(sys.executable, ["--version"]).ok
    assert probe_command("__definitely_missing_noisefilter__").status == "missing"
    print("✓ Agent-Reach 工具探活")


def test_suggest_video_selects_complement():
    old_search, old_chat = ts._yt_search, ts._chat_json
    try:
        ts._yt_search = lambda query: [
            _candidate("too-short", duration=300),
            _candidate("already-used"),
            _candidate("best-video", title="真正补足热点的视频"),
        ]
        ts._chat_json = lambda prompt, temperature=0.1: {
            "pick": {
                "index": 1,
                "match_score": 88,
                "complement_reason": "热点只给出结果，这段视频进一步解释背后的机制与实际案例",
            }
        }
        signal = {
            "title": "一条热点",
            "summary": "热点总结。",
            "why": "产品价值。",
            "missing_angle": "背后的机制与案例",
            "video_queries": ["AI product mechanism examples"],
        }
        picked = ts.suggest_video(signal, {"already-used"})
        assert picked["id"] == "best-video", picked
        assert picked["match_score"] == 88
        assert picked["published"] == "2026-07-01"
        assert picked["complement_reason"].endswith("。")
        print("✓ 过滤短视频/已入库内容并选择互补视频")
    finally:
        ts._yt_search, ts._chat_json = old_search, old_chat


def test_suggest_video_rejects_weak_match():
    old_search, old_chat = ts._yt_search, ts._chat_json
    try:
        ts._yt_search = lambda query: [_candidate("weak-video")]
        ts._chat_json = lambda prompt, temperature=0.1: {
            "pick": {
                "index": 1,
                "match_score": 74,
                "complement_reason": "只有关键词相关",
            }
        }
        signal = {"title": "热点", "video_queries": ["query"]}
        assert ts.suggest_video(signal, set()) is None
        print("✓ 低于 75 分不展示")
    finally:
        ts._yt_search, ts._chat_json = old_search, old_chat


def test_normalize_editor_pick_breaking_action():
    raw = {
        "index": 1,
        "summary": "Fable 5 发布并开放测试",
        "why": "这会改变未来几个月 C 端 Agent 的交互门槛",
        "action": "本周应该测试",
        "missing_angle": "真实使用场景",
        "video_queries": ["Fable 5 agent product demo", "AI agent consumer UX"],
    }
    picked = ts._normalize_editor_pick(
        raw,
        [{"title": "Fable 5 发布", "url": "https://example.com/fable", "source": "Official"}],
        breaking=True,
        actions=["本周应该测试", "值得持续关注", "暂时知道即可"],
    )
    assert picked["is_breaking"] is True
    assert picked["action"] == "本周应该测试"
    assert picked["summary"].endswith("。")
    assert picked["why"].endswith("。")
    assert picked["verification_label"] == "已核对原文"
    print("✓ 大新闻归一化包含行动判断与原文核验标记")


def test_priority_model_research_detected_and_ranked():
    priority = {
        "title": "语言模型中的全局工作空间",
        "source": "Anthropic：Research（发表成果 · 网页）",
        "url": "https://www.anthropic.com/research/global-workspace",
        "summary": "Anthropic在Claude中发现一组名为J-space的内部神经模式，可用于监测隐藏目标和虚假数据。",
        "score": 1,
    }
    generic = {
        "title": "普通高分行业新闻",
        "source": "Example",
        "url": "https://example.com/news",
        "summary": "一条普通趋势。",
        "score": 999,
        "category": "tip",
    }
    broad_interpretability = {
        "title": "用可解释性理解标注者安全策略",
        "source": "Apple Machine Learning Research（RSS）",
        "url": "https://machinelearning.apple.com/research/annotator-safety-policy-interpretability",
        "summary": "标注分歧可源于操作失败、政策模糊或价值多元。",
        "score": 100,
    }
    assert ts._priority_signal_kind(priority)["slot"] == "industry_trend"
    assert ts._priority_signal_kind(broad_interpretability) is None
    assert ts._pool_candidates([generic, priority])[0]["title"] == priority["title"]
    print("✓ 官方模型机制研究会被识别，泛可解释性论文不会误命中")


def test_priority_model_research_overrides_generic_industry_trend():
    candidates = [
        {
            "title": "普通就业趋势",
            "url": "https://example.com/jobs",
            "source": "Example",
            "summary": "初级开发者就业变化。",
            "_original": {"text": "原文"},
        },
        {
            "title": "语言模型中的全局工作空间",
            "source": "Anthropic：Research（发表成果 · 网页）",
            "url": "https://www.anthropic.com/research/global-workspace",
            "summary": "Anthropic在Claude中发现一组名为J-space的内部神经模式，类似神经科学的全局工作空间。",
            "_original": {"text": "原文"},
        },
    ]
    signals = [ts._normalize_editor_pick(
        {"index": 1, "summary": "就业趋势。", "why": "影响人才结构。"},
        candidates,
        slot="industry_trend",
        slot_label="1–3 个月行业趋势",
    )]
    ensured = ts._ensure_priority_research_signal(
        signals,
        candidates,
        used_indices={1},
        slots=[{"key": "industry_trend", "label": "1–3 个月行业趋势"}],
    )
    assert len(ensured) == 1
    assert ensured[0]["title"] == "语言模型中的全局工作空间"
    assert ensured[0]["priority_label"] == "模型内部机制与可解释性"
    print("✓ 官方模型机制研究会替换普通行业趋势")


def test_attention_candidate_surfaces_buzzy_unselected_item():
    item = {
        "title": "语言模型中的全局工作空间",
        "source": "Anthropic：Research（发表成果 · 网页）",
        "url": "https://www.anthropic.com/research/global-workspace",
        "summary": "Anthropic在Claude中发现名为J-space的内部神经模式。",
        "score": 90,
    }
    attention = ts._build_attention_candidates([item], selected_items=[])
    assert len(attention) == 1
    assert attention[0]["title"] == item["title"]
    assert attention[0]["buzz_label"] == "模型内部机制与可解释性"
    assert ts._build_attention_candidates([item], selected_items=[item]) == []
    print("✓ 高优先级热议内容未入选时会浮现给用户确认")


def test_promote_attention_item_adds_manual_signal_without_file_write():
    old_write = ts._write_signal_cache
    try:
        ts._write_signal_cache = lambda payload: payload
        cache = {
            "signals": [],
            "attention": [{
                "item_id": "hot1",
                "title": "一条热议内容",
                "url": "https://example.com/hot",
                "source": "AI HOT",
                "summary": "很多人在讨论。",
                "why": "需要用户确认是否值得看。",
                "suggested_slot": "industry_trend",
            }],
        }
        updated, changed = ts.promote_attention_item(cache, "hot1")
    finally:
        ts._write_signal_cache = old_write
    assert changed is True
    assert updated["attention"] == []
    assert updated["signals"][0]["slot_label"] == "热议补充"
    assert updated["signals"][0]["manual_promoted"] is True
    print("✓ 用户确认后热议候选可加入首页判断")


def test_evidence_status_for_signal_shapes():
    assert ts.evidence_status({"links": [{"title": "库内"}]}) == "linked"
    assert ts.evidence_status({"suggest": {"title": "外部视频"}}) == "suggested"
    assert ts.evidence_status({"links": [], "suggest": None}) == "pending"
    print("✓ evidence status follows links/suggest/pending")


def test_promoted_attention_without_links_has_pending_evidence():
    old_write = ts._write_signal_cache
    try:
        ts._write_signal_cache = lambda payload: payload
        cache = {
            "signals": [],
            "attention": [{
                "item_id": "hot-pending",
                "title": "一条热议内容",
                "url": "https://example.com/hot",
                "source": "AI HOT",
                "summary": "很多人在讨论。",
                "why": "需要用户确认是否值得看。",
                "suggested_slot": "industry_trend",
            }],
        }
        updated, changed = ts.promote_attention_item(cache, "hot-pending")
    finally:
        ts._write_signal_cache = old_write
    assert changed is True
    assert updated["signals"][0]["manual_promoted"] is True
    assert updated["signals"][0]["evidence_status"] == "pending"
    print("✓ 手动加入但暂无证据时显示 pending")


def test_behavior_summary_positive_events_only():
    old_path = prefs.CLICK_LOG
    profile = {
        "learning": {
            "enabled": True,
            "days": 90,
            "event_weights": {
                "open_news": 0.5,
                "open_local": 1.5,
                "deep_library": 3.0,
            },
        }
    }
    with tempfile.TemporaryDirectory() as td:
        prefs.CLICK_LOG = Path(td) / "clicks.log"
        prefs.CLICK_LOG.write_text(
            "\n".join([
                '{"ts":"2026-07-07 08:31:00","kind":"open_news","slot":"consumer_growth","source":"aihot"}',
                '{"ts":"2026-07-07 08:32:00","kind":"deep_library","slot":"consumer_growth","source":"youtube"}',
                '{"ts":"2026-07-07 08:33:00","kind":"ignored","slot":"industry_trend","source":"aihot"}',
            ]),
            encoding="utf-8",
        )
        summary = prefs.behavior_summary(profile)
    prefs.CLICK_LOG = old_path
    assert summary["events_considered"] == 2
    assert summary["slot_weights"]["consumer_growth"] == 3.5
    assert "industry_trend" not in summary["slot_weights"]
    print("✓ 行为学习只累计正向动作，不把无操作当负反馈")


def test_suggestion_card_renders_explicit_confirmation_without_scores():
    from flask import render_template
    from app import app

    signal = {
        "title": "热点标题",
        "url": "https://example.com/news",
        "source": "测试信源",
        "summary": "一句完整总结。",
        "why": "产品人需要关注。",
        "links": [],
        "suggest": {
            "title": "互补视频",
            "url": "https://www.youtube.com/watch?v=abcdefghijk",
            "channel": "Example",
            "dur_min": 28,
            "published": "2026-07-01",
            "match_score": 88,
            "complement_reason": "热点给出结果；视频补充机制与真实案例。",
            "from_whitelist": True,
        },
        "slot": "consumer_growth",
        "slot_label": "C 端 AI 产品与增长",
        "item_id": "abc123",
    }
    with app.test_request_context("/"):
        html = render_template(
            "_signals.html",
            breaking=None,
            signals=[signal],
            signal_meta={"window_hours": 48, "generated_at": "2026-07-07 08:30"},
        )
    assert "库里缺这一块" in html
    assert "88% 互补" not in html
    assert "先看视频" in html
    assert "加入深度库" in html
    assert "确认入库" not in html
    assert "window.confirm" in html
    assert 'data-track-kind="watch_video"' in html
    print("✓ 推荐卡片隐藏内部评分，展示补足理由并二次确认")


def test_cached_library_link_enriches_and_renders_quote():
    from flask import render_template
    from app import app

    cache = {
        "signals": [{
            "title": "语言模型中的全局工作空间",
            "url": "https://example.com/news",
            "source": "测试信源",
            "summary": "一句完整总结。",
            "why": "产品人需要关注。",
            "links": [{
                "record_id": "local1",
                "title": "可解释性：理解AI模型如何思考",
                "platform": "YouTube",
                "deeplink": "https://www.youtube.com/watch?v=fGKNUvivvnc&t=30s",
                "ts": "0:30",
            }],
            "slot": "industry_trend",
            "slot_label": "1–3 个月行业趋势",
            "item_id": "abc123",
        }]
    }
    records = [{
        "id": "local1",
        "guests": "Jack、Emmanuel、Josh",
        "key_quotes": [
            "我们有时能抓住模型在写下它声称的思考过程的同时，看到它大脑里真正的思考过程——两者不一样。"
        ],
    }]
    enriched = ts.enrich_cached_link_quotes(cache, records)
    link = enriched["signals"][0]["links"][0]
    assert link["quote"].startswith("我们有时能抓住模型")
    assert link["quote_speaker"] == "Jack"

    with app.test_request_context("/"):
        html = render_template(
            "_signals.html",
            breaking=None,
            signals=enriched["signals"],
            attention=[],
            signal_meta={"window_hours": 48},
        )
    assert "你库里的相关金句" in html
    assert "Jack 说" in html
    assert "从 0:30 看" in html
    assert "signal-quote-link" in html
    print("✓ 库内补充展示为相关金句")


def test_attention_card_renders_user_choice():
    from flask import render_template
    from app import app

    attention = [{
        "item_id": "hot1",
        "title": "语言模型中的全局工作空间",
        "url": "https://www.anthropic.com/research/global-workspace",
        "source": "Anthropic Research",
        "summary": "Anthropic发现J-space内部神经模式。",
        "buzz_label": "模型内部机制与可解释性",
        "buzz_reason": "一手研究揭示模型内部机制。",
    }]
    with app.test_request_context("/"):
        html = render_template(
            "_signals.html",
            breaking=None,
            signals=[],
            attention=attention,
            signal_meta={"window_hours": 48},
        )
    assert "热议浮现" in html
    assert "加入首页判断" in html
    assert "先不加" in html
    assert "/signal/attention" in html
    print("✓ 热议浮现卡片展示用户选择")


def test_breaking_card_renders_action():
    from flask import render_template
    from app import app

    breaking = {
        "title": "Fable 5 正式发布",
        "url": "https://example.com/fable",
        "source": "Official",
        "summary": "Fable 5 正式发布并提供新的 Agent 产品形态。",
        "why": "它可能改变未来 1–3 个月的 C 端 Agent 交互设计。",
        "action": "本周应该测试",
        "verification_label": "已核对原文",
        "is_breaking": True,
        "item_id": "breaking1",
        "links": [],
    }
    with app.test_request_context("/"):
        html = render_template(
            "_signals.html",
            breaking=breaking,
            signals=[],
            signal_meta={"window_hours": 48},
        )
    assert "顶级大新闻" in html
    assert "本周应该测试" in html
    assert 'data-track-kind="open_breaking"' in html
    print("✓ 顶级大新闻展示行动判断")


def test_signal_freshness_daily_window():
    profile = {"delivery": {"hour": 8, "minute": 30}}
    payload = {"generated_at": "2026-07-07 08:31", "signals": []}
    fresh = ts.signal_freshness(
        payload,
        now_ts=datetime(2026, 7, 7, 9, 0).timestamp(),
        profile=profile,
    )
    assert fresh["status"] == "fresh", fresh
    assert fresh["label"] == "新鲜"
    expired = ts.signal_freshness(
        payload,
        now_ts=datetime(2026, 7, 8, 8, 31).timestamp(),
        profile=profile,
    )
    assert expired["status"] == "expired", expired
    assert expired["is_expired"] is True
    print("✓ 今日判断按每日 8:30 窗口判断 freshness")


def test_signal_freshness_stays_fresh_until_next_delivery_time():
    profile = {"delivery": {"hour": 8, "minute": 30}}
    payload = {"generated_at": "2026-07-07 08:31", "signals": []}

    next_day_early = ts.signal_freshness(
        payload,
        now_ts=datetime(2026, 7, 8, 1, 0).timestamp(),
        profile=profile,
    )
    next_day_before_delivery = ts.signal_freshness(
        payload,
        now_ts=datetime(2026, 7, 8, 8, 29).timestamp(),
        profile=profile,
    )
    at_next_delivery = ts.signal_freshness(
        payload,
        now_ts=datetime(2026, 7, 8, 8, 30).timestamp(),
        profile=profile,
    )

    assert next_day_early["status"] == "fresh", next_day_early
    assert next_day_before_delivery["status"] == "fresh", next_day_before_delivery
    assert at_next_delivery["status"] == "expired", at_next_delivery
    print("✓ 今日判断在次日 8:30 前仍保持 fresh")


def test_missing_signal_state():
    state = ts.missing_signal_state({"delivery": {"hour": 8, "minute": 30}})
    assert state["freshness"]["status"] == "missing"
    assert state["signals"] == []
    assert state["attention"] == []
    print("✓ 缺失今日判断缓存有显式状态")


def test_read_signal_cache_marks_non_dict_json_invalid():
    old_cache = ts.SIGNAL_CACHE
    with tempfile.TemporaryDirectory() as td:
        try:
            for name, raw in (
                ("array", "[1]"),
                ("string", '"not a signal cache"'),
                ("number", "42"),
            ):
                path = Path(td) / f"{name}.json"
                path.write_text(raw, encoding="utf-8")
                ts.SIGNAL_CACHE = path
                cache = ts.read_signal_cache()
                assert cache is not None
                assert cache["freshness"]["status"] == "invalid", cache
                assert cache["signals"] == []
                assert cache["attention"] == []
        finally:
            ts.SIGNAL_CACHE = old_cache
    print("✓ 非对象 JSON 今日判断缓存返回显式 invalid 状态")


def test_read_signal_cache_marks_malformed_object_fields_invalid():
    old_cache = ts.SIGNAL_CACHE
    payload = {
        "generated_at": "2026-07-07 08:31",
        "signals": 42,
        "attention": [],
    }
    with tempfile.TemporaryDirectory() as td:
        try:
            path = Path(td) / "malformed-object.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            ts.SIGNAL_CACHE = path
            cache = ts.read_signal_cache()
        finally:
            ts.SIGNAL_CACHE = old_cache

    assert cache is not None
    assert cache["freshness"]["status"] == "invalid", cache
    assert cache["signals"] == []
    assert cache["attention"] == []
    print("✓ 对象 JSON 今日判断缓存字段形状异常时返回显式 invalid 状态")


def test_read_signal_cache_marks_malformed_breaking_field_invalid():
    old_cache = ts.SIGNAL_CACHE
    payload = {
        "generated_at": "2026-07-07 08:31",
        "breaking": 42,
        "signals": [],
        "attention": [],
    }
    with tempfile.TemporaryDirectory() as td:
        try:
            path = Path(td) / "malformed-breaking.json"
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            ts.SIGNAL_CACHE = path
            cache = ts.read_signal_cache()
        finally:
            ts.SIGNAL_CACHE = old_cache

    assert cache is not None
    assert cache["freshness"]["status"] == "invalid", cache
    assert cache["breaking"] is None
    assert cache["signals"] == []
    assert cache["attention"] == []
    print("✓ breaking 字段形状异常时返回显式 invalid 状态")


if __name__ == "__main__":
    test_probe()
    test_suggest_video_selects_complement()
    test_suggest_video_rejects_weak_match()
    test_normalize_editor_pick_breaking_action()
    test_priority_model_research_detected_and_ranked()
    test_priority_model_research_overrides_generic_industry_trend()
    test_attention_candidate_surfaces_buzzy_unselected_item()
    test_promote_attention_item_adds_manual_signal_without_file_write()
    test_evidence_status_for_signal_shapes()
    test_promoted_attention_without_links_has_pending_evidence()
    test_behavior_summary_positive_events_only()
    test_suggestion_card_renders_explicit_confirmation_without_scores()
    test_cached_library_link_enriches_and_renders_quote()
    test_attention_card_renders_user_choice()
    test_breaking_card_renders_action()
    test_signal_freshness_daily_window()
    test_signal_freshness_stays_fresh_until_next_delivery_time()
    test_missing_signal_state()
    test_read_signal_cache_marks_non_dict_json_invalid()
    test_read_signal_cache_marks_malformed_object_fields_invalid()
    test_read_signal_cache_marks_malformed_breaking_field_invalid()
    print("\n全部通过 ✅")
