# 今日 AI 判断可信度与学习闭环修复 Design Spec

> 状态：用户已确认 B 版范围  
> 日期：2026-07-07  
> 仓库：`/Users/yishu/YiShu Claude/content-curation`  
> 本 spec 只定义设计与验收标准，不包含实现计划与代码修改。

## 1. 需求定义

- 产品名称：NoiseFilter / 今日 AI 判断
- 目标用户：AI 产品经理本人优先，兼顾未来同类 AI PM、AI 创业者和内容研究者。
- 使用场景：用户每天 8:30 后打开首页，用极短时间判断过去 48 小时全球 AI 市场是否有必须关注的大事，以及哪些内容值得继续看、加入深度库或迁移到自己的产品判断里。
- 解决问题：AI 信息太多、热点过吵、推荐过载。用户不需要更多内容流，而需要一个可信判断台：少量候选、明确理由、库内证据、可行动结论。
- 产品形态：本地优先的 Flask Web 内容判断台，数据来自本地 archive、AI HOT、YouTube/外部补充和用户自主行为事件。
- 本轮目标：修复「可信度 + 数据口径 + 行为学习闭环 + 加入深度库状态反馈」，让当前半成品今日判断链路变成可持续迭代的稳定底座。

## 2. 输入类型判断

本需求属于明确需求。

已确认的信息：

- 给谁用：AI 产品经理本人。
- 在什么场景用：每日 8:30 后查看。
- 解决什么问题：信息太多，看不完，需要极少但可信的判断。
- 产品形态：本地 Web 内容判断台。
- 本轮做到什么程度：不大改架构，不加用户可见 Agent，先把核心闭环稳住。

## 3. 产品原则

### 3.1 降噪优先

首页不是推荐流。每一条进入「今日 AI 判断」的内容，都必须回答：

> 这件事值不值得我继续看？为什么？

系统默认减少推荐数量，而不是扩大候选池。

### 3.2 库内优先

当外部热点与本地深度库存在相关内容时，优先展示库内内容作为理解支撑。

库内补充应优先展示为：

- 一句金句
- 一个可迁移方法论
- 一个已有访谈或视频里的判断框架
- 一个帮助用户快速理解热点的上下文

### 3.3 注意力异常不等于推荐

「很多人都在讨论」只代表注意力异常，不代表内容一定值得进入首页判断。

产品表达应是：

> 大家在说，要不要加入今日判断？

而不是自动把热议内容塞进核心推荐。

### 3.4 可信度高于实时性

用户接受「晚一点没关系，但要相对可靠」。系统不做即时推送，不做刷屏提醒。

今日判断按每天 8:30 的节奏工作。若当天没有成功生成，页面必须如实说明当前展示的是旧判断或无判断。

## 4. 当前代码事实

真实仓库中已经存在的能力：

- `blog/today_signal.py` 已有两阶段编辑：AI HOT 粗筛 → 原文核验 → 大新闻/三槽判断。
- `blog/today_signal.py` 已有 priority lane，能优先处理「模型内部机制与可解释性」类研究。
- `blog/today_signal.py` 已有 attention 候选、promote/dismiss 基础函数。
- `blog/templates/_signals.html` 已有「热议浮现」「加入首页判断」「加入深度库」基础 UI。
- `blog/templates/index.html` 已有 `card`、`open_attention` 等前端埋点。
- `blog/user_preferences.py` 已有基于 `clicks.log` 的行为汇总。
- `scripts/rescore.py`、`scripts/sync-feishu.js`、`scripts/sync-feishu-doc.js` 基本已经使用新评分体系。

当前实测发现的问题：

- 当前 `blog/data/today_signal.json` 已过期，但页面仍会读取并展示为今日判断。
- `config/preferences.json` 的 `event_weights` 没有覆盖前端实际发送的 `card`、`open_attention`、`promote_attention`。
- `promote_attention_item()` 会把 attention item 加入 `signals`，但 `links` 为空，且没有证据状态说明。
- `scripts/rewrite.js` 仍在 markdown 输出和日志中使用旧评分口径：AI相关性 / 故事性 / 加分项。
- `scripts/sync-feishu.js` 的 `TOPIC_OPTIONS` 缺少 `AI 前沿`。
- `blog/templates/detail.html` 的相关推荐仍使用 `cover_token`，但当前 archive 真相源使用 `cover_url`。
- `blog/static/css/style.css` 有明显新旧样式叠层，但本轮不做 CSS 大重构。

## 5. 范围和优先级

| 优先级 | 一级模块 | 二级模块 | 功能 | 是否本轮做 | 说明 |
|---|---|---|---|---|---|
| P0 | 今日判断 | 新鲜度可信 | 今日判断读取时计算 fresh/stale/expired/missing 状态 | 是 | 不能把旧内容伪装成今日 |
| P0 | 今日判断 | 页面状态 | 首页展示新鲜、过期、无缓存、读取失败状态 | 是 | 用户必须知道当前判断是否可信 |
| P0 | 数据口径 | 话题枚举 | 全链路支持 `AI 前沿`，未知 topic 映射为 `其他` | 是 | 当前数据 29 条里 `AI 前沿` 占多数 |
| P0 | 数据口径 | 评分体系 | 新生成内容、metadata markdown、日志统一为洞察原创/信源质量/故事可读 | 是 | 消除新旧评分混用 |
| P0 | 详情页 | 相关封面 | 相关推荐使用 `cover_url`，不再依赖 legacy `cover_token` | 是 | 小修但明显影响质感 |
| P1 | 行为学习 | 事件权重 | 补齐 `card`、`open_attention`、`promote_attention` 等事件权重 | 是 | 让自主行为真正进入学习 |
| P1 | 行为学习 | 使用边界 | 行为只作为上下文和 tie-break，不放大推荐数量 | 是 | 避免个性化变成信息流 |
| P1 | 注意力异常 | 手动加入证据状态 | promote 后显示已手动加入，并标记 `evidence_status` | 是 | 用户知道是否已有库内证据 |
| P1 | 深度库 | 入库状态 | 为加入深度库提供 queued/running/done/exists/failed 状态 | 是 | 完成「看到 → 判断 → 入库」动作闭环 |
| P2 | 文档 | README 口径 | 只修正明显错误的评分/端口/本地 archive 口径 | 可做 | 不做完整品牌文档重写 |
| 暂不做 | 前端结构 | CSS/JS 大重构 | 拆分 CSS、抽离 JS 模块 | 否 | 避免本轮 scope 过大 |
| 暂不做 | 产品能力 | 用户可见 Agent | 新增推荐 Agent 或聊天 Agent | 否 | 当前不是 Agent 能力瓶颈 |

## 6. 推荐技术方向

| 层级/功能 | 推荐方案 | 推荐理由 | 更简单替代 | 风险/成本 |
|---|---|---|---|---|
| 今日判断新鲜度 | 在 `today_signal.py` 中新增 freshness 计算函数，页面读取缓存时动态补齐 | 集中处理，便于测试 | 只在模板里判断 | 模板逻辑变重，难测试 |
| 今日判断有效期 | 基于 `config/preferences.json.delivery` 的每天 8:30 计算下一次过期时间 | 符合产品节奏 | 沿用 30 分钟 `SIGNAL_TTL` | 30 分钟后就过期，不符合每日判断 |
| topic/score 口径 | 增加一个跨 Python/Node 可读的轻量 schema JSON，或在本轮至少加一致性测试 | 防止再次漂移 | 手动改缺失文件 | 快但容易复发 |
| 行为学习 | 扩展 `preferences.json.event_weights`，保持正向弱学习 | 不引入复杂 memory，适合自用阶段 | 只记录日志不使用 | 学习闭环仍断 |
| attention 证据状态 | `manual_promoted` item 增加 `evidence_status` 和展示文案 | 不强行生成证据，不编造 | promote 后不提示 | 用户误以为已有深度支撑 |
| 入库状态 | 本地 JSON job store，按 URL/content key 记录状态 | 本地项目足够，无需数据库 | 只改按钮文案 | 刷新后状态丢失 |
| 测试 | 继续使用现有 Python 单测 + Flask test client + Node syntax check | 贴合现有项目 | 只手测 | 回归风险高 |

## 7. 核心页面原型

### 7.1 首页：今日 AI 判断

```text
┌────────────────────────────────────────────────────────────┐
│ 今日核心推荐                                                │
│ 🔥 今日 AI 判断                                             │
│ AI HOT · 48 小时滚动 · 2026-07-07 08:30 · 新鲜              │
│ [每条只回答：值不值得继续看] [收起]                         │
├────────────────────────────────────────────────────────────┤
│ 如果已过期：                                                │
│ ⚠️ 上次生成于 2026-07-06 08:30，已超过今日更新窗口。         │
│ 当前内容仅供回看，不代表今日判断。                           │
├────────────────────────────────────────────────────────────┤
│ 如果无缓存：                                                │
│ 还没有生成今日判断。运行 ./run.sh signals 后再查看。          │
├────────────────────────────────────────────────────────────┤
│ 顶级大新闻，可空缺                                           │
│ 标题 / 来源 / 已核对原文 / 行动判断                          │
│ 一句话总结                                                   │
│ 为什么重要                                                   │
│ 你库里的相关金句 / 外部补充 / 暂无证据                        │
├────────────────────────────────────────────────────────────┤
│ 三个日常判断，可少于三条                                     │
│ C 端 AI 产品与增长 / 流量模式与商业化 / 1–3 个月行业趋势      │
├────────────────────────────────────────────────────────────┤
│ 热议浮现                                                     │
│ 很多人在提，但先不自动塞进判断                               │
│ [加入首页判断] [先不加]                                      │
└────────────────────────────────────────────────────────────┘
```

### 7.2 加入深度库按钮状态

```text
默认：         ＋ 加入深度库
提交后：       已提交
运行中：       入库中…
已存在：       已在深度库
完成：         已加入深度库
失败：         入库失败 · 查看原因
```

### 7.3 手动加入首页后的证据状态

```text
已手动加入首页判断

证据状态：
- 已补库内金句：展示金句和来源
- 已补外部视频：展示互补视频
- 待补证据：已加入判断，下一轮生成会尝试补库内证据
```

## 8. 详细功能设计

### 8.1 今日判断新鲜度

#### 目的

避免旧缓存被误认为「今日判断」。

#### 产品语义

今日判断不是 30 分钟缓存。它是每日判断面板。

有效期规则：

- 使用 `config/preferences.json.delivery.hour` 和 `delivery.minute` 作为每日生成基准，当前为 8:30。
- 一份今日判断从 `generated_at` 起，到下一次本地时间 8:30 前有效。
- 如果到了下一次 8:30 后仍没有新生成结果，状态变为 `expired`。
- AI HOT 请求缓存仍可保持 30 分钟；这不等于今日判断展示有效期。

#### 状态枚举

| 状态 | 含义 | 页面文案 |
|---|---|---|
| `fresh` | 当前判断仍在本次每日窗口内 | `新鲜` |
| `expired` | 已超过下一次 8:30，未生成新判断 | `已过期` |
| `missing` | 没有 `today_signal.json` | `还没有生成今日判断` |
| `invalid` | 缓存存在但 JSON 损坏或结构不合法 | `今日判断读取失败` |

#### 建议数据结构

`freshness` 可以由读取函数动态补齐，不必须写入 JSON。

```json
{
  "generated_at": "2026-07-07 08:30",
  "window_hours": 48,
  "freshness": {
    "status": "fresh",
    "is_expired": false,
    "age_hours": 2.5,
    "expires_at": "2026-07-08 08:30",
    "label": "新鲜"
  }
}
```

#### 实现边界

- 页面请求仍然只读缓存，不在 HTTP 请求里生成今日判断。
- `read_signal_cache()` 或其包装函数负责返回 freshness 状态。
- 模板只根据 `freshness.status` 展示文案，不自己推导日期逻辑。

### 8.2 数据口径统一

#### 话题枚举

本轮必须统一支持以下 topic：

- AI 前沿
- AI 编程
- AI 产品
- AI 创业
- AI 商业
- 投资
- 个人效率
- 其他

未知 topic 的处理：

- 展示层可显示原值，但同步/筛选等结构化场景必须映射为 `其他`。
- 日志中记录原始 topic，便于下一轮把高频未知 topic 纳入枚举。

#### 评分体系

统一评分维度：

- 洞察原创：0-50
- 信源质量：0-25
- 故事可读：0-25

总分为三项相加，满分 100。

必须修正的旧口径：

- `scripts/rewrite.js` 的 `formatScores()`。
- `scripts/rewrite.js` 的 `writeMetadataMd()`。
- `scripts/rewrite.js` 的完成日志。
- README 中明显错误的评分字段说明。

兼容要求：

- 历史内容若仍有旧字段，页面不崩溃。
- 新生成内容不得再输出 `AI相关性 / 故事性 / 加分项`。
- `scores_v1` 仅作为历史备份，不进入新 UI。

### 8.3 行为学习闭环

#### 目的

通过用户自主行为学习口味，但不做黑箱推荐。

#### 事件权重

| 事件 | 权重 | 含义 |
|---|---:|---|
| `card` | 0.3 | 普通卡片浏览，弱兴趣 |
| `open_attention` | 0.5 | 用户对热议浮现感兴趣 |
| `open_news` | 0.5 | 用户打开外部新闻 |
| `watch_video` | 1.0 | 用户愿意看视频补充 |
| `open_breaking` | 1.5 | 用户关注大新闻 |
| `open_local` | 1.5 | 用户打开库内内容，明确深读 |
| `promote_attention` | 2.0 | 用户手动确认值得进入首页 |
| `deep_library` | 3.0 | 用户认为值得长期保存 |

`dismiss_attention` 不作为负反馈进入权重。它只表示本次不想加入，不代表以后不喜欢这个主题。

#### 使用边界

行为学习只能用于：

- `prompt_context()` 中的用户上下文。
- 同质量内容的排序参考。
- 判断用户更关注哪些 slot/source。

行为学习不得用于：

- 自动扩大推荐数量。
- 绕过信源质量和原文核验。
- 把低质量内容推上首页。
- 把未点击解释为负反馈。

### 8.4 注意力异常手动加入

#### 目的

让「今天全在讨论某件事」能浮现给用户，但仍由用户决定是否进入首页判断。

#### 功能行为

- attention item 默认不进入核心推荐。
- 用户点击「加入首页判断」后：
  - 记录 `promote_attention` 行为。
  - item 从 `attention` 移到 `signals`。
  - 设置 `manual_promoted: true`。
  - 设置 `slot_label: 热议补充`。
  - 设置 `verification_label: 你手动加入`。
  - 设置 `evidence_status`。

#### 证据状态

| 状态 | 含义 | 页面展示 |
|---|---|---|
| `linked` | 已有库内 link 或金句 | 展示库内金句/深度补充 |
| `suggested` | 已有外部 YouTube 补充 | 展示外部补充 |
| `pending` | 暂无证据 | `已加入判断，待下一轮生成补证据` |

#### 约束

- 不得为手动加入内容编造金句。
- 如果没有库内匹配，允许显示 pending。
- 下一次 `run.sh signals` 后可重新匹配库内内容和外部补充。

### 8.5 加入深度库状态

#### 目的

让用户知道「加入深度库」是否成功，补齐从判断到沉淀的动作闭环。

#### 状态枚举

| 状态 | 含义 |
|---|---|
| `idle` | 可加入 |
| `queued` | 已提交，等待处理 |
| `running` | 正在抓取/改写/刷新 |
| `done` | 已完成入库 |
| `exists` | 本地 archive 已存在，不重复入库 |
| `failed` | 入库失败 |

#### Job 数据

建议使用本地 JSON，不引入数据库。

路径：

```text
blog/data/ingest_jobs.json
```

结构：

```json
{
  "yt:VIDEO_ID": {
    "job_id": "yt:VIDEO_ID",
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "title": "视频标题",
    "status": "running",
    "message": "正在抓取和改写",
    "archive_dir": "",
    "created_at": "2026-07-07 08:31:00",
    "updated_at": "2026-07-07 08:32:10",
    "return_code": null
  }
}
```

#### 后端行为

- `POST /ingest`：
  - 校验 URL。
  - 提取 content key。
  - 如果 archive 已存在，返回 `exists`。
  - 如果 job 已在 `queued/running`，返回当前 job。
  - 否则写入 `queued`，启动后台任务，返回 `job_id`。

- `GET /ingest/status?job_id=...`：
  - 返回 job 当前状态。
  - 找不到 job 时返回 404。

#### 前端行为

- 点击「加入深度库」后按钮立即变成「已提交」。
- 前端轮询 job status。
- `running` 时显示「入库中…」。
- `done` 时显示「已加入深度库」。
- `exists` 时显示「已在深度库」。
- `failed` 时显示「入库失败」，并展示短原因。

#### 约束

- 入库任务仍可用现有 `scripts/fetch.py --url` 和 `run.sh refresh`。
- 不引入 Celery、Redis、SQLite 或外部队列。
- 后台任务失败不得影响首页渲染。

### 8.6 详情页相关封面

#### 目的

修复 archive 真相源与 legacy 飞书封面字段不一致的问题。

#### 功能行为

- 相关推荐优先使用 `r.cover_url`。
- 只有 legacy 飞书记录存在 `cover_token` 时才使用 `/cover/<token>`。
- 两者都没有时显示占位图。

## 9. AI Agent 设计

本轮不新增用户可见 Agent。

理由：

- 当前问题是可信度、状态、口径一致性和行为闭环，不是 Agent 编排能力不足。
- 用户希望降噪，新增 Agent 容易让推荐链路更黑箱。

允许保留的模型/Agent 能力：

- `today_signal.py` 中现有 LLM 编辑判断。
- 原文核验、视频互补性判断、库内匹配。
- 后续实现阶段可以用 evaluator agent 做代码挑刺；这属于开发流程，不属于产品功能。

## 10. 验收标准

### 10.1 今日判断新鲜度

- Given `today_signal.json` 的 `generated_at` 在当前每日窗口内  
  When 用户打开首页  
  Then 今日判断区域展示 `新鲜`，并显示生成时间。

- Given 当前时间已经超过下一次 8:30 且没有新生成缓存  
  When 用户打开首页  
  Then 今日判断区域展示 `已过期`，并说明当前内容仅供回看。

- Given 本地不存在 `blog/data/today_signal.json`  
  When 用户打开首页  
  Then 页面展示「还没有生成今日判断」，并提示运行 `./run.sh signals`。

- Given `today_signal.json` 是非法 JSON  
  When 用户打开首页  
  Then 页面展示「今日判断读取失败」，首页其他内容仍正常渲染。

### 10.2 话题枚举

- Given 一条内容的 topic 是 `AI 前沿`  
  When 执行首页筛选、飞书同步字段创建或一致性测试  
  Then 系统接受该 topic，不把它丢失或改为空。

- Given 一条内容的 topic 是未知字符串  
  When 进入结构化同步或一致性检查  
  Then 系统将其映射为 `其他`，并保留日志信息。

### 10.3 评分体系

- Given 新处理一条 archive 内容  
  When `scripts/rewrite.js` 写入 `rewritten.md`、`metadata.md` 和控制台日志  
  Then 输出字段均为「洞察原创 / 信源质量 / 故事可读」。

- Given 历史内容存在旧评分字段  
  When 用户打开首页或详情页  
  Then 页面不崩溃，并优先展示新评分字段或总分。

### 10.4 行为学习

- Given 用户点击普通内容卡片  
  When 前端发送 `card` 事件  
  Then `behavior_summary()` 按 0.3 权重累计该事件。

- Given 用户打开热议浮现链接  
  When 前端发送 `open_attention` 事件  
  Then `behavior_summary()` 按 0.5 权重累计该事件。

- Given 用户点击「加入首页判断」  
  When 后端记录 `promote_attention` 事件  
  Then `behavior_summary()` 按 2.0 权重累计该事件。

- Given 用户点击「先不加」  
  When 后端记录 `dismiss_attention`  
  Then `behavior_summary()` 不把它作为负反馈累计。

### 10.5 注意力异常手动加入

- Given attention item 没有库内链接  
  When 用户点击「加入首页判断」  
  Then 该 item 进入 signals，并展示「待下一轮生成补证据」。

- Given promoted signal 后续获得库内 link  
  When 用户刷新首页  
  Then 页面展示库内金句或深度补充，不再显示 pending。

### 10.6 加入深度库状态

- Given 用户点击「加入深度库」  
  When URL 合法且本地 archive 不存在  
  Then `POST /ingest` 返回 `job_id` 和 `queued` 或 `running` 状态。

- Given 入库任务正在执行  
  When 前端轮询 `/ingest/status?job_id=...`  
  Then 接口返回 `running`，按钮显示「入库中…」。

- Given 入库任务成功完成  
  When 前端再次查询 job status  
  Then 接口返回 `done`，按钮显示「已加入深度库」。

- Given 该视频已存在于 archive  
  When 用户点击「加入深度库」  
  Then 接口返回 `exists`，按钮显示「已在深度库」。

- Given 后台命令返回非 0  
  When 前端查询 job status  
  Then 接口返回 `failed` 和短错误原因，按钮显示「入库失败」。

### 10.7 详情页相关封面

- Given related record 存在 `cover_url`  
  When 用户打开详情页  
  Then 相关推荐卡片显示该封面。

- Given related record 没有 `cover_url` 但有 `cover_token`  
  When 用户打开详情页  
  Then 相关推荐卡片使用 legacy `/cover/<token>`。

## 11. 建议测试清单

### Python

- `blog/test_today_signal.py`
  - `test_signal_cache_marks_fresh_within_delivery_window`
  - `test_signal_cache_marks_expired_after_next_delivery`
  - `test_signal_cache_missing_state`
  - `test_promoted_attention_without_links_has_pending_evidence`

- 用户偏好测试
  - `test_card_event_updates_preferences_with_low_weight`
  - `test_open_attention_event_updates_preferences`
  - `test_promote_attention_event_updates_preferences`
  - `test_dismiss_attention_is_not_negative_feedback`

- 入库状态测试
  - `test_ingest_existing_archive_returns_exists`
  - `test_ingest_job_lifecycle_queued_running_done`
  - `test_ingest_job_failed_records_message`

### Node

- `node --check scripts/rewrite.js`
- `node --check scripts/sync-feishu.js`
- `node --check scripts/sync-feishu-doc.js`
- 增加轻量 fixture 或可测试函数，验证 `rewrite.js` 输出新评分维度。

### Flask smoke

- `/` 返回 200。
- `/search?q=AI` 返回 200。
- `/search?q=最近有什么AI产品趋势` 返回 200。
- 首页在 fresh、expired、missing、invalid 四种 signal 状态下均可渲染。

### 数据一致性

- topic options 包含 `AI 前沿`。
- 新评分维度只有 `insight/source/storytelling`。
- 前端实际发送的正向事件都存在学习权重。

## 12. 暂不做范围

- 不做即时推送。
- 不做多用户登录。
- 不引入数据库或队列系统。
- 不新增用户可见 Agent。
- 不把 attention 自动变成推荐。
- 不重构整份 CSS。
- 不重写完整 README 或产品文档。
- 不改变现有 archive 作为真相源的架构。

## 13. 实现顺序建议

正式进入 plan/tasks 后，建议拆为以下任务：

1. 今日判断 freshness 状态与首页状态展示。
2. topic / score / README 局部口径统一。
3. 行为学习事件权重补齐。
4. attention promote 证据状态。
5. 加入深度库 job 状态。
6. 详情页 related cover 修复。
7. 测试、对抗压测和 evaluator review loop。

## 14. 开放问题

本 spec 为 B 版已收敛范围，只有两个实现细节需要在 plan 阶段固定：

1. 入库 job 的后台执行方式：使用现有 `subprocess.Popen` 包一层 Python runner，还是新增一个小型 helper 脚本管理状态。推荐新增 helper，避免 Flask endpoint 拼过长 shell。
2. topic/score schema 是否本轮抽成 `config/product_schema.json`。推荐抽出，因为 Python 和 Node 都要读，且这次 bug 正是多处手写漂移造成的。
