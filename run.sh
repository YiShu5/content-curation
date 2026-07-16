#!/usr/bin/env bash
# 每日内容策展工作流 - 统一入口
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

usage() {
  echo ""
  echo "用法: ./run.sh <命令> [选项]"
  echo ""
  echo "命令:"
  echo "  auto [--limit N]         【定时任务用】全自动：抓取→改写→同步，无需人工干预"
  echo "  batch [--limit N]        扫描所有订阅源，列出新内容供交互选择"
  echo "  url <URL> [URL2 ...]     直接处理指定 URL，无需确认"
  echo "  rewrite <archive_dir>    对已归档内容重新运行 AI 改写"
  echo "  sync                     将已改写但未同步的内容推送到飞书多维表格"
  echo "  sync-doc [archive_dir]   将已改写内容创建为飞书文档（长文阅读视图）"
  echo "  all [--limit N]          执行 batch（交互），完成后同步多维表格 + 飞书文档"
  echo "  embed                    构建语义搜索向量索引（智谱 embedding-3）"
  echo "  signals                  后台生成「今日必读」缓存（网页只读）"
  echo "  publish-daily            【每日定时】带闸门自动发布今日简报（配合 signals）"
  echo "  enrich-guests [--force]  为已归档内容生成嘉宾介绍（头衔/背景/本期角色）"
  echo "  select-quotes [--n 3]    从已有金句中精选最精华的 N 条"
  echo "  refresh                  新归档后一把补全：嘉宾+金句精选+索引+今日必读"
  echo "  daily [--limit N]        【每日定时】抓取→补全→索引→今日必读（不同步飞书）"
  echo ""
  echo "示例:"
  echo "  ./run.sh auto                         # 每日定时任务用这个"
  echo "  ./run.sh auto --limit 3"
  echo "  ./run.sh batch"
  echo "  ./run.sh url https://www.youtube.com/watch?v=xxxxxxx"
  echo "  ./run.sh sync"
  echo ""
}

CMD="${1:-}"
shift || true

case "$CMD" in
  auto)
    echo "=== [自动模式] $(date '+%Y-%m-%d %H:%M:%S') 开始 ==="
    python scripts/fetch.py --batch --auto "$@"
    echo ""
    echo "--- 同步到飞书多维表格 ---"
    node scripts/sync-feishu.js
    echo ""
    echo "--- 同步到飞书文档 ---"
    node scripts/sync-feishu-doc.js
    echo ""
    echo "=== 完成 $(date '+%Y-%m-%d %H:%M:%S') ==="
    ;;
  batch)
    python scripts/fetch.py --batch "$@"
    ;;
  url)
    if [ $# -eq 0 ]; then
      echo "[ERROR] 请提供至少一个 URL"
      usage
      exit 1
    fi
    python scripts/fetch.py --url "$@"
    ;;
  rewrite)
    if [ $# -eq 0 ]; then
      echo "[ERROR] 请提供归档目录路径"
      usage
      exit 1
    fi
    node scripts/rewrite.js "$@"
    ;;
  sync)
    node scripts/sync-feishu.js
    ;;
  sync-doc)
    node scripts/sync-feishu-doc.js "$@"
    ;;
  embed)
    # 优先用博客 venv（已装 numpy/flask 等），否则退回系统 python
    if [ -x "blog/.venv/bin/python" ]; then
      blog/.venv/bin/python blog/embeddings.py build
    else
      python blog/embeddings.py build
    fi
    ;;
  signals)
    # 后台生成「今日必读」缓存（网页只读它，不阻塞）
    if [ -x "blog/.venv/bin/python" ]; then
      blog/.venv/bin/python blog/today_signal.py
    else
      python blog/today_signal.py
    fi
    ;;
  publish-daily)
    # 带闸门自动发布今日简报：闸门不过宁可不发（先跑 signals 生成草稿）
    if [ -x "blog/.venv/bin/python" ]; then
      blog/.venv/bin/python blog/auto_publish.py
    else
      python blog/auto_publish.py
    fi
    ;;
  enrich-guests)
    # 为已归档内容生成嘉宾介绍（头衔/背景/本期角色）
    if [ -x ".venv/bin/python" ]; then
      .venv/bin/python scripts/enrich-guests.py "$@"
    else
      python scripts/enrich-guests.py "$@"
    fi
    ;;
  select-quotes)
    # 从已有金句中精选最精华的 N 条（默认 3）
    if [ -x ".venv/bin/python" ]; then
      .venv/bin/python scripts/select-quotes.py "$@"
    else
      python scripts/select-quotes.py "$@"
    fi
    ;;
  refresh)
    # 新归档后一把补全：嘉宾卡 → 金句精选 → 重建向量索引 → 生成今日必读
    .venv/bin/python scripts/enrich-guests.py || true
    .venv/bin/python scripts/select-quotes.py --n 3 || true
    blog/.venv/bin/python blog/embeddings.py build
    blog/.venv/bin/python blog/today_signal.py
    ;;
  daily)
    # 每日定时用：抓白名单新内容 → 补全 → 索引 → 今日必读
    # （博客已改为读本地 archive，不再同步飞书，避免重复记录）
    echo "=== [每日] $(date '+%Y-%m-%d %H:%M:%S') 开始 ==="
    .venv/bin/python scripts/fetch.py --batch --auto "$@" || true
    .venv/bin/python scripts/enrich-guests.py || true
    .venv/bin/python scripts/select-quotes.py --n 3 || true
    blog/.venv/bin/python blog/embeddings.py build || true
    blog/.venv/bin/python blog/today_signal.py || true
    echo "=== [每日] 完成 $(date '+%Y-%m-%d %H:%M:%S') ==="
    ;;
  all)
    python scripts/fetch.py --batch --auto "$@"
    echo ""
    echo "批量处理完成，开始同步到飞书多维表格..."
    echo ""
    node scripts/sync-feishu.js
    echo ""
    echo "开始同步到飞书文档..."
    echo ""
    node scripts/sync-feishu-doc.js
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "[ERROR] 未知命令: '${CMD}'"
    usage
    exit 1
    ;;
esac
