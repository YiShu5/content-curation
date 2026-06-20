# CLAUDE.md — content-curation（NoiseFilter / 降噪）

内容策展工具：抓取音视频长内容 → AI 转录/改写/打分 → 归档 + 飞书 + 博客。总览见 README.md。
本文件只记**易踩坑的项目约定**（与全局 ~/.claude/CLAUDE.md 合并生效）。

## 运行
- 博客用 `blog/.venv` 跑，端口 **5055**（5000 会撞 macOS AirPlay Receiver）。
- 两个 Python 环境：根 `.venv`（fetch.py，含 yt-dlp）+ `blog/.venv`（flask/numpy/markdown/dotenv）。
- 统一入口 `run.sh <cmd>`：auto / url / batch / sync / sync-doc / embed / enrich-guests / select-quotes / rescore。

## 密钥与产物（勿提交）
- `config/.env` 存所有密钥（飞书/DeepSeek/智谱/BibiGPT），已 gitignore，**绝不入库**。
- `archive/`、`blog/data/`、`.venv/`、`blog/.venv/`、`.claude/` 均已忽略（生成物/本地）。

## 数据流与匹配
- 博客以**飞书多维表格为真相源**（`fetch_records`）；本地 `archive/` 只做增强。
- enrich 先按 `feishu_record_id` 匹配，再按视频 id（`_content_key`，blog/app.py）兜底——所以重跑生成、未回填 record_id 的归档也能对上，同一视频的重复飞书记录共享一份归档。

## 评分体系（2026-06 已重构）
- 现行三维：**洞察原创 0-50 + 信源质量 0-25 + 故事可读 0-25**（旧 ai_relevance/storytelling/bonus 已废弃，旧分备份在 metadata 的 `scores_v1`）。
- ⚠️ **已知遗留**：`scripts/sync-feishu.js` 和飞书表的评分列仍是旧维度。重新同步飞书前必须先改 sync-feishu.js 的评分字段，否则会写错/写空。
- 重打分用 `scripts/rescore.py`（从已有摘要重算，不重跑整条流水线）。

## 转录
- BibiGPT 为主（按**时长**计费，注意余额），baoyu 免费降级**仅支持 YouTube**。
- 小红书/online-media 的字幕在 `detail.subtitlesArray`（fetch.py 已处理）。
