"""Local ingest job state for adding YouTube videos to the deep library."""

import json
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).parent.parent
DATA_DIR = Path(__file__).parent / "data"
JOBS_PATH = DATA_DIR / "ingest_jobs.json"
ARCHIVE_ROOT = ROOT / "archive"
YOUTUBE_RE = re.compile(r'^https://(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([A-Za-z0-9_-]{11})')
VALID_STATUSES = {"queued", "running", "done", "exists", "failed"}


def now_str():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def content_key(url):
    match = re.search(r'(?:youtu\.be/|[?&]v=)([A-Za-z0-9_-]{11})', str(url or ""))
    return "yt:" + match.group(1) if match else ""


def video_id_from_key(job_id):
    return job_id[3:] if str(job_id or "").startswith("yt:") else ""


def load_jobs():
    if not JOBS_PATH.exists():
        return {}
    try:
        return json.loads(JOBS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_jobs(jobs):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    JOBS_PATH.write_text(json.dumps(jobs, ensure_ascii=False, indent=2), encoding="utf-8")


def get_job(job_id):
    return load_jobs().get(str(job_id or ""))


def update_job(job_id, **patch):
    jobs = load_jobs()
    job = dict(jobs.get(job_id) or {"job_id": job_id, "created_at": now_str()})
    job.update(patch)
    job["updated_at"] = now_str()
    jobs[job_id] = job
    save_jobs(jobs)
    return job


def archive_record_id(archive_dir):
    """从归档目录的 metadata.json 读记录 id（/article/<id> 的主键）。
    metadata 缺失/损坏时返回空串，由调用方决定兜底。"""
    try:
        meta = json.loads((Path(archive_dir) / "metadata.json").read_text(encoding="utf-8"))
        return str(meta.get("id") or "")
    except Exception:
        return ""


def find_existing_archive(url):
    key = content_key(url)
    if not key or not ARCHIVE_ROOT.exists():
        return ""
    video_id = video_id_from_key(key)
    for mp in ARCHIVE_ROOT.glob("*/metadata.json"):
        try:
            meta = json.loads(mp.read_text(encoding="utf-8"))
        except Exception:
            continue
        matches_archive = meta.get("id") == video_id or content_key(meta.get("url") or "") == key
        if matches_archive and meta.get("rewrite_complete") is True:
            return str(mp.parent)
    return ""


def launch_worker(job_id):
    subprocess.Popen(
        [str(Path(__file__).parent / ".venv" / "bin" / "python"), str(Path(__file__).parent / "ingest_worker.py"), job_id],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def start_job(url, title="", launch=True):
    if not YOUTUBE_RE.match(str(url or "")):
        return {"status": "bad_url", "message": "只支持 YouTube 视频链接"}
    job_id = content_key(url)
    existing_archive = find_existing_archive(url)
    if existing_archive:
        return update_job(
            job_id,
            url=url,
            title=title,
            status="exists",
            message="已在深度库",
            archive_dir=existing_archive,
            record_id=archive_record_id(existing_archive) or video_id_from_key(job_id),
            return_code=0,
        )
    current = get_job(job_id)
    if current and current.get("status") in {"queued", "running"}:
        return current
    job = update_job(
        job_id,
        url=url,
        title=title,
        status="queued",
        message="已提交",
        archive_dir="",
        return_code=None,
    )
    if launch:
        launch_worker(job_id)
    return job
