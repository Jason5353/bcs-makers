/* BCS Shropshire Maker & Tech Showcase: progressive enhancements.
   Without JavaScript the page still works: the headline shows in full
   and the TV links to YouTube. */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var menu = document.querySelector('.menu-btn');
  if (menu) menu.addEventListener('click', function () {
    var head = document.querySelector('.site-head');
    var open = head.classList.toggle('nav-open');
    menu.setAttribute('aria-expanded', String(open));
  });
  document.querySelectorAll('.nav a').forEach(function (a) { a.addEventListener('click', function () {
    var head = document.querySelector('.site-head'); head.classList.remove('nav-open'); if (menu) menu.setAttribute('aria-expanded', 'false'); }); });
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* 1. Typed headline ------------------------------------------------ */
  var h = document.querySelector('[data-type]');
  if (h && !reduce) {
    var lines = Array.prototype.slice.call(h.querySelectorAll('[data-line]'));
    var words = lines.map(function (el) { return el.textContent; });
    var cursor = document.createElement('span');
    cursor.className = 'cursor';
    cursor.setAttribute('aria-hidden', 'true');
    lines.forEach(function (el) { el.textContent = ''; });
    var li = 0, ci = 0;
    lines[0].after(cursor);
    var step = function () {
      if (li >= lines.length) return;
      lines[li].textContent = words[li].slice(0, ++ci);
      if (ci >= words[li].length) {
        li++; ci = 0;
        if (li < lines.length) { setTimeout(function () { lines[li].after(cursor); setTimeout(step, 130); }, 260); return; }
        return;
      }
      setTimeout(step, 110 + Math.random() * 60);
    };
    setTimeout(step, 500);
  } else if (h) {
    var c = document.createElement('span');
    c.className = 'cursor'; c.setAttribute('aria-hidden', 'true');
    h.querySelector('[data-line]:last-of-type').after(c);
  }

  /* 2. Hero video montage: respect "reduce motion" by showing the still frame */
  var hv = document.querySelector('.hero-video');
  if (hv && reduce) { hv.removeAttribute('autoplay'); hv.pause(); }

  /* 3. Pop-up helpers (used by the retro TV) */
  var lastFocus = null;
  function openModal(m) {
    lastFocus = document.activeElement;
    m.classList.add('open');
    document.body.style.overflow = 'hidden';
    var f = m.querySelector('.x'); if (f) f.focus();
  }
  function closeModal(m) {
    m.classList.remove('open');
    document.body.style.overflow = '';
    var fr = m.querySelector('iframe'); if (fr) fr.remove();
    if (lastFocus) lastFocus.focus();
  }

  /* 4. Retro TV: loads Hackerman's official tutorial only when asked */
  var tv = document.getElementById('tvbox');
  var tvBtn = document.querySelector('[data-tv]');
  if (tv && tvBtn) {
    tvBtn.addEventListener('click', function (e) {
      e.preventDefault();
      var screen = tv.querySelector('.screen');
      var fr = document.createElement('iframe');
      fr.src = 'https://www.youtube-nocookie.com/embed/KEkrWRHCDQU?autoplay=1&rel=0&playsinline=1';
      fr.title = "Hackerman's Hacking Tutorials: How To Hack Time";
      fr.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      fr.allowFullscreen = true;
      fr.referrerPolicy = 'strict-origin-when-cross-origin';
      screen.appendChild(fr);
      openModal(tv);
    });
  }

  /* Shared close behaviour: X button, backdrop click, Escape, arrows */
  document.querySelectorAll('.modal').forEach(function (m) {
    m.addEventListener('click', function (e) {
      if (e.target === m || e.target.closest('.x')) closeModal(m);
    });
  });
  document.addEventListener('keydown', function (e) {
    var open = document.querySelector('.modal.open');
    if (!open) return;
    if (e.key === 'Escape') closeModal(open);
    if (e.key === 'Tab') { /* keep focus inside the open dialog */
      var f = open.querySelectorAll('button, a[href], iframe');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
})();
