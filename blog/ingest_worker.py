"""Background ingest worker.

Run: blog/.venv/bin/python blog/ingest_worker.py yt:VIDEO_ID
"""

import subprocess
import sys
from pathlib import Path

import ingest_jobs as jobs


ROOT = Path(__file__).parent.parent


def _run(cmd):
    return subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=1800,
    )


def main(job_id):
    job = jobs.get_job(job_id)
    if not job:
        raise SystemExit(f"missing job: {job_id}")
    url = job.get("url") or ""
    jobs.update_job(job_id, status="running", message="正在抓取和改写")
    fetch_cmd = [str(ROOT / ".venv" / "bin" / "python"), str(ROOT / "scripts" / "fetch.py"), "--url", url]
    fetch = _run(fetch_cmd)
    if fetch.returncode != 0:
        detail = ((fetch.stderr or "") + "\n" + (fetch.stdout or "")).strip()[-500:]
        jobs.update_job(job_id, status="failed", message=f"入库失败：{detail}", return_code=fetch.returncode)
        return
    archive = jobs.find_existing_archive(url)
    if not archive:
        detail = ((fetch.stderr or "") + "\n" + (fetch.stdout or "")).strip()[-300:]
        message = "入库失败：抓取完成但未找到可用归档。"
        if detail:
            message = f"{message} {detail}"
        jobs.update_job(job_id, status="failed", message=message, archive_dir="", return_code=fetch.returncode)
        return
    refresh = _run(["bash", str(ROOT / "run.sh"), "refresh"])
    if refresh.returncode != 0:
        detail = ((refresh.stderr or "") + "\n" + (refresh.stdout or "")).strip()[-500:]
        jobs.update_job(job_id, status="failed", message=f"刷新失败：{detail}", return_code=refresh.returncode)
        return
    archive = jobs.find_existing_archive(url) or archive
    jobs.update_job(job_id, status="done", message="已加入深度库", archive_dir=archive, return_code=0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: ingest_worker.py <job_id>")
    main(sys.argv[1])
