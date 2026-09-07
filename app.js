/* Язык, тема, фильтры и появление карточек. Без зависимостей. */
(function () {
  'use strict';

  var root = document.documentElement;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* приватный режим */ } }
  };

  /* ── Язык ─────────────────────────────────────────── */
  var langBtns = document.querySelectorAll('[data-lang]');

  function applyLang(lang) {
    root.lang = lang;
    var key = 'data-' + lang;

    document.querySelectorAll('[data-ru][data-en]').forEach(function (el) {
      var v = el.getAttribute(key);
      if (v !== null) el.textContent = v;
    });

    document.querySelectorAll('[data-alt-ru][data-alt-en]').forEach(function (el) {
      el.alt = el.getAttribute('data-alt-' + lang) || '';
    });

    document.querySelectorAll('[data-label-ru][data-label-en]').forEach(function (el) {
      el.setAttribute('aria-label', el.getAttribute('data-label-' + lang) || '');
    });

    langBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
    });

    document.title = lang === 'ru'
      ? 'Константин · 3D motion designer'
      : 'Konstantin · 3D motion designer';
  }

  langBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      store.set('lang', b.dataset.lang);
      applyLang(b.dataset.lang);
    });
  });

  /* ── Тема ─────────────────────────────────────────── */
  var themeBtn = document.getElementById('theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.dataset.theme === 'light' ? 'dark' : 'light';
      root.dataset.theme = next;
      store.set('theme', next);
    });
  }

  /* ── Появление карточек ───────────────────────────── */
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var io = null;

  if ('IntersectionObserver' in window) {
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    cards.forEach(function (c) { io.observe(c); });
  } else {
    cards.forEach(function (c) { c.classList.add('in'); });
  }

  /* ── Плеер ────────────────────────────────────────── */
  /* Превью меняем на iframe только по клику: до этого YouTube молчит. */
  document.querySelectorAll('.player__btn').forEach(function (btn) {
    btn.addEventListener('click', function (ev) {
      var box = btn.closest('.player');
      var id = btn.dataset.yt;
      if (!box || !id) return;   // без этого ссылка просто уводит на YouTube
      ev.preventDefault();

      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
              '?autoplay=1&rel=0&modestbranding=1&playsinline=1';
      f.title = btn.getAttribute('aria-label') || 'YouTube';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      f.allowFullscreen = true;
      f.loading = 'lazy';

      box.replaceChildren(f);
      f.focus();
    });
  });

  /* ── Фильтры ──────────────────────────────────────── */
  var chips = document.querySelectorAll('.chip');
  var empty = document.getElementById('empty');
  var valid = {};
  chips.forEach(function (c) { valid[c.dataset.filter] = true; });

  function applyFilter(key, push) {
    if (!valid[key]) key = 'all';

    var shown = 0;
    cards.forEach(function (card) {
      var ok = key === 'all' || card.dataset.cat === key;
      card.hidden = !ok;
      if (ok) {
        // Перезапускаем stagger, чтобы новая раскладка проявилась волной.
        card.style.setProperty('--i', shown);
        card.classList.remove('in');
        if (io) io.observe(card); else card.classList.add('in');
        shown++;
      }
    });

    if (empty) empty.hidden = shown > 0;

    chips.forEach(function (c) {
      c.setAttribute('aria-selected', String(c.dataset.filter === key));
    });

    if (push) {
      var hash = key === 'all' ? ' ' : '#' + key;
      history.replaceState(null, '', key === 'all' ? location.pathname + location.search : hash);
    }
  }

  chips.forEach(function (c) {
    c.addEventListener('click', function () { applyFilter(c.dataset.filter, true); });
  });

  window.addEventListener('hashchange', function () {
    var h = location.hash.slice(1);
    if (valid[h]) applyFilter(h, false);
  });

  /* ── Старт ────────────────────────────────────────── */
  applyLang(root.lang === 'en' ? 'en' : 'ru');

  var initial = location.hash.slice(1);
  if (valid[initial] && initial !== 'all') applyFilter(initial, false);

  root.classList.add('ready');
})();
