# 文字金句卡 + 云端 Whisper 转录 设计（场景串联第二期）

## 目标

用户已明确场景为「个人 + 公司同事看懂内容要点」，非对外发布：

1. 金句卡改为**纯文字设计卡**（无视频帧），入口放在详情页金句区——点按钮即出，可下载 PNG 或复制文字版发给同事。彻底绕开视频下载/反爬/cookies 问题。
2. 转录链贯彻「云端优先、花钱可接受、本地最最兜底」：新增 **Groq Whisper 云端转录**（$0.04/小时音频，2 小时播客约 8 美分），whisper 本地挪到最后。

## A. 文字金句卡

### 形态

- 1280×720 PNG：深色渐变设计底（无视频帧），金句「」大字 + 署名（guest_info→guests→uploader 降级链）+ 底部小字（内容中文标题 · 平台 · 降噪 NoiseFilter）。
- 排版复用 make_quote_shots.py 已验证的纯函数：`font_size_for` 字号阶梯、`normalize_quote` 归一化、`resolve_attribution` 署名链、HTML 转义、`text-wrap: balance`。

### 入口与交互

- detail.html 金句区每条金句旁加「金句卡」按钮：点击 → 弹层预览 `<img>` + 「下载 PNG」+「复制文字版」。
- 复制文字版格式：`「金句」\n— 署名\n《中文标题》· 平台`（零后端成本，纯前端拼接）。
- 埋点：新增 kind=`share_card`（event_weights 加 1.5，同一提交）。

### 后端

- 渲染逻辑放独立模块 `blog/text_card.py`（不 import numpy/embeddings——文字卡不需要语义定位，避免把重依赖拖进请求路径）；make_quote_shots.py 的三个纯函数**搬家**到 text_card.py，make_quote_shots 反向 import（单一真相源，帧版 CLI 保留继续可用）。
- 路由 `GET /article/<record_id>/quote-card.png?i=<index>`：按（记录、index、金句文本 hash）缓存到 `blog/data/quote_cards/`，命中直接 send_file；未命中同步渲染（headless Chrome 1-2 秒，单人使用可接受）后 send_file。金句文本 hash 进缓存键——select-quotes 重排后不出旧卡。
- 越界 index / 无金句 / 记录不存在 → 404；Chrome 缺失 → 503 + 明确文案。
- Chrome 渲染在请求内同步执行，加 30s 超时；临时 html 渲染成功即删。

## B. 云端 Whisper（Groq）

### 通道实现

- fetch.py 新增 `get_transcript_groq(url, video_id)`：
  1. 音频下载复用 whisper 路径的缓存目录（`~/.cache/whisper-cpp/jobs/{key}.*`，已下过不重下）；下载命令**去掉遗留的 `youtube:player_client=android`**（whisper 路径同步去掉——全局 yt-dlp 配置已有 js-runtimes 药方）
  2. ffmpeg 转 16kHz 单声道 mp3 32kbps（2 小时 ≈ 28MB，稳在 Groq 文件上限内）
  3. POST Groq `audio/transcriptions`（model=whisper-large-v3-turbo，response_format=verbose_json），从 segments 拼 `[HH:MM:SS] text` 行——与其他通道同格式，时间戳深链/信号匹配不受影响
  4. `GROQ_API_KEY` 不存在则直接 raise（跳到下一通道）；走系统代理（海外 API，默认 session）
- 转录顺序调整（process_item）：字幕API（baoyu→ytapi，免费云）→ **groq（音频下载+云转录，几分钱）** → **bibigpt（全托管付费云，本地下载被拦时的接棒者）** → whisper 本地（最最兜底）。
- 密钥：`config/.env` 加 `GROQ_API_KEY`（用户注册 https://console.groq.com 获取，有免费额度）。

### 为什么 Groq 排在 BibiGPT 前

Groq $0.04/小时 vs BibiGPT 按时长计费更贵；Groq 失败（音频下载被反爬拦/文件超限/无 key）时快速失败落到 BibiGPT，链路不断。

## 测试与约束

- 沿用仓库测试惯例；text_card 纯函数直接测，路由用 test_client + 打桩 Chrome 渲染；Groq 通道打桩 requests（触达真实 API 即测试失败），验证 segments→时间戳行的拼装与无 key 时的快速失败。
- 不碰真实 archive/blog/data；金句卡渲染的人工验收用真实记录跑一次（无需联网——文字卡零下载）。
- CLAUDE.md 转录一节同步更新顺序描述。

## 非目标

- 不做 core_ideas 展示/复制（用户拍板留下期）。
- 不做帧版金句卡的 UI 接入（CLI 保留，发布场景用）。
- 不做飞书文档按钮、周报（下期）。
- 不动 BibiGPT 通道实现。
