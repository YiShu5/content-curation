import os
from pathlib import Path

ROOT = Path(__file__).parent.parent

class Config:
    # 飞书应用配置
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")

    # 多维表格配置
    BASE_ID = os.getenv("FEISHU_APP_TOKEN", "")
    TABLE_ID = os.getenv("FEISHU_TABLE_ID", "")

    # 缓存时间（秒）
    CACHE_TTL = 300

    # 语义搜索 / Embedding（智谱 embedding-3）
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
    EMBED_MODEL = os.getenv("EMBED_MODEL", "embedding-3")
    EMBED_DIM = int(os.getenv("EMBED_DIM", "1024"))

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "content-curation-blog-2026")
    BLOG_ADMIN_PASSWORD = os.getenv("BLOG_ADMIN_PASSWORD", "")
    BLOG_TIMEZONE = os.getenv("BLOG_TIMEZONE", "America/Los_Angeles")
    PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")
    DAILY_ISSUES_DIR = os.getenv("DAILY_ISSUES_DIR", str(ROOT / "blog" / "data" / "daily_issues"))
    DAILY_EDITOR_LOG = os.getenv("DAILY_EDITOR_LOG", str(ROOT / "blog" / "data" / "daily_editor_events.jsonl"))
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "").lower() == "true"
