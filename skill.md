# NoiseFilter · 每日内容策展工作流

> 自动抓取 YouTube / Bilibili / 小宇宙，获取转录，用 AI 改写成结构化中文深度摘要，归档到本地并同步飞书多维表格。

---

## 快速使用

```bash
# 处理单个视频（无需确认，自动完成）
./run.sh url "https://www.youtube.com/watch?v=xxxxxxx"

# 扫描所有订阅源，交互式选择要处理的内容
./run.sh batch

# 同步已处理内容到飞书多维表格（结构化数据库视图）
./run.sh sync

# 同步已处理内容到飞书文档（长文阅读视图，含完整排版）
./run.sh sync-doc

# 同步指定单条内容到飞书文档
./run.sh sync-doc archive/20260312-some-title

# 一步到位：batch + 多维表格 + 飞书文档
./run.sh all
```

---

## 工作流架构

```
[订阅源 / URL 输入]
        ↓
   scripts/fetch.py          ← Python：抓取元数据 + BibiGPT 转录 + 封面下载
        ↓
   scripts/rewrite.js        ← Node.js：AI 改写（DeepSeek / OpenAI / Gemini）
        ↓
   scripts/sync-feishu.js    ← Node.js：飞书 Bitable API 推送
        ↓
[archive/ 本地归档]  +  [飞书多维表格]
```

### 四个核心脚本

| 脚本 | 语言 | 职责 |
|------|------|------|
| `scripts/fetch.py` | Python | 订阅源扫描、元数据提取（yt-dlp）、转录获取（BibiGPT / youtube-transcript-api）、封面下载、调用 rewrite.js |
| `scripts/rewrite.js` | Node.js | 读取 transcript.md + metadata.json，调用 AI 接口，生成 rewritten.md / metadata.md |
| `scripts/sync-feishu.js` | Node.js | 扫描 archive/ 中未同步条目，上传封面，写入飞书 Bitable 记录（结构化数据库视图）|
| `scripts/sync-feishu-doc.js` | Node.js | 将内容创建为飞书文档（Docx），含完整 markdown 排版，适合长文阅读 |

---

## 配置文件

### `config/.env`（不提交 git）

```bash
# 转录服务
BIBIGPT_API_TOKEN=your_token_here

# AI 改写（支持 OpenAI 兼容接口）
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.deepseek.com   # 或 https://api.openai.com/v1
OPENAI_MODEL=deepseek-chat                  # 或 gpt-4o / gemini-2.5-pro-preview-03-25

# 飞书多维表格（sync 命令使用）
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_APP_TOKEN=xxxxxxxxxxxxxxxxxxxxx      # 多维表格 URL 中的 appToken
FEISHU_TABLE_ID=tblxxxxxxxxxxxxxxxxx        # 多维表格 URL 中的 tableId

# 飞书文档（sync-doc 命令使用，App ID/Secret 与多维表格共用）
FEISHU_DOC_FOLDER_TOKEN=                    # 可选：文档存放的云空间文件夹 token
                                            # 留空则创建在个人空间根目录

# 归档目录（可选，默认 ./archive）
ARCHIVE_DIR=./archive
```

**获取方式：**
- BibiGPT Token：`bibigpt.co/user/integration`
- 飞书 App ID/Secret：飞书开发者后台 → 新建自建应用 → 凭证与基础信息
- 飞书 App Token / Table ID：从多维表格 URL 中提取（`/base/{appToken}?table={tableId}`）
- 飞书文档 Folder Token：打开云空间目标文件夹，URL 中 `folder/` 后面的字符串

**飞书应用需开启的权限（文档同步额外需要）：**
- `docx:document`（创建、编辑飞书文档）
- `drive:drive`（访问云空间，如需指定文件夹）

### `config/sources.yaml`（订阅源）

```yaml
youtube:
  - id: UCxxxxxxxxxxxxxxxxxxxxxx
    name: "Lex Fridman"
    url: "https://www.youtube.com/@lexfridman"
    limit: 5            # 每次检查最近几条

bilibili:
  - id: "12345678"      # UP主 UID（主页 URL 中）
    name: "硬地骇客"
    url: "https://space.bilibili.com/12345678"
    limit: 5

xiaoyuzhou:
  - id: "tech_podcast"  # 自定义标识符，用于去重
    name: "科技早知道"
    rss_url: "https://feeds.example.com/podcast.xml"
    limit: 10
```

### `config/rewrite-prompt.md`（AI 提示词）

定义 AI 输出的 JSON 结构，包含以下字段：

| 字段 | 说明 |
|------|------|
| `chinese_title` | 重拟中文标题，20字以内 |
| `guests` | 识别嘉宾姓名数组 |
| `key_quotes` | 3-5条金句（30-80字） |
| `core_ideas` | 3-5条核心观点（20-40字） |
| `key_insights` | 深度洞察段落，约500字 |
| `deep_summary` | 完整深度摘要，约1500字 |

---

## 归档结构

```
archive/
└── 20260312-投资入门：从柠檬水摊到价值投资的完整指南/
    ├── metadata.json      ← 机器可读，含所有字段 + 处理状态
    ├── metadata.md        ← 人类可读：标题、来源、嘉宾、金句
    ├── transcript.md      ← 带时间戳的原始转录（含 YAML frontmatter）
    ├── rewritten.md       ← AI 生成：核心观点 + 关键洞察 + 深度摘要
    └── cover.jpg          ← 封面图（可能是 .webp / .png）
```

`metadata.json` 关键字段：

```json
{
  "id": "视频ID",
  "url": "原始链接",
  "title": "原始标题",
  "chinese_title": "AI生成中文标题",
  "platform": "youtube|bilibili|xiaoyuzhou",
  "uploader": "创作者",
  "upload_date": "YYYYMMDD",
  "duration": 3600,
  "guests": ["嘉宾A", "嘉宾B"],
  "key_quotes": ["金句1", "金句2"],
  "rewrite_complete": true,
  "feishu_synced": false,
  "feishu_record_id": null
}
```

---

## 飞书多维表格字段配置

新建多维表格时添加以下字段：

| 字段名 | 字段类型 |
|--------|----------|
| 标题（主字段） | 文本 |
| 原标题 | 文本 |
| 来源平台 | 单选（选项：YouTube / Bilibili / 小宇宙） |
| 创作者 | 文本 |
| 发布日期 | 日期 |
| 原始链接 | 链接 |
| 时长（分钟） | 数字 |
| 嘉宾 | 文本 |
| 深度摘要 | 文本 |
| 封面 | 附件 |
| 总分 | 数字（0-100） |
| 评级 | 单选（选项：必读 / 强烈推荐 / 推荐 / 一般 / 可跳过） |
| AI相关性 | 数字（0-40） |
| 故事性 | 数字（0-30） |
| 加分项 | 数字（0-30） |

---

## 转录服务说明

工作流使用双层降级策略：

1. **主力：BibiGPT API**（付费，支持 YouTube / Bilibili / 播客）
   - 接口：`https://api.bibigpt.co/api/v1/getSubtitle`
   - 支持语言参数：`audioLanguage=zh`

2. **降级：youtube-transcript-api**（免费，仅 YouTube，需视频有字幕）
   - 自动在 BibiGPT 失败时触发
   - 输出带时间戳格式：`[HH:MM:SS] 文字内容`

---

## 去重与状态管理

- 已处理内容记录在 `config/state.yaml`（键为内容 ID，值为处理时间戳）
- 批量模式（`--batch`）：列出新内容让用户选择后才处理
- URL 模式（`--url`）：直接处理，无需确认
- 重新处理：删除对应 `metadata.json` 中的 `rewrite_complete: true` 后重跑

---

## AI 接口切换

在 `config/.env` 中修改两行即可：

```bash
# DeepSeek（推荐，性价比高）
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat

# OpenAI GPT-4o
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# Gemini（通过聚合平台）
OPENAI_BASE_URL=https://yunwu.ai/v1
OPENAI_MODEL=gemini-2.5-pro-preview-03-25
```

---

## 安装依赖

```bash
# Python
pip install -r requirements.txt
# 包含：yt-dlp, feedparser, requests, pyyaml, python-dotenv, youtube-transcript-api

# Node.js
npm install
# 包含：openai, js-yaml, dotenv
```

---

## 常见问题

**BibiGPT 返回空转录？**
→ 检查 token 是否有效，视频是否有音轨。YouTube 视频会自动降级到 youtube-transcript-api。

**rewrite.js 报错 `response_format not supported`？**
→ 正常，脚本会自动切换为普通模式重试。

**飞书同步失败 `code: 99991663`？**
→ 应用未获得多维表格权限。到飞书开发者后台 → 应用权限 → 开启 `bitable:app` 读写权限并发布。

**批量模式抓不到频道内容？**
→ YouTube 频道 URL 格式要用 `https://www.youtube.com/@handle` 或含频道 ID 的格式，不支持播放列表 URL。

**想重新改写某条内容？**

```bash
# 方式1：直接调用 rewrite.js
./run.sh rewrite archive/20260312-some-title

# 方式2：删除改写标记后重新跑 fetch
# 手动将 metadata.json 中 rewrite_complete 改为 false，再运行 ./run.sh url <原URL>
```
