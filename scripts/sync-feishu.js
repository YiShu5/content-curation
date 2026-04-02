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

dotenv.config({ path: path.join(CONFIG_DIR, '.env') });

const ARCHIVE_DIR = path.join(PROJECT_ROOT, process.env.ARCHIVE_DIR || 'archive');

const FEISHU_BASE = 'https://open.feishu.cn';
const APP_ID = process.env.FEISHU_APP_ID;
const APP_SECRET = process.env.FEISHU_APP_SECRET;
const APP_TOKEN = process.env.FEISHU_APP_TOKEN;
const TABLE_ID = process.env.FEISHU_TABLE_ID;

// ── 带超时 + 限速重试的 fetch 封装 ──────────────────────────────────────────
async function feishuFetch(url, options = {}, { timeout = 30000, retries = 3 } = {}) {
  for (let attempt = 0; attempt < retries; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);
    try {
      const resp = await fetch(url, { ...options, signal: controller.signal });
      if (resp.status === 429) {
        const wait = (attempt + 1) * 3000;
        console.warn(`  [WARN] 飞书 API 频率限制，${wait / 1000}s 后重试...`);
        await new Promise(r => setTimeout(r, wait));
        continue;
      }
      return resp;
    } catch (err) {
      if (err.name === 'AbortError') throw new Error(`飞书 API 请求超时 (${timeout}ms): ${url}`);
      if (attempt === retries - 1) throw err;
      await new Promise(r => setTimeout(r, 1000));
    } finally {
      clearTimeout(timer);
    }
  }
  throw new Error('飞书 API 多次重试后仍失败');
}

// ── Token 管理 ─────────────────────────────────────────────────────────────
let _tokenCache = { token: '', expiry: 0 };

async function getAccessToken() {
  if (_tokenCache.token && Date.now() < _tokenCache.expiry - 60000) {
    return _tokenCache.token;
  }

  const resp = await feishuFetch(`${FEISHU_BASE}/open-apis/auth/v3/app_access_token/internal/`, {
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

    const ext = path.extname(imagePath).toLowerCase();
    const mimeMap = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };
    const mimeType = mimeMap[ext] || 'image/jpeg';

    const formData = new FormData();
    formData.append('file_name', fileName);
    formData.append('parent_type', 'bitable_image');
    formData.append('parent_node', APP_TOKEN);
    formData.append('size', String(fileSize));
    formData.append('file', new Blob([fileBuffer], { type: mimeType }), fileName);

    const resp = await feishuFetch(`${FEISHU_BASE}/open-apis/drive/v1/medias/upload_all`, {
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

// ── Markdown 纯文本提取 ────────────────────────────────────────────────────
function stripMarkdown(text) {
  if (!text) return '';
  return text
    .replace(/#{1,6}\s+/gm, '')           // 标题
    .replace(/\*\*(.+?)\*\*/gs, '$1')     // 粗体
    .replace(/\*(.+?)\*/gs, '$1')         // 斜体
    .replace(/`{3}[\s\S]*?`{3}/g, '')     // 代码块
    .replace(/`(.+?)`/g, '$1')            // 行内代码
    .replace(/^\s*[-*+]\s+/gm, '')        // 无序列表
    .replace(/^\s*\d+\.\s+/gm, '')        // 有序列表
    .replace(/\[(.+?)\]\(.+?\)/g, '$1')   // 链接
    .replace(/^>\s*/gm, '')               // 引用
    .replace(/^-{3,}$/gm, '')             // 分割线
    .replace(/\n{3,}/g, '\n\n')           // 多余空行
    .trim();
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
    '摘要纯文本': stripMarkdown(metadata.deep_summary),
  };

  if (metadata.topic) {
    record['话题'] = metadata.topic;
  }

  // 评分字段
  if (metadata.score_total != null) {
    record['总分'] = metadata.score_total;
    record['评级'] = metadata.score_verdict || '';
    const sc = metadata.scores || {};
    if (sc.ai_relevance?.score != null) record['AI相关性'] = sc.ai_relevance.score;
    if (sc.storytelling?.score != null) record['故事性'] = sc.storytelling.score;
    if (sc.bonus?.score != null) record['加分项'] = sc.bonus.score;
  }

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
  const resp = await feishuFetch(url, {
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

// ── 确保"摘要纯文本"字段存在 ──────────────────────────────────────────────
async function ensureSummaryTextField(token) {
  const url = `${FEISHU_BASE}/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields`;
  const resp = await feishuFetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const data = await resp.json();
  if (data.code !== 0) return;

  const exists = (data.data?.items || []).some(f => f.field_name === '摘要纯文本');
  if (exists) return;

  console.log('  创建字段：摘要纯文本...');
  const createResp = await feishuFetch(url, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ field_name: '摘要纯文本', type: 1 }),
  });
  const createData = await createResp.json();
  if (createData.code === 0) {
    console.log('  字段创建成功');
  } else {
    console.warn(`  [WARN] 字段创建失败: ${JSON.stringify(createData)}`);
  }
}

// ── 确保"话题"单选字段存在 ────────────────────────────────────────────────
const TOPIC_OPTIONS = ['AI 编程', 'AI 产品', 'AI 创业', 'AI 商业', '投资', '个人效率', '其他'];

async function ensureTopicField(token) {
  const url = `${FEISHU_BASE}/open-apis/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields`;
  const resp = await feishuFetch(url, { headers: { Authorization: `Bearer ${token}` } });
  const data = await resp.json();
  if (data.code !== 0) return;

  const exists = (data.data?.items || []).some(f => f.field_name === '话题');
  if (exists) return;

  console.log('  创建字段：话题（单选）...');
  const createResp = await feishuFetch(url, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      field_name: '话题',
      type: 3,  // 单选
      property: {
        options: TOPIC_OPTIONS.map(name => ({ name })),
      },
    }),
  });
  const createData = await createResp.json();
  if (createData.code === 0) {
    console.log('  话题字段创建成功');
  } else {
    console.warn(`  [WARN] 话题字段创建失败: ${JSON.stringify(createData)}`);
  }
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

  // 确保字段存在
  try {
    await ensureSummaryTextField(token);
    await ensureTopicField(token);
  } catch (err) {
    console.warn(`  [WARN] 检查字段失败: ${err.message}`);
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
