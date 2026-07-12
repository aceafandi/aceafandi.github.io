/* ══════════════════════════════════════════
   Blog Common JS — Dark Mode + Progress + Reading Time
   ══════════════════════════════════════════ */

(function() {
  // ── Dark Mode Toggle ──
  var DARK_KEY = 'aceafandi-dark-mode';
  var toggle = document.getElementById('darkToggle');
  var body = document.body;

  // Load saved preference
  if (localStorage.getItem(DARK_KEY) === 'true') {
    body.classList.add('dark');
  }

  if (toggle) {
    toggle.addEventListener('click', function() {
      body.classList.toggle('dark');
      localStorage.setItem(DARK_KEY, body.classList.contains('dark'));
    });
  }

  // ── Reading Progress Bar ──
  var bar = document.getElementById('readingProgress');
  if (bar) {
    window.addEventListener('scroll', function() {
      var winH = document.documentElement.scrollHeight - window.innerHeight;
      if (winH > 0) {
        bar.style.width = Math.min((window.scrollY / winH) * 100, 100) + '%';
      }
    }, {passive: true});
  }

  // ── Reading Time ──
  var rtEl = document.getElementById('readingTime');
  if (rtEl) {
    var article = document.querySelector('.content');
    if (article) {
      var words = article.textContent.trim().split(/\s+/).length;
      var minutes = Math.max(1, Math.round(words / 200));
      rtEl.textContent = '\u23F1\uFE0F ' + minutes + ' menit baca';
    }
  }
})();
