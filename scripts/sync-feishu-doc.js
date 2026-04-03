#!/usr/bin/env node
/**
 * Daily content curation - sync rewritten content into Feishu Docs.
 *
 * Usage:
 *   node scripts/sync-feishu-doc.js
 *   node scripts/sync-feishu-doc.js <archive_dir>
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

async function feishuFetch(url, options = {}, { timeout = 30000, retries = 3 } = {}) {
  for (let attempt = 0; attempt < retries; attempt++) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeout);
    try {
      const resp = await fetch(url, { ...options, signal: controller.signal });
      const retryableStatus = resp.status === 429 || resp.status >= 500;
      if (retryableStatus) {
        const wait = (attempt + 1) * 3000;
        if (attempt === retries - 1) {
          const body = await resp.text().catch(() => '');
          throw new Error(`飞书 API 响应异常 (${resp.status}): ${body.slice(0, 200)}`);
        }
        console.warn(`  [WARN] 飞书 API 响应异常 (${resp.status})，${wait / 1000}s 后重试...`);
        await new Promise((resolve) => setTimeout(resolve, wait));
        continue;
      }
      return resp;
    } catch (err) {
      if (err.name === 'AbortError') {
        throw new Error(`飞书 API 请求超时 (${timeout}ms): ${url}`);
      }
      if (attempt === retries - 1) {
        throw err;
      }
      await new Promise((resolve) => setTimeout(resolve, 1000));
    } finally {
      clearTimeout(timer);
    }
  }
  throw new Error('飞书 API 多次重试后仍失败');
}

let tokenCache = { token: '', expiry: 0 };

async function getAccessToken() {
  if (tokenCache.token && Date.now() < tokenCache.expiry - 60000) {
    return tokenCache.token;
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

  tokenCache = {
    token: data.app_access_token,
    expiry: Date.now() + data.expire * 1000,
  };
  return tokenCache.token;
}

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

function parseInlineMarkdown(line) {
  const elements = [];
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
    } else if (line.trim() !== '') {
      blocks.push(para(parseInlineMarkdown(line.trim())));
    }
  }

  return blocks;
}

function buildDocumentBlocks(metadata) {
  const blocks = [];

  const platformLabel = {
    youtube: 'YouTube',
    bilibili: 'Bilibili',
    xiaoyuzhou: '小宇宙',
    audio: '音频',
  }[metadata.platform] || metadata.platform;

  const uploadDate = metadata.upload_date || '';
  const dateStr = uploadDate.length >= 8
    ? `${uploadDate.slice(0, 4)}-${uploadDate.slice(4, 6)}-${uploadDate.slice(6, 8)}`
    : (uploadDate || '未知');
  const durationMin = Math.round((metadata.duration || 0) / 60);

  const scores = metadata.scores;
  if (scores && scores.total != null) {
    const verdictMap = {
      '必读': '🔥',
      '强烈推荐': '⭐',
      '推荐': '👍',
      '一般': '👌',
      '可跳过': '·',
    };
    const icon = verdictMap[scores.verdict] || '';
    blocks.push(para([
      makeTextRun(`综合评分  ${scores.total}/100　${icon} ${scores.verdict || ''}`, { bold: true }),
    ]));

    const dims = [
      { label: 'AI 相关性', data: scores.ai_relevance, max: 40 },
      { label: '故事性', data: scores.storytelling, max: 30 },
      { label: '加分项', data: scores.bonus, max: 30 },
    ];

    for (const dim of dims) {
      const score = dim.data?.score ?? '—';
      const reason = dim.data?.reason || '';
      const items = dim.label === '加分项' && dim.data?.items?.length
        ? `  [${dim.data.items.join('、')}]`
        : '';
      blocks.push(bulletItem([
        makeTextRun(`${dim.label}  `, { bold: true }),
        makeTextRun(`${score}/${dim.max}　${reason}${items}`),
      ]));
    }

    blocks.push(divider());
  }

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

  const guests = metadata.guests || [];
  if (guests.length > 0) {
    blocks.push(h2('嘉宾'));
    for (const guest of guests) {
      blocks.push(bulletItem(guest));
    }
  }

  const quotes = metadata.key_quotes || [];
  if (quotes.length > 0) {
    blocks.push(h2('金句'));
    for (const quote of quotes) {
      blocks.push(quoteBlock(quote));
    }
  }

  const ideas = metadata.core_ideas || [];
  if (ideas.length > 0) {
    blocks.push(h2('核心观点'));
    for (const idea of ideas) {
      blocks.push(bulletItem(parseInlineMarkdown(idea)));
    }
  }

  blocks.push(divider());

  if (metadata.key_insights) {
    blocks.push(h2('关键洞察'));
    blocks.push(...markdownToBlocks(metadata.key_insights));
  }

  blocks.push(divider());

  if (metadata.deep_summary) {
    blocks.push(h2('深度摘要'));
    blocks.push(...markdownToBlocks(metadata.deep_summary));
  }

  return blocks;
}

async function createDocument(token, title) {
  const body = { title };
  if (FOLDER_TOKEN) body.folder_token = FOLDER_TOKEN;

  const resp = await feishuFetch(`${FEISHU_BASE}/open-apis/docx/v1/documents`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const data = await resp.json();

  if (data.code !== 0) {
    throw new Error(`创建飞书文档失败: ${JSON.stringify(data)}`);
  }

  return data.data.document;
}

async function getRootBlockId(token, documentId) {
  const resp = await feishuFetch(
    `${FEISHU_BASE}/open-apis/docx/v1/documents/${documentId}/blocks?page_size=1`,
    { headers: { Authorization: `Bearer ${token}` } },
  );
  const data = await resp.json();

  if (data.code !== 0) {
    throw new Error(`获取文档结构失败: ${JSON.stringify(data)}`);
  }

  const root = (data.data.items || []).find((item) => item.block_type === 1);
  if (!root) {
    throw new Error('找不到文档根块(page block)');
  }

  return root.block_id;
}

async function appendBlocksToDocument(token, documentId, rootBlockId, blocks, startIndex = 0, onBatchComplete = null) {
  const batchSize = 50;
  let insertIndex = startIndex;

  for (let i = startIndex; i < blocks.length; i += batchSize) {
    const batch = blocks.slice(i, i + batchSize);
    const resp = await feishuFetch(
      `${FEISHU_BASE}/open-apis/docx/v1/documents/${documentId}/blocks/${rootBlockId}/children`,
      {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ children: batch, index: insertIndex }),
      },
    );
    const data = await resp.json();

    if (data.code !== 0) {
      throw new Error(`写入文档块失败(batch ${Math.floor(i / batchSize) + 1}): ${JSON.stringify(data)}`);
    }

    insertIndex += batch.length;
    if (onBatchComplete) {
      await onBatchComplete(insertIndex);
    }
  }
}

function metadataPathFor(archiveDir) {
  return path.join(archiveDir, 'metadata.json');
}

function readMetadata(archiveDir) {
  return JSON.parse(fs.readFileSync(metadataPathFor(archiveDir), 'utf-8'));
}

function writeMetadata(archiveDir, meta) {
  fs.writeFileSync(metadataPathFor(archiveDir), JSON.stringify(meta, null, 2), 'utf-8');
}

function updateMetadata(archiveDir, patch) {
  const meta = readMetadata(archiveDir);
  Object.assign(meta, patch);
  writeMetadata(archiveDir, meta);
  return meta;
}

function scanUnsyncedItems() {
  if (!fs.existsSync(ARCHIVE_DIR)) return [];

  return fs
    .readdirSync(ARCHIVE_DIR)
    .filter((name) => {
      const fullPath = path.join(ARCHIVE_DIR, name);
      return fs.statSync(fullPath).isDirectory() && /^\d{8}-/.test(name);
    })
    .sort()
    .flatMap((dirName) => {
      const archiveDir = path.join(ARCHIVE_DIR, dirName);
      const metaPath = metadataPathFor(archiveDir);
      if (!fs.existsSync(metaPath)) return [];

      try {
        const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
        if (meta.rewrite_complete && !meta.feishu_doc_synced) {
          return [{ dir: archiveDir, metadata: meta }];
        }
      } catch {}
      return [];
    });
}

function markDocSyncStarted(archiveDir, docId, docUrl, totalBlocks) {
  updateMetadata(archiveDir, {
    feishu_doc_synced: false,
    feishu_doc_id: docId,
    feishu_doc_url: docUrl,
    feishu_doc_sync_started_at: new Date().toISOString(),
    feishu_doc_blocks_written: 0,
    feishu_doc_total_blocks: totalBlocks,
  });
}

function markDocSyncProgress(archiveDir, writtenCount, totalBlocks) {
  updateMetadata(archiveDir, {
    feishu_doc_blocks_written: writtenCount,
    feishu_doc_total_blocks: totalBlocks,
  });
}

function markSynced(archiveDir, docId, docUrl) {
  const meta = updateMetadata(archiveDir, {
    feishu_doc_synced: true,
    feishu_doc_id: docId,
    feishu_doc_url: docUrl,
    feishu_doc_synced_at: new Date().toISOString(),
  });
  delete meta.feishu_doc_sync_started_at;
  delete meta.feishu_doc_blocks_written;
  delete meta.feishu_doc_total_blocks;
  writeMetadata(archiveDir, meta);
}

async function main() {
  if (!APP_ID || APP_ID === 'cli_xxxxxxxxxxxxxxxxxx') {
    console.error('[ERROR] 飞书配置未填写，请检查 config/.env 中的 FEISHU_APP_ID 和 FEISHU_APP_SECRET');
    process.exit(1);
  }

  let items;
  const targetDir = process.argv[2];

  if (targetDir) {
    const resolvedDir = path.resolve(targetDir);
    const metaPath = metadataPathFor(resolvedDir);
    if (!fs.existsSync(metaPath)) {
      console.error(`[ERROR] 找不到 metadata.json: ${metaPath}`);
      process.exit(1);
    }

    const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));
    if (!meta.rewrite_complete) {
      console.error('[ERROR] 该条目尚未完成 AI 改写，无法同步到飞书文档');
      process.exit(1);
    }
    if (meta.feishu_doc_synced) {
      console.log('该条目已同步到飞书文档，无需重复创建');
      return;
    }

    items = [{ dir: resolvedDir, metadata: meta }];
  } else {
    items = scanUnsyncedItems();
  }

  if (items.length === 0) {
    console.log('没有需要同步到飞书文档的条目（可能已同步或尚未完成改写）');
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

  let ok = 0;
  let fail = 0;

  for (const { dir, metadata } of items) {
    const title = metadata.chinese_title || metadata.title;
    console.log(`同步: ${title.slice(0, 60)}`);

    try {
      token = await getAccessToken();

      const blocks = buildDocumentBlocks(metadata);
      const totalBlocks = blocks.length;

      let docId = metadata.feishu_doc_id || '';
      let docUrl = metadata.feishu_doc_url || '';
      let writtenCount = Number.isInteger(metadata.feishu_doc_blocks_written)
        ? metadata.feishu_doc_blocks_written
        : 0;

      if (writtenCount < 0 || writtenCount > totalBlocks) {
        writtenCount = 0;
      }

      if (!docId) {
        console.log('  Creating Feishu doc...');
        const doc = await createDocument(token, title);
        docId = doc.document_id;
        docUrl = `https://feishu.cn/docx/${docId}`;
        markDocSyncStarted(dir, docId, docUrl, totalBlocks);
        console.log(`  文档已创建: ${docUrl}`);
      } else {
        if (!docUrl) {
          docUrl = `https://feishu.cn/docx/${docId}`;
        }
        markDocSyncProgress(dir, writtenCount, totalBlocks);
        console.log(`  [INFO] Reusing pending doc: ${docUrl}`);
      }

      const rootBlockId = await getRootBlockId(token, docId);

      if (writtenCount < totalBlocks) {
        console.log('  写入内容块...');
        await appendBlocksToDocument(token, docId, rootBlockId, blocks, writtenCount, async (nextWritten) => {
          markDocSyncProgress(dir, nextWritten, totalBlocks);
        });
      } else {
        console.log('  [INFO] 内容块已写入，补记同步状态...');
      }

      markSynced(dir, docId, docUrl);
      console.log(`  [OK] 完成，共 ${blocks.length} 个块 -> ${docUrl}`);
      ok++;
    } catch (err) {
      console.error(`  [ERROR] ${err.message}`);
      fail++;
    }
  }

  console.log(`\n同步完成：成功 ${ok}，失败 ${fail}`);
}

main();
