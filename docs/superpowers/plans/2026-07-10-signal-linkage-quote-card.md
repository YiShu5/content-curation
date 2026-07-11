# 信号串联与金句卡参数化 实施计划

对应 spec：`docs/superpowers/specs/2026-07-10-signal-linkage-quote-card-design.md`

## 执行顺序与依据

```
T1 C提交1 legacy删除     ──┐ 先行：A 要在删完的 app.py 上加 filter，
                           │ 否则 C 的行号清单全部失效
T2 A 信号内链改站内       ──┤ 串行：A/B/C1 都改 app.py 或 _signals.html，
T3 B 入库闭环收尾         ──┘ 同文件不同区域，按序合入避免行号漂移
T4 C提交2 fetch去重+清理脚本   独立文件（fetch.py/scripts/），可与 T2/T3 交错
T5 D 金句卡参数化 CLI     ── 文件完全不相交 → 独立 worktree 并行开发
T6 集成：合并 T5 分支，全量回归
T7 提交链 + /code-review（≤3 轮 review-fix）
T8 PR + comments → 等用户确认 → merge
T9 E 环境迁移（合并后执行：.env / 根.venv / archive同步 / launchd 改指向）
T10 deploy 验证（重启 5055 实点页面）+ worktree 清理
```

## 每个任务的完成定义

每完成一项：evaluator agent 对照 spec 挑刺 → 修复 → 跑该项测试 + 全量回归 → 对抗压测用例全绿，才算 done。

- **T1**：删 app.py 三块/detail.html 死分支/config.py 五项，改 CLAUDE.md。验收：6 个测试文件全绿，重启 5055 实点首页/详情/封面。
- **T2**：quote_anchor filter + render_deep 宏改造 + detail.html 锚点/CSS/降级 JS + preferences.json 加 open_origin（同一提交）。更新 test_today_signal 现有断言，新增旧缓存兼容/无 quote/空 link 用例，test_app_routes 新增锚点用例。
- **T3**：archive_record_id helper + exists/done 双路径补 record_id + worker try/except + 前端按钮替换与轮询上限（1200 次）。test_ingest_jobs 新增 4 用例 + status 透传契约测试。
- **T4**：resolve_archive_dir（含 reused 标记，rmtree 只删本次新建；复用有效转录跳过转录链）+ cleanup_dup_archives.py（默认 dry-run、quarantine 移动、二次运行不覆盖）。新增 test_fetch_dedup.py（sys.modules 桩 yt_dlp，转录函数逐个按名打桩，bibigpt 触达即失败）。产出 dry-run 清单给用户。
- **T5**（worktree）：make_quote_shots.py 原地改造 + 删三个旧脚本 + test_quote_card.py（纯函数/降级链/缓存/fail-fast/对抗用例）。联网仅人工验收一次（挑已有 chunk 向量缓存的记录，避免额外 embed 调用）。
- **T7**：提交拆分——`refactor: remove legacy feishu read path`、`feat: signal in-site links with quote anchors`、`feat: ingest job returns record id`、`feat: fetch archive dedup + cleanup script`、`feat: parameterize quote card CLI`。
- **T9**：迁移五步见 spec；launchd plist 里显式写 node 绝对路径解决 `bash -lc` PATH 问题。

## 风险与对策

- **A/B/C1 行号漂移**：严格按 T1→T2→T3 串行，每步先跑测试再进下一步。
- **rmtree 误删付费转录**（spec 硬约束）：T4 的 evaluator 必须专项验证「复用目录 + fake rewrite 失败 → 目录仍在、transcript.md 字节不变」。
- **测试误触真实数据/付费 API**：全部 tempfile + 按名打桩；bibigpt 桩 raise；评审时 grep 测试文件确认无真实路径。
- **worktree 合并冲突**：T5 只动 make_quote_shots.py/三个删除文件/新测试文件，与主线零交集；合并前跑全量测试。
- **5055 正在后台跑旧代码**：deploy 验证时显式重启（debug reload 不可信）。

## 已拍板决策（2026-07-10）

- 四个工作项方案（含 rmtree 保护修正）：确认。
- 双副本：迁移到新路径，旧副本保留。
- 存量 72 冗余目录：先 dry-run 清单，`--apply` 等确认。
- 三个旧金句脚本：删除。
