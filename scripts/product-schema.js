import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, '..');
const SCHEMA_PATH = path.join(PROJECT_ROOT, 'config', 'product_schema.json');

export function loadProductSchema() {
  return JSON.parse(fs.readFileSync(SCHEMA_PATH, 'utf-8'));
}

export function topics() {
  return loadProductSchema().topics.slice();
}

export function normalizeTopic(value) {
  const schema = loadProductSchema();
  const topic = String(value || '').trim();
  return schema.topics.includes(topic) ? topic : schema.unknown_topic;
}

export function scoreDimensions() {
  return loadProductSchema().score_dimensions.slice();
}

export function verdictThresholds() {
  return loadProductSchema().verdict_thresholds.slice();
}

// 评分分段表与评级表的唯一来源是 product_schema.json；
// rewrite-prompt.md 用 {{rubric_<key>}} / {{verdict_table}} 占位，此处渲染成 markdown
export function rubricTable(key) {
  const dim = scoreDimensions().find((d) => d.key === key);
  if (!dim || !Array.isArray(dim.rubric)) return '';
  const rows = dim.rubric.map((band) => `| ${band.range} | ${band.label} |`);
  return ['| 分段 | 标准 |', '|------|------|', ...rows].join('\n');
}

export function verdictTable() {
  const rows = verdictThresholds().map((t, i, all) => {
    const upper = i === 0 ? 100 : all[i - 1].min - 1;
    return `| ${t.min}-${upper} | ${t.label} |`;
  });
  return ['| 总分 | verdict |', '|------|---------|', ...rows].join('\n');
}

export function verdictOf(total) {
  for (const t of verdictThresholds()) {
    if (total >= t.min) return t.label;
  }
  return verdictThresholds().at(-1).label;
}
