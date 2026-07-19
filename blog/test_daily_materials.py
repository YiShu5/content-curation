"""每日素材盘的离线测试（不触发真实网络/飞书）。

运行：blog/.venv/bin/python blog/test_daily_materials.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import daily_materials as dm


def ai(title, score):
    return {"title": title, "score": score, "source": "机器之心", "url": f"https://n/{score}"}


def ag(term, heat, posts=3):
    return {"term_zh": term, "heat": heat, "post_ids": list(range(posts)), "id": term}


def test_collect_sorts_each_source_and_caps_top_n():
    aihot = [ai(f"新闻{i}", i) for i in range(15)]
    trends = [ag(f"趋势{i}", float(i)) for i in range(15)]
    rows_ai, rows_ag = dm.collect(aihot, trends, top_n=10)
    assert len(rows_ai) == 10 and len(rows_ag) == 10
    assert rows_ai[0]["score"] == 14 and rows_ai[-1]["score"] == 5   # 降序取前10
    assert rows_ag[0]["heat"] == 14.0


def test_cross_source_dup_marked_not_removed():
    aihot = [ai("Kimi K3 正式发布", 85), ai("别的新闻", 70)]
    trends = [ag("Kimi K3 正式发布并刷榜", 13.7), ag("另一个趋势", 5.0)]
    rows_ai, rows_ag = dm.collect(aihot, trends, top_n=10)
    # 都保留（看全），且相似的两条互标 dup
    assert len(rows_ai) == 2 and len(rows_ag) == 2
    assert rows_ai[0]["dup"] and rows_ag[0]["dup"]
    assert not rows_ai[1]["dup"] and not rows_ag[1]["dup"]


def test_featured_covers_both_sources():
    rows_ai, rows_ag = dm.collect([ai("A新闻", 90), ai("A2", 80)],
                                  [ag("G趋势", 12.0), ag("G2", 8.0)], top_n=10)
    picks = dm._featured(rows_ai, rows_ag)
    kinds = [k for k, _ in picks]
    assert len(picks) == 3
    assert "aihot" in kinds and "agihunt" in kinds   # 两源都露头


def test_build_card_structure_and_dup_marker():
    rows_ai, rows_ag = dm.collect([ai("Kimi K3 发布", 85)], [ag("Kimi K3 发布刷榜", 13.7)], top_n=10)
    card = dm.build_card(rows_ai, rows_ag, "07-18")
    assert card["header"]["title"]["content"].startswith("📋 今日讨论素材")
    blob = str(card["elements"])
    assert "查看原文" in blob and "↔" in blob        # 有原文按钮 + 去重标记
    assert "AI HOT" in blob and "AGI Hunt" in blob    # 两源分区都在


def test_send_falls_back_to_text_when_card_rejected():
    calls = []

    def post(url, payload):
        calls.append(payload.get("msg_type"))
        return {"code": 0} if payload.get("msg_type") == "text" else {"code": 9499, "msg": "bad card"}

    rc = dm.send({"header": {}}, "纯文本兜底", webhook="https://x", post=post)
    assert rc == 0
    assert calls == ["interactive", "text"]           # 卡片被拒 → 降级文本


def test_send_no_webhook_is_noop():
    assert dm.send({}, "t", webhook="", post=lambda u, p: {"code": 0}) == 0


def test_send_posters_uploads_and_posts_each_image():
    from pathlib import Path as P
    sent = []

    def render(items, tmp):
        out = []
        for i in range(len(items)):
            p = P(tmp) / f"hot-{i+1:02d}.png"
            p.write_bytes(b"PNG")
            out.append((p, True, ""))
        return out

    rc = dm.send_posters(
        [{"title": "a"}, {"title": "b"}],
        webhook="https://x",
        post=lambda url, payload: (sent.append(payload), {"code": 0})[1],
        token_fn=lambda: "tok",
        upload_fn=lambda token, png: (f"key-{png.name}", ""),
        render_fn=render,
    )
    assert rc == 0
    assert [p["msg_type"] for p in sent] == ["image", "image"]
    assert sent[0]["content"]["image_key"] == "key-hot-01.png"


def test_send_posters_upload_failure_skips_gracefully():
    def render(items, tmp):
        from pathlib import Path as P
        p = P(tmp) / "hot-01.png"
        p.write_bytes(b"PNG")
        return [(p, True, "")]

    rc = dm.send_posters([{"title": "a"}], webhook="https://x",
                         post=lambda u, p: {"code": 0}, token_fn=lambda: "tok",
                         upload_fn=lambda t, p: (None, "code=99991672 缺权限"),
                         render_fn=render)
    assert rc == 0  # 上传失败只跳过，绝不让素材盘整体失败


if __name__ == "__main__":
    tests = [v for n, v in sorted(globals().items()) if n.startswith("test_")]
    for t in tests:
        t()
    print(f"OK: {len(tests)} daily materials tests passed")
