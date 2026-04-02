#!/usr/bin/env node
/**
 * 每日内容策展 - 飞书文档同步脚本
 * 将处理好的内容创建为飞书文档（Docx），比多维表格更适合长文阅读
 *
 * 用法:
 *   node scripts/sync-feishu-doc.js                  # 扫描 archive/ 中所有未同步的条目
 *   node scripts/sync-feishu-doc.js <archive_dir>    # 同步指定目录
 *
 * 需要在 config/.env 中配置：
 *   FEISHU_APP_ID / FEISHU_APP_SECRET（与多维表格共用）
 *   FEISHU_DOC_FOLDER_TOKEN（可选，文档存放的云文件夹 token）
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
const FOLDER_TOKEN = process.env.FEISHU_DOC_FOLDER_TOKEN || '';

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
  if (data.code !== 0) throw new Error(`飞书 Token 获取失败: ${JSON.stringify(data)}`);
  _tokenCache = { token: data.app_access_token, expiry: Date.now() + data.expire * 1000 };
  return _tokenCache.token;
}

// ── Feishu Docx Block 构建器 ───────────────────────────────────────────────
// 飞书文档 block_type 对应关系（参考飞书开放平台文档）：
//   2  = 普通文本段落（text）
//   3  = 一级标题（heading1）
//   4  = 二级标题（heading2）
//   5  = 三级标题（heading3）
//   12 = 无序列表项（bullet）
//   15 = 引用块（quote）
//   22 = 分割线（divider）

function makeTextRun(content, { bold = false, italic = false, link = '' } = {}) {
  const run = { type: 'text_run', text_run: { content: String(content) } };
  const style = {};
  if (bold) style.bold = true;
  if (italic) style.italic = true;
  if (link) style.link = { url: encodeURI(link) };
  if (Object.keys(style).length) run.text_run.text_element_style = style;
  return run;
}

function makeBlock(blockType, key, elements) {
  // 飞书 API 不接受空 style 对象，只传 elements
  return { block_type: blockType, [key]: { elements } };
}

const h1 = (text) => makeBlock(3, 'heading1', [makeTextRun(text)]);
const h2 = (text) => makeBlock(4, 'heading2', [makeTextRun(text)]);
const h3 = (text) => makeBlock(5, 'heading3', [makeTextRun(text)]);
const para = (elements) => makeBlock(2, 'text', Array.isArray(elements) ? elements : [makeTextRun(elements)]);
const bulletItem = (elements) => makeBlock(12, 'bullet', Array.isArray(elements) ? elements : [makeTextRun(elements)]);
const orderedItem = (elements) => makeBlock(13, 'ordered', Array.isArray(elements) ? elements : [makeTextRun(elements)]);
const quoteBlock = (text) => makeBlock(15, 'quote', [makeTextRun(text, { italic: true })]);
const divider = () => ({ block_type: 22, divider: {} });

// 解析行内 markdown（**bold**、普通文本），返回 elements 数组
function parseInlineMarkdown(line) {
  const elements = [];
  // 匹配 **bold**
  const re = /(\*\*([^*]+)\*\*)/g;
  let lastIndex = 0;
  let match;
  while ((match = re.exec(line)) !== null) {
    if (match.index > lastIndex) {
      elements.push(makeTextRun(line.slice(lastIndex, match.index)));
    }
    elements.push(makeTextRun(match[2], { bold: true }));
    lastIndex = match.index + match[0].length;
  }
  if (lastIndex < line.length) {
    elements.push(makeTextRun(line.slice(lastIndex)));
  }
  return elements.length ? elements : [makeTextRun(line)];
}

// 将多行 markdown 字符串转换为 Feishu block 数组
function markdownToBlocks(markdown) {
  if (!markdown) return [];
  const blocks = [];
  const lines = markdown.split('\n');

  for (const raw of lines) {
    const line = raw.trimEnd();

    if (line.startsWith('### ')) {
      blocks.push(h3(line.slice(4).trim()));
    } else if (line.startsWith('## ')) {
      blocks.push(h2(line.slice(3).trim()));
    } else if (line.startsWith('# ')) {
      blocks.push(h1(line.slice(2).trim()));
    } else if (line.startsWith('> ')) {
      blocks.push(quoteBlock(line.slice(2).trim()));
    } else if (/^[-*] /.test(line)) {
      blocks.push(bulletItem(parseInlineMarkdown(line.slice(2).trim())));
    } else if (/^\d+\.\s/.test(line)) {
      const text = line.replace(/^\d+\.\s+/, '').trim();
      blocks.push(orderedItem(parseInlineMarkdown(text)));
    } else if (line.trim() === '---') {
      blocks.push(divider());
    } else if (line.trim() === '') {
      // 空行忽略，飞书文档用块分隔
    } else {
      blocks.push(para(parseInlineMarkdown(line.trim())));
    }
  }

  return blocks;
}

// ── 构建完整文档内容 ───────────────────────────────────────────────────────
function buildDocumentBlocks(metadata) {
  const blocks = [];

  const PLATFORM_LABEL = {
    youtube: 'YouTube', bilibili: 'Bilibili',
    xiaoyuzhou: '小宇宙', audio: '音频',
  };
  const platformLabel = PLATFORM_LABEL[metadata.platform] || metadata.platform;

  const ud = metadata.upload_date || '';
  const dateStr = ud.length >= 8
    ? `${ud.slice(0, 4)}-${ud.slice(4, 6)}-${ud.slice(6, 8)}`
    : (ud || '未知');
  const durationMin = Math.round((metadata.duration || 0) / 60);

  // ── 评分卡片（如有）
  const sc = metadata.scores;
  if (sc && sc.total != null) {
    const verdictMap = { '必读': '🔥', '强烈推荐': '⭐⭐⭐', '推荐': '⭐⭐', '一般': '⭐', '可跳过': '—' };
    const icon = verdictMap[sc.verdict] || '';
    blocks.push(para([
      makeTextRun(`综合评分  ${sc.total}/100　${icon} ${sc.verdict || ''}`, { bold: true }),
    ]));
    const dims = [
      { label: 'AI 相关性', data: sc.ai_relevance, max: 40 },
      { label: '故事性',   data: sc.storytelling,  max: 30 },
      { label: '加分项',   data: sc.bonus,          max: 30 },
    ];
    for (const d of dims) {
      const score = d.data?.score ?? '—';
      const reason = d.data?.reason || '';
      const items = d.label === '加分项' && d.data?.items?.length
        ? `  [${d.data.items.join('、')}]` : '';
      blocks.push(bulletItem([
        makeTextRun(`${d.label}  `, { bold: true }),
        makeTextRun(`${score}/${d.max}　${reason}${items}`),
      ]));
    }
    blocks.push(divider());
  }

  // ── 元信息区
  blocks.push(para([makeTextRun('来源平台：', { bold: true }), makeTextRun(platformLabel)]));
  blocks.push(para([makeTextRun('创作者：', { bold: true }), makeTextRun(metadata.uploader || '未知')]));
  blocks.push(para([makeTextRun('发布日期：', { bold: true }), makeTextRun(dateStr)]));
  blocks.push(para([makeTextRun('时长：', { bold: true }), makeTextRun(`约 ${durationMin} 分钟`)]));
  blocks.push(para([makeTextRun('原标题：', { bold: true }), makeTextRun(metadata.title || '')]));
  if (metadata.url) {
    blocks.push(para([
      makeTextRun('原始链接：', { bold: true }),
      makeTextRun(metadata.url, { link: metadata.url }),
    ]));
  }
  blocks.push(divider());

  // ── 嘉宾
  const guests = metadata.guests || [];
  if (guests.length > 0) {
    blocks.push(h2('嘉宾'));
    for (const g of guests) {
      blocks.push(bulletItem(g));
    }
  }

  // ── 金句
  const quotes = metadata.key_quotes || [];
  if (quotes.length > 0) {
    blocks.push(h2('金句'));
    for (const q of quotes) {
      blocks.push(quoteBlock(q));
    }
  }

  // ── 核心观点
  const ideas = metadata.core_ideas || [];
  if (ideas.length > 0) {
    blocks.push(h2('核心观点'));
    for (const idea of ideas) {
      blocks.push(bulletItem(parseInlineMarkdown(idea)));
    }
  }

  blocks.push(divider());

  // ── 关键洞察（含 markdown 结构）
  if (metadata.key_insights) {
    blocks.push(h2('关键洞察'));
    blocks.push(...markdownToBlocks(metadata.key_insights));
  }

  blocks.push(divider());

  // ── 深度摘要（含 markdown 结构）
  if (metadata.deep_summary) {
    blocks.push(h2('深度摘要'));
    blocks.push(...markdownToBlocks(metadata.deep_summary));
  }

  return blocks;
}

// ── Feishu Docx API 调用 ───────────────────────────────────────────────────

async function createDocument(token, title) {
  const body = { title };
  if (FOLDER_TOKEN) body.folder_token = FOLDER_TOKEN;

  const resp = await feishuFetch(`${FEISHU_BASE}/open-apis/docx/v1/documents`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`创建飞书文档失败: ${JSON.stringify(data)}`);
  return data.data.document; // { document_id, ... }
}

async function getRootBlockId(token, documentId) {
  const resp = await feishuFetch(
    `${FEISHU_BASE}/open-apis/docx/v1/documents/${documentId}/blocks?page_size=1`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`获取文档结构失败: ${JSON.stringify(data)}`);
  // 根页面 block_type === 1
  const root = (data.data.items || []).find(b => b.block_type === 1);
  if (!root) throw new Error('找不到文档根块（page block）');
  return root.block_id;
}

async function appendBlocksToDocument(token, documentId, rootBlockId, blocks) {
  // 飞书 API 单次最多写入 50 个 block
  const BATCH = 50;
  let insertIndex = 0;

  for (let i = 0; i < blocks.length; i += BATCH) {
    const batch = blocks.slice(i, i + BATCH);
    const resp = await feishuFetch(
      `${FEISHU_BASE}/open-apis/docx/v1/documents/${documentId}/blocks/${rootBlockId}/children`,
      {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ children: batch, index: insertIndex }),
      }
    );
    const data = await resp.json();
    if (data.code !== 0) throw new Error(`写入文档块失败 (batch ${i / BATCH + 1}): ${JSON.stringify(data)}`);
    insertIndex += batch.length;
  }
}

// ── 扫描 / 标记 ────────────────────────────────────────────────────────────

function scanUnsyncedItems() {
  if (!fs.existsSync(ARCHIVE_DIR)) return [];

  return fs
    .readdirSync(ARCHIVE_DIR)
    .filter(name => {
      const p = path.join(ARCHIVE_DIR, name);
      return fs.statSync(p).isDirectory() && /^\d{8}-/.test(name);
    })
    .sort()
    .flatMap(dir => {
      const metaPath = path.join(ARCHIVE_DIR, dir, 'metadata.json');
      if (!fs.existsSync(metaPath)) return [];
      try {
        const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
        if (meta.rewrite_complete && !meta.feishu_doc_synced) {
          return [{ dir: path.join(ARCHIVE_DIR, dir), metadata: meta }];
        }
      } catch {}
      return [];
    });
}

function markSynced(archiveDir, docId, docUrl) {
  const metaPath = path.join(archiveDir, 'metadata.json');
  const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
  Object.assign(meta, {
    feishu_doc_synced: true,
    feishu_doc_id: docId,
    feishu_doc_url: docUrl,
    feishu_doc_synced_at: new Date().toISOString(),
  });
  fs.writeFileSync(metaPath, JSON.stringify(meta, null, 2), 'utf-8');
}

// ── 主函数 ────────────────────────────────────────────────────────────────
async function main() {
  if (!APP_ID || APP_ID === 'cli_xxxxxxxxxxxxxxxxxx') {
    console.error('[ERROR] 飞书配置未填写，请在 config/.env 中设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET');
    process.exit(1);
  }

  let items;
  const targetDir = process.argv[2];

  if (targetDir) {
    const resolvedDir = path.resolve(targetDir);
    const metaPath = path.join(resolvedDir, 'metadata.json');
    if (!fs.existsSync(metaPath)) {
      console.error(`[ERROR] 找不到 metadata.json: ${metaPath}`);
      process.exit(1);
    }
    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
    items = [{ dir: resolvedDir, metadata: meta }];
  } else {
    items = scanUnsyncedItems();
  }

  if (items.length === 0) {
    console.log('没有需要同步到飞书文档的条目（已全部同步或尚无完成改写的内容）。');
    return;
  }

  console.log(`找到 ${items.length} 条待同步内容\n`);

  let token = await getAccessToken();
  let ok = 0, fail = 0;

  for (const { dir, metadata } of items) {
    const title = metadata.chinese_title || metadata.title;
    console.log(`同步: ${title.slice(0, 60)}`);

    try {
      token = await getAccessToken();

      // 1. 创建空文档
      console.log('  创建飞书文档...');
      const doc = await createDocument(token, title);
      const docId = doc.document_id;
      const docUrl = `https://feishu.cn/docx/${docId}`;
      console.log(`  文档已创建: ${docUrl}`);

      // 2. 获取根块 ID
      const rootBlockId = await getRootBlockId(token, docId);

      // 3. 构建并写入所有内容块
      console.log('  写入内容块...');
      const blocks = buildDocumentBlocks(metadata);
      await appendBlocksToDocument(token, docId, rootBlockId, blocks);

      // 4. 标记同步完成
      markSynced(dir, docId, docUrl);
      console.log(`  [OK] 完成，共 ${blocks.length} 个块 → ${docUrl}`);
      ok++;

    } catch (err) {
      console.error(`  [ERROR] ${err.message}`);
      fail++;
    }
  }

  console.log(`\n同步完成：成功 ${ok}，失败 ${fail}`);
}

main();
