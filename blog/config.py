import os

class Config:
    # 飞书应用配置
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")

    # 多维表格配置
    BASE_ID = os.getenv("FEISHU_APP_TOKEN", "")
    TABLE_ID = os.getenv("FEISHU_TABLE_ID", "")

    # 缓存时间（秒）
    CACHE_TTL = 300

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "content-curation-blog-2026")
