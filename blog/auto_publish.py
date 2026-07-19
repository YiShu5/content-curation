"""带闸门的每日简报自动发布（配合 cron 使用）。

用法：blog/.venv/bin/python blog/auto_publish.py
闸门与手动发布完全一致：走 daily_editor.trusted_draft / apply_selection /
DailyIssueStore.publish 的全套校验（当日新鲜度、每主题 ≥1 已核验信源、
最多 3 条），任何一道不过就不发——宁缺毋滥由机器执行。

退出码：0 = 已发布，或按设计跳过（当日已发布 / 无达标主题）；
        1 = 异常（草稿缺失/过期、闸门拦截、存储损坏），值得告警。
"""
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

# 经 app 导入以复用 config/.env 加载与 _selected_attention，
# 保证自动发布与手动发布走同一条代码路径
from app import app, _selected_attention  # noqa: E402
import daily_editor  # noqa: E402
import today_signal  # noqa: E402
from daily_issues import (  # noqa: E402
    DailyIssueConflict,
    DailyIssueCorrupt,
    DailyIssueStore,
    DailyIssueValidationError,
)


def auto_publish(*, cache, store, editor_log, now):
    """核心流程，可注入依赖以便测试。返回 (exit_code, message)。"""
    today = now.date().isoformat()
    if store.get(today) is not None:
        return 0, f"{today} 已发布，跳过（幂等）"
    try:
        draft = daily_editor.trusted_draft(cache or {}, expected_date=today)
    except ValueError as exc:
        return 1, f"今日草稿不可用，不发布：{exc}"
    topics = draft.get("topics") or []
    if not topics:
        return 0, f"{today} 无达标主题，宁缺毋滥，不发布"
    rows = [{"topic_id": row["topic_id"]} for row in topics[:3]]
    selected = daily_editor.apply_selection(draft, rows)
    attention = _selected_attention(draft, selected)
    main_line = str(draft.get("main_line") or "").strip()
    issue = store.publish(today, selected, attention, main_line=main_line, now=now)
    audit = "ok"
    try:
        daily_editor.append_editor_event(editor_log, {
            "kind": "auto_publish",
            "issue_date": today,
            "revision": issue["revision"],
            "published_topic_ids": [row["topic_id"] for row in selected],
        }, now=now)
    except Exception:
        audit = "failed"  # 与手动发布一致：发布已成立，审计失败只标记不回滚
    # 主线拼进单行消息（run.sh 按行 grep [auto-publish]，不能换行）
    line_note = f"｜主线：{issue['main_line']}" if issue.get("main_line") else ""
    return 0, (
        f"已发布 {today} · 第 {issue['issue_number']:03d} 期 · "
        f"{len(selected)} 条主题（审计:{audit}）{line_note}"
    )


def main():
    now = datetime.now(ZoneInfo(app.config["BLOG_TIMEZONE"]))
    store = DailyIssueStore(
        Path(app.config["DAILY_ISSUES_DIR"]), app.config["BLOG_TIMEZONE"]
    )
    cache = today_signal.read_signal_cache() or {}
    try:
        code, message = auto_publish(
            cache=cache,
            store=store,
            editor_log=Path(app.config["DAILY_EDITOR_LOG"]),
            now=now,
        )
    except (DailyIssueValidationError, DailyIssueConflict, DailyIssueCorrupt) as exc:
        code, message = 1, f"发布被闸门拦下：{exc}"
    print(f"[auto-publish] {message}")
    return code


if __name__ == "__main__":
    sys.exit(main())
