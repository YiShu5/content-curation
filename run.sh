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
