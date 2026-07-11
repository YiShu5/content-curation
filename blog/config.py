import os

class Config:
    # 语义搜索 / Embedding（智谱 embedding-3）
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
    EMBED_MODEL = os.getenv("EMBED_MODEL", "embedding-3")
    EMBED_DIM = int(os.getenv("EMBED_DIM", "1024"))

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "content-curation-blog-2026")
