"""盘中巨热点监控的离线测试。

运行：blog/.venv/bin/python blog/test_hot_watch.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

from hot_watch import format_message, load_state, run_once

TZ = ZoneInfo("Asia/Shanghai")
NOW = datetime(2026, 7, 16, 14, 37, tzinfo=TZ)


def item(title, score, *, url=None, source="机器之心", summary="一句话摘要。"):
    return {
        "title": title,
        "score": score,
        "url": url or f"https://news.example/{abs(hash(title))}",
        "source": source,
        "summary": summary,
    }


class Recorder:
    def __init__(self, ok=True):
        self.ok = ok
        self.sent = []

    def __call__(self, text):
        self.sent.append(text)
        return self.ok


def seeded(tmp, items, now=NOW):
    """先跑一轮完成播种，返回状态文件路径。"""
    path = Path(tmp) / "state.json"
    code = run_once(fetch=lambda h: items, send=Recorder(), now=now, state_path=path)
    assert code == 0
    return path


def test_first_run_seeds_silently_and_sets_champion():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "state.json"
        send = Recorder()
        code = run_once(fetch=lambda h: [item("存量爆点", 95)], send=send, now=NOW, state_path=path)
        assert code == 0
        assert send.sent == []
        state = load_state(path)
        rows = list(state["items"].values())
        assert len(rows) == 1 and rows[0]["status"] == "seeded"
        assert state["champion"] == {"date": "2026-07-16", "score": 95}


def test_new_high_score_item_notifies_once():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        code = run_once(fetch=lambda h: [item("Kimi K3 正式发布", 93)], send=send, now=NOW, state_path=path)
        assert code == 0
        assert len(send.sent) == 1
        assert "Kimi K3 正式发布" in send.sent[0]
        assert "热度 93" in send.sent[0]
        assert "https://" in send.sent[0]
        # 同 key 分数更高也不重发
        send2 = Recorder()
        run_once(fetch=lambda h: [item("Kimi K3 正式发布", 97)], send=send2, now=NOW, state_path=path)
        assert send2.sent == []


def test_below_threshold_then_crossing_triggers():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        low = item("低开高走", 70, url="https://news.example/rise")
        send = Recorder()
        run_once(fetch=lambda h: [low], send=send, now=NOW, state_path=path)
        assert send.sent == []  # 70 分不入库不通知
        high = dict(low, score=89)
        run_once(fetch=lambda h: [high], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1 and "低开高走" in send.sent[0]


def test_same_round_only_champion_pushes():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        items = [item("甲", 90), item("乙", 95), item("丙", 92)]
        run_once(fetch=lambda h: items, send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1
        text = send.sent[0]
        assert "乙" in text and "甲" not in text and "丙" not in text
        # 次轮同批：甲/丙未超冠军 95，依旧不推
        send2 = Recorder()
        run_once(fetch=lambda h: items, send=send2, now=NOW, state_path=path)
        assert send2.sent == []


def test_quiet_hours_accumulate_escalating_champions_then_merge():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        t2 = datetime(2026, 7, 16, 2, 0, tzinfo=TZ)
        t4 = datetime(2026, 7, 16, 4, 0, tzinfo=TZ)
        run_once(fetch=lambda h: [item("夜半新高", 80)], send=send, now=t2,
                 state_path=path, quiet_spec="23-8")
        run_once(fetch=lambda h: [item("凌晨反超", 85)], send=send, now=t4,
                 state_path=path, quiet_spec="23-8")
        assert send.sent == []
        morning = datetime(2026, 7, 16, 8, 7, tzinfo=TZ)
        run_once(fetch=lambda h: [], send=send, now=morning,
                 state_path=path, quiet_spec="23-8")
        assert len(send.sent) == 1
        text = send.sent[0]
        assert "（2 条）" in text and "1. 凌晨反超" in text and "2. 夜半新高" in text


def test_format_message_folds_overflow_into_tail():
    rows = [
        {"title": f"新闻{i}", "score": 88 + i, "source": "源", "summary": "", "url": f"https://e/{i}",
         "first_over_at": NOW.isoformat(timespec="seconds")}
        for i in range(7)
    ]
    rows.sort(key=lambda r: -r["score"])
    text = format_message(rows, NOW, max_items=5)
    assert "（7 条）" in text and "另有 2 条超阈值" in text


def test_quiet_hours_hold_then_morning_catchup_with_detected_note():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        night = datetime(2026, 7, 16, 2, 0, tzinfo=TZ)
        send = Recorder()
        code = run_once(fetch=lambda h: [item("深夜爆点", 94)], send=send, now=night,
                        state_path=path, quiet_spec="23-8")
        assert code == 0 and send.sent == []
        state = load_state(path)
        assert list(state["items"].values())[0]["status"] == "pending"
        morning = datetime(2026, 7, 16, 8, 7, tzinfo=TZ)
        code = run_once(fetch=lambda h: [], send=send, now=morning,
                        state_path=path, quiet_spec="23-8")
        assert code == 0 and len(send.sent) == 1
        assert "02:00 检测" in send.sent[0]


def test_send_failure_retries_then_gives_up():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        bad = Recorder(ok=False)
        hot = [item("发不出去", 91)]
        for round_no in (1, 2, 3):
            code = run_once(fetch=lambda h: hot, send=bad, now=NOW, state_path=path)
            assert code == 1
            row = list(load_state(path)["items"].values())[0]
            assert row["attempts"] == round_no
        assert row["status"] == "gave_up"
        # 第 4 轮不再尝试
        before = len(bad.sent)
        code = run_once(fetch=lambda h: hot, send=bad, now=NOW, state_path=path)
        assert code == 0 and len(bad.sent) == before


def test_pending_survives_leaving_fetch_window():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        bad = Recorder(ok=False)
        run_once(fetch=lambda h: [item("滑窗新闻", 92)], send=bad, now=NOW, state_path=path)
        good = Recorder()
        code = run_once(fetch=lambda h: [], send=good, now=NOW, state_path=path)  # 上游已不返回
        assert code == 0 and len(good.sent) == 1 and "滑窗新闻" in good.sent[0]


def test_fetch_failure_leaves_state_untouched():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [item("已播种", 90)])
        before = path.read_bytes()

        def boom(hours):
            raise RuntimeError("上游 403")

        code = run_once(fetch=boom, send=Recorder(), now=NOW, state_path=path)
        assert code == 2
        assert path.read_bytes() == before


def test_old_entries_pruned_by_ttl():
    with TemporaryDirectory() as tmp:
        old_time = datetime(2026, 7, 13, 10, 0, tzinfo=TZ)  # 75h 前
        path = seeded(tmp, [item("旧闻", 90)], now=old_time)
        run_once(fetch=lambda h: [], send=Recorder(), now=NOW, state_path=path)
        assert load_state(path)["items"] == {}


def test_threshold_override():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        run_once(fetch=lambda h: [item("89分新闻", 89)], send=send, now=NOW,
                 state_path=path, threshold=90)
        assert send.sent == []


def test_lower_item_after_champion_not_pushed():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        run_once(fetch=lambda h: [item("今日冠军", 85)], send=send, now=NOW, state_path=path)
        run_once(fetch=lambda h: [item("次高新闻", 82)], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1 and "次高新闻" not in send.sent[0]


def test_escalating_champions_push_in_sequence():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        run_once(fetch=lambda h: [item("上午头条", 85)], send=send, now=NOW, state_path=path)
        run_once(fetch=lambda h: [item("下午反超", 91)], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 2 and "下午反超" in send.sent[1]


def test_midnight_resets_champion():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        day1 = datetime(2026, 7, 16, 20, 0, tzinfo=TZ)
        run_once(fetch=lambda h: [item("昨日冠军", 85)], send=send, now=day1, state_path=path)
        day2 = datetime(2026, 7, 17, 9, 0, tzinfo=TZ)
        run_once(fetch=lambda h: [item("次日平开", 79)], send=send, now=day2, state_path=path)
        assert len(send.sent) == 2 and "次日平开" in send.sent[1]


def test_risen_score_of_known_item_raises_bar_silently():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        first = item("持续发酵", 85, url="https://news.example/rise-again")
        run_once(fetch=lambda h: [first], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1
        # 同一条新闻分数涨到 93：不重推，但冠军线被抬高
        risen = dict(first, score=93)
        run_once(fetch=lambda h: [risen], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1
        # 随后 89 分的新条目低于被抬高的冠军线，不得冒充新高
        run_once(fetch=lambda h: [risen, item("次高冒充者", 89)], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1


def test_dry_run_previews_without_marking_notified():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        code = run_once(fetch=lambda h: [item("预览新闻", 92)], send=send, now=NOW,
                        state_path=path, dry_run=True)
        assert code == 0 and send.sent == []
        row = list(load_state(path)["items"].values())[0]
        assert row["status"] == "pending"


def trend(term, heat, *, tid=None, blurb="趋势一句话。"):
    return {
        "id": tid or f"trend-{abs(hash(term))}",
        "term_zh": term,
        "term_en": term,
        "blurb": blurb,
        "heat": heat,
        "rank": 1,
        "is_new": True,
        "prev_rank": None,
    }


def test_agihunt_champion_triggers_with_native_metric():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        code = run_once(fetch=lambda h: [], fetch_agihunt=lambda: [trend("Kimi K3 正式发布并刷榜", 12.0)],
                        send=send, now=NOW, state_path=path)
        assert code == 0 and len(send.sent) == 1
        assert "heat 12.0" in send.sent[0]
        assert "AGI HUNT · agihunt.info" in send.sent[0]


def test_agihunt_below_floor_not_stored():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        run_once(fetch=lambda h: [], fetch_agihunt=lambda: [trend("小热点", 6.0)],
                 send=send, now=NOW, state_path=path)
        assert send.sent == []
        assert load_state(path)["items"] == {}


def test_agihunt_same_id_no_repush_and_risen_heat_raises_bar():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        first = trend("大新闻", 12.0, tid="t-1")
        run_once(fetch=lambda h: [], fetch_agihunt=lambda: [first], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1
        risen = dict(first, heat=13.5)
        run_once(fetch=lambda h: [], fetch_agihunt=lambda: [risen], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1  # 同 id 不重推
        # 冠军线已被抬到 13.5，后续 12.8 的新趋势不冒充新高
        run_once(fetch=lambda h: [], fetch_agihunt=lambda: [risen, trend("次高", 12.8, tid="t-2")],
                 send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1


def test_dual_tracks_merge_into_single_message():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        run_once(fetch=lambda h: [item("AI HOT 头条", 85)],
                 fetch_agihunt=lambda: [trend("AGI Hunt 头条", 12.0)],
                 send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1
        text = send.sent[0]
        assert "AI HOT 头条" in text and "AGI Hunt 头条" in text
        assert "热度 85" in text and "heat 12.0" in text


def test_cross_source_duplicate_suppressed():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        run_once(fetch=lambda h: [item("Kimi K3 正式发布", 85)], send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1
        run_once(fetch=lambda h: [], fetch_agihunt=lambda: [trend("Kimi K3 正式发布并刷榜", 13.7)],
                 send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1  # 同事件被相似度抑制
        rows = load_state(path)["items"]
        assert any(row.get("status") == "dup_suppressed" for row in rows.values())


def test_agihunt_failure_does_not_hurt_aihot_track():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()

        def boom():
            raise RuntimeError("agihunt 挂了")

        code = run_once(fetch=lambda h: [item("主轨新闻", 85)], fetch_agihunt=boom,
                        send=send, now=NOW, state_path=path)
        assert code == 0 and len(send.sent) == 1 and "主轨新闻" in send.sent[0]


def test_both_sources_failing_returns_2_untouched():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [item("已播种", 90)])
        before = path.read_bytes()

        def boom_fetch(hours):
            raise RuntimeError("aihot 403")

        def boom_agihunt():
            raise RuntimeError("agihunt 403")

        code = run_once(fetch=boom_fetch, fetch_agihunt=boom_agihunt,
                        send=Recorder(), now=NOW, state_path=path)
        assert code == 2
        assert path.read_bytes() == before


def test_seeding_initializes_agihunt_champion():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "state.json"
        send = Recorder()
        code = run_once(fetch=lambda h: [], fetch_agihunt=lambda: [trend("存量趋势", 13.7)],
                        send=send, now=NOW, state_path=path)
        assert code == 0 and send.sent == []
        state = load_state(path)
        assert state["champion_agihunt"] == {"date": "2026-07-16", "heat": 13.7}
        assert all(row["status"] == "seeded" for row in state["items"].values())


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"OK: {len(tests)} hot watch tests passed")
