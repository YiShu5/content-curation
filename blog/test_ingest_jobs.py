"""Ingest job state tests.

Run: blog/.venv/bin/python blog/test_ingest_jobs.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import ingest_jobs as jobs


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


if __name__ == "__main__":
    test_content_key_youtube()
    test_job_lifecycle_without_launch()
    print("\n全部通过 ✅")
