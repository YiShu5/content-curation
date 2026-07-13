export function rowState(topic) {
  return {
    topic_id: topic.topic_id,
    category: topic.category || '',
    title: topic.title || '',
    what_happened: topic.what_happened || '',
    discussion_focus: (topic.discussion_focus || []).slice(0, 3),
    why_ranked: topic.why_ranked || '',
    sources: (topic.sources || []).map((source) => ({
      ...source,
      included: true,
      trusted_status: source.verification_status,
    })),
  };
}

export function rowPayload(topic) {
  return {
    topic_id: topic.topic_id,
    category: topic.category,
    title: topic.title,
    what_happened: topic.what_happened,
    discussion_focus: topic.discussion_focus,
    why_ranked: topic.why_ranked,
    source_ids: (topic.sources || []).filter((source) => source.included).map((source) => source.source_id),
    source_updates: (topic.sources || [])
      .filter((source) => source.included && source.verification_status === 'unavailable' && source.trusted_status !== 'unavailable')
      .map((source) => ({ source_id: source.source_id, verification_status: 'unavailable' })),
  };
}

export function downgradeSource(source) {
  if (!source || source.verification_status === 'unavailable') return false;
  source.verification_status = 'unavailable';
  return true;
}

export function moveTopic(state, from, to) {
  if (to < 0 || to >= state.selected.length || from < 0 || from >= state.selected.length) return false;
  const [topic] = state.selected.splice(from, 1);
  state.selected.splice(to, 0, topic);
  return true;
}

export function removeTopic(state, index) {
  if (index < 0 || index >= state.selected.length) return false;
  state.candidates.push(state.selected[index]);
  state.selected.splice(index, 1);
  return true;
}

export function addCandidate(state, topicId) {
  if (state.selected.length >= 3) return false;
  const index = state.candidates.findIndex((item) => item.topic_id === topicId);
  if (index < 0) return false;
  state.selected.push(state.candidates.splice(index, 1)[0]);
  return true;
}
