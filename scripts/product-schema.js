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

export function verdictOf(total) {
  for (const t of verdictThresholds()) {
    if (total >= t.min) return t.label;
  }
  return verdictThresholds().at(-1).label;
}
