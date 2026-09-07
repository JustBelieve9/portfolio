/* Язык, тема, печать. Без зависимостей — как на портфолио. */
(function () {
  'use strict';

  var root = document.documentElement;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* приватный режим */ } }
  };

  var langBtns = document.querySelectorAll('[data-lang]');

  function applyLang(lang) {
    root.lang = lang;

    /* Текстовые узлы. */
    document.querySelectorAll('[data-ru][data-en]').forEach(function (el) {
      var v = el.getAttribute('data-' + lang);
      if (v !== null) el.textContent = v;
    });

    /* Узлы с разметкой внутри — контент свой, не пользовательский. */
    document.querySelectorAll('[data-ru-html][data-en-html]').forEach(function (el) {
      var v = el.getAttribute('data-' + lang + '-html');
      if (v !== null) el.innerHTML = v;
    });

    document.querySelectorAll('[data-label-ru][data-label-en]').forEach(function (el) {
      el.setAttribute('aria-label', el.getAttribute('data-label-' + lang) || '');
    });

    langBtns.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
    });

    document.title = lang === 'ru'
      ? 'Родин Константин — Senior 3D Motion Designer'
      : 'Konstantin Rodin — Senior 3D Motion Designer';
  }

  langBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      store.set('lang', b.dataset.lang);
      applyLang(b.dataset.lang);
    });
  });

  var themeBtn = document.getElementById('theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = root.dataset.theme === 'light' ? 'dark' : 'light';
      root.dataset.theme = next;
      store.set('theme', next);
    });
  }

  var printBtn = document.getElementById('print');
  if (printBtn) printBtn.addEventListener('click', function () { window.print(); });

  applyLang(root.lang === 'en' ? 'en' : 'ru');
  root.classList.add('ready');
})();
