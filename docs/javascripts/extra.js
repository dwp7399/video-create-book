// 正文中句内的视频/音频链接后加一个“播放”按钮，就地展开播放器
document$.subscribe(() => {
  document.querySelectorAll('.md-content a[href$=".mp4"], .md-content a[href$=".wav"]').forEach(a => {
    if (a.dataset.enhanced || a.closest('figure')) return;
    a.dataset.enhanced = '1';
    const b = document.createElement('button');
    b.className = 'inline-play'; b.textContent = '▶ 播放'; b.type = 'button';
    b.onclick = () => {
      const next = b.nextElementSibling;
      if (next && next.classList.contains('inline-media')) { next.remove(); return; }
      const box = document.createElement('span'); box.className = 'inline-media';
      const isAudio = a.href.endsWith('.wav');
      box.innerHTML = isAudio ? `<audio controls autoplay src="${a.href}"></audio>` : `<video controls autoplay src="${a.href}"></video>`;
      b.after(box);
    };
    a.after(b);
  });
});
