(function () {
  const button = document.getElementById('dailyCopyButton');
  const payload = document.getElementById('dailySharePayload');
  if (!button || !payload) return;
  const text = JSON.parse(payload.textContent || '{}').text || '';

  async function copy(value) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(value);
    }
    const area = document.createElement('textarea');
    area.value = value;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand('copy');
    area.remove();
    if (!ok) throw new Error('copy failed');
  }

  button.addEventListener('click', async function () {
    try {
      await copy(text);
      button.textContent = '已复制';
    } catch (_error) {
      button.textContent = '复制失败，请重试';
    }
    window.setTimeout(function () { button.textContent = '复制本期 ↗'; }, 1600);
  });
})();
