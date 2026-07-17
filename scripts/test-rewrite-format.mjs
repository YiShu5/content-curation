import assert from 'node:assert/strict';
import { formatScores, normalizeScores } from './rewrite.js';

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
