// Sidebar: highlight the section in view, and open/close the menu on small screens.
export function initNav() {
  const toggle = document.getElementById('nav-toggle');
  const panel = document.getElementById('side-panel');
  const links = [...document.querySelectorAll('.side__nav a')];
  const sections = links.map(l => document.querySelector(l.getAttribute('href'))).filter(Boolean);

  function setOpen(open) {
    panel.classList.toggle('open', open);
    toggle.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  }
  toggle.addEventListener('click', () => setOpen(!panel.classList.contains('open')));
  links.forEach(a => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') setOpen(false); });

  // Active section = the last one whose top has passed 40% of the viewport,
  // so exactly one link is lit, and Contact lights up at the very bottom.
  let ticking = false;
  function update() {
    const h = document.documentElement;
    let current = sections[0];
    if (h.scrollTop >= h.scrollHeight - h.clientHeight - 2) current = sections[sections.length - 1];
    else for (const s of sections) if (s.getBoundingClientRect().top <= innerHeight * 0.4) current = s;
    links.forEach(l => {
      const on = l.getAttribute('href') === '#' + current.id;
      l.classList.toggle('active', on);
      if (on) l.setAttribute('aria-current', 'true'); else l.removeAttribute('aria-current');
    });
    ticking = false;
  }
  window.addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(update);
  }, { passive: true });
  update();
}
