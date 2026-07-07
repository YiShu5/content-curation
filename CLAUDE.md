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

## 数据流（2026-06 已改为「本地 archive 为真相源」）
- 博客直接读 `archive/*/metadata.json`（`load_archive_records`，blog/app.py），**不再依赖飞书**。新抓内容刷新即见。
- 记录 `id` = metadata 的 `id`（视频 id / audio-xxx）；详情页 `/article/<id>`、向量索引、今日信号都按这个 id 对齐。
- 封面走本地：`/cover-local/<archive_dir>` 直接发 archive 里的 cover.*。
- ⚠️ 改完 fetch 新内容后，**首页/详情立刻可见(实时读 archive)，但语义搜索/相关推荐/今日信号要 `run.sh embed` 重建索引才会纳入**。
- 旧的飞书读取链路（`fetch_records`/`_enrich_from_local`/`_build_local_index`/`cover_proxy`）保留为 legacy，未删但已不被路由调用。
- 「今日必读」优先关联库内深度内容；库内无匹配时，生成两个 YouTube 搜索词并用互补性重排，只展示 ≥75 分的一个视频，用户二次确认后才入库。
- YouTube 搜索前的 CLI 探活改编自 Agent-Reach（MIT），来源与许可见 `THIRD_PARTY_NOTICES.md`。

## 评分体系（2026-06 已重构）
- 现行三维：**洞察原创 0-50 + 信源质量 0-25 + 故事可读 0-25**（旧 ai_relevance/storytelling/bonus 已废弃，旧分备份在 metadata 的 `scores_v1`）。
- 同步脚本已对齐新维度：`sync-feishu.js` 推 洞察原创/信源质量/故事可读（数字列，缺失自动建），`sync-feishu-doc.js` 文档同理。飞书表里旧的 AI相关性/故事性/加分项 列已不再写入（可手动删）。
- 重打分用 `scripts/rescore.py`（从已有摘要重算，不重跑整条流水线）。
- ⚠️ `sync-feishu.js` 只**新建**记录、不更新已有；重跑生成的 archive 其 `feishu_record_id` 为 null，直接 sync 会产生重复记录。

## 转录
- BibiGPT 为主（按**时长**计费，注意余额），baoyu 免费降级**仅支持 YouTube**。
- 小红书/online-media 的字幕在 `detail.subtitlesArray`（fetch.py 已处理）。
