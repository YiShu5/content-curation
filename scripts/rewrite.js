#!/usr/bin/env node
/**
 * 每日内容策展 - AI 改写脚本
 * 用法: node scripts/rewrite.js <archive_dir>
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import OpenAI from 'openai';
import * as dotenv from 'dotenv';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, '..');
const CONFIG_DIR = path.join(PROJECT_ROOT, 'config');

dotenv.config({ path: path.join(CONFIG_DIR, '.env') });

// ── OpenAI 客户端 ─────────────────────────────────────────────────────────
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1',
});
const MODEL = process.env.OPENAI_MODEL || 'gpt-4o';

// ── 工具函数 ──────────────────────────────────────────────────────────────
function formatDuration(seconds) {
  if (!seconds) return '未知';
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  return `${m}:${String(s).padStart(2, '0')}`;
}

function formatDate(yyyymmdd) {
  if (!yyyymmdd || yyyymmdd.length < 8) return yyyymmdd || '未知';
  return `${yyyymmdd.slice(0, 4)}-${yyyymmdd.slice(4, 6)}-${yyyymmdd.slice(6, 8)}`;
}

// ── 读取文件 ──────────────────────────────────────────────────────────────
function readArchiveFiles(archiveDir) {
  const transcriptPath = path.join(archiveDir, 'transcript.md');
  const metadataPath = path.join(archiveDir, 'metadata.json');
  const promptPath = path.join(CONFIG_DIR, 'rewrite-prompt.md');

  if (!fs.existsSync(transcriptPath)) throw new Error(`找不到 transcript.md: ${transcriptPath}`);
  if (!fs.existsSync(metadataPath)) throw new Error(`找不到 metadata.json: ${metadataPath}`);
  if (!fs.existsSync(promptPath)) throw new Error(`找不到 rewrite-prompt.md: ${promptPath}`);

  const transcript = fs.readFileSync(transcriptPath, 'utf-8');
  const metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf-8'));
  const promptTemplate = fs.readFileSync(promptPath, 'utf-8');

  return { transcript, metadata, promptTemplate };
}

// ── 构建提示词 ─────────────────────────────────────────────────────────────
function buildPrompt(template, metadata, transcript) {
  // Strip YAML frontmatter from transcript for cleaner input
  const transcriptClean = transcript.replace(/^---[\s\S]*?---\n/, '').trim();

  const vars = {
    original_title: metadata.title || '未知',
    platform: metadata.platform || '未知',
    uploader: metadata.uploader || '未知',
    upload_date: formatDate(metadata.upload_date),
    duration: formatDuration(metadata.duration),
    transcript_content: transcriptClean,
  };

  return template.replace(/\{\{(\w+)\}\}/g, (_, key) => vars[key] ?? '');
}

// ── 调用 AI ───────────────────────────────────────────────────────────────
async function callAI(prompt) {
  const requestParams = {
    model: MODEL,
    messages: [{ role: 'user', content: prompt }],
    temperature: 0.3,
    max_tokens: 4096,
  };

  // Try with json_object format first (OpenAI supports this)
  try {
    const response = await client.chat.completions.create({
      ...requestParams,
      response_format: { type: 'json_object' },
    });
    return response.choices[0].message.content;
  } catch (err) {
    // If response_format not supported (some providers), retry without it
    if (err.message?.includes('response_format') || err.status === 400) {
      console.error('  [INFO] 该模型不支持 response_format，切换为普通模式');
      const response = await client.chat.completions.create(requestParams);
      return response.choices[0].message.content;
    }
    throw err;
  }
}

// ── 解析 AI 输出 ───────────────────────────────────────────────────────────
function parseAIResponse(raw) {
  if (!raw) throw new Error('AI 返回了空内容');

  // Remove markdown code fences if present
  let cleaned = raw.trim();
  cleaned = cleaned.replace(/^```(?:json)?\s*/, '').replace(/\s*```$/, '').trim();

  try {
    return JSON.parse(cleaned);
  } catch {
    // Try to extract JSON object with regex
    const match = cleaned.match(/\{[\s\S]*\}/);
    if (match) {
      try {
        return JSON.parse(match[0]);
      } catch {}
    }
    throw new Error(`无法解析 AI 输出为 JSON:\n${raw.slice(0, 500)}`);
  }
}

// ── 写入输出文件 ───────────────────────────────────────────────────────────
function writeRewrittenMd(archiveDir, result, metadata) {
  const today = new Date().toISOString().slice(0, 10);
  const platformLabel = {
    youtube: 'YouTube',
    bilibili: 'Bilibili',
    xiaoyuzhou: '小宇宙',
    audio: '音频',
  }[metadata.platform] || metadata.platform;

  const coreIdeas = (result.core_ideas || [])
    .map(idea => `- ${idea}`)
    .join('\n');

  const content = `# ${result.chinese_title || metadata.title}

## 核心观点

${coreIdeas || '- （无）'}

## 关键洞察

${result.key_insights || ''}

## 深度摘要

${result.deep_summary || ''}

---
*基于 ${platformLabel} | ${metadata.uploader} 转录自动生成，处理时间：${today}*
`;

  fs.writeFileSync(path.join(archiveDir, 'rewritten.md'), content, 'utf-8');
}

function writeMetadataMd(archiveDir, result, metadata) {
  const dateDisplay = formatDate(metadata.upload_date);
  const durationDisplay = formatDuration(metadata.duration);
  const platformLabel = {
    youtube: 'YouTube',
    bilibili: 'Bilibili',
    xiaoyuzhou: '小宇宙',
    audio: '音频',
  }[metadata.platform] || metadata.platform;

  const guests = result.guests?.length
    ? result.guests.map(g => `- ${g}`).join('\n')
    : '- 暂无识别到的嘉宾';

  const quotes = (result.key_quotes || [])
    .map(q => `> "${q}"`)
    .join('\n\n');

  const content = `# ${result.chinese_title || metadata.title}

**原标题**: ${metadata.title}
**来源**: ${platformLabel} | ${metadata.uploader}
**发布时间**: ${dateDisplay}
**原始链接**: ${metadata.url}
**处理时间**: ${metadata.processed_at || new Date().toISOString()}
**时长**: ${durationDisplay}

## 嘉宾

${guests}

## 金句

${quotes || '（未提取）'}
`;

  fs.writeFileSync(path.join(archiveDir, 'metadata.md'), content, 'utf-8');
}

function updateMetadataJson(archiveDir, result) {
  const metaPath = path.join(archiveDir, 'metadata.json');
  const meta = JSON.parse(fs.readFileSync(metaPath, 'utf-8'));

  const updated = {
    ...meta,
    chinese_title: result.chinese_title || meta.title,
    guests: result.guests || [],
    key_quotes: result.key_quotes || [],
    core_ideas: result.core_ideas || [],
    key_insights: result.key_insights || '',
    deep_summary: result.deep_summary || '',
    rewrite_complete: true,
    rewritten_at: new Date().toISOString(),
  };

  fs.writeFileSync(metaPath, JSON.stringify(updated, null, 2), 'utf-8');
  return updated;
}

// ── 主函数 ────────────────────────────────────────────────────────────────
async function main() {
  const archiveDir = process.argv[2];
  if (!archiveDir) {
    console.error('用法: node scripts/rewrite.js <archive_dir>');
    process.exit(1);
  }

  const resolvedDir = path.resolve(archiveDir);
  if (!fs.existsSync(resolvedDir)) {
    console.error(`目录不存在: ${resolvedDir}`);
    process.exit(1);
  }

  try {
    console.log(`  读取归档文件...`);
    const { transcript, metadata, promptTemplate } = readArchiveFiles(resolvedDir);

    // Check if transcript has content
    const transcriptClean = transcript.replace(/^---[\s\S]*?---\n/, '').trim();
    if (!transcriptClean || transcriptClean.startsWith('[转录获取失败') || transcriptClean.startsWith('[无可用转录]')) {
      console.error('  [ERROR] 转录内容为空或无效，无法进行 AI 改写');
      process.exit(1);
    }

    console.log(`  构建提示词 (转录长度: ${transcriptClean.length} 字符)...`);
    const prompt = buildPrompt(promptTemplate, metadata, transcript);

    console.log(`  调用 AI (${MODEL})...`);
    const rawResponse = await callAI(prompt);

    console.log(`  解析 AI 响应...`);
    const result = parseAIResponse(rawResponse);

    // Validate required fields
    if (!result.chinese_title || !result.deep_summary) {
      throw new Error('AI 响应缺少必要字段 (chinese_title 或 deep_summary)');
    }

    console.log(`  写入输出文件...`);
    writeRewrittenMd(resolvedDir, result, metadata);
    writeMetadataMd(resolvedDir, result, metadata);
    const updated = updateMetadataJson(resolvedDir, result);

    console.log(`  [完成] 标题: "${updated.chinese_title}"`);
    if (result.guests?.length) {
      console.log(`  嘉宾: ${result.guests.join('、')}`);
    }

  } catch (err) {
    // Save error details for debugging
    const errorPath = path.join(resolvedDir, 'rewrite_error.json');
    fs.writeFileSync(errorPath, JSON.stringify({
      error: err.message,
      timestamp: new Date().toISOString(),
    }, null, 2), 'utf-8');
    console.error(`  [ERROR] ${err.message}`);
    process.exit(1);
  }
}

main();
