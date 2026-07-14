import assert from 'node:assert/strict';
import { topics, normalizeTopic, scoreDimensions } from './product-schema.js';

assert.deepEqual(topics(), [
  'AI 前沿', 'AI 编程', 'AI 产品', 'AI 创业',
  'AI 商业', '投资', '个人效率', '其他',
]);
assert.equal(normalizeTopic('AI 前沿'), 'AI 前沿');
assert.equal(normalizeTopic('未知话题'), '其他');
assert.deepEqual(scoreDimensions(), [
  { key: 'insight', label: '洞察原创', max: 50 },
  { key: 'source', label: '信源质量', max: 25 },
  { key: 'storytelling', label: '故事可读', max: 25 },
]);
console.log('✓ product schema');

import { verdictOf } from './product-schema.js';
assert.equal(verdictOf(90), '必读');
assert.equal(verdictOf(89), '强烈推荐');
assert.equal(verdictOf(75), '强烈推荐');
assert.equal(verdictOf(60), '推荐');
assert.equal(verdictOf(45), '一般');
assert.equal(verdictOf(44), '可跳过');
console.log('✓ verdict thresholds');
