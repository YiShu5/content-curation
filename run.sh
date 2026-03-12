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
  echo "  batch [--limit N]        扫描所有订阅源，列出新内容供选择处理（默认5条/源）"
  echo "  url <URL> [URL2 ...]     直接处理指定 URL，无需确认"
  echo "  rewrite <archive_dir>    对已归档内容重新运行 AI 改写"
  echo "  sync                     将已改写但未同步的内容推送到飞书多维表格"
  echo "  all [--limit N]          执行 batch，完成后自动执行 sync"
  echo ""
  echo "示例:"
  echo "  ./run.sh batch"
  echo "  ./run.sh batch --limit 10"
  echo "  ./run.sh url https://www.youtube.com/watch?v=xxxxxxx"
  echo "  ./run.sh rewrite archive/20260312-some-title"
  echo "  ./run.sh sync"
  echo "  ./run.sh all --limit 3"
  echo ""
}

CMD="${1:-}"
shift || true

case "$CMD" in
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
  all)
    python scripts/fetch.py --batch "$@"
    echo ""
    echo "批量处理完成，开始同步到飞书..."
    echo ""
    node scripts/sync-feishu.js
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
