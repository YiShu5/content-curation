"""Atomic local persistence for dated daily issues."""

import fcntl
import json
import os
import re
import secrets
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit


class DailyIssueError(RuntimeError):
    pass


class DailyIssueValidationError(DailyIssueError):
    pass


class DailyIssueConflict(DailyIssueError):
    pass


class DailyIssueCorrupt(DailyIssueError):
    pass


DAILY_TEXT_LIMITS = {
    "category_max": 20,
    "title_max": 60,
    "lead_title_warning": 34,
    "side_title_warning": 24,
    "what_happened_max": 160,
    "discussion_focus_max_items": 3,
    "discussion_focus_item_max": 32,
    "why_ranked_max": 120,
}


_STORE_LOCK = threading.RLock()

_TOPIC_FIELDS = (
    "topic_id",
    "rank",
    "category",
    "title",
    "what_happened",
    "discussion_focus",
    "why_ranked",
)
_SOURCE_FIELDS = (
    "source_id",
    "title",
    "url",
    "canonical_url",
    "publisher",
    "publisher_key",
    "published_at",
    "is_primary",
    "verification_status",
)
_ISSUE_FIELDS = (
    "schema_version",
    "issue_date",
    "issue_number",
    "status",
    "revision",
    "published_at",
    "revised_at",
    "timezone",
    "topics",
    "attention",
)


def _clean_limited_text(value, field_name, limit, *, required):
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise DailyIssueValidationError(f"{field_name} 必须为文本")
    cleaned = value.strip()
    if required and not cleaned:
        raise DailyIssueValidationError(f"{field_name} 不能为空")
    if len(cleaned) > limit:
        raise DailyIssueValidationError(f"{field_name} 超出长度限制")
    return cleaned


def validate_issue_date(value: str) -> str:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except (TypeError, ValueError) as exc:
        raise DailyIssueValidationError("日期必须为有效的 YYYY-MM-DD") from exc
    normalized = parsed.strftime("%Y-%m-%d")
    if value != normalized:
        raise DailyIssueValidationError("日期必须为有效的 YYYY-MM-DD")
    return normalized


def _atomic_write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.{secrets.token_hex(6)}.tmp")
    try:
        with temp.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()


def format_share_text(issue: dict, stable_url: str) -> str:
    issue_date = datetime.strptime(issue["issue_date"], "%Y-%m-%d")
    topics = issue.get("topics") or []
    lines = [f"降噪｜{issue_date.year} 年 {issue_date.month} 月 {issue_date.day} 日"]
    if len(topics) < 3:
        lines.append(f"本期仅有 {len(topics)} 个主题达到标准")
    else:
        lines.append("本期留下 3 个主题")
    for index, row in enumerate(topics):
        lines.append(f"{'①②③'[index]} {row['title']}")
        lines.append(str(row.get("why_ranked") or "").strip())
    lines.append(stable_url)
    return "\n\n".join(lines)


class DailyIssueStore:
    def __init__(self, root: Path, timezone_name: str):
        self.root = Path(root)
        self.timezone_name = timezone_name

    def _issue_path(self, issue_date):
        return self.root / f"{issue_date}.json"

    def _revision_path(self, issue_date, revision):
        return self.root / "revisions" / f"{issue_date}-r{revision:02d}.json"

    @contextmanager
    def _exclusive_write_lock(self):
        with _STORE_LOCK:
            self.root.mkdir(parents=True, exist_ok=True)
            lock_path = self.root / ".daily-issues.lock"
            with lock_path.open("a+", encoding="utf-8") as lock_handle:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
                try:
                    yield
                finally:
                    fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    def _validated_sources(self, sources):
        if not isinstance(sources, list):
            raise DailyIssueValidationError("信源必须为列表")
        result = []
        for source in sources:
            if not isinstance(source, dict):
                raise DailyIssueValidationError("信源必须为对象")
            clean = {}
            for field in _SOURCE_FIELDS:
                if field not in source:
                    continue
                value = source[field]
                if field == "is_primary":
                    if not isinstance(value, bool):
                        raise DailyIssueValidationError("信源主来源标记必须为布尔值")
                    clean[field] = value
                    continue
                if not isinstance(value, str):
                    raise DailyIssueValidationError(f"信源 {field} 必须为文本")
                clean[field] = value.strip()
            required_fields = (
                "source_id",
                "title",
                "url",
                "canonical_url",
                "publisher",
                "publisher_key",
                "verification_status",
            )
            if any(not clean.get(field) for field in required_fields):
                raise DailyIssueValidationError("信源核心字段不能为空")
            if clean["verification_status"] not in {
                "readable",
                "unchecked",
                "unavailable",
            }:
                raise DailyIssueValidationError("信源验证状态不受支持")
            for field in ("url", "canonical_url"):
                value = clean.get(field, "")
                parsed = urlsplit(value)
                if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                    raise DailyIssueValidationError("信源链接必须为 http(s) URL")
            result.append(clean)
        return result

    def _validated_topics(self, topics, *, is_attention=False):
        result = []
        for raw in topics:
            if not isinstance(raw, dict):
                raise DailyIssueValidationError("主题必须为对象")
            topic_id = str(raw.get("topic_id") or "").strip()
            if not topic_id:
                raise DailyIssueValidationError("主题标识不能为空")
            rank = raw.get("rank")
            if isinstance(rank, bool) or not isinstance(rank, int):
                raise DailyIssueValidationError("主题排名必须为整数")
            focus = raw.get("discussion_focus")
            if not isinstance(focus, list) or len(focus) > DAILY_TEXT_LIMITS[
                "discussion_focus_max_items"
            ]:
                raise DailyIssueValidationError("讨论焦点数量超出限制")
            clean_focus = [
                _clean_limited_text(
                    item,
                    "discussion_focus",
                    DAILY_TEXT_LIMITS["discussion_focus_item_max"],
                    required=True,
                )
                for item in focus
            ]
            clean = {
                "topic_id": topic_id,
                "rank": rank,
                "category": _clean_limited_text(
                    raw.get("category"),
                    "category",
                    DAILY_TEXT_LIMITS["category_max"],
                    required=False,
                ),
                "title": _clean_limited_text(
                    raw.get("title"),
                    "title",
                    DAILY_TEXT_LIMITS["title_max"],
                    required=True,
                ),
                "what_happened": _clean_limited_text(
                    raw.get("what_happened"),
                    "what_happened",
                    DAILY_TEXT_LIMITS["what_happened_max"],
                    required=True,
                ),
                "discussion_focus": clean_focus,
                "why_ranked": _clean_limited_text(
                    raw.get("why_ranked"),
                    "why_ranked",
                    DAILY_TEXT_LIMITS["why_ranked_max"],
                    required=True,
                ),
            }
            if is_attention:
                clean["attention_status"] = raw.get("attention_status")
            clean["sources"] = self._validated_sources(raw.get("sources", []))
            clean["independent_source_count"] = len({
                str(source.get("publisher_key") or "").strip()
                for source in clean["sources"]
                if str(source.get("publisher_key") or "").strip()
            })
            result.append(clean)
        return result

    def _validated_content(
        self,
        topics,
        attention,
        *,
        previous_topics=None,
        require_trusted_evidence=True,
    ):
        if not isinstance(topics, list) or not 1 <= len(topics) <= 3:
            raise DailyIssueValidationError("今日主题必须为 1 至 3 个")
        if not isinstance(attention, list) or len(attention) > 3:
            raise DailyIssueValidationError("关注中主题必须为 0 至 3 个")

        validated_topics = self._validated_topics(topics)
        validated_attention = self._validated_topics(attention, is_attention=True)
        if any(
            row.get("attention_status") not in {"rising", "watch", "stable"}
            for row in validated_attention
        ):
            raise DailyIssueValidationError("关注状态不受支持")
        topic_ids = [
            row["topic_id"] for row in [*validated_topics, *validated_attention]
        ]
        if len(topic_ids) != len(set(topic_ids)):
            raise DailyIssueValidationError("主题标识不能为空或重复")
        if [row["rank"] for row in validated_topics] != list(
            range(1, len(validated_topics) + 1)
        ):
            raise DailyIssueValidationError("今日主题排名必须从 1 连续递增")

        if require_trusted_evidence:
            previous_by_id = {
                row.get("topic_id"): row
                for row in (previous_topics or [])
                if isinstance(row, dict)
            }

            def has_trusted_evidence(row):
                sources = row["sources"]
                if any(
                    source.get("verification_status") == "readable"
                    for source in sources
                ):
                    return True
                previous = previous_by_id.get(row["topic_id"])
                if previous is None:
                    return False
                prior_trusted_ids = {
                    source.get("source_id")
                    for source in previous.get("sources", [])
                    if isinstance(source, dict)
                    and source.get("source_id")
                    and source.get("verification_status")
                    in {"readable", "unavailable"}
                }
                return any(
                    source.get("source_id") in prior_trusted_ids
                    and source.get("verification_status") == "unavailable"
                    for source in sources
                )

            if any(not has_trusted_evidence(row) for row in validated_topics):
                raise DailyIssueValidationError("每个今日主题至少需要一条可读信源")
        return validated_topics, validated_attention

    def _payload(
        self,
        issue_date,
        topics,
        attention,
        *,
        issue_number,
        revision,
        published_at,
        revised_at,
        previous_topics=None,
        status="published",
    ):
        validated_topics, validated_attention = self._validated_content(
            topics,
            attention,
            previous_topics=previous_topics,
        )
        return {
            "schema_version": 1,
            "issue_date": issue_date,
            "issue_number": issue_number,
            "status": status,
            "revision": revision,
            "published_at": published_at,
            "revised_at": revised_at,
            "timezone": self.timezone_name,
            "topics": validated_topics,
            "attention": validated_attention,
        }

    def _validate_snapshot(
        self,
        payload,
        *,
        expected_date=None,
        expected_revision=None,
    ):
        if not isinstance(payload, dict) or set(payload) != set(_ISSUE_FIELDS):
            raise DailyIssueValidationError("期刊快照结构无效")
        if payload["schema_version"] != 1 or payload["status"] != "published":
            raise DailyIssueValidationError("期刊快照版本或状态无效")
        issue_date = validate_issue_date(payload["issue_date"])
        if expected_date is not None and issue_date != expected_date:
            raise DailyIssueValidationError("期刊日期与文件名不一致")
        for field in ("issue_number", "revision"):
            value = payload[field]
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                raise DailyIssueValidationError("期刊编号或修订号无效")
        if (
            expected_revision is not None
            and payload["revision"] != expected_revision
        ):
            raise DailyIssueValidationError("期刊修订号与文件名不一致")
        for field in ("published_at", "revised_at"):
            value = payload[field]
            if not isinstance(value, str):
                raise DailyIssueValidationError("期刊时间无效")
            datetime.fromisoformat(value)
        if not isinstance(payload["timezone"], str) or not payload["timezone"].strip():
            raise DailyIssueValidationError("期刊时区无效")
        topics, attention = self._validated_content(
            payload["topics"],
            payload["attention"],
            require_trusted_evidence=False,
        )
        if topics != payload["topics"] or attention != payload["attention"]:
            raise DailyIssueValidationError("期刊内容结构无效")
        return payload

    def _read_snapshot(self, path, *, expected_date=None, expected_revision=None):
        try:
            with path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
            return self._validate_snapshot(
                payload,
                expected_date=expected_date,
                expected_revision=expected_revision,
            )
        except (OSError, ValueError, TypeError, KeyError, DailyIssueValidationError) as exc:
            raise DailyIssueCorrupt("期刊数据损坏，请先恢复后再试") from exc

    def _valid_archived_revisions(self, issue_date):
        revisions = []
        pattern = re.compile(rf"^{re.escape(issue_date)}-r(\d{{2,}})\.json$")
        for path in (self.root / "revisions").glob(f"{issue_date}-r*.json"):
            match = pattern.fullmatch(path.name)
            if match is None:
                continue
            revision = int(match.group(1))
            try:
                payload = self._read_snapshot(
                    path,
                    expected_date=issue_date,
                    expected_revision=revision,
                )
            except DailyIssueCorrupt:
                continue
            revisions.append(payload)
        return sorted(revisions, key=lambda payload: payload["revision"], reverse=True)

    def _current_issue_dates(self):
        issue_dates = set()
        for path in self.root.glob("????-??-??.json"):
            try:
                issue_dates.add(validate_issue_date(path.stem))
            except DailyIssueValidationError:
                continue
        return issue_dates

    def unrecoverable_dates(self):
        with _STORE_LOCK:
            result = []
            for issue_date in self._current_issue_dates():
                try:
                    self._read_snapshot(
                        self._issue_path(issue_date),
                        expected_date=issue_date,
                    )
                except DailyIssueCorrupt:
                    if not self._valid_archived_revisions(issue_date):
                        result.append(issue_date)
            return sorted(result)

    def _assert_integrity(self):
        if self.unrecoverable_dates():
            raise DailyIssueCorrupt("存在无法恢复的期刊，请先恢复后再继续")

    def get(self, issue_date: str, *, fallback_revision: bool = True):
        issue_date = validate_issue_date(issue_date)
        with _STORE_LOCK:
            path = self._issue_path(issue_date)
            if not path.exists():
                if fallback_revision:
                    archived = self._valid_archived_revisions(issue_date)
                    if archived:
                        return archived[0]
                return None
            try:
                return self._read_snapshot(path, expected_date=issue_date)
            except DailyIssueCorrupt:
                if fallback_revision:
                    archived = self._valid_archived_revisions(issue_date)
                    if archived:
                        return archived[0]
                raise

    def assert_revisable(self, issue_date: str):
        issue_date = validate_issue_date(issue_date)
        with _STORE_LOCK:
            current = self.get(issue_date, fallback_revision=False)
            if current is None:
                raise DailyIssueConflict("该日期尚未发布")
            return current

    def list_issues(self):
        with _STORE_LOCK:
            issues = []
            issue_dates = self._current_issue_dates()
            revision_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})-r\d{2,}\.json$")
            for path in (self.root / "revisions").glob("*.json"):
                match = revision_pattern.fullmatch(path.name)
                if match is None:
                    continue
                try:
                    issue_dates.add(validate_issue_date(match.group(1)))
                except DailyIssueValidationError:
                    continue
            for issue_date in issue_dates:
                try:
                    issue = self.get(issue_date, fallback_revision=True)
                except DailyIssueCorrupt:
                    continue
                if issue is not None:
                    issues.append(issue)
            return sorted(issues, key=lambda issue: issue["issue_date"], reverse=True)

    def latest(self):
        issues = self.list_issues()
        return issues[0] if issues else None

    def next_issue_number(self):
        with _STORE_LOCK:
            self._assert_integrity()
            issues = self.list_issues()
            return max((issue["issue_number"] for issue in issues), default=0) + 1

    def preview(self, issue_date, topics, attention, *, now):
        issue_date = validate_issue_date(issue_date)
        with _STORE_LOCK:
            self._assert_integrity()
            stamp = now.isoformat()
            if self.get(issue_date, fallback_revision=True) is not None:
                current = self.assert_revisable(issue_date)
                issue_number = current["issue_number"]
                revision = current["revision"] + 1
                published_at = current["published_at"]
                previous_topics = current["topics"]
            else:
                issue_number = self.next_issue_number()
                revision = 1
                published_at = stamp
                previous_topics = None
            return self._payload(
                issue_date,
                topics,
                attention,
                issue_number=issue_number,
                revision=revision,
                published_at=published_at,
                revised_at=stamp,
                previous_topics=previous_topics,
                status="preview",
            )

    def publish(self, issue_date, topics, attention, *, now):
        issue_date = validate_issue_date(issue_date)
        with self._exclusive_write_lock():
            self._assert_integrity()
            if self.get(issue_date, fallback_revision=True) is not None:
                raise DailyIssueConflict("该日期已发布")
            stamp = now.isoformat()
            issue = self._payload(
                issue_date,
                topics,
                attention,
                issue_number=self.next_issue_number(),
                revision=1,
                published_at=stamp,
                revised_at=stamp,
            )
            _atomic_write_json(self._issue_path(issue_date), issue)
            return issue

    def revise(
        self,
        issue_date,
        topics,
        attention,
        *,
        expected_revision,
        now,
    ):
        issue_date = validate_issue_date(issue_date)
        with self._exclusive_write_lock():
            self._assert_integrity()
            current = self.assert_revisable(issue_date)
            if current["revision"] != expected_revision:
                raise DailyIssueConflict("期刊已被其他编辑修订")
            revised = self._payload(
                issue_date,
                topics,
                attention,
                issue_number=current["issue_number"],
                revision=current["revision"] + 1,
                published_at=current["published_at"],
                revised_at=now.isoformat(),
                previous_topics=current["topics"],
            )
            _atomic_write_json(
                self._revision_path(issue_date, current["revision"]),
                current,
            )
            _atomic_write_json(self._issue_path(issue_date), revised)
            return revised
