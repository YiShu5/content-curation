# 运维手册（OPERATIONS）

> 受众：在服务器上部署/维护本站的人（包括未来的自己）。本地开发见根目录 README.md。
> 最后核对：2026-07-17

## 部署形态

- 生产站点：https://www.yishucc.top/ （VPS + 反向代理 HTTPS，Flask 只监听 127.0.0.1:5055）
- **卡片/图片渲染依赖 headless Chrome**：金句卡、今日判断日卡、小红书导出、素材盘热点板都走
  「HTML→Chrome 截图」。Mac 本机用系统 Chrome；VPS 需 `apt install chromium` 并在
  `.env` 设 `CHROME=/usr/bin/chromium`。缺 Chrome 时这些出口 503/跳过，其余功能不受影响。
- **本地机器是 `archive/` 的唯一真相源**（archive 被 gitignore、无 git 兜底），服务器是镜像；
  本地新增内容后用 `./scripts/deploy-content.sh` 推送（rsync archive + 向量索引 + 转录分块；
  本地成品 <5 条时拒绝同步，防止误删后把空目录镜像上去）。
- 每日简报数据（`blog/data/daily_issues/`）在**服务器上**原生产生，服务器是它的真相源，需独立备份。

## 服务器 crontab

```cron
# 每日简报：signals 生成 → 带闸门自动发布 → 飞书通知结果
35 8 * * * cd /path/to/content-curation && mkdir -p logs && ./run.sh daily-brief >> logs/daily.log 2>&1

# 盘中热度新高监控（双信源），:07/:37 错开整点与简报
7,37 * * * * cd /path/to/content-curation && ./run.sh hot-watch >> logs/hot_watch.log 2>&1

# 每日素材盘：双源 Top5 文字卡片 + 三合一热点板图（简报和终审之后）
50 8 * * * cd /path/to/content-curation && ./run.sh materials >> logs/materials.log 2>&1

# 每周备份服务器原生数据
0 3 * * 0 cd /path/to/content-curation && mkdir -p backups && tar czf backups/daily_issues_$(date +\%Y\%m\%d).tar.gz blog/data/daily_issues
```

**8:35 不是随便选的**：今日信号的 freshness 窗口锚定在每日 8:30 投递时间，
8:30 之后生成的缓存全天新鲜；早于 8:30 生成会在 8:30 被判过期。

## 环境变量（config/.env，全部勿入库）

| 变量 | 作用 | 备注 |
|---|---|---|
| `BLOG_TIMEZONE` | 全站"当日"判断的时区 | **服务器必须设 `Asia/Shanghai`**，否则自动发布/新鲜度差 15 小时 |
| `BLOG_ADMIN_PASSWORD` / `SECRET_KEY` | 管理员登录与会话签名 | 设了密码但 SECRET_KEY 为默认值时应用拒绝启动 |
| `SESSION_COOKIE_SECURE` | 公网 HTTPS 下设 `true` | |
| `FLASK_DEBUG` / `BLOG_HOST` / `BLOG_PORT` | 开发覆写 | 默认 debug 关、只听 127.0.0.1（Werkzeug 调试器可执行任意代码） |
| `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL` | DeepSeek（改写/聚类/主编） | signals 每天 2+ 次调用 |
| `ZHIPU_API_KEY` | 语义搜索 embedding | 搜索页实时调用 |
| `GROQ_API_KEY` | 云端 whisper 转录（本地抓取用） | 约 $0.04/小时 |
| `FEISHU_BOT_WEBHOOK` / `FEISHU_BOT_SECRET` | 飞书群自定义机器人 | 未配置时所有通知静默跳过 |
| `HOT_WATCH_THRESHOLD` | AI HOT 轨入围下限（默认 78） | 实测 AI HOT 分数上限约 83，勿设 85+ |
| `HOT_WATCH_AGIHUNT` / `HOT_WATCH_AGIHUNT_FLOOR` | AGI Hunt 轨开关（默认开）/ heat 下限（默认 10） | heat 无量纲承诺，按触发密度微调 |
| `HOT_WATCH_QUIET` | 安静时段如 `23-8`，空=全天实时 | 夜间积攒、早晨合并补报 |
| `REWRITE_MAX_TOKENS` | 改写超长保护阈值（默认 32000） | 转录估算超阈值自动分段浓缩（map-reduce）再改写 |
| `CHROME` | headless Chrome 路径 | 默认 macOS 系统 Chrome；VPS 设 `/usr/bin/chromium` |
| `MATERIALS_TOP_N` / `MATERIALS_POSTERS` | 素材盘每源条数（默认 5）/ 热点板图开关（默认开） | |
| `DEPLOY_SSH_HOST` / `DEPLOY_REMOTE_DIR` | deploy-content.sh 的目标 | 本地机器配置 |

## 每日简报自动发布（run.sh daily-brief）

流程：`signals`（拉 AI HOT → DeepSeek 聚类 → 逐条抓原文核验 → 主编选 ≤3 条草稿）
→ `publish-daily`（带闸门发布）→ 飞书通知成败。

闸门与手动发布完全同源：当日新鲜度、每主题 ≥1 条已核验（readable）信源、最多 3 条；
**不达标宁可不发**（当天空刊，首页显示上一期为"最新一期"）。发布后可随时在
`/admin/login` 登录做修订（修订历史公开可查）。幂等：当日已发布则跳过，cron 重跑安全。

期刊级可选字段（2026-07-19 起，空值省略键）：**今日主线**（主编 LLM 跨主题一句定调，
可空可改，进首页副标题位、分享文本和飞书通知）；**主编手记**（纯人工字段，机器路径
永不写入——早上读完简报后在 admin 修订里补写，页面带「人工撰写」标记，这是全站唯一
的人格声音位）。旧快照没有这两个键，照常可读。

飞书通知语义：✅ 也每天发——**沉默即异常**（哪天早上 8:40 没消息，说明 cron 本身死了）。

发布成功后附带**终审官**结论（`blog/issue_review.py`，提醒模式）：对照 AI HOT 与
AGI Hunt 两源当日热榜，检查本期有无遗漏的大事或硬伤，结论行（✅/⚠️）拼进飞书通知。
永不拦截发布；两源热榜全部不可用时弃权不出具结论；自身故障静默降级（诊断进 cron 日志）。

## 观测与质量护栏

- **LLM 调用日志**：全部 9 个 AI 角色（改写/重评/嘉宾/金句/聚类/主编/延伸阅读/问答/终审）
  的每次调用都追加一行到 `blog/data/llm_calls.jsonl`（caller/model/耗时/tokens/错误），
  排查成本或失败率从这里入手；grounding 丢弃、解析降级等事件也记在同一文件（含 `event` 字段的行）。
- **金句 grounding**：改写要求模型同时交出 `key_quotes_source`（原文语言出处句），
  程序核对出处句逐字存在于转录，对不上的金句整条丢弃——日志里 `quote_grounding_dropped`
  频繁出现时说明模型在虚构，值得关注。
- 精选金句（select-quotes）会同步重排 `key_quotes_source` 保持配对。

## 每日素材盘（run.sh materials）

飞书晨间信息流的第三层（判断层=简报+终审、告警层=hot-watch、**素材层=这个**）：
双源各 Top5 原始榜单发**文字卡片**（保留源名与原生热度数字，供本人 triage；
跨源重复标 ↔ 不删），随后发一张**三合一热点板图**（1 大 + 2 小，1080×1440 纸墨风）。

**分层纪律**：对内文字卡片透明（源名+数字都在）；对外分享图收敛——
**绝不出现聚合源名与原始热度量纲**（两套数字并排即可指纹识别数据源），
用「今日最热/还在热议」定性标签 + 「综合公开讨论热度」中性脚注，有测试锁死该契约。
零 LLM 调用（素材层的意义就是不加工）。

**发图的飞书前置条件**（三道门，缺一发图跳过、文字卡不受影响）：
① 应用开通 `im:resource:upload` 权限；② 应用添加「机器人」能力；③ 每次变更后**发布版本**才生效。
报错自查：`99991672`=缺①，`234007`=缺②。

## 小红书导出

简报页管理员按钮「导出小红书」→ `GET /admin/xhs/<date>.zip`：把已发布简报渲染成 3:4 竖版
PNG 图组 + DeepSeek 生成的 `文案.txt`（标题/正文/tag，失败不影响图片），打包 zip。
图组按受众动线排序（受众=关注 AI 但没时间刷热点的人）：`00 封面`（时间承诺 + 今日主线）→
`01 速览卡`（主线 + 每条一句话结论 + 主编手记，只想拿结论看到这张就够）→ `02+ 主题卡`（逐条拆解）。
依赖 Chrome（见「部署形态」）。文案 agent 是第 10 个 AI 角色。

## 盘中监控（run.sh hot-watch）——双信源独立冠军

| 轨 | 信源 | 触发规则 |
|---|---|---|
| AI HOT | aihot.virxact.com（0-100 分，实测上限 ~83） | score ≥78 且刷新当日最高分的**新**条目 |
| AGI Hunt | agihunt.info/api/trends（heat 浮点，头部 8-14） | heat ≥10 且刷新当日 AGI Hunt 冠军的**新**趋势 |

- 两轨各用原生量纲**绝不换算**（AGI Hunt 官方声明 heat "仅用于排序，无绝对含义"）；
- 同一新闻只推一次；已推新闻分数后涨只抬高冠军线不重推；
- 跨源同事件用标题 bigram 相似度抑制（日志里 grep "跨源去重抑制" 可看两源重叠度）;
- 单源失败只弃该轨，两源全失败才报错且状态不动；状态在 `blog/data/hot_watch_state.json`，
  删除即重新播种（静默、不会轰炸）；
- **红线：AGI Hunt 只用免鉴权站点 API（/api/trends），绝不接其 /agent/v1 skill 体系**
  ——那是给 agent 的授权接口，含远程指令更新通道（426）且条款禁止定时轮询；
- 消息署名「AGI HUNT · agihunt.info」是引用礼貌，保留。

选型依据（2026-07-17 实测）：AI HOT 系统性低估 X 原生大事件（Kimi K3 在其全量流仅 33-53 分），
AGI Hunt 趋势榜对同事件 heat 13.7 / rank 1。故双源互补，不做替换。

## 故障排查速查

| 症状 | 大概率原因 | 处置 |
|---|---|---|
| 早晨没有任何飞书消息 | cron 没跑（服务器重启等） | `crontab -l` 核对，看 logs/daily.log |
| ❌ 日报失败：草稿不可用/已过期 | signals 没跑成或跑早了 | 手动 `./run.sh signals && ./run.sh publish-daily` |
| 首页显示"已过期，仅供回看" | 当日 signals 未生成 | 同上 |
| hot-watch 从不触发 | 阈值高于信源实际分布 | 看本手册环境变量表的实测参考值 |
| 网站没有本地新抓的内容 | 忘了 deploy-content | 本地跑 `./scripts/deploy-content.sh` |
| 简报发布报 storage_corrupt | daily_issues 快照损坏 | 从 backups/ 或 revisions/ 恢复；快照校验要求逐字节 round-trip |

## 备份与恢复

- 本地 archive 快照：`~/noisefilter-archive-backup-*.tar.gz`（重大操作前手动打）；
- 历史教训（2026-07-13）：archive 曾被 `git pull` 检出误删（当时被 git 跟踪、远端删除），
  靠历史 commit `git restore --source=<sha> --worktree -- archive/` 全量恢复。
  archive 现已 gitignore，**唯一兜底是备份**，重大操作前先 tar；
- 服务器 daily_issues：每周日 cron tar 到 backups/。
