// High-contrast mode. The saved choice is applied by an inline script in <head> to avoid a flash.
export function initContrast() {
  const btn = document.getElementById('contrast-toggle');
  const root = document.documentElement;
  const sync = () => btn.setAttribute('aria-pressed', String(root.dataset.contrast === 'high'));
  btn.addEventListener('click', () => {
    const high = root.dataset.contrast !== 'high';
    if (high) root.dataset.contrast = 'high'; else delete root.dataset.contrast;
    try { localStorage.setItem('site-contrast', high ? 'high' : 'normal'); } catch (e) {}
    sync();
  });
  sync();
}
