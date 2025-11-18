document.querySelectorAll('button[data-copy]').forEach(btn => {
  btn.addEventListener('click', () => {
    const sel = btn.getAttribute('data-copy');
    const el = document.querySelector(sel);
    if (!el) return;
    const text = el.innerText.trim();
    navigator.clipboard.writeText(text).then(() => {
      const prev = btn.textContent;
      btn.textContent = 'Copié';
      setTimeout(() => btn.textContent = prev, 1200);
    });
  });
});
