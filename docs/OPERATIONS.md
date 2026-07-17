# 运维手册（OPERATIONS）

> 受众：在服务器上部署/维护本站的人（包括未来的自己）。本地开发见根目录 README.md。
> 最后核对：2026-07-17

## 部署形态

- 生产站点：https://www.yishucc.top/ （VPS + 反向代理 HTTPS，Flask 只监听 127.0.0.1:5055）
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
| `DEPLOY_SSH_HOST` / `DEPLOY_REMOTE_DIR` | deploy-content.sh 的目标 | 本地机器配置 |

## 每日简报自动发布（run.sh daily-brief）

流程：`signals`（拉 AI HOT → DeepSeek 聚类 → 逐条抓原文核验 → 主编选 ≤3 条草稿）
→ `publish-daily`（带闸门发布）→ 飞书通知成败。

闸门与手动发布完全同源：当日新鲜度、每主题 ≥1 条已核验（readable）信源、最多 3 条；
**不达标宁可不发**（当天空刊，首页显示上一期为"最新一期"）。发布后可随时在
`/admin/login` 登录做修订（修订历史公开可查）。幂等：当日已发布则跳过，cron 重跑安全。

飞书通知语义：✅ 也每天发——**沉默即异常**（哪天早上 8:40 没消息，说明 cron 本身死了）。

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
