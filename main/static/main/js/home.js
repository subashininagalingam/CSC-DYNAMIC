/* ==========================================================================
   Home page behaviour: slider, offer popup, animated programme details
   ========================================================================== */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function openModal(m) {
    m.classList.add('open'); document.body.style.overflow = 'hidden';
    var f = m.querySelector('.modal__close'); if (f) f.focus();
  }
  function closeModal(m) { m.classList.remove('open'); document.body.style.overflow = ''; }

  /* ---------------- Slider (admin: Home slides) ---------------- */
  function initSlider() {
    var root = $('[data-slider]'); if (!root) return;
    var slides = $$('.hslide', root), dots = $$('.hslider__dot', root), i = 0, timer = null;
    if (slides.length < 2) return;
    function show(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('is-active', k === i); s.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
      dots.forEach(function (d, k) { d.classList.toggle('is-active', k === i); });
    }
    function play() { if (reduce || timer) return; timer = setInterval(function () { show(i + 1); }, 5500); }
    function stop() { clearInterval(timer); timer = null; }
    var prev = $('[data-prev]', root), next = $('[data-next]', root);
    if (prev) prev.addEventListener('click', function () { show(i - 1); });
    if (next) next.addEventListener('click', function () { show(i + 1); });
    dots.forEach(function (d) { d.addEventListener('click', function () { show(parseInt(d.getAttribute('data-dot'), 10)); }); });
    root.addEventListener('mouseenter', stop); root.addEventListener('mouseleave', play);
    root.addEventListener('focusin', stop); root.addEventListener('focusout', play);
    var tx = null;
    root.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    root.addEventListener('touchend', function (e) {
      if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; tx = null;
      if (Math.abs(dx) > 40) show(i + (dx < 0 ? 1 : -1));
    });
    show(0); play();
  }

  /* ---------------- Offer popup (admin: Special offers) ---------------- */
  function initOfferPopup() {
    var pop = $('#offerPopup'); if (!pop) return;
    var key = 'csc_offer_seen', ids = pop.getAttribute('data-ids') || '';
    var slides = $$('.offer-slide', pop), n = 0, count = $('[data-offer-count]', pop);
    function show(k) {
      n = (k + slides.length) % slides.length;
      slides.forEach(function (s, j) { s.classList.toggle('is-active', j === n); });
      if (count) count.textContent = (n + 1) + ' / ' + slides.length;
    }
    var p = $('[data-offer-prev]', pop), nx = $('[data-offer-next]', pop);
    if (p) p.addEventListener('click', function () { show(n - 1); });
    if (nx) nx.addEventListener('click', function () { show(n + 1); });
    var seen = null; try { seen = sessionStorage.getItem(key); } catch (e) {}
    if (seen === ids) return;                       // already shown this visit
    setTimeout(function () {
      openModal(pop);
      try { sessionStorage.setItem(key, ids); } catch (e) {}
    }, 1200);
  }

  /* ---------------- Animated programme details ---------------- */
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text !== undefined) e.textContent = text; return e; }
  function link(cls, href, label, icon) {
    var a = el('a', cls); a.href = href; a.appendChild(document.createTextNode(label + ' '));
    if (icon) { var i = el('i', icon); a.appendChild(i); } return a;
  }
  function initQuickView() {
    var modal = $('#qvModal'), data = $('#qvData'); if (!modal || !data) return;
    var list = []; try { list = JSON.parse(data.textContent); } catch (e) { return; }
    var map = {}; list.forEach(function (p) { map[p.slug] = p; });
    var box = $('#qvContent'), idx = 0;
    function item(node) { node.classList.add('qv-item'); node.style.setProperty('--i', idx++); return node; }

    function build(p) {
      idx = 0; box.textContent = '';
      var head = el('div', 'qv-head');
      head.appendChild(item(el('span', 'qv-code' + (p.code.length > 8 ? ' qv-code--long' : ''), p.code)));
      var meta = el('div', 'qv-headtext');
      meta.appendChild(item(el('span', 'badge', p.level)));
      var h = item(el('h2', null, p.name)); h.id = 'qvTitle'; meta.appendChild(h);
      head.appendChild(meta); box.appendChild(head);

      var body = el('div', 'qv-body');
      var stats = item(el('div', 'qv-stats'));
      [[p.module_count, 'Modules'], [p.topic_count, 'Topics']].forEach(function (s) {
        var d = el('div'); d.appendChild(el('b', null, String(s[0]))); d.appendChild(el('span', null, s[1])); stats.appendChild(d);
      });
      body.appendChild(stats);

      function section(title, text) {
        if (!text) return;
        var s = item(el('div', 'qv-sec')); s.appendChild(el('h3', null, title)); s.appendChild(el('p', null, text)); body.appendChild(s);
      }
      section('Objective', p.objective);
      section('Overview', p.overview);
      section('Target audience', p.audience);
      section('Prerequisites', p.prerequisites);

      var cov = item(el('div', 'qv-sec')); cov.appendChild(el('h3', null, 'What you will study'));
      p.modules.forEach(function (m) {
        var g = el('div', 'qv-group'); g.appendChild(el('h4', null, m.section));
        var ul = el('ul', 'chips');
        m.names.forEach(function (nm, k) { var li = el('li', 'chip qv-chip', nm); li.style.setProperty('--c', k); ul.appendChild(li); });
        g.appendChild(ul); cov.appendChild(g);
      });
      body.appendChild(cov);

      if (p.tools && p.tools.length) {
        var t = item(el('div', 'qv-sec')); t.appendChild(el('h3', null, 'Tools & technologies'));
        var ul2 = el('ul', 'chips'); p.tools.forEach(function (x) { ul2.appendChild(el('li', 'chip', x)); });
        t.appendChild(ul2); body.appendChild(t);
      }
      var act = item(el('div', 'qv-actions'));
      act.appendChild(link('btn btn--primary', p.url, 'View full syllabus', 'fa-solid fa-arrow-right'));
      act.appendChild(link('btn btn--ghost', '#register', 'Register for SAT 2026'));
      body.appendChild(act);
      box.appendChild(body);
      var scroller = modal; scroller.scrollTop = 0; $('.qv-box', modal).scrollTop = 0;
    }

    $$('[data-quickview]').forEach(function (card) {
      card.addEventListener('click', function (e) {
        var p = map[card.getAttribute('data-quickview')]; if (!p) return;
        e.preventDefault(); build(p); openModal(modal);
      });
    });
    // "Register" inside the pop-up should close it and jump to the form
    modal.addEventListener('click', function (e) {
      var a = e.target.closest('a[href="#register"]');
      if (a) closeModal(modal);
    });
  }

  document.addEventListener('DOMContentLoaded', function () { initSlider(); initOfferPopup(); initQuickView(); });
})();
