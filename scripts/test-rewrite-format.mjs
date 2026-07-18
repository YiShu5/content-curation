import assert from 'node:assert/strict';
import {
  formatScores, normalizeScores, groundQuotes, estimateTokens, splitTranscript,
} from './rewrite.js';

const markdown = formatScores({
  insight: { score: 42, reason: '有反直觉洞察' },
  source: { score: 23, reason: '一手信源' },
  storytelling: { score: 18, reason: '结构清晰' },
  total: 83,
  verdict: '强烈推荐',
});

assert.match(markdown, /洞察原创/);
assert.match(markdown, /信源质量/);
assert.match(markdown, /故事可读/);
assert.doesNotMatch(markdown, /AI 相关性/);
assert.doesNotMatch(markdown, /加分项/);
console.log('✓ rewrite score format');

// 越界分钳位到 [0, max]，total/verdict 不信任模型自算
const clamped = normalizeScores({
  insight: { score: 70, reason: 'x' },
  source: { score: -3, reason: 'y' },
  storytelling: { score: 20, reason: 'z' },
  total: 999,
  verdict: '必读',
});
assert.equal(clamped.insight.score, 50);
assert.equal(clamped.source.score, 0);
assert.equal(clamped.storytelling.score, 20);
assert.equal(clamped.total, 70);
assert.equal(clamped.verdict, '推荐');

// 维度分合法但模型算错 total/verdict 时，以代码侧重算为准
const recomputed = normalizeScores({
  insight: { score: 42, reason: '' },
  source: { score: 23, reason: '' },
  storytelling: { score: 18, reason: '' },
  total: 60,
  verdict: '推荐',
});
assert.equal(recomputed.total, 83);
assert.equal(recomputed.verdict, '强烈推荐');

// 非数字得分按 0 处理，缺失维度不炸
const garbage = normalizeScores({ insight: { score: '很高' }, total: 'NaN' });
assert.equal(garbage.insight.score, 0);
assert.equal(garbage.source.score, 0);
assert.equal(garbage.total, 0);
assert.equal(garbage.verdict, '可跳过');

// 无评分保持 null，不改变失败语义
assert.equal(normalizeScores(null), null);
console.log('✓ rewrite score normalization');

// grounding：出处句逐字在转录中则保留，跨时间戳行可匹配；对不上整条丢弃
const transcript = '[00:00:01] Old media, you have very restricted channels.\n[00:00:05] The brands were the companies.';
const grounded = groundQuotes({
  key_quotes: ['旧媒体渠道非常受限', '品牌就是公司', '虚构的金句内容'],
  key_quotes_source: [
    'Old media, you have very restricted channels.',
    'The brands were the companies.',
    'This sentence never appeared anywhere in it.',
  ],
}, transcript);
assert.deepEqual(grounded.key_quotes, ['旧媒体渠道非常受限', '品牌就是公司']);
assert.equal(grounded.key_quotes_source.length, 2);

// 模型完全没交出处 → 按承诺整批丢弃（否则"完全不服从"待遇好于"部分服从"，激励倒挂）
const unverified = groundQuotes({ key_quotes: ['a quote'], key_quotes_source: [] }, transcript);
assert.equal(unverified.key_quotes.length, 0);

// 分段浓缩模式下模型把 "QUOTE: " 前缀抄进出处 → 剥掉前缀后仍能配对
const prefixed = groundQuotes({
  key_quotes: ['旧媒体渠道非常受限'],
  key_quotes_source: ['QUOTE: Old media, you have very restricted channels.'],
}, transcript);
assert.equal(prefixed.key_quotes.length, 1);
assert.ok(!prefixed.key_quotes_source[0].startsWith('QUOTE'));

// token 估算：CJK 按字计，ASCII 按 1/4
assert.ok(estimateTokens('中文十个字中文十个字') >= 10);
assert.equal(estimateTokens('a'.repeat(400)), 100);

// 超长转录分段：块数随长度增长；无换行的整段长文本也必须被硬切
assert.ok(splitTranscript('line\n'.repeat(20000), 1000).length > 3);
assert.ok(splitTranscript('x'.repeat(100000), 1000).length > 10);
console.log('✓ quote grounding & chunking');
