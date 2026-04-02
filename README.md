<div align="center">

# 🔇 NoiseFilter

**从噪音中提炼信号，用 AI 把优质内容变成你的知识资产**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?logo=node.js&logoColor=white)](https://nodejs.org)
[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)

每天有 720,000 小时的视频上传到 YouTube，500+ 播客在小宇宙更新。

**你不需要看完所有内容，你需要一个降噪系统。**

[快速开始](#-快速开始) · [工作原理](#-工作原理) · [博客展示](#-博客展示) · [配置说明](#-配置说明)

</div>

---

## ✨ NoiseFilter 能做什么

```
YouTube / Bilibili / 小宇宙
        ↓ 自动抓取
   原始转录文本（BibiGPT / youtube-transcript-api）
        ↓ AI 深度改写
   结构化中文摘要（标题 · 金句 · 核心观点 · 2000字深度解读）
        ↓ 归档 + 同步
   本地 Markdown + 飞书多维表格 + 博客网站
```

**一条命令，5 分钟获取一小时播客的全部精华。**

### 核心能力

| 能力 | 说明 |
|------|------|
| 🎯 **多源抓取** | YouTube 频道、Bilibili UP主、小宇宙播客，统一配置 |
| 🗣 **智能转录** | BibiGPT API 主力 + youtube-transcript-api 免费兜底 |
| 🧠 **AI 深度改写** | 不是简单摘要，而是：中文标题重拟 + 嘉宾识别 + 金句提取 + 核心观点 + 1500字深度解读 |
| 📁 **结构化归档** | 每条内容独立文件夹：metadata / transcript / rewritten / cover |
| 📊 **飞书同步** | 一键推送到多维表格，封面图自动上传 |
| 🌐 **博客展示** | 内置 Flask 站点，降噪风格，开箱即用 |

---

## 🚀 快速开始

### 1. 克隆 & 安装

```bash
git clone https://github.com/YiShu5/content-curation.git
cd content-curation

# Python 依赖
pip install -r requirements.txt

# Node.js 依赖
npm install
```

### 2. 配置 API 密钥

```bash
cp config/.env.example config/.env
```

编辑 `config/.env`，填入你的密钥：

| 配置项 | 获取方式 |
|--------|----------|
| `BIBIGPT_API_TOKEN` | [bibigpt.co/user/integration](https://bibigpt.co/user/integration) |
| `OPENAI_API_KEY` | DeepSeek / OpenAI / 任意兼容接口的 Key |
| `OPENAI_BASE_URL` | DeepSeek: `https://api.deepseek.com`，OpenAI: `https://api.openai.com/v1` |
| `FEISHU_APP_ID` / `APP_SECRET` | [飞书开发者后台](https://open.feishu.cn/app) 创建自建应用 |
| `FEISHU_APP_TOKEN` / `TABLE_ID` | 多维表格 URL 中提取 |

### 3. 配置订阅源

编辑 `config/sources.yaml`：

```yaml
youtube:
  - id: UCxxxxxx
    name: "Lex Fridman"
    url: "https://www.youtube.com/@lexfridman"
    limit: 5

bilibili:
  - id: "12345678"
    name: "硬地骇客"
    url: "https://space.bilibili.com/12345678"
    limit: 5

xiaoyuzhou:
  - id: "tech_podcast"
    name: "科技早知道"
    rss_url: "https://feeds.example.com/podcast.xml"
    limit: 10
```

### 4. 开始使用

```bash
# 处理单个视频（最快体验）
./run.sh url "https://www.youtube.com/watch?v=xxxxxxx"

# 扫描所有订阅源，交互式选择
./run.sh batch

# 同步到飞书多维表格（结构化数据库视图）
./run.sh sync

# 同步到飞书文档（长文阅读视图，含完整排版）
./run.sh sync-doc

# 一步到位：批量抓取 + 飞书同步（多维表格 + 文档）
./run.sh all
```

---

## 🔍 工作原理

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   fetch.py   │────▶│  rewrite.js  │────▶│sync-feishu.js│
│   (Python)   │     │  (Node.js)   │     │  (Node.js)   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
  yt-dlp 元数据        DeepSeek AI          飞书 API
  BibiGPT 转录        结构化 JSON          封面上传
  封面下载            金句/观点/摘要        记录创建
       │                    │                    │
       ▼                    ▼                    ▼
  transcript.md       rewritten.md          飞书多维表格
  metadata.json       metadata.md
  cover.jpg
```

### 归档结构

每条处理过的内容生成独立文件夹：

```
archive/
└── 20260312-投资入门：从柠檬水摊到价值投资的完整指南/
    ├── metadata.json      # 机器可读，含所有字段
    ├── metadata.md        # 人类可读：标题、来源、嘉宾、金句
    ├── transcript.md      # 带时间戳的原始转录
    ├── rewritten.md       # AI 生成的深度摘要
    └── cover.jpg          # 封面图
```

### AI 改写输出示例

```json
{
  "chinese_title": "投资入门：从柠檬水摊到价值投资的完整指南",
  "guests": [],
  "key_quotes": [
    "爱因斯坦说过，宇宙中最强大的力量是复利...",
    "巴菲特说，投资的第一条规则是永远不要亏钱..."
  ],
  "core_ideas": [
    "复利是长期投资的核心引擎，关键在于尽早开始",
    "优秀企业的特征：强护城河、低资本需求、高自由现金流"
  ],
  "key_insights": "500字深度洞察...",
  "deep_summary": "1500字完整摘要..."
}
```

---

## 🌐 博客展示

内置一个「降噪」风格的博客站点，数据直接读取飞书多维表格：

```bash
cd blog
pip install flask
python app.py
# 打开 http://localhost:5000
```

**首页**：三列卡片网格，封面 + 平台标签 + 创作者 + 摘要预览

**详情页**：大图 Hero + 侧边导航 + 金句精选 + 核心观点 + 深度摘要

---

## ⚙️ 配置说明

### 飞书多维表格字段

在飞书中新建多维表格，添加以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 标题 | 文本（主字段） | AI 生成中文标题 |
| 原标题 | 文本 | 原始标题 |
| 来源平台 | 单选 | 选项：YouTube / Bilibili / 小宇宙 |
| 创作者 | 文本 | 频道/UP主/播客名 |
| 发布日期 | 日期 | 内容发布日期 |
| 原始链接 | 链接 | 视频/播客 URL |
| 时长（分钟） | 数字 | 内容时长（分钟） |
| 嘉宾 | 文本 | 嘉宾姓名，多人用顿号分隔 |
| 深度摘要 | 文本 | AI 生成完整摘要 |
| 封面 | 附件 | 封面图片 |
| 总分 | 数字 | AI 综合评分 0-100 |
| 评级 | 单选 | 选项：必读 / 强烈推荐 / 推荐 / 一般 / 可跳过 |
| AI相关性 | 数字 | AI/科技议题相关性得分 0-40 |
| 故事性 | 数字 | 叙事质量得分 0-30 |
| 加分项 | 数字 | 数据/框架/反直觉加分 0-30 |

### 飞书文档字段（sync-doc）

`sync-doc` 命令会将内容创建为飞书文档（Docx），无需额外建表，文档结构如下：

```
[评分卡片]  综合评分 82/100 ⭐⭐⭐ 强烈推荐
            AI相关性 35/40 | 故事性 25/30 | 加分项 22/30
[元信息]    来源平台 / 创作者 / 发布日期 / 原始链接
[嘉宾]
[金句]
[核心观点]
[关键洞察]  含完整 markdown 结构
[深度摘要]  含完整 markdown 结构
```

需在 `config/.env` 中配置（可选）：

```bash
FEISHU_DOC_FOLDER_TOKEN=  # 文档存放的云空间文件夹 token，留空则放个人根目录
```

飞书应用需额外开启权限：`docx:document`、`drive:drive`

### AI 接口切换

在 `config/.env` 中修改即可切换不同 AI 服务商：

```bash
# DeepSeek（推荐，性价比高）
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-chat

# OpenAI
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o

# 云雾 AI（聚合平台）
OPENAI_BASE_URL=https://yunwu.ai/v1
OPENAI_MODEL=gemini-2.5-pro-preview-03-25
```

### 自定义 AI 提示词

编辑 `config/rewrite-prompt.md` 可自定义 AI 改写的风格、输出结构和质量要求。

---

## 📂 项目结构

```
content-curation/
├── config/
│   ├── .env.example          # API 配置模板
│   ├── sources.yaml          # 订阅源
│   └── rewrite-prompt.md     # AI 提示词
├── scripts/
│   ├── fetch.py              # 抓取 + 转录 + 归档
│   ├── rewrite.js            # AI 改写
│   ├── sync-feishu.js        # 飞书多维表格同步
│   └── sync-feishu-doc.js    # 飞书文档同步（长文阅读视图）
├── blog/
│   ├── app.py                # Flask 博客
│   ├── config.py
│   ├── templates/
│   └── static/
├── archive/                  # 归档输出
├── run.sh                    # 统一入口
├── requirements.txt
└── package.json
```

---

## 📄 License

MIT
