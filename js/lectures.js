// Lectures: show a thumbnail, and load the YouTube player only when it is clicked.
export function initLectures() {
  document.querySelectorAll('.episode__thumb[data-yt]').forEach(link => {
    link.addEventListener('click', e => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;  // let new-tab clicks through
      e.preventDefault();
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(link.dataset.yt)}?autoplay=1&rel=0`;
      frame.title = link.closest('.episode').querySelector('.entry__title').textContent;
      frame.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      frame.allowFullscreen = true;
      const box = document.createElement('div');
      box.className = 'episode__thumb';
      box.append(frame);
      link.replaceWith(box);
      frame.focus();
    });
  });
}
