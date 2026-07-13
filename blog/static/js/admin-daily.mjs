import { addCandidate, downgradeSource, moveTopic, removeTopic, rowPayload, rowState } from './admin-daily-state.mjs';

const button = document.getElementById('dailyAdminButton');
const dialog = document.getElementById('dailyAdminDialog');
if (!button || !dialog) throw new Error('Administrator editor markup is missing');

const csrfToken = JSON.parse(document.getElementById('adminCsrfToken').textContent).token;
const limits = JSON.parse(document.getElementById('adminEditorConfig').textContent);
const rowsHost = document.getElementById('dailyAdminRows');
const stateMessage = document.getElementById('dailyAdminState');
const candidateSelect = document.getElementById('dailyCandidateSelect');
const publishButton = document.getElementById('dailyPublishButton');
const preview = document.getElementById('dailyAdminPreview');
const state = {
  action: button.dataset.action,
  issueDate: button.dataset.date,
  previewSurface: button.dataset.previewSurface,
  revision: null,
  selected: [],
  candidates: [],
};

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function actionButton(text, onClick, disabled = false) {
  const node = el('button', '', text);
  node.type = 'button';
  node.disabled = disabled;
  node.addEventListener('click', onClick);
  return node;
}

function requestJson(url, options = {}) {
  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': csrfToken,
      ...(options.headers || {}),
    },
  }).then(async (response) => {
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error(body.message || `请求失败（HTTP ${response.status}）`);
      error.status = response.status;
      error.body = body;
      throw error;
    }
    return body;
  });
}

function showError(error) {
  stateMessage.textContent = error.message || '请求失败';
  stateMessage.className = 'daily-admin-error';
}

function field(labelText, value, maxLength, onInput, multiline = false) {
  const label = el('label', 'daily-admin-field');
  label.append(el('span', '', labelText));
  const input = document.createElement(multiline ? 'textarea' : 'input');
  if (!multiline) input.type = 'text';
  input.value = value;
  input.maxLength = maxLength;
  input.addEventListener('input', () => onInput(input.value));
  label.append(input);
  return label;
}

function renderSource(source, topic) {
  const item = el('div', 'daily-admin-source');
  const includeLabel = el('label');
  const include = document.createElement('input');
  include.type = 'checkbox'; include.checked = source.included;
  include.addEventListener('change', () => { source.included = include.checked; renderRows(); });
  includeLabel.append(include, document.createTextNode(' 纳入本期依据'));
  const identity = el('p', '', `${source.publisher || '未知来源'} · ${source.title || source.url || ''}`);
  item.append(includeLabel, identity);
  if (source.url) {
    try {
      const url = new URL(source.url, window.location.origin);
      if (url.protocol === 'http:' || url.protocol === 'https:') {
        const link = el('a', '', '查看原文');
        link.href = url.href; link.target = '_blank'; link.rel = 'noopener noreferrer';
        item.append(link);
      }
    } catch (_error) { /* Invalid trusted metadata is shown as text, never as a link. */ }
  }
  const unavailableLabel = el('label');
  const unavailable = document.createElement('input');
  unavailable.type = 'checkbox';
  unavailable.checked = source.verification_status === 'unavailable';
  unavailable.disabled = source.trusted_status === 'unavailable';
  unavailable.addEventListener('change', () => {
    if (!unavailable.checked) return;
    downgradeSource(source);
    unavailable.disabled = true;
    validateEditor();
  });
  unavailableLabel.append(unavailable, document.createTextNode(' 来源暂不可访问'));
  item.append(unavailableLabel);
  return item;
}

function replaceAt(index, topicId) {
  const candidateIndex = state.candidates.findIndex((item) => item.topic_id === topicId);
  if (candidateIndex < 0) return;
  const replacement = state.candidates.splice(candidateIndex, 1)[0];
  state.candidates.push(state.selected[index]);
  state.selected[index] = replacement;
  renderRows(); renderCandidates();
}

function renderRows() {
  rowsHost.replaceChildren();
  state.selected.forEach((topic, index) => {
    const row = el('article', 'daily-admin-row');
    row.draggable = true;
    row.dataset.index = String(index);
    row.append(el('strong', 'daily-admin-rank', `${index + 1}`));
    row.append(el('span', 'daily-admin-drag', '拖动排序'));
    const controls = el('div', 'daily-admin-row-controls');
    controls.append(
      actionButton('上移', () => { if (moveTopic(state, index, index - 1)) renderRows(); }, index === 0),
      actionButton('下移', () => { if (moveTopic(state, index, index + 1)) renderRows(); }, index === state.selected.length - 1),
      actionButton('移除', () => { removeTopic(state, index); renderRows(); renderCandidates(); }),
    );
    row.append(controls);
    row.append(
      field('分类', topic.category, limits.category_max, (v) => { topic.category = v; validateEditor(); }),
      field('标题', topic.title, limits.title_max, (v) => { topic.title = v; validateEditor(); }),
      field('核心事实', topic.what_happened, limits.what_happened_max, (v) => { topic.what_happened = v; validateEditor(); }, true),
      field('讨论焦点（逗号分隔）', topic.discussion_focus.join(', '), limits.discussion_focus_max_items * (limits.discussion_focus_item_max + 2), (v) => {
        topic.discussion_focus = v.split(/[,，]/).map((x) => x.trim()).filter(Boolean);
        validateEditor();
      }, true),
      field('编辑判断', topic.why_ranked, limits.why_ranked_max, (v) => { topic.why_ranked = v; validateEditor(); }, true),
    );
    const evidence = el('fieldset', 'daily-admin-evidence');
    evidence.append(el('legend', '', '来源依据（只读）'));
    topic.sources.forEach((source) => evidence.append(renderSource(source, topic)));
    row.append(evidence);
    if (state.candidates.length) {
      const replace = el('label', 'daily-admin-replace', '替换此主题 ');
      const select = document.createElement('select');
      select.append(new Option('选择候选', ''));
      state.candidates.forEach((item) => select.append(new Option(item.title, item.topic_id)));
      const apply = actionButton('替换', () => replaceAt(index, select.value));
      replace.append(select, apply); row.append(replace);
    }
    row.addEventListener('dragstart', (event) => event.dataTransfer.setData('text/plain', String(index)));
    row.addEventListener('dragover', (event) => event.preventDefault());
    row.addEventListener('drop', (event) => {
      event.preventDefault();
      if (moveTopic(state, Number(event.dataTransfer.getData('text/plain')), index)) renderRows();
    });
    rowsHost.append(row);
  });
  validateEditor();
}

function renderCandidates() {
  candidateSelect.replaceChildren(new Option('选择候选', ''));
  state.candidates.forEach((item) => candidateSelect.append(new Option(item.title, item.topic_id)));
  document.getElementById('dailyCandidateAdd').disabled = !state.candidates.length || state.selected.length >= 3;
}

function validateEditor() {
  const blocking = [];
  const warnings = [];
  if (state.selected.length < 1 || state.selected.length > 3) blocking.push('请保留 1–3 个主题');
  state.selected.forEach((topic, index) => {
    const required = [['标题', topic.title, limits.title_max], ['核心事实', topic.what_happened, limits.what_happened_max], ['编辑判断', topic.why_ranked, limits.why_ranked_max]];
    required.forEach(([name, value, max]) => { if (!value.trim() || value.length > max) blocking.push(`第 ${index + 1} 条${name}无效`); });
    if (topic.category.length > limits.category_max) blocking.push(`第 ${index + 1} 条分类过长`);
    if (topic.discussion_focus.length > limits.discussion_focus_max_items || topic.discussion_focus.some((x) => !x || x.length > limits.discussion_focus_item_max)) blocking.push(`第 ${index + 1} 条讨论焦点无效`);
    const included = topic.sources.filter((source) => source.included);
    if (!included.length) blocking.push(`第 ${index + 1} 条没有来源`);
    if (state.action === 'publish' && !included.some((source) => source.verification_status === 'readable')) blocking.push(`第 ${index + 1} 条没有可读来源`);
    const publishers = new Set(included.map((source) => source.publisher_key || source.publisher).filter(Boolean));
    if (publishers.size === 1) warnings.push(`第 ${index + 1} 条仅有一个独立发布者`);
    const warningLimit = index === 0 ? limits.lead_title_warning : limits.side_title_warning;
    if (topic.title.length > warningLimit) warnings.push(`第 ${index + 1} 条标题可能影响版式`);
  });
  publishButton.disabled = blocking.length > 0;
  stateMessage.className = blocking.length ? 'daily-admin-error' : warnings.length ? 'daily-admin-warning' : '';
  stateMessage.textContent = blocking[0] || warnings.join('；') || '可以预览或提交';
  return blocking.length === 0;
}

function loadDraft(message = '') {
  stateMessage.textContent = '正在读取候选…';
  stateMessage.className = '';
  publishButton.disabled = true;
  if (!dialog.open) dialog.showModal();
  return requestJson('/admin/daily/draft?date=' + encodeURIComponent(state.issueDate), { method: 'GET' }).then((body) => {
    state.action = body.published ? 'revise' : 'publish';
    state.selected = (body.draft.topics || []).map(rowState);
    const selectedIds = new Set(state.selected.map((item) => item.topic_id));
    state.candidates = [...(body.draft.candidates || []), ...(body.draft.attention || [])]
      .filter((item) => !selectedIds.has(item.topic_id)).map(rowState);
    state.revision = body.published ? body.published.revision : null;
    document.getElementById('dailyAdminMeta').textContent = [
      body.issue_meta.issue_date,
      `第 ${String(body.issue_meta.issue_number).padStart(3, '0')} 期`,
      body.issue_meta.generated_at ? `候选生成 ${body.issue_meta.generated_at}` : '',
    ].filter(Boolean).join(' · ');
    document.getElementById('dailyAdminTitle').textContent = state.action === 'revise' ? '修订本期' : '发布今日简报';
    publishButton.textContent = state.action === 'revise' ? '保存修订' : '确认发布';
    renderRows(); renderCandidates();
    if (message) { stateMessage.textContent = message; stateMessage.className = 'daily-admin-warning'; }
  });
}

button.addEventListener('click', () => loadDraft().catch(showError));
document.getElementById('dailyAdminClose').addEventListener('click', () => dialog.close());
document.getElementById('dailyCandidateAdd').addEventListener('click', () => {
  if (addCandidate(state, candidateSelect.value)) { renderRows(); renderCandidates(); }
});
document.getElementById('dailyPreviewButton').addEventListener('click', () => {
  if (!validateEditor()) return;
  requestJson(`/admin/daily/${encodeURIComponent(state.issueDate)}/preview`, {
    method: 'POST', body: JSON.stringify({ topics: state.selected.map(rowPayload), preview_surface: state.previewSurface }),
  }).then((body) => {
    const frame = document.createElement('iframe');
    frame.title = '读者页面预览'; frame.sandbox = ''; frame.srcdoc = body.html;
    preview.replaceChildren(frame); preview.hidden = false;
  }).catch(showError);
});
publishButton.addEventListener('click', () => {
  if (!validateEditor()) return;
  publishButton.disabled = true;
  const payload = { topics: state.selected.map(rowPayload) };
  if (state.action === 'revise') payload.expected_revision = state.revision;
  requestJson(`/admin/daily/${encodeURIComponent(state.issueDate)}/${state.action}`, { method: 'POST', body: JSON.stringify(payload) })
    .then((body) => { window.location.assign(body.redirect_url); })
    .catch((error) => {
      if (error.status === 409 && error.body.code === 'already_published') {
        return loadDraft('本期已发布，已切换为修订').catch(showError);
      } else showError(error);
    }).finally(() => validateEditor());
});
