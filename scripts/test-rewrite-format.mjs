import assert from 'node:assert/strict';
import { formatScores } from './rewrite.js';

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
