"""Ingest job state tests.

Run: blog/.venv/bin/python blog/test_ingest_jobs.py
"""

import json
import sys
import tempfile
from types import SimpleNamespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import ingest_jobs as jobs
import ingest_worker


def test_content_key_youtube():
    assert jobs.content_key("https://www.youtube.com/watch?v=abcdefghijk") == "yt:abcdefghijk"
    assert jobs.content_key("https://youtu.be/abcdefghijk") == "yt:abcdefghijk"
    print("✓ youtube content key")


def test_job_lifecycle_without_launch():
    old_path = jobs.JOBS_PATH
    try:
        with tempfile.TemporaryDirectory() as td:
            jobs.JOBS_PATH = Path(td) / "jobs.json"
            job = jobs.start_job("https://www.youtube.com/watch?v=abcdefghijk", "视频", launch=False)
            assert job["status"] == "queued"
            assert job["job_id"] == "yt:abcdefghijk"
            running = jobs.update_job(job["job_id"], status="running", message="正在抓取和改写")
            assert running["status"] == "running"
            done = jobs.update_job(job["job_id"], status="done", message="已加入深度库", return_code=0)
            assert done["status"] == "done"
            assert jobs.get_job(job["job_id"])["message"] == "已加入深度库"
    finally:
        jobs.JOBS_PATH = old_path
    print("✓ job lifecycle")


def test_start_job_queues_when_matching_archive_is_incomplete():
    old_jobs_path = jobs.JOBS_PATH
    old_archive_root = jobs.ARCHIVE_ROOT
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs.JOBS_PATH = root / "jobs.json"
            jobs.ARCHIVE_ROOT = root / "archive"
            partial = jobs.ARCHIVE_ROOT / "partial"
            partial.mkdir(parents=True)
            (partial / "metadata.json").write_text(
                json.dumps(
                    {
                        "id": "abcdefghijk",
                        "url": "https://www.youtube.com/watch?v=abcdefghijk",
                        "rewrite_complete": False,
                    }
                ),
                encoding="utf-8",
            )

            job = jobs.start_job("https://www.youtube.com/watch?v=abcdefghijk", "视频", launch=False)

            assert job["status"] == "queued", job
            assert job["archive_dir"] == ""
    finally:
        jobs.ARCHIVE_ROOT = old_archive_root
        jobs.JOBS_PATH = old_jobs_path
    print("✓ start job ignores incomplete matching archive")


def test_worker_fails_when_fetch_succeeds_without_usable_archive():
    old_jobs_path = jobs.JOBS_PATH
    old_archive_root = jobs.ARCHIVE_ROOT
    old_run = ingest_worker._run
    commands = []
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs.JOBS_PATH = root / "jobs.json"
            jobs.ARCHIVE_ROOT = root / "empty-archive"
            jobs.ARCHIVE_ROOT.mkdir()
            job = jobs.start_job("https://www.youtube.com/watch?v=abcdefghijk", "视频", launch=False)

            def fake_run(cmd):
                commands.append(cmd)
                return SimpleNamespace(returncode=0, stdout="ok", stderr="")

            ingest_worker._run = fake_run
            ingest_worker.main(job["job_id"])

            stored = jobs.get_job(job["job_id"])
            assert stored["status"] == "failed", stored
            assert "未找到可用归档" in stored["message"]
            assert len(commands) == 1, commands
    finally:
        ingest_worker._run = old_run
        jobs.ARCHIVE_ROOT = old_archive_root
        jobs.JOBS_PATH = old_jobs_path
    print("✓ worker does not mark done when fetch creates no usable archive")


def test_worker_fails_when_fetch_leaves_matching_archive_incomplete():
    old_jobs_path = jobs.JOBS_PATH
    old_archive_root = jobs.ARCHIVE_ROOT
    old_run = ingest_worker._run
    commands = []
    try:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            jobs.JOBS_PATH = root / "jobs.json"
            jobs.ARCHIVE_ROOT = root / "archive"
            partial = jobs.ARCHIVE_ROOT / "partial"
            partial.mkdir(parents=True)
            (partial / "metadata.json").write_text(
                json.dumps(
                    {
                        "id": "abcdefghijk",
                        "url": "https://www.youtube.com/watch?v=abcdefghijk",
                        "rewrite_complete": False,
                    }
                ),
                encoding="utf-8",
            )
            job = jobs.update_job(
                "yt:abcdefghijk",
                url="https://www.youtube.com/watch?v=abcdefghijk",
                title="视频",
                status="queued",
                message="已提交",
                archive_dir="",
                return_code=None,
            )

            def fake_run(cmd):
                commands.append(cmd)
                return SimpleNamespace(returncode=0, stdout="ok", stderr="")

            ingest_worker._run = fake_run
            ingest_worker.main(job["job_id"])

            stored = jobs.get_job(job["job_id"])
            assert stored["status"] == "failed", stored
            assert "未找到可用归档" in stored["message"]
            assert stored["archive_dir"] == ""
            assert len(commands) == 1, commands
    finally:
        ingest_worker._run = old_run
        jobs.ARCHIVE_ROOT = old_archive_root
        jobs.JOBS_PATH = old_jobs_path
    print("✓ worker rejects incomplete matching archive")


if __name__ == "__main__":
    test_content_key_youtube()
    test_job_lifecycle_without_launch()
    test_start_job_queues_when_matching_archive_is_incomplete()
    test_worker_fails_when_fetch_succeeds_without_usable_archive()
    test_worker_fails_when_fetch_leaves_matching_archive_incomplete()
    print("\n全部通过 ✅")
