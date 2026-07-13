import assert from 'node:assert/strict';
import {
  addCandidate,
  downgradeSource,
  moveTopic,
  removeTopic,
  rowPayload,
  rowState,
} from './static/js/admin-daily-state.mjs';

const trusted = {
  topic_id: 'topic-a', category: 'AI', title: 'Title', what_happened: 'Fact',
  discussion_focus: ['Focus'], why_ranked: 'Why',
  sources: [{ source_id: 'source-a', publisher: 'Official', publisher_key: 'official.ai', verification_status: 'readable' }],
};

const row = rowState(trusted);
assert.deepEqual(rowPayload(row).source_ids, ['source-a'], 'trusted source remains included');

const state = { selected: [row], candidates: [] };
removeTopic(state, 0);
addCandidate(state, 'topic-a');
assert.equal(state.selected[0].sources[0].included, true);
assert.equal(state.selected[0].sources[0].trusted_status, 'readable');

assert.equal(downgradeSource(state.selected[0].sources[0]), true);
assert.equal(downgradeSource(state.selected[0].sources[0]), false, 'downgrade cannot be reversed or repeated');
assert.equal(state.selected[0].sources[0].verification_status, 'unavailable');

state.selected.push(rowState({ ...trusted, topic_id: 'topic-b' }));
moveTopic(state, 1, 0);
assert.equal(state.selected[0].topic_id, 'topic-b');
moveTopic(state, 0, -1);
assert.equal(state.selected[0].topic_id, 'topic-b', 'out-of-bounds move is ignored');

console.log('admin daily state tests passed');
