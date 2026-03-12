#!/usr/bin/env node
/**
 * 每日内容策展 - 飞书多维表格同步脚本
 * 用法: node scripts/sync-feishu.js
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import * as dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, '..');
const CONFIG_DIR = path.join(PROJECT_ROOT, 'config');
const ARCHIVE_DIR = path.join(PROJECT_ROOT, process.env.ARCHIVE_DIR || 'archive');

dotenv.config({ path: path.join(CONFIG_DIR, '.env') });

const FEISHU_BASE = 'https://open.feishu.cn';
const APP_ID = process.env.FEISHU_APP_ID;
const APP_SECRET = process.env.FEISHU_APP_SECRET;
const APP_TOKEN = process.env.FEISHU_APP_TOKEN;
const TABLE_ID = process.env.FEISHU_TABLE_ID;

// ── Token 管理 ─────────────────────────────────────────────────────────────
let _tokenCache = { token: '', expiry: 0 };

async function getAccessToken() {
  // Refresh if token expires within 60s
  if (_tokenCache.token && Date.now() < _tokenCache.expiry - 60000) {
    return _tokenCache.token;
  }

  const resp = await fetch(`${FEISHU_BASE}/open-apis/auth/v3/app_access_token/internal/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }),
  });
  const data = await resp.json();

  if (data.code !== 0) {
    throw new Error(`飞书 Token 获取失败: ${JSON.stringify(data)}`);
  }

  _tokenCache = {
    token: data.app_access_token,
    expiry: Date.now() + data.expire * 1000,
  };
  return _tokenCache.token;
}

// ── 工具函数 ──────────────────────────────────────────────────────────────
function feishuTimestamp(yyyymmdd) {
  if (!yyyymmdd || yyyymmdd.length < 8) return null;
  const y = yyyymmdd.slice(0, 4);
  const m = yyyymmdd.slice(4, 6);
  const d = yyyymmdd.slice(6, 8);
  return new Date(`${y}-${m}-${d}T00:00:00Z`).getTime();
}

function findCoverFile(archiveDir) {
  for (const ext of ['cover.jpg', 'cover.webp', 'cover.png']) {
    const p = path.join(archiveDir, ext);
    if (fs.existsSync(p)) return p;
  }
  return null;
}

// ── 封面上传 ──────────────────────────────────────────────────────────────
async function uploadCoverImage(token, imagePath) {
  if (!imagePath || !fs.existsSync(imagePath)) return null;

  try {
    const fileBuffer = fs.readFileSync(imagePath);
    const fileName = path.basename(imagePath);
    const fileSize = fileBuffer.length;

    const formData = new FormData();
    formData.append('file_name', fileName);
    formData.append('parent_type', 'bitable_image');
    formData.append('parent_node', APP_TOKEN);
    formData.append('size', String(fileSize));
    formData.append('file', new Blob([fileBuffer], { type: 'image/jpeg' }), fileName);

    const resp = await fetch(`${FEISHU_BASE}/open-apis/drive/v1/medias/upload_all`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });
    const data = await resp.json();

    if (data.code !== 0) {
      console.warn(`  [WARN] 封面上传失败: ${JSON.stringify(data)}`);
      return null;
    }
    return data.data?.file_token || null;
  } catch (err) {
    console.warn(`  [WARN] 封面上传异常: ${err.message}`);
    return null;
  }
}

// ── 构建表格记录 ───────────────────────────────────────────────────────────
function buildBitableRecord(metadata, fileToken) {
  const platformLabel = {
    youtube: 'YouTube',
    bilibili: 'Bilibili',
    xiaoyuzhou: '小宇宙',
    audio: '音频',
  }[metadata.platform] || metadata.platform;

  const record = {
    '标题': metadata.chinese_title || metadata.title,
    '原标题': metadata.title,
    '来源平台': platformLabel,
    '创作者': metadata.uploader,
    '原始链接': { link: metadata.url, text: metadata.title },
    '时长（分钟）': Math.round((metadata.duration || 0) / 60),
    '嘉宾': (metadata.guests || []).join('、'),
    '深度摘要': metadata.deep_summary || '',
  };

  // Date field (Feishu requires ms timestamp)
  const ts = feishuTimestamp(metadata.upload_date);
  if (ts) record['发布日期'] = ts;

  // Cover attachment
  if (fileToken) {
    record['封面'] = [{ file_token: fileToken }];
  }

  return record;
}

// ── 创建 Bitable 记录 ──────────────────────────────────────────────────────
async function createBitableRecord(token, fields) {
  const url = `${FEISHU_BASE}/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ fields }),
  });
  const data = await resp.json();

  if (data.code !== 0) {
    throw new Error(`创建 Bitable 记录失败: ${JSON.stringify(data)}`);
  }
  return data.data?.record?.record_id;
}

// ── 扫描未同步条目 ─────────────────────────────────────────────────────────
function scanUnsyncedItems() {
  if (!fs.existsSync(ARCHIVE_DIR)) return [];

  const dirs = fs.readdirSync(ARCHIVE_DIR).filter(name => {
    const p = path.join(ARCHIVE_DIR, name);
    return fs.statSync(p).isDirectory() && /^\d{8}-/.test(name);
  });

  const items = [];
  for (const dir of dirs.sort()) {
    const metaPath = path.join(ARCHIVE_DIR, dir, 'metadata.json');
    if (!fs.existsSync(metaPath)) continue;
    try {
      const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
      if (meta.rewrite_complete && !meta.feishu_synced) {
        items.push({ dir: path.join(ARCHIVE_DIR, dir), metadata: meta });
      }
    } catch {}
  }
  return items;
}

function markSynced(archiveDir, recordId) {
  const metaPath = path.join(archiveDir, 'metadata.json');
  const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
  meta.feishu_synced = true;
  meta.feishu_record_id = recordId;
  meta.feishu_synced_at = new Date().toISOString();
  fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2), 'utf-8');
}

// ── 主函数 ────────────────────────────────────────────────────────────────
async function main() {
  // Validate config
  if (!APP_ID || APP_ID === 'cli_xxxxxxxxxxxxxxxxxx') {
    console.error('[ERROR] 飞书配置未填写，请在 config/.env 中设置 FEISHU_APP_ID 等字段');
    process.exit(1);
  }

  const items = scanUnsyncedItems();
  if (items.length === 0) {
    console.log('没有需要同步到飞书的条目。');
    return;
  }

  console.log(`找到 ${items.length} 条待同步内容\n`);

  let token;
  try {
    console.log('获取飞书访问令牌...');
    token = await getAccessToken();
    console.log('令牌获取成功\n');
  } catch (err) {
    console.error(`[ERROR] ${err.message}`);
    process.exit(1);
  }

  let ok = 0, fail = 0;

  for (const { dir, metadata } of items) {
    const title = metadata.chinese_title || metadata.title;
    console.log(`同步: ${title.slice(0, 50)}`);

    try {
      // Refresh token if needed
      token = await getAccessToken();

      // Upload cover
      const coverPath = findCoverFile(dir);
      let fileToken = null;
      if (coverPath) {
        console.log('  上传封面...');
        fileToken = await uploadCoverImage(token, coverPath);
        if (fileToken) {
          console.log('  封面上传成功');
        }
      }

      // Build record
      const fields = buildBitableRecord(metadata, fileToken);

      // Create record
      console.log('  创建表格记录...');
      const recordId = await createBitableRecord(token, fields);
      markSynced(dir, recordId);
      console.log(`  [OK] 记录 ID: ${recordId}`);
      ok++;

    } catch (err) {
      console.error(`  [ERROR] ${err.message}`);
      fail++;
    }
  }

  console.log(`\n同步完成：成功 ${ok}，失败 ${fail}`);
}

main();
