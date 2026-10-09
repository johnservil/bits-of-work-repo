/* Page behavior: theme, contents, scrollspy, math, hero lattice. */
(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const D = window.SITE_DATA || {};

  // ---- theme toggle (stamps data-theme so it wins over the OS setting both ways)
  const root = document.documentElement;
  const isDark = () => root.dataset.theme ? root.dataset.theme === 'dark'
    : matchMedia('(prefers-color-scheme: dark)').matches;
  $('#theme-toggle').addEventListener('click', () => {
    root.dataset.theme = isDark() ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
    document.dispatchEvent(new CustomEvent('themechange'));
  });

  // ---- dates
  const gen = D.generated || '';
  $$('[data-generated]').forEach(el => { el.textContent = gen; });
  const dEl = $('[data-date]');
  if (dEl && gen) dEl.textContent = new Date(gen + 'T12:00:00').toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

  // ---- contents, rail, heading anchors
  const sections = $$('main .section');
  const toc = $('#toc-list'), rail = $('#rail');
  let n = 0;
  sections.forEach(sec => {
    const h2 = $('h2', sec), appendix = sec.classList.contains('appendix');
    const num = appendix ? 'A' : String(++n);
    h2.insertAdjacentHTML('beforeend', `<a class="anchor" href="#${sec.id}" aria-label="Link to section">#</a>`);
    toc.insertAdjacentHTML('beforeend',
      `<li class="top"><span class="n">${num}</span><a href="#${sec.id}">${h2.firstChild.textContent.trim()}</a><span class="leader"></span></li>`);
    let m = 0;
    $$('h3', sec).forEach(h3 => {
      const id = h3.id || (h3.id = sec.id + '-' + (++m));
      h3.insertAdjacentHTML('beforeend', `<a class="anchor" href="#${id}" aria-label="Link to subsection">#</a>`);
      toc.insertAdjacentHTML('beforeend',
        `<li class="sub"><span class="n">${num}.${m}</span><a href="#${id}">${h3.firstChild.textContent.trim()}</a><span class="leader"></span></li>`);
    });
    rail.insertAdjacentHTML('beforeend', `<a href="#${sec.id}" data-sec="${sec.id}">${num}<span>${sec.dataset.short || ''}</span></a>`);
  });
  // figure numbers in the contents' sense: list figures under their section
  $$('main figure.fig').forEach((f, i) => {
    const t = $('.fig-title', f);
    if (t) t.setAttribute('data-fignum', i + 1);
  });

  // ---- scrollspy
  const links = [...$$('#rail a'), ...$$('#topnav a')];
  const spy = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      links.forEach(a => a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  sections.forEach(s => spy.observe(s));
  const bar = $('#topbar');
  const onScroll = () => bar.classList.toggle('scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // ---- math
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [{ left: '$$', right: '$$', display: true }, { left: '\\(', right: '\\)', display: false }],
      ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option', 'svg'],
      throwOnError: false,
    });
  }

  // ---- bibtex copy
  const copy = $('#bibtex .copy');
  if (copy) copy.addEventListener('click', () => {
    const txt = $('#bibtex').innerText.replace(/^copy\s*/, '');
    navigator.clipboard && navigator.clipboard.writeText(txt).then(() => {
      copy.firstChild.textContent = 'copied'; setTimeout(() => (copy.firstChild.textContent = 'copy'), 1400);
    });
  });

  // ---- hero: Lagrange-Gauss reduction of a 2-D lattice basis, animated.
  // The lattice points never move; only the basis drawn on them changes.
  const svg = $('#hero-lattice');
  if (!svg) return;
  const NS = 'http://www.w3.org/2000/svg';
  const el = (tag, attrs, parent) => {
    const e = document.createElementNS(NS, tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    (parent || svg).appendChild(e); return e;
  };
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function gaussSteps(b1, b2) {
    const dot = (a, b) => a[0] * b[0] + a[1] * b[1];
    const steps = [[b1, b2]];
    for (let i = 0; i < 12; i++) {
      if (dot(b1, b1) > dot(b2, b2)) { [b1, b2] = [b2, b1]; }
      const mu = Math.round(dot(b1, b2) / dot(b1, b1));
      if (mu === 0) break;
      b2 = [b2[0] - mu * b1[0], b2[1] - mu * b1[1]];
      steps.push([b1, b2]);
    }
    return steps;
  }

  let frame = 0, raf = 0;
  function build() {
    cancelAnimationFrame(raf);
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    const W = svg.clientWidth || innerWidth, H = svg.clientHeight || 600;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    const u = Math.max(38, Math.min(64, W / 22));
    // short, reduced basis (pixels, y up) and a skewed basis for the same lattice
    const r1 = [u, 0.18 * u], r2 = [0.42 * u, 1.02 * u];
    const U = [[5, 3], [3, 2]];                      // unimodular, det = 1
    const s1 = [U[0][0] * r1[0] + U[0][1] * r2[0], U[0][0] * r1[1] + U[0][1] * r2[1]];
    const s2 = [U[1][0] * r1[0] + U[1][1] * r2[0], U[1][0] * r1[1] + U[1][1] * r2[1]];
    const steps = gaussSteps(s1, s2);
    const O = [W * 0.14, H * 0.82];
    const P = v => [O[0] + v[0], O[1] - v[1]];

    const gPts = el('g', { fill: 'var(--ink-3)' });
    const det = r1[0] * r2[1] - r1[1] * r2[0];
    const R = Math.ceil(Math.hypot(W, H) / Math.min(u, det / u)) + 2;
    for (let i = -R; i <= R; i++) for (let j = -R; j <= R; j++) {
      const p = P([i * r1[0] + j * r2[0], i * r1[1] + j * r2[1]]);
      if (p[0] < -10 || p[0] > W + 10 || p[1] < -10 || p[1] > H + 10) continue;
      el('circle', { cx: p[0].toFixed(1), cy: p[1].toFixed(1), r: (i === 0 && j === 0) ? 3.2 : 1.6, opacity: (i === 0 && j === 0) ? 1 : 0.55 }, gPts);
    }
    const defs = el('defs', {});
    const mk = el('marker', { id: 'arr', viewBox: '0 0 10 10', refX: 8.5, refY: 5, markerWidth: 7, markerHeight: 7, orient: 'auto-start-reverse' }, defs);
    el('path', { d: 'M0,1 L9,5 L0,9 Z', fill: 'var(--accent)' }, mk);
    const cell = el('path', { fill: 'var(--accent-wash)', stroke: 'var(--accent)', 'stroke-width': 0.6, 'stroke-dasharray': '3 3', opacity: 0.9 });
    const v1 = el('line', { stroke: 'var(--accent)', 'stroke-width': 1.8, 'marker-end': 'url(#arr)' });
    const v2 = el('line', { stroke: 'var(--accent)', 'stroke-width': 1.8, 'marker-end': 'url(#arr)' });
    const t1 = el('text', { 'font-family': 'var(--serif)', 'font-style': 'italic', 'font-weight': 700, 'font-size': 17, fill: 'var(--accent)' });
    const t2 = el('text', { 'font-family': 'var(--serif)', 'font-style': 'italic', 'font-weight': 700, 'font-size': 17, fill: 'var(--accent)' });
    t1.innerHTML = 'b<tspan font-size="12" dy="4" font-style="normal" font-weight="400">1</tspan>';
    t2.innerHTML = 'b<tspan font-size="12" dy="4" font-style="normal" font-weight="400">2</tspan>';
    const stepLbl = el('text', { x: W - 18, y: H - 18, 'text-anchor': 'end', 'font-family': 'var(--mono)', 'font-size': 11, fill: 'var(--ink-3)' });

    function draw(a, b, label) {
      const pa = P(a), pb = P(b), pab = P([a[0] + b[0], a[1] + b[1]]);
      cell.setAttribute('d', `M${O[0]},${O[1]} L${pa[0]},${pa[1]} L${pab[0]},${pab[1]} L${pb[0]},${pb[1]} Z`);
      for (const [ln, p] of [[v1, pa], [v2, pb]]) {
        ln.setAttribute('x1', O[0]); ln.setAttribute('y1', O[1]); ln.setAttribute('x2', p[0]); ln.setAttribute('y2', p[1]);
      }
      const off = (p, q) => { const d = Math.hypot(p[0] - O[0], p[1] - O[1]) || 1; return [p[0] + (p[0] - O[0]) / d * 14 + 4, p[1] + (p[1] - O[1]) / d * 14 + 5]; };
      const l1 = off(pa), l2 = off(pb);
      t1.setAttribute('x', l1[0]); t1.setAttribute('y', l1[1]);
      t2.setAttribute('x', l2[0]); t2.setAttribute('y', l2[1]);
      if (label != null) stepLbl.textContent = label;
    }
    const last = steps[steps.length - 1];
    if (W < 760) { [cell, v1, v2, t1, t2, stepLbl].forEach(n => n.remove()); return; }  // keep phones calm: dots only
    if (reduceMotion) { draw(last[0], last[1], 'Lagrange–Gauss reduced'); return; }

    // timeline: each reduction step eases over 1.3s, holds 0.5s; final basis holds 3s; then resets
    const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    const STEP = 1300, HOLD = 500, END = 3200;
    const total = (steps.length - 1) * (STEP + HOLD) + END + 900;
    let t0 = null;
    function tick(now) {
      if (t0 === null) t0 = now;
      const t = Math.max(0, now - t0) % total;
      const k = Math.floor(t / (STEP + HOLD));
      if (k < steps.length - 1) {
        const f = Math.min(1, (t - k * (STEP + HOLD)) / STEP), e = ease(f);
        const [a0, b0] = steps[k], [a1, b1] = steps[k + 1];
        // reduction swaps roles of b1/b2; interpolate the drawn vectors to the nearest successor
        const d = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]);
        const pair = d(a0, a1) + d(b0, b1) <= d(a0, b1) + d(b0, a1) ? [a1, b1] : [b1, a1];
        const lerp = (p, q) => [p[0] + (q[0] - p[0]) * e, p[1] + (q[1] - p[1]) * e];
        draw(lerp(a0, pair[0]), lerp(b0, pair[1]), `reduction step ${k + 1}/${steps.length - 1}`);
        svg.style.opacity = '';
      } else {
        draw(last[0], last[1], 'reduced basis');
        const f = t - (steps.length - 1) * (STEP + HOLD);   // fade out before the loop restarts
        svg.style.opacity = f > END ? String(0.9 * Math.max(0, 1 - (f - END) / 900)) : '';
      }
      raf = requestAnimationFrame(tick);
    }
    raf = requestAnimationFrame(tick);
  }
  build();
  let rt; addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(build, 200); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) cancelAnimationFrame(raf); else build(); });
})();
