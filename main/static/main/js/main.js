/* ==========================================================================
   CSC Anna Nagar - site behaviour (vanilla JS, no dependencies)
   ========================================================================== */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---- Header: shadow on scroll, scroll progress, back-to-top ---------- */
  function initScroll() {
    var header = $('#siteHeader'), bar = $('#scrollProgress'), top = $('#toTop');
    function onScroll() {
      var y = window.scrollY || document.documentElement.scrollTop;
      if (header) header.classList.toggle('scrolled', y > 10);
      if (bar) {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
      }
      if (top) top.classList.toggle('show', y > 500);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  /* ---- Mobile menu + "More" dropdown ----------------------------------- */
  function initNav() {
    var toggle = $('#navToggle'), nav = $('#siteNav'), more = $('#navMore');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        toggle.querySelector('i').className = open ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
      });
    }
    if (more) {
      var btn = more.querySelector('button');
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = more.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
    document.addEventListener('click', function (e) {
      if (more && !more.contains(e.target)) more.classList.remove('open');
      if (nav && toggle && !nav.contains(e.target) && !toggle.contains(e.target)) nav.classList.remove('open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (more) more.classList.remove('open');
        if (nav) nav.classList.remove('open');
        $$('.modal.open').forEach(function (m) { m.classList.remove('open'); document.body.style.overflow = ''; });
      }
    });
  }

  /* ---- Reveal on scroll ------------------------------------------------ */
  function initReveal() {
    var els = $$('.reveal');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('visible'); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('visible'); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ---- Animated counters:  <b data-target="1000" data-suffix="+"> ------ */
  function initCounters() {
    var els = $$('[data-target]');
    if (!els.length || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.unobserve(en.target);
        var el = en.target, end = parseInt(el.getAttribute('data-target'), 10), suf = el.getAttribute('data-suffix') || '';
        if (isNaN(end)) return;
        var start = null, dur = 1500;
        (function step(ts) {
          if (start === null) start = ts;
          var p = Math.min(1, (ts - start) / dur), eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.floor(end * eased).toLocaleString('en-IN') + suf;
          if (p < 1) requestAnimationFrame(step); else el.textContent = end.toLocaleString('en-IN') + suf;
        })(performance.now());
      });
    }, { threshold: 0.5 });
    els.forEach(function (e) { io.observe(e); });
  }

  /* ---- Scroll-snap carousel:  [data-carousel] with .carousel__track ---- */
  function initCarousels() {
    $$('[data-carousel]').forEach(function (root) {
      var track = $('.carousel__track', root), prev = $('[data-prev]', root), next = $('[data-next]', root);
      if (!track) return;
      function step() { var c = track.children[0]; return c ? c.getBoundingClientRect().width + 20 : 300; }
      function go(dir) {
        var max = track.scrollWidth - track.clientWidth;
        if (dir > 0 && track.scrollLeft >= max - 4) track.scrollTo({ left: 0, behavior: 'smooth' });
        else if (dir < 0 && track.scrollLeft <= 4) track.scrollTo({ left: max, behavior: 'smooth' });
        else track.scrollBy({ left: dir * step(), behavior: 'smooth' });
      }
      if (prev) prev.addEventListener('click', function () { go(-1); });
      if (next) next.addEventListener('click', function () { go(1); });
      if (root.hasAttribute('data-autoplay') && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        var t = setInterval(function () { go(1); }, 4500);
        root.addEventListener('mouseenter', function () { clearInterval(t); });
        root.addEventListener('mouseleave', function () { t = setInterval(function () { go(1); }, 4500); });
      }
    });
  }

  /* ---- Auto-dismiss toast messages ------------------------------------- */
  function initMessages() {
    $$('.msg').forEach(function (m) {
      setTimeout(function () { m.style.opacity = '0'; m.style.transform = 'translateY(-8px)'; setTimeout(function () { m.remove(); }, 450); }, 6500);
    });
  }

  /* ---- Video sound toggle:  <button data-video-sound="#videoId"> ------- */
  function initVideo() {
    $$('[data-video-sound]').forEach(function (btn) {
      var v = $(btn.getAttribute('data-video-sound'));
      if (!v) return;
      v.play && v.play().catch(function () {});
      btn.addEventListener('click', function () {
        v.muted = !v.muted;
        btn.innerHTML = v.muted ? '<i class="fa-solid fa-volume-xmark"></i> Tap to unmute' : '<i class="fa-solid fa-volume-high"></i> Mute';
        if (v.paused) v.play();
      });
      document.addEventListener('visibilitychange', function () { if (!document.hidden && v.paused) v.play().catch(function () {}); });
    });
  }

  /* ---- Modal helpers:  [data-open-modal="#id"]  [data-close-modal] ----- */
  function initModals() {
    $$('[data-open-modal]').forEach(function (b) {
      b.addEventListener('click', function () {
        var m = $(b.getAttribute('data-open-modal'));
        if (m) { m.classList.add('open'); document.body.style.overflow = 'hidden'; var f = m.querySelector('input,textarea,select'); f && f.focus(); }
      });
    });
    $$('.modal').forEach(function (m) {
      m.addEventListener('click', function (e) { if (e.target === m || e.target.closest('[data-close-modal]')) { m.classList.remove('open'); document.body.style.overflow = ''; } });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initScroll(); initNav(); initReveal(); initCounters(); initCarousels(); initMessages(); initVideo(); initModals();
  });
})();
