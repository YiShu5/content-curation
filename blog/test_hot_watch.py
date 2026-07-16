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

from hot_watch import run_once, load_state

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


def test_first_run_seeds_silently():
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "state.json"
        send = Recorder()
        code = run_once(fetch=lambda h: [item("存量爆点", 95)], send=send, now=NOW, state_path=path)
        assert code == 0
        assert send.sent == []
        state = load_state(path)
        rows = list(state["items"].values())
        assert len(rows) == 1 and rows[0]["status"] == "seeded"


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


def test_multiple_items_merge_into_one_message():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        items = [item("甲", 90), item("乙", 95), item("丙", 92)]
        run_once(fetch=lambda h: items, send=send, now=NOW, state_path=path)
        assert len(send.sent) == 1
        text = send.sent[0]
        assert "（3 条）" in text and "1. 乙" in text and "2. 丙" in text and "3. 甲" in text


def test_overflow_items_folded_into_tail_and_all_marked():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        items = [item(f"新闻{i}", 88 + i) for i in range(7)]
        run_once(fetch=lambda h: items, send=send, now=NOW, state_path=path)
        text = send.sent[0]
        assert "另有 2 条超阈值" in text
        state = load_state(path)
        assert all(row["status"] == "notified" for row in state["items"].values())
        # 尾行提及的也算已通知，下一轮不再发
        send2 = Recorder()
        run_once(fetch=lambda h: items, send=send2, now=NOW, state_path=path)
        assert send2.sent == []


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


def test_dry_run_previews_without_marking_notified():
    with TemporaryDirectory() as tmp:
        path = seeded(tmp, [])
        send = Recorder()
        code = run_once(fetch=lambda h: [item("预览新闻", 92)], send=send, now=NOW,
                        state_path=path, dry_run=True)
        assert code == 0 and send.sent == []
        row = list(load_state(path)["items"].values())[0]
        assert row["status"] == "pending"


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    print(f"OK: {len(tests)} hot watch tests passed")
