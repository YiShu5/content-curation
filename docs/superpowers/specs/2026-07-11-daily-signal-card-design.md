# 今日 AI 判断日卡 设计（场景串联第三期）

## 目标

把首页「今日 AI 判断」压成一张横版分享图：同事扫一眼等于看完当天判断，
用户每天发进公司群——分享物每天自动产生，无需手写。

## 形态

- 横版 **1920×1080**，深色渐变底（与金句卡同设计语言）。
- 头部：降噪 NoiseFilter · 今日 AI 判断 · 日期（取信号缓存 generated_at）。
- 顶级大新闻（breaking）存在时加一条横幅：标题 + 一句总结 + 行动建议章
  （本周应该测试/值得持续关注/暂时知道即可）。
- 主体三栏并排，每栏 = 栏目标签 + 热点标题 + 一句总结 + why（产品人视角）；
  信号不足 3 条放几条是几条。
- 底部脚注。全字段 HTML 转义。

## 入口与交互

- `_signals.html` 面板头部动作区加「分享今日卡」按钮 → 弹层（独立 id `sc-modal`，
  与详情页 qc-modal 互不干扰）→ 预览 + 下载 PNG + 复制文字版。
- 文字版数据经 `<script type="application/json">` 块（tojson 转义防标签闭合注入）
  传给 JS 拼纯文本（头行 + breaking + 每条「▍栏目｜标题 / 总结 / → why」），
  复制走与金句卡相同的 clipboard+execCommand 降级。
- 埋点：复用 kind=`share_card`，source=`signals`（区分于详情页的 source=detail，
  event_weights 无需改动）。

## 后端

- `text_card.py`：渲染管线泛化——`run_chrome_screenshot` 加 size 参数；
  新增 `daily_card_html(payload, date_str)` 与 `render_daily_card(payload, out_png)`；
  金句卡沿用 1280×720，日卡 1920×1080。
- 路由 `GET /signal-card.png`：读 `today_signal.read_signal_cache()`，
  无缓存或空信号 404；缓存键 = generated_at + 信号/breaking item_id 摘要的 hash
  （一天正常只渲一次；手动 promote 改变 signals 时键随之失效，不出旧卡），
  产物存 `blog/data/quote_cards/dailycard-*.png`；`max_age=0`。
- 过期缓存（昨天的信号）照常出卡——用户可能晚发，卡上日期如实标注。

## 测试

- daily_card_html：三栏/breaking/转义/空 why 分支；render_daily_card 打桩 Chrome；
- 路由：打桩 read_signal_cache + render_daily_card，验证 404/503/缓存命中；
- 模板：render _signals.html 断言按钮与 data-copy 内容；
- 全量回归 10 个测试文件。

## 非目标

- 不做定时自动发送（发的动作留给人——这是场景的核心）。
- 不改信号生成逻辑。
