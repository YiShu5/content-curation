#!/bin/bash
# 把本地策展成果同步到线上服务器：archive（真相源）+ 向量索引 + 转录分块缓存。
# 本地是唯一真相源，服务器是镜像；每日简报数据（daily_issues）在服务器原生产生，不在此列。
#
# 配置写在 config/.env：
#   DEPLOY_SSH_HOST=user@your-server        # SSH 目标（建议用 ~/.ssh/config 里的别名）
#   DEPLOY_REMOTE_DIR=/srv/content-curation # 服务器上的项目根目录
set -euo pipefail
cd "$(dirname "$0")/.."

DEPLOY_SSH_HOST=$(grep -E '^DEPLOY_SSH_HOST=' config/.env | head -1 | cut -d= -f2-)
DEPLOY_REMOTE_DIR=$(grep -E '^DEPLOY_REMOTE_DIR=' config/.env | head -1 | cut -d= -f2-)
: "${DEPLOY_SSH_HOST:?config/.env 缺 DEPLOY_SSH_HOST}"
: "${DEPLOY_REMOTE_DIR:?config/.env 缺 DEPLOY_REMOTE_DIR}"

# 防呆闸门：本地 archive 异常（如被误删）时拒绝镜像，避免 --delete 把服务器也清空
complete_count=$(grep -l '"rewrite_complete": true' archive/*/metadata.json 2>/dev/null | wc -l | tr -d ' ')
if [ "$complete_count" -lt 5 ]; then
  echo "[deploy-content] 本地成品仅 $complete_count 条（<5），疑似 archive 异常，拒绝同步" >&2
  exit 1
fi

echo "[deploy-content] 同步 archive（$complete_count 条成品）→ $DEPLOY_SSH_HOST:$DEPLOY_REMOTE_DIR"
rsync -az --delete \
  --exclude '_duplicates_quarantine' \
  archive/ "$DEPLOY_SSH_HOST:$DEPLOY_REMOTE_DIR/archive/"

rsync -az blog/data/embeddings.json "$DEPLOY_SSH_HOST:$DEPLOY_REMOTE_DIR/blog/data/embeddings.json"

if [ -d blog/data/transcript_chunks ]; then
  rsync -az blog/data/transcript_chunks/ "$DEPLOY_SSH_HOST:$DEPLOY_REMOTE_DIR/blog/data/transcript_chunks/"
fi

echo "[deploy-content] 完成"
