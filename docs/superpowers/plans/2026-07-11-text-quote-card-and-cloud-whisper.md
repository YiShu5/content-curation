# 文字金句卡 + 云端 Whisper 实施计划

对应 spec：`docs/superpowers/specs/2026-07-11-text-quote-card-and-cloud-whisper-design.md`

## 任务拆解

```
U1 blog/text_card.py：纯函数搬家（font_size_for/normalize_quote/resolve_attribution）
   + 文字卡 overlay HTML + Chrome 渲染函数；make_quote_shots.py 改为反向 import
U2 app.py 路由 /article/<id>/quote-card.png?i=N（缓存键含金句 hash）
U3 detail.html 金句按钮 + 弹层预览 + 复制文字版 + share_card 埋点
   （preferences.json event_weights 同一提交）
U4 fetch.py：get_transcript_groq + 顺序调整 + 去两处 android client 遗留
U5 测试：test_text_card.py（纯函数/路由/缓存键）+ test_fetch_dedup 补 groq
   通道打桩用例；全量回归
U6 evaluator 挑刺 → 修复 → code-review（≤3 轮）→ PR → merge → deploy 验证
```

执行顺序：U1→U2→U3 串行（同链路）；U4 独立可交错；U5/U6 收尾。
单分支 `feat/text-quote-card`，不再并行 worktree（改动集中、无文件冲突面）。

## 依赖用户的事项

- **GROQ_API_KEY**：注册 console.groq.com → key 放 `config/.env`（`GROQ_API_KEY=gsk_...`）。
  没 key 前 Groq 通道自动跳过，链路照常（字幕API → BibiGPT → 本地）。

## 风险与对策

- Chrome 渲染进请求路径：30s 超时 + 503 兜底；缓存命中率高（同卡只渲一次）。
- 纯函数搬家可能破坏帧版 CLI：test_quote_card.py 全量回归钉住。
- Groq segments 时间戳格式差异：verbose_json 的 start 秒数直接换算，测试用真实响应形状打桩。

## 已拍板（2026-07-11）

- 金句卡 = 纯文字设计卡 + 详情页按钮：确认。
- core_ideas 一键复制：留下期。
- 转录云端优先、本地最兜底：确认方向；Groq 通道以 env 开关落地。
