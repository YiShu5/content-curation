# CLAUDE.md — content-curation（NoiseFilter / 降噪）

内容策展工具：抓取音视频长内容 → AI 转录/改写/打分 → 归档 + 飞书 + 博客。总览见 README.md。
本文件只记**易踩坑的项目约定**（若存在全局 ~/.claude/CLAUDE.md 则合并生效）。

## 运行
- 博客用 `blog/.venv` 跑，端口 **5055**（5000 会撞 macOS AirPlay Receiver）；默认只监听 127.0.0.1 且 debug 关（Werkzeug 调试器=任意代码执行），开发要热重载/局域网用 `FLASK_DEBUG=true` / `BLOG_HOST=0.0.0.0` 显式打开。
- 两个 Python 环境：根 `.venv`（fetch.py，含 yt-dlp）+ `blog/.venv`（flask/numpy/markdown/dotenv）。
- 统一入口 `run.sh <cmd>`：auto / batch / url / rewrite / sync / sync-doc / embed / signals / publish-daily / daily-brief / hot-watch / enrich-guests / select-quotes / refresh / daily / all。重打分是 `scripts/rescore.py`（不是 run.sh 子命令）。
- ⚠️ run.sh 有 `set -euo pipefail`：分支里"赋值=$(命令)"失败会直接终止整个脚本——要读退出码必须写成 `v=$(cmd) || st=$?`，否则失败分支永远不执行（2026-07-17 daily-brief 的 ❌ 通知因此从未发出过）。

## 生产与自动化（2026-07，运维细节见 docs/OPERATIONS.md）
- 线上 https://www.yishucc.top/（VPS）；服务器 `.env` 必须有 `BLOG_TIMEZONE=Asia/Shanghai`，否则"当日"判断差 15 小时。
- signals 必须在每日 8:30 之后跑（freshness 窗口锚定 8:30 投递时间，早跑当天就过期）。
- ⚠️ hot-watch 的 AGI Hunt 轨只用免鉴权 `agihunt.info/api/trends`，**绝不接其 /agent/v1 skill 体系**（远程指令通道 + 条款禁轮询）；heat 与 AI HOT score 两套量纲**绝不换算混轨**。
- 每日简报快照加载校验要求清洗结果与存盘**逐字节相等**——给 topic 加可选字段必须"空值省略键"，否则历史快照全部判损坏（2026-07-14 踩过）。

## 前端 CSS（2026-07 已做减法）
- 加载顺序 `style.css → daily.css → theme-tokens.css`（最后加载，`!important` 统一纸墨编辑部视觉）。改视觉先看 theme-tokens 的令牌（纸底/墨字/陶土单强调/唯一蓝/3档圆角）。
- ⚠️ **别再往 style.css 叠新 `:root` 或重复选择器块**（历史上叠了 5 层考古、171 个色值，已清到单一 :root）——要改令牌就改 theme-tokens，否则考古层重新长回来。令牌下沉进 style.css 消除 !important 是未排期的后续（见记忆 open-items）。

## 密钥与产物（勿提交）
- `config/.env` 存所有密钥（飞书/DeepSeek/智谱/BibiGPT），已 gitignore，**绝不入库**。
- `archive/`、`blog/data/`、`.venv/`、`blog/.venv/`、`.claude/` 均已忽略（生成物/本地）。

## 数据流（2026-06 已改为「本地 archive 为真相源」）
- 博客直接读 `archive/*/metadata.json`（`load_archive_records`，blog/app.py），**不再依赖飞书**。新抓内容刷新即见。
- 记录 `id` = metadata 的 `id`（视频 id / audio-xxx）；详情页 `/article/<id>`、向量索引、今日信号都按这个 id 对齐。
- 封面走本地：`/cover-local/<archive_dir>` 直接发 archive 里的 cover.*。
- ⚠️ 改完 fetch 新内容后，**首页/详情立刻可见(实时读 archive)，但语义搜索/相关推荐/今日信号要 `run.sh embed` 重建索引才会纳入**。
- 旧的飞书读取链路（`fetch_records`/`_enrich_from_local`/`_build_local_index`/`cover_proxy`）已于 2026-07 删除（git 历史可查）；飞书仅剩 `scripts/sync-feishu*.js` 的写出方向。
- 「今日必读」优先关联库内深度内容；库内无匹配时，生成两个 YouTube 搜索词并用互补性重排，只展示 ≥75 分的一个视频，用户二次确认后才入库。
- YouTube 搜索前的 CLI 探活改编自 Agent-Reach（MIT），来源与许可见 `THIRD_PARTY_NOTICES.md`。

## 评分体系（2026-06 已重构）
- 现行三维：**洞察原创 0-50 + 信源质量 0-25 + 故事可读 0-25**（旧 ai_relevance/storytelling/bonus 已废弃，旧分备份在 metadata 的 `scores_v1`）。
- 维度上限与评级阈值**单源于 `config/product_schema.json`**（rewrite.js 与 rescore.py 共用）；改评分体系只改 schema，两侧代码都对模型分数钳位重算、不信任 LLM 算术。
- 同步脚本已对齐新维度：`sync-feishu.js` 推 洞察原创/信源质量/故事可读（数字列，缺失自动建），`sync-feishu-doc.js` 文档同理。飞书表里旧的 AI相关性/故事性/加分项 列已不再写入（可手动删）。
- 重打分用 `scripts/rescore.py`（从已有摘要重算，不重跑整条流水线）。
- ⚠️ `sync-feishu.js` 只**新建**记录、不更新已有；重跑生成的 archive 其 `feishu_record_id` 为 null，直接 sync 会产生重复记录。

## 去重与清理（2026-07）
- fetch.py 建目录前按 id 的 sha1 后缀复用既有归档（`resolve_archive_dir`），同一视频不再因日期/标题漂移每天新建目录；复用目录里的有效转录直接复用，失败时**不 rmtree**（只清理本次新建的空壳）。
- 存量重复目录用 `scripts/cleanup_dup_archives.py` 清理：默认 dry-run，`--apply` 把冗余份**移动**到 `archive/_duplicates_quarantine/`（绝不删除，转录是付费资产）。

## 转录（2026-07 云端优先）
- 顺序：免费字幕 API（baoyu/ytapi，**仅 YouTube**）→ Groq 云端 whisper（约 $0.04/小时，需 `GROQ_API_KEY`，无 key 自动跳过）→ BibiGPT（全托管付费，按**时长**计费注意余额）→ whisper 本地（最最兜底，慢）。
- 小红书/online-media 的字幕在 `detail.subtitlesArray`（fetch.py 已处理）。
