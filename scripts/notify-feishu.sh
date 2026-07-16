#!/bin/bash
# 发一条文本消息到飞书群「自定义机器人」。
# 未配置 webhook 时静默退出（码 0），因此任何流程都可以无条件调用它。
#
# config/.env：
#   FEISHU_BOT_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxxx
#   FEISHU_BOT_SECRET=   # 可选：机器人开启「签名校验」时填
set -euo pipefail
cd "$(dirname "$0")/.."
TEXT="${1:?用法: notify-feishu.sh <消息文本>}"

WEBHOOK=$(grep -E '^FEISHU_BOT_WEBHOOK=' config/.env 2>/dev/null | head -1 | cut -d= -f2- || true)
SECRET=$(grep -E '^FEISHU_BOT_SECRET=' config/.env 2>/dev/null | head -1 | cut -d= -f2- || true)
[ -z "$WEBHOOK" ] && exit 0

if [ -n "$SECRET" ]; then
  TS=$(date +%s)
  # 飞书签名规范：key = timestamp + "\n" + secret，对空串做 HMAC-SHA256 再 base64
  SIGN=$(printf '' | openssl dgst -sha256 -hmac "$TS
$SECRET" -binary | base64)
  PAYLOAD=$(python3 -c 'import json,sys; print(json.dumps({"timestamp": sys.argv[1], "sign": sys.argv[2], "msg_type": "text", "content": {"text": sys.argv[3]}}))' "$TS" "$SIGN" "$TEXT")
else
  PAYLOAD=$(python3 -c 'import json,sys; print(json.dumps({"msg_type": "text", "content": {"text": sys.argv[1]}}))' "$TEXT")
fi

resp=$(curl -sS -m 10 -X POST -H 'Content-Type: application/json' -d "$PAYLOAD" "$WEBHOOK")
echo "$resp" | grep -q '"code":0' || { echo "[notify-feishu] 发送失败: $resp" >&2; exit 1; }
