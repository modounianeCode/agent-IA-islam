/* Interactions communes : thème, menu mobile, filtre des sourates. */
(function () {
  'use strict';

  const root = document.documentElement;
  const themeButton = document.getElementById('theme-toggle');

  function applyTheme(theme) {
    root.dataset.theme = theme;
    if (themeButton) {
      themeButton.textContent = theme === 'dark' ? '☀️' : '🌙';
      themeButton.setAttribute(
        'aria-label',
        theme === 'dark' ? 'Passer au thème clair' : 'Passer au thème sombre'
      );
    }
    try {
      localStorage.setItem('agent-ia-theme', theme);
    } catch (error) {
      /* stockage indisponible */
    }
  }

  applyTheme(root.dataset.theme === 'dark' ? 'dark' : 'light');

  if (themeButton) {
    themeButton.addEventListener('click', function () {
      applyTheme(root.dataset.theme === 'dark' ? 'light' : 'dark');
    });
  }

  // ── Menu latéral sur mobile ─────────────────────────────
  const sidebar = document.getElementById('sidebar');
  const backdrop = document.getElementById('sidebar-backdrop');
  const menuButton = document.getElementById('menu-toggle');

  function setMenu(open) {
    if (!sidebar) return;
    sidebar.classList.toggle('is-open', open);
    if (menuButton) menuButton.setAttribute('aria-expanded', String(open));
    if (backdrop) backdrop.hidden = !open;
    document.body.style.overflow = open ? 'hidden' : '';
  }

  if (menuButton) {
    menuButton.addEventListener('click', function () {
      setMenu(!sidebar.classList.contains('is-open'));
    });
  }

  if (backdrop) {
    backdrop.addEventListener('click', function () {
      setMenu(false);
    });
  }

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') setMenu(false);
  });

  if (sidebar) {
    sidebar.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.matchMedia('(max-width: 980px)').matches) setMenu(false);
      });
    });
  }

  // ── Filtre des sourates ─────────────────────────────────
  const filterInput = document.getElementById('surah-filter');
  const surahList = document.getElementById('surah-list');
  const surahEmpty = document.getElementById('surah-empty');

  function normalize(value) {
    return value
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim();
  }

  if (filterInput && surahList) {
    const items = Array.from(surahList.querySelectorAll('.surah-item'));

    function filter() {
      const term = normalize(filterInput.value);
      let visible = 0;
      items.forEach(function (item) {
        const haystack = normalize(item.dataset.name || item.textContent);
        const match = !term || haystack.includes(term);
        item.hidden = !match;
        if (match) visible += 1;
      });
      if (surahEmpty) surahEmpty.hidden = visible !== 0;
    }

    filterInput.addEventListener('input', filter);

    filterInput.addEventListener('keydown', function (event) {
      if (event.key !== 'Enter') return;
      event.preventDefault();
      const first = items.find(function (item) {
        return !item.hidden;
      });
      if (first) window.location.href = first.getAttribute('href');
    });
  }

  // ── Mémoriser la position de lecture ────────────────────
  const reader = document.querySelector('.reader-panel');
  if (reader && window.location.hash) {
    const target = document.querySelector(window.location.hash);
    if (target) {
      requestAnimationFrame(function () {
        target.scrollIntoView({ block: 'center' });
      });
    }
  }
})();
