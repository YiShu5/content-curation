# 信号串联与金句卡参数化（场景串联第一期）设计

## 目标

把「今日必读」和深度库两个孤岛串联起来，并把金句卡生产线从硬编码脚本升级为参数化工具，为「个人学习」与「分享同事」两个场景铺设共用的底层连接件。本期只做四个已确认的工作项 + 一次环境迁移，不做 UI 分享按钮、不做方向雷达、不做笔记系统。

## 工作项

### A. 信号内链改站内

今日信号里库内金句的主链接从外部平台时间戳 URL 改为站内 `/article/<record_id>`，外链降级为次要动作。

关键决策：

- 站内 href 在**模板层**计算（`_signals.html` render_deep 宏）：不改缓存结构、不落盘。派生逻辑不得进入 `read_signal_cache` / `enrich_cached_link_quotes` 的返回值持久化路径，否则 promote/dismiss 会把派生字段写进 `today_signal.json` 脏化真相源。
- 锚点 = 归一化金句文本的 sha1 短 hash（`q-` + 前 8 位），通过 app.py 注册的 Jinja filter `quote_anchor` 实现，归一化复用 `today_signal._quote_text`。**禁止按 index 定位**：金句会被 select-quotes 重排、rescore 重建，且 `_pick_local_quote` 两条路径（有/无 vector）选中的 index 含义漂移。
- 详情页金句循环加 `id="{{ q|quote_anchor }}"`，金句区加 `id="key-quotes"`；高亮用纯 CSS `:target`；hash 无命中时 3 行 JS 降级滚动到金句区（诚实降级，不假装精确定位）。
- 外链作为主链的 sibling `<a>`（嵌套 `<a>` 非法）：「原片 [ts] ↗」小动作，`target=_blank`；主链去掉 `target=_blank`（站内导航）。
- 埋点：主链 kind=`open_local` **严格不变**（preferences.json event_weights 依赖此名）；外链新增 kind=`open_origin`，权重 1.5，**与模板改动同一提交**写入 `config/preferences.json`（避免新 kind 不计入画像的窗口期）。
- 旧缓存兼容：link 缺 `record_id` 时回退 `deeplink` 外链；`record_id` 与 `deeplink` 均缺时整块（含 label 和 `.signal-deep` 外壳）不渲染，避免有标题无内容的空块。

### B. 入库闭环收尾

「＋加入深度库」job 完成后返回 record_id，按钮变「查看 → /article/<id>」。

关键决策：

- record_id 从归档目录 `metadata.json` 的 `id` 读取（新增 helper `archive_record_id`），兜底 `video_id_from_key(job_id)`；异常捕获须覆盖文件缺失和 `json.JSONDecodeError`。
- **只写 `blog/data/ingest_jobs.json`，绝不写 metadata.json**（会被 fetch.py 重抓重建、失败 rmtree 抹掉；record_id 本就是 metadata 派生的冗余数据，丢了可从 archive 现算回来）。
- `start_job` 的 exists 分支同样补 record_id——done 后刷新页面再点走的是 exists，两条路径体验必须一致。不改 `find_existing_archive` 签名（被现有测试钉死）。
- 顺手修僵尸 job bug：`ingest_worker.main()` 主体包 try/except → 置 failed 带异常摘要（当前 TimeoutExpired/FileNotFoundError 未捕获会让 job 永卡 running 并挡住所有重试）。
- 前端：done/exists 且有 record_id 时按钮 `replaceWith` 为 `<a href="/article/"+encodeURIComponent(id)>`，带 `open_local`/`library` 埋点；record_id 缺失（旧格式 job）回退现有 disabled 文案。轮询加上限 **1200 次（约 60 分钟）**——worker 两步 subprocess 各有 1800s 超时，30 分钟上限会在慢转录时误停；超限文案不得暗示失败。
- app.py 零改动（/ingest/status 原样透传 job dict）。

### C. legacy 删除 + 抓取去重（两个独立提交）

**提交 1（纯删，零行为变更）**：

- app.py 整删三块：62-196（飞书 API：`_token_cache`/`get_access_token`/`fetch_records`/`_text_value`/`_num_value`）、301-389（`_local_index_cache`/`_content_key`/`_build_local_index`/`_enrich_from_local`）、563-578（`cover_proxy` 路由），约 240 行；删 `import requests`、flask 的 `Response`、死掉的 `import os`；**保留 `import html`**（markdown ImportError fallback 在用）。
- detail.html 只删 165-166 的 `{% elif r.cover_token %}` 死分支。
- config.py 删 FEISHU_APP_ID/FEISHU_APP_SECRET/BASE_ID/TABLE_ID/CACHE_TTL（CACHE_TTL 必须与 app.py 同一提交删）；保留 SECRET_KEY 和 ZHIPU/EMBED 配置。
- 同步更新 CLAUDE.md 的 legacy 描述。
- 删除边界原则：只删 grep 零引用且调用链闭合的符号，存疑一律保留。

**提交 2（fetch.py id 级去重）**：

- 在 `process_item` 建目录之前加纯函数 `resolve_archive_dir(archive_root, item_id)`：glob `*-{sha1(id)[:8]}` → 读 metadata 校验 `id` 相等（防后缀撞车）→ 优先 rewrite_complete=True、否则目录名最新；命中即复用目录不新建。`--url` 和 `--batch` 两条链路同时受益。
- ⚠️ **数据安全硬约束（对抗审查结论）**：
  1. `process_item` 必须区分「本次新建」与「复用」目录：fetch.py:610/:614 的 `rmtree` **仅对本次新建目录执行**，复用目录失败时原样保留——否则复用 stub 后一次 rewrite 失败就会把既有付费转录连目录删掉（当前环境 rewrite 必败，这是常态路径不是边角）。
  2. 复用目录时若已有 transcript.md 且正文非失败标记，**直接复用正文、跳过整条转录链**（消除 BibiGPT 重复计费；「目录复用≠转录复用」是原方案的错误前提，已修正为显式复用）。
- 空 id 直接走新建不复用；metadata 损坏的目录跳过。

**存量 72 个冗余目录（已拍板：先 dry-run）**：

- 新增 `scripts/cleanup_dup_archives.py`：按 metadata id 分组，保留 rewrite_complete 且后处理字段最全、并列取目录名最新的一份，其余**移动**到 `archive/_duplicates_quarantine/`（绝不 rm——转录是付费资产，archive 无 git 兜底）。默认 dry-run，`--apply` 才移动；二次运行遇同名不覆盖。
- 本期只交付脚本 + dry-run 清单，`--apply` 等用户确认清单后执行。
- 已验证：所有读取链路（`load_archive_records`/`find_existing_archive`/`_existing_video_ids`）都是单层 glob，扫不到隔离子目录；此免疫性写进测试断言。

### D. 金句卡参数化 CLI

以 `blog/make_quote_shots.py` 原地改造（保 git 可 diff），吸收 grab_quote_frame 的定位/下载/抽帧为同文件函数；删除 grab_quote_frame.py / make_quote_2.py / grab_frames_multi.py（已拍板，git 历史保底）。

关键决策：

- CLI：`make_quote_shots.py <record_id> [--dir DIR] [--index 0,2] [--text 覆盖文案] [--name/--role 覆盖署名] [--out DIR] [--shift 秒] [--force] [--strict]`。
- record_id→目录解析与 app.py 同规则：目录名倒序 + 只认 rewrite_complete=True + metadata id 相等（规避重复目录命中 stub）。
- 署名降级链：`guest_info[0].name` → `guests`（字符串按 、,，/| 切第一个）→ `uploader`；头衔截断约 20 字；全空只渲染人名。
- 中文换行：删手写 `<br>`，纯函数 `font_size_for(text)` 字号阶梯（≤22 字 60px / ≤36 字 50px / ≤54 字 42px / 更长 36px）+ CSS `text-wrap: balance`；人工精修走 `--text`，不引入 LLM。
- 下载缓存：低清整片按视频 id 缓存到 `blog/data/video_cache/{id}.*`（0 字节视为无效重下）；同记录多金句只下载一次；产物命名 `shot-{record_id}-{i}.png`，默认输出 `blog/data/quote_cards/`（gitignore 区，成品手动挑选入 docs/images/）。
- 工具路径 `shutil.which()` 探测；archive 根路径与输出目录定义为**模块级常量**（测试 monkeypatch 依赖）。
- fail-fast：非 YouTube URL 拒绝；transcript 无时间戳退出码 2；匹配分 <0.35 警告（`--strict` 时中止）；金句 HTML 转义防注入。

### E. 环境迁移（已拍板：迁移到新路径）

代码合并后执行（顺序有意：先合去重修复，再迁移，避免每日任务在新路径重演 stub 累积）：

1. 旧路径 `config/.env` 拷贝到新路径。
2. 新路径重建根 `.venv`（fetch.py 依赖，含 yt-dlp）。
3. 同步旧路径 7/8 之后新增的 archive 目录到新路径。
4. launchd `com.noisefilter.daily.plist` 改指向新路径（注意 `bash -lc` 下 node/nvm 的 PATH 问题，plist 中显式处理）。
5. 旧副本保留不删，仅不再是生产。

## 数据安全与测试总约束

- 测试一律 tempfile + monkeypatch 模块常量（沿用仓库裸 assert 脚本 + `__main__` 手动注册的惯例，**不引入 pytest**）；新测试函数必须注册进 `__main__`。
- 绝不触碰真实 `archive/`、`blog/data/`、`docs/`；转录函数逐个按名打桩（它们是 requests 函数，「桩掉 subprocess」覆盖不到）；`get_transcript_bibigpt` 桩成触达即失败。
- 端到端 ingest 永不进自动化测试（防真实计费）。
- 人工验收会向真实 clicks.log 写少量行为记录（可接受）；压测流量一律走 tmp 重定向。

## 验收标准

- 首页点库内金句 → 落到站内 `/article/<id>` 且对应金句高亮；点「原片 ↗」新标签打开带时间戳的外部链接;手改 hash 为不存在值时滚动到金句区。
- 对库内已有视频点「＋加入深度库」→ 按钮变「查看 →」并能打开详情页；worker 异常的 job 状态为 failed 而非永久 running。
- legacy 删除后 6 个测试文件全绿，重启 5055 后首页/详情/封面无 500。
- 对同 id 跑两次 fetch 不再新增目录；复用目录在 rewrite 失败后原样保留、transcript.md 字节不变。
- cleanup 脚本 dry-run 输出「保留/移动」清单且不动任何文件。
- 对任意一条 rewrite_complete 记录跑金句卡 CLI 产出排版正确的 PNG；同记录第二次运行不重复下载视频。
- 全部新旧测试通过；每个工作项经 evaluator agent 挑刺并修复；review-fix ≤3 轮。

## 非目标

- 不做详情页「生成分享卡」按钮、不加任何新路由（UI 接入是下期）。
- 不放开 `_locate_timestamp` 对无时间戳转录的限制（匹配范围行为变更，独立决策）。
- 不做方向雷达、笔记框、飞书评论回流、周报自动化。
- 不改 run.sh 子命令。
- 不执行 cleanup `--apply`（等用户核对清单）。
