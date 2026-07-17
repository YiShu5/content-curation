import assert from 'node:assert/strict';
import { topics, normalizeTopic, scoreDimensions, rubricTable, verdictTable } from './product-schema.js';

assert.deepEqual(topics(), [
  'AI 前沿', 'AI 编程', 'AI 产品', 'AI 创业',
  'AI 商业', '投资', '个人效率', '其他',
]);
assert.equal(normalizeTopic('AI 前沿'), 'AI 前沿');
assert.equal(normalizeTopic('未知话题'), '其他');
assert.deepEqual(
  scoreDimensions().map(({ key, label, max }) => ({ key, label, max })),
  [
    { key: 'insight', label: '洞察原创', max: 50 },
    { key: 'source', label: '信源质量', max: 25 },
    { key: 'storytelling', label: '故事可读', max: 25 },
  ],
);
// 每个维度必须带 rubric 分段（rewrite 与 rescore 两条链路的唯一评分标准来源）
for (const dim of scoreDimensions()) {
  assert.ok(Array.isArray(dim.rubric) && dim.rubric.length >= 4, `${dim.key} 缺 rubric`);
}
assert.match(rubricTable('insight'), /^\| 分段 \| 标准 \|/);
assert.match(rubricTable('insight'), /43-50 \| 范式级/);
assert.match(verdictTable(), /\| 90-100 \| 必读 \|/);
assert.match(verdictTable(), /\| 0-44 \| 可跳过 \|/);
console.log('✓ product schema');

import { verdictOf } from './product-schema.js';
assert.equal(verdictOf(90), '必读');
assert.equal(verdictOf(89), '强烈推荐');
assert.equal(verdictOf(75), '强烈推荐');
assert.equal(verdictOf(60), '推荐');
assert.equal(verdictOf(45), '一般');
assert.equal(verdictOf(44), '可跳过');
console.log('✓ verdict thresholds');
