/* Researcher explorer. All data comes from window.PEOPLE_DATA (assets/people-data.js).
   Same figure conventions as charts.js: pgfplots frame, inward ticks, serif labels, CSS-variable colours. */
(function () {
  const D = window.PEOPLE_DATA;
  if (!D || !window.d3) return;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  const Y0 = D.y0, Y1 = D.y1, NY = Y1 - Y0 + 1;
  const CLS = D.classes, CI = Object.fromEntries(CLS.map((c, i) => [c.key, i]));
  const MAIN = ['lattice', 'ecdlp', 'code', 'factoring', 'isogeny', 'mq'];
  const COLOR = { mlwe: 'lattice', lwe: 'lattice' };
  const col = k => `var(--s-${COLOR[k] || k})`;
  const SHORT = { lattice: 'Lattices', ecdlp: 'ECDLP', code: 'Codes', factoring: 'Factoring', isogeny: 'Isogenies', mq: 'Multivariate', mlwe: 'MLWE', lwe: 'Plain LWE' };
  const PEOPLE = D.people, PAPERS = D.papers;
  const f1 = v => d3.format(',.1f')(Math.round((v + 1e-9) * 10) / 10);
  const f2 = v => d3.format(',.2f')(v);
  const pct = v => d3.format('.0%')(v);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  $$('[data-generated]').forEach(el => { el.textContent = D.generated; });
  $$('[data-named-min]').forEach(el => { el.textContent = D.named_min; });
  $$('[data-ambiguous]').forEach(el => { el.textContent = D.ambiguous_withheld; });

  // person -> paper indices
  const byPerson = PEOPLE.map(() => []);
  PAPERS.forEach((p, j) => p.a.forEach(i => byPerson[i].push(j)));
  const label = i => {
    const p = PEOPLE[i];
    return p.n + (p.r === 'u' ? ' †' : '') + (p.h && p.pid ? ` [${p.pid}]` : '');
  };

  // ---------- per-field aggregates (cached) ----------
  const cache = {};
  function field(key) {
    if (cache[key]) return cache[key];
    const c = CI[key];
    const credit = new Map(), papers = new Map(), total = new Float64Array(NY), cells = new Map();
    let first = Y1;
    PAPERS.forEach((p, j) => {
      const w = p.w[c]; if (!(w > 0)) return;
      const t = p.y - Y0, n = p.a.length;
      total[t] += w; first = Math.min(first, p.y);
      p.a.forEach(i => {
        if (!credit.has(i)) { credit.set(i, new Float64Array(NY)); papers.set(i, new Float64Array(NY)); }
        credit.get(i)[t] += w / n; papers.get(i)[t] += w;
        const k = i * NY + t; (cells.get(k) || cells.set(k, []).get(k)).push(j);
      });
    });
    // average year of each person's credit in this field (for the "by period" order)
    const center = new Map();
    credit.forEach((a, i) => { let s = 0, m = 0; a.forEach((v, t) => { s += v; m += v * t; }); center.set(i, Y0 + m / s); });
    return (cache[key] = { key, c, credit, papers, total, cells, center, first: Math.max(first, Y0) });
  }
  const winSum = (a, lo, hi) => { let s = 0; for (let y = lo; y <= hi; y++) s += a[y - Y0]; return s; };

  // ---------- state (mirrored in the URL hash) ----------
  const S = { f: 'lattice', m: 'credit', lo: null, hi: null, rows: 30, sort: 'total', who: null };
  function readHash() {
    const h = new URLSearchParams(location.hash.slice(1));
    Object.assign(S, { f: 'lattice', m: 'credit', lo: null, hi: null, rows: 30, sort: 'total', who: null });
    if (CI[h.get('f')] !== undefined) S.f = h.get('f');
    if (['credit', 'papers'].includes(h.get('m'))) S.m = h.get('m');
    const w = (h.get('w') || '').match(/^(\d{4})-(\d{4})$/);
    if (w) { S.lo = Math.max(Y0, +w[1]); S.hi = Math.min(Y1, +w[2]); if (S.lo > S.hi) S.lo = S.hi = null; }
    if (['15', '30', '60'].includes(h.get('n'))) S.rows = +h.get('n');
    if (['total', 'time'].includes(h.get('s'))) S.sort = h.get('s');
    const who = h.get('p');
    S.who = who ? PEOPLE.findIndex(p => p.n && (p.pid || p.n) === who) : null;
    if (S.who < 0) S.who = null;
  }
  function writeHash() {
    const h = new URLSearchParams({ f: S.f, m: S.m });
    if (S.lo !== null) h.set('w', `${S.lo}-${S.hi}`);
    if (S.rows !== 30) h.set('n', S.rows);
    if (S.sort !== 'total') h.set('s', S.sort);
    if (S.who !== null) h.set('p', PEOPLE[S.who].pid || PEOPLE[S.who].n);
    history.replaceState(null, '', '#' + h.toString());
  }
  const win = F => [S.lo ?? F.first, S.hi ?? Y1];

  // ---------- shared chart plumbing ----------
  function tooltip(container) {
    let t = container.querySelector('.tip');
    if (!t) { t = document.createElement('div'); t.className = 'tip'; container.appendChild(t); }
    return {
      show(html, x, y) {
        t.innerHTML = html; t.classList.add('on');
        const cw = container.clientWidth, tw = t.offsetWidth, th = t.offsetHeight;
        let left = x + 16; if (left + tw > cw) left = x - tw - 16;
        t.style.left = Math.max(0, left) + 'px'; t.style.top = Math.max(0, y - th / 2) + 'px';
      },
      hide() { t.classList.remove('on'); },
    };
  }
  function xTicks(g, x, h, ticks, f, top = true) {
    ticks.forEach(v => {
      const k = g.append('g').attr('class', 'tick').attr('transform', `translate(${x(v)},0)`);
      k.append('line').attr('y1', h).attr('y2', h - 5);
      if (top) k.append('line').attr('y1', 0).attr('y2', 5);
      k.append('text').attr('y', h + 18).attr('text-anchor', 'middle').text(f(v));
    });
  }
  function yTicks(g, y, w, ticks, f) {
    g.insert('g', ':first-child').attr('class', 'grid').selectAll('line').data(ticks).join('line')
      .attr('x1', 0).attr('x2', w).attr('y1', d => y(d)).attr('y2', d => y(d));
    ticks.forEach(v => {
      const k = g.append('g').attr('class', 'tick').attr('transform', `translate(0,${y(v)})`);
      k.append('line').attr('x1', 0).attr('x2', 5);
      k.append('line').attr('x1', w).attr('x2', w - 5);
      k.append('text').attr('x', -8).attr('dy', '0.32em').attr('text-anchor', 'end').text(f(v));
    });
  }
  const yearStep = (n, w) => [1, 2, 5, 10, 20].find(s => (n / s) * 38 < w) || 20;
  const yearTicks = (a, b, w) => { const s = yearStep(b - a, w); return d3.range(Math.ceil(a / s) * s, b + 1, s); };
  function saveSVG(svg, name) {
    const clone = svg.cloneNode(true);
    const src = svg.querySelectorAll('*'), dst = clone.querySelectorAll('*');
    const props = ['fill', 'fill-opacity', 'stroke', 'stroke-width', 'opacity', 'font-family', 'font-size', 'font-style', 'font-weight', 'stroke-dasharray'];
    src.forEach((n, i) => { const cs = getComputedStyle(n); dst[i].setAttribute('style', props.map(p => `${p}:${cs.getPropertyValue(p)}`).join(';')); });
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    clone.insertAdjacentHTML('afterbegin', `<rect width="100%" height="100%" fill="${getComputedStyle(document.body).backgroundColor}"/>`);
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([clone.outerHTML], { type: 'image/svg+xml' }));
    a.download = name + '.svg'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  }
  function wireFoot(fig, getTable) {
    const tb = fig.querySelector('[data-table]'), sv = fig.querySelector('[data-png]');
    let box = null;
    const fill = () => {
      const [head, rows] = getTable();
      box.innerHTML = `<table class="booktabs"><thead><tr>${head.map(h => `<th>${h}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>`;
    };
    tb.addEventListener('click', () => {
      if (!box) { box = document.createElement('div'); box.className = 'datatable'; fig.querySelector('.fig-foot').after(box); }
      fill(); box.classList.toggle('on');
      tb.textContent = box.classList.contains('on') ? 'hide data' : 'show data';
    });
    sv.addEventListener('click', () => saveSVG(fig.querySelector('.chart svg'), fig.id));
    return () => { if (box && box.classList.contains('on')) fill(); };
  }
  function seg(name, initial, onChange) {
    const el = $(`.seg[data-ctl="${name}"]`);
    const set = v => el.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === String(v)));
    set(initial);
    el.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; set(b.dataset.v); onChange(b.dataset.v); });
    return set;
  }

  // ---------- field chips, measure, search ----------
  const chips = $('#fields');
  chips.innerHTML = CLS.map(c => `<button class="chip${COLOR[c.key] ? ' sub' : ''}" data-f="${c.key}" aria-pressed="false"><i style="background:${col(c.key)}"></i>${esc(SHORT[c.key])}</button>`).join('');
  chips.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || b.dataset.f === S.f) return;
    S.f = b.dataset.f; S.lo = S.hi = null; renderAll();
  });
  const setMetric = seg('metric', S.m, v => { S.m = v; renderAll(); });
  const setRows = seg('rows', S.rows, v => { S.rows = +v; renderAll(); });
  const setSort = seg('sort', S.sort, v => { S.sort = v; renderAll(); });
  const named = PEOPLE.map((p, i) => i).filter(i => PEOPLE[i].n).sort((a, b) => label(a).localeCompare(label(b)));
  $('#who-list').innerHTML = named.map(i => `<option value="${esc(label(i))}">`).join('');
  const byLabel = new Map(named.map(i => [label(i), i]));
  $('#who').addEventListener('change', e => {
    const i = byLabel.get(e.target.value.trim());
    if (i !== undefined) { openProfile(i); e.target.value = ''; }
  });
  $('#win-all').addEventListener('click', () => { S.lo = S.hi = null; renderAll(); });

  // ---------- figure 1: output per year with a brushable window ----------
  const figW = $('#fig-window'), chartW = $('.chart', figW);
  function renderWindow(F) {
    const W = chartW.clientWidth, H = 150, m = { t: 8, r: 12, b: 30, l: 44 };
    if (W < 240) return;
    const w = W - m.l - m.r, h = H - m.t - m.b;
    const years = d3.range(F.first, Y1 + 1);
    const x = d3.scaleBand().domain(years).range([0, w]).paddingInner(0.18);
    const ymax = d3.max(years, y => F.total[y - Y0]) || 1;
    const y = d3.scaleLinear().domain([0, ymax]).nice(4).range([h, 0]);
    const [lo, hi] = win(F);
    chartW.innerHTML = '';
    const svg = d3.select(chartW).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img')
      .attr('aria-label', `${SHORT[S.f]} paper credit per year, ${F.first} to ${Y1}`);
    const g = svg.append('g').attr('transform', `translate(${m.l},${m.t})`);
    yTicks(g, y, w, y.ticks(4), d3.format(',~g'));
    g.append('g').selectAll('rect').data(years).join('rect')
      .attr('x', d => x(d)).attr('width', x.bandwidth()).attr('y', d => y(F.total[d - Y0])).attr('height', d => h - y(F.total[d - Y0]))
      .attr('fill', col(S.f)).attr('fill-opacity', d => d >= lo && d <= hi ? (d === Y1 ? 0.55 : 0.9) : 0.22);
    g.append('rect').attr('class', 'frame').attr('width', w).attr('height', h);
    const xt = g.append('g');
    xTicks(xt, v => x(v) + x.bandwidth() / 2, h, yearTicks(F.first, Y1, w), v => v === Y1 ? v + '*' : v, false);
    g.append('text').attr('class', 'axis-label').attr('transform', `translate(${-34},${h / 2}) rotate(-90)`).attr('text-anchor', 'middle').text('paper credit');
    // brush snaps to whole years
    const step = x.step(), inv = px => years[Math.max(0, Math.min(years.length - 1, Math.floor((px + step * x.paddingInner() / 2) / step)))];
    const brush = d3.brushX().extent([[0, 0], [w, h]]).on('end', ev => {
      if (!ev.sourceEvent) return;
      if (!ev.selection) { S.lo = S.hi = null; renderAll(); return; }
      const a = inv(ev.selection[0]), b = inv(ev.selection[1] - 1);
      if (a === F.first && b === Y1) { S.lo = S.hi = null; } else { S.lo = a; S.hi = b; }
      renderAll();
    });
    const bg = g.append('g').attr('class', 'brush').call(brush);
    if (S.lo !== null) bg.call(brush.move, [x(lo), x(hi) + x.bandwidth()]);
    $('#win-label').textContent = S.lo === null ? `· all years, ${F.first}–${Y1}` : `· ${lo}–${hi}`;
    $('#win-all').hidden = S.lo === null;
  }

  // ---------- ranking within the window ----------
  function ranked(F) {
    const [lo, hi] = win(F);
    const src = S.m === 'credit' ? F.credit : F.papers;
    const all = [];
    F.credit.forEach((a, i) => {
      const cr = winSum(a, lo, hi); if (!(cr > 0)) return;
      let np = 0; for (let y = lo; y <= hi; y++) np += (F.cells.get(i * NY + y - Y0) || []).length;
      all.push({ i, credit: cr, v: winSum(src.get(i), lo, hi), np });
    });
    all.sort((a, b) => b.v - a.v || b.credit - a.credit);
    return all;
  }

  // ---------- stats strip ----------
  function renderStats(F, all) {
    const [lo, hi] = win(F);
    const tot = d3.sum(all, d => d.credit), byCredit = all.map(d => d.credit).sort((a, b) => b - a);
    const top10 = d3.sum(byCredit.slice(0, 10)) / (tot || 1);
    const one = all.filter(d => d.np === 1).length / (all.length || 1);
    const nNamed = all.filter(d => PEOPLE[d.i].n).length;
    const papers = new Set(); for (let y = lo; y <= hi; y++) F.credit.forEach((_, i) => (F.cells.get(i * NY + y - Y0) || []).forEach(j => papers.add(j)));
    $('#stats').innerHTML = [
      [d3.format(',')(all.length), 'contributors', `${d3.format(',')(nNamed)} named here`],
      [f1(tot), 'paper credit', `${d3.format(',')(papers.size)} papers`],
      [pct(top10), 'held by top 10', 'share of paper credit'],
      [pct(one), 'wrote one paper', 'in this field and period'],
    ].map(([v, k, s]) => `<div class="keyfig"><div class="v">${v}</div><div class="k"><span class="caps">${k}</span>${s}</div></div>`).join('');
  }

  // ---------- figure 2: researcher x year heatmap ----------
  const figH = $('#fig-heat'), chartH = $('.chart', figH);
  const tipH = tooltip(chartH);
  let heatRows = [];
  const refreshHeatTable = wireFoot(figH, () => [
    ['Rank', 'Researcher', S.m === 'credit' ? 'Paper credit' : 'Papers', 'Papers (whole)', 'Active in field'],
    heatRows.filter(r => r.i !== null).map((r, k) => {
      const yrs = [...(F_cur().credit.get(r.i) || [])].map((v, t) => v > 0 ? Y0 + t : 0).filter(Boolean);
      return [k + 1, esc(label(r.i)), f2(r.v), r.np, `${d3.min(yrs)}–${d3.max(yrs)}`];
    }),
  ]);
  const F_cur = () => field(S.f);

  function renderHeat(F, all) {
    const [lo, hi] = win(F);
    const src = S.m === 'credit' ? F.credit : F.papers;
    const top = all.filter(d => PEOPLE[d.i].n).slice(0, S.rows);
    if (S.sort === 'time') top.sort((a, b) => F.center.get(a.i) - F.center.get(b.i));
    const inTop = new Set(top.map(d => d.i));
    const rest = new Float64Array(NY);
    src.forEach((a, i) => { if (!inTop.has(i)) a.forEach((v, t) => { rest[t] += v; }); });
    const nRest = all.length - top.length;
    const restV = winSum(rest, lo, hi);
    heatRows = [...top.map(d => ({ i: d.i, v: d.v, np: d.np, a: src.get(d.i) })), { i: null, v: restV, a: rest, n: nRest }];

    const W = chartH.clientWidth, narrow = W < 560;
    if (W < 240) return;
    const nameW = narrow ? 112 : 176, barW = narrow ? 54 : 96, gap = 10, rowH = 17, m = { t: 24, b: 30 };
    // columns span the period plus the shown people's activity, not the field's sparse early years
    // in all-years mode start where the field reaches 2% of its cumulative credit (or earlier, if a shown person did)
    let ya = lo;
    if (S.lo === null) { let c = 0; const tot = d3.sum(F.total); for (ya = F.first; ya < Y1 && (c += F.total[ya - Y0]) < 0.02 * tot; ya++); }
    top.forEach(d => { const a = src.get(d.i); for (let t = 0; t < NY; t++) if (a[t] > 0) { ya = Math.min(ya, Y0 + t); break; } });
    const years = d3.range(ya, Y1 + 1);
    const gw = W - nameW - barW - gap * 2;
    const x = d3.scaleBand().domain(years).range([0, gw]).paddingInner(years.length > 40 ? 0.08 : 0.12);
    const H = m.t + heatRows.length * rowH + 6 + m.b;
    const vmax = d3.max(top, d => d3.max(years, y => src.get(d.i)[y - Y0])) || 1;
    const op = d3.scaleSqrt().domain([0, vmax]).range([0.1, 1]).clamp(true);
    const opRest = d3.scaleSqrt().domain([0, d3.max(years, y => rest[y - Y0]) || 1]).range([0.1, 1]);
    const bmax = d3.max(heatRows.slice(0, -1), r => r.v) || 1;
    const bx = d3.scaleLinear().domain([0, bmax]).range([0, barW - (narrow ? 4 : 34)]);
    const rowY = k => m.t + k * rowH + (k === heatRows.length - 1 ? 6 : 0);

    chartH.querySelector('svg')?.remove();
    const svg = d3.select(chartH).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img')
      .attr('aria-label', `Top ${top.length} contributors to ${SHORT[S.f]}, ${lo} to ${hi}, by year`);
    const g = svg.append('g').attr('transform', `translate(${nameW + gap},0)`);
    // period bracket
    const px0 = x(lo), px1 = x(hi) + x.bandwidth();
    if (S.lo !== null) g.append('rect').attr('class', 'win-band').attr('x', px0 - 2).attr('width', px1 - px0 + 4).attr('y', m.t - 6).attr('height', H - m.t - m.b + 8);
    if (S.lo !== null) g.append('text').attr('class', 'win-cap').attr('x', (px0 + px1) / 2).attr('y', m.t - 10).attr('text-anchor', 'middle')
      .text(`${lo}–${hi}`);

    const rows = svg.append('g').selectAll('g.hrow').data(heatRows).join('g')
      .attr('class', d => 'hrow' + (d.i === null ? ' rest' : '') + (d.i !== null && d.i === S.who ? ' sel' : ''))
      .attr('transform', (d, k) => `translate(0,${rowY(k)})`);
    rows.append('rect').attr('class', 'hrow-bg').attr('x', 0).attr('width', W).attr('height', rowH);
    const nm = rows.append('text').attr('class', 'hname').attr('x', nameW).attr('y', rowH / 2).attr('dy', '0.34em').attr('text-anchor', 'end')
      .text(d => d.i === null ? `everyone else (${d3.format(',')(d.n)})` : label(d.i))
      .each(function () { // truncate to the name column
        let t = this.textContent; while (this.getComputedTextLength() > nameW - 4 && t.length > 4) { t = t.slice(0, -2); this.textContent = t + '…'; }
      });
    nm.filter(d => d.i !== null).attr('tabindex', 0).attr('role', 'button')
      .on('click', (e, d) => openProfile(d.i))
      .on('keydown', (e, d) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openProfile(d.i); } });
    nm.append('title').text(d => d.i === null ? 'All other contributors, including people with too few papers to be named' : label(d.i));

    const cells = rows.append('g').attr('transform', `translate(${nameW + gap},0)`);
    cells.each(function (d) {
      const data = years.map(y => ({ y, v: d.a[y - Y0] })).filter(c => c.v > 0);
      d3.select(this).selectAll('rect').data(data).join('rect')
        .attr('class', c => 'hcell' + (c.y < lo || c.y > hi ? ' out' : ''))
        .attr('x', c => x(c.y)).attr('y', 1.5).attr('width', x.bandwidth()).attr('height', rowH - 3)
        .attr('fill', col(S.f)).attr('fill-opacity', c => (d.i === null ? opRest : op)(c.v));
    });
    // right-hand totals
    const bars = rows.append('g').attr('transform', `translate(${nameW + gap + gw + gap},0)`);
    bars.filter(d => d.i !== null).append('rect').attr('class', 'hbar').attr('y', 4).attr('height', rowH - 8)
      .attr('width', d => Math.max(1, bx(d.v))).attr('fill', col(S.f));
    if (!narrow) bars.append('text').attr('class', 'hval').attr('x', d => d.i === null ? 0 : bx(d.v) + 4).attr('y', rowH / 2).attr('dy', '0.34em')
      .text(d => f1(d.v));

    // axis
    const ax = svg.append('g').attr('transform', `translate(${nameW + gap},${H - m.b})`);
    ax.append('line').attr('class', 'haxis').attr('x2', gw);
    yearTicks(ya, Y1, gw).forEach(v => {
      const k = ax.append('g').attr('class', 'tick').attr('transform', `translate(${x(v) + x.bandwidth() / 2},0)`);
      k.append('line').attr('y2', 4);
      k.append('text').attr('y', 18).attr('text-anchor', 'middle').text(v === Y1 ? v + '*' : v);
    });
    svg.append('text').attr('class', 'hhead').attr('x', nameW + gap + gw + gap).attr('y', m.t - 10)
      .text(narrow ? 'period' : (S.m === 'credit' ? 'credit in period' : 'papers in period'));

    // hover: one tooltip for the whole grid
    const gx = nameW + gap;
    svg.on('mousemove', ev => {
      const [mx, my] = d3.pointer(ev);
      const k = heatRows.findIndex((_, j) => my >= rowY(j) && my < rowY(j) + rowH);
      const yi = Math.floor((mx - gx) / x.step());
      if (k < 0 || yi < 0 || yi >= years.length) { tipH.hide(); return; }
      const r = heatRows[k], yr = years[yi], v = r.a[yr - Y0];
      if (!(v > 0)) { tipH.hide(); return; }
      let body = '';
      if (r.i !== null) {
        const ps = (F.cells.get(r.i * NY + yr - Y0) || []).map(j => PAPERS[j]);
        body = ps.slice(0, 4).map(p => `<div class="t-paper">${esc(p.t)}</div>`).join('') + (ps.length > 4 ? `<div class="t-more">and ${ps.length - 4} more</div>` : '');
      }
      tipH.show(`<div class="t-head">${esc(r.i === null ? 'Everyone else' : label(r.i))}, ${yr}${yr === Y1 ? ' (partial)' : ''}</div>
        <div class="row"><span>${S.m === 'credit' ? 'paper credit' : 'papers'}</span><span class="val">${f2(v)}</span></div>${body}`, mx, my);
    }).on('mouseleave', () => tipH.hide());
    refreshHeatTable();
  }

  // ---------- figure 3: concentration over time ----------
  const figC = $('#fig-conc'), chartC = $('.chart', figC);
  const tipC = tooltip(chartC);
  let concRows = [];
  const refreshConcTable = wireFoot(figC, () => [
    ['Window', 'Contributors', 'Paper credit', 'Top 10', 'Next 40', 'Everyone else'],
    concRows.map(r => [`${r.y - 2}–${Math.min(r.y + 2, Y1)}`, r.n, f1(r.tot), pct(r.s[0]), pct(r.s[1]), pct(r.s[2])]),
  ]);
  function concentration(F) {
    const out = [];
    for (let y = F.first + 2; y <= Y1; y++) {
      const lo = y - 2, hi = Math.min(y + 2, Y1);
      const v = []; F.credit.forEach(a => { const s = winSum(a, lo, hi); if (s > 0) v.push(s); });
      v.sort((a, b) => b - a);
      const tot = d3.sum(v); if (tot < 3) continue;
      const a = d3.sum(v.slice(0, 10)) / tot, b = d3.sum(v.slice(10, 50)) / tot;
      out.push({ y, n: v.length, tot, s: [a, b, 1 - a - b] });
    }
    return out;
  }
  function renderConc(F) {
    concRows = concentration(F);
    chartC.querySelectorAll('svg, .conc-key').forEach(n => n.remove());
    if (concRows.length < 2) { refreshConcTable(); return; }
    if (chartC.clientWidth < 240) return;
    const W = chartC.clientWidth, H = Math.round(Math.min(300, Math.max(210, W * 0.36))), m = { t: 10, r: W < 560 ? 12 : 104, b: 32, l: 46 };
    const w = W - m.l - m.r, h = H - m.t - m.b;
    const x = d3.scaleLinear().domain([concRows[0].y, concRows[concRows.length - 1].y]).range([0, w]);
    const y = d3.scaleLinear().domain([0, 1]).range([h, 0]);
    const svg = d3.select(chartC).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img')
      .attr('aria-label', `Share of ${SHORT[S.f]} paper credit held by the top 10 and next 40 contributors, by five-year window`);
    const g = svg.append('g').attr('transform', `translate(${m.l},${m.t})`);
    const [lo, hi] = win(F);
    if (S.lo !== null) {
      const a = Math.max(lo, x.domain()[0]), b = Math.min(hi, x.domain()[1]);
      if (b >= a) g.append('rect').attr('class', 'win-band').attr('x', x(a) - (a === b ? 2 : 0)).attr('width', Math.max(4, x(b) - x(a))).attr('y', 0).attr('height', h);
    }
    const bands = [
      { k: 0, label: 'top 10', op: 0.85 }, { k: 1, label: 'next 40', op: 0.45 }, { k: 2, label: 'everyone else', op: 0.14 },
    ];
    const lower = (d, k) => d3.sum(d.s.slice(0, k));
    bands.forEach(b => {
      g.append('path').attr('fill', col(S.f)).attr('fill-opacity', b.op)
        .attr('d', d3.area().x(d => x(d.y)).y0(d => y(lower(d, b.k))).y1(d => y(lower(d, b.k + 1))).curve(d3.curveMonotoneX)(concRows));
    });
    yTicks(g, y, w, [0, 0.25, 0.5, 0.75, 1], d3.format('.0%'));
    g.select('.grid').raise().attr('opacity', 0.6);
    g.append('rect').attr('class', 'frame').attr('width', w).attr('height', h);
    const xt = g.append('g'); xTicks(xt, x, h, yearTicks(x.domain()[0], x.domain()[1], w), String);
    // direct labels at the right edge
    const last = concRows[concRows.length - 1];
    if (W >= 560) bands.forEach(b => {
      const mid = (lower(last, b.k) + lower(last, b.k + 1)) / 2;
      g.append('text').attr('class', 'dlabel').attr('x', w + 8).attr('y', y(mid)).attr('dy', '0.34em').text(b.label);
    });
    else d3.select(chartC).append('div').attr('class', 'conc-key').html(bands.map(b =>
      `<span><i style="background:${col(S.f)};opacity:${Math.max(b.op, 0.25)}"></i>${b.label}</span>`).join(''));
    const cross = g.append('line').attr('class', 'crosshair').attr('y1', 0).attr('y2', h).attr('opacity', 0);
    g.append('rect').attr('width', w).attr('height', h).attr('fill', 'transparent')
      .on('mousemove', ev => {
        const [mx] = d3.pointer(ev);
        const yr = Math.round(x.invert(mx)), d = concRows.reduce((p, c) => Math.abs(c.y - yr) < Math.abs(p.y - yr) ? c : p);
        cross.attr('x1', x(d.y)).attr('x2', x(d.y)).attr('opacity', 1);
        tipC.show(`<div class="t-head">${d.y - 2}–${Math.min(d.y + 2, Y1)}</div>` +
          bands.map(b => `<div class="row"><span class="sw" style="background:${col(S.f)};opacity:${Math.max(b.op, 0.25)}"></span>${b.label}<span class="val">${pct(d.s[b.k])}</span></div>`).join('') +
          `<div class="row"><span>contributors</span><span class="val">${d3.format(',')(d.n)}</span></div>`, x(d.y) + m.l, d3.pointer(ev, chartC)[1]);
      })
      .on('mouseleave', () => { cross.attr('opacity', 0); tipC.hide(); });
    refreshConcTable();
  }

  // ---------- co-author groups ----------
  // Group = connected component of the co-author graph on the field's papers in [lo, hi].
  function groups(c, lo, hi) {
    const par = new Map(), credit = new Map(), links = new Map();
    const find = x => { while (par.get(x) !== x) { par.set(x, par.get(par.get(x))); x = par.get(x); } return x; };
    let papers = 0;
    PAPERS.forEach(p => {
      if (!(p.w[c] > 0) || p.y < lo || p.y > hi) return;
      papers++;
      const n = p.a.length;
      p.a.forEach(a => { if (!par.has(a)) par.set(a, a); credit.set(a, (credit.get(a) || 0) + p.w[c] / n); });
      for (let u = 0; u < n; u++) for (let v = u + 1; v < n; v++) {
        const a = Math.min(p.a[u], p.a[v]), b = Math.max(p.a[u], p.a[v]), k = a * 1e5 + b;
        links.set(k, (links.get(k) || 0) + 1);
        par.set(find(a), find(b));
      }
    });
    const byRoot = new Map();
    par.forEach((_, x) => { const r = find(x); (byRoot.get(r) || byRoot.set(r, []).get(r)).push(x); });
    const tot = d3.sum([...credit.values()]) || 1;
    const list = [...byRoot.values()].map(m => ({ m, credit: d3.sum(m, x => credit.get(x)) }))
      .sort((a, b) => b.credit - a.credit || b.m.length - a.m.length);
    list.forEach((g, k) => { g.k = k; g.share = g.credit / tot; });
    const of = new Map(); list.forEach(g => g.m.forEach(x => of.set(x, g)));
    const eff = 1 / (d3.sum(list, g => g.share * g.share) || 1);
    return { list, of, links, credit, tot, eff, papers, people: par.size };
  }
  const linkKey = (a, b) => Math.min(a, b) * 1e5 + Math.max(a, b);

  // ---------- figure 4: network of the top contributors in the period ----------
  const figN = $('#fig-net'), chartN = $('.chart', figN);
  const tipN = tooltip(chartN);
  let netGroups = null;
  const refreshNetTable = wireFoot(figN, () => [
    ['Group', 'People', 'Share of credit', 'Named members (by credit in period)'],
    (netGroups ? netGroups.list.filter(g => g.m.length > 1).slice(0, 40) : []).map(g => [g.k + 1, g.m.length, pct(g.share),
      g.m.filter(x => PEOPLE[x].n).sort((a, b) => netGroups.credit.get(b) - netGroups.credit.get(a)).map(x => esc(label(x))).join(', ') || '—']),
  ]);
  function renderNet(F, all) {
    const [lo, hi] = win(F);
    const G = netGroups = groups(F.c, lo, hi);
    chartN.querySelector('svg')?.remove();
    const W = chartN.clientWidth; if (W < 240) return;
    const top = all.filter(d => PEOPLE[d.i].n).slice(0, S.rows);
    const H = Math.round(Math.max(380, Math.min(680, W * (S.rows > 30 ? 0.8 : 0.66))));
    const nodes = top.map(d => ({ i: d.i, v: G.credit.get(d.i) || 0, g: G.of.get(d.i) }));
    const idx = new Map(nodes.map((n, k) => [n.i, k]));
    const links = [];
    for (let u = 0; u < nodes.length; u++) for (let v = u + 1; v < nodes.length; v++) {
      const n = G.links.get(linkKey(nodes[u].i, nodes[v].i));
      if (n) links.push({ source: u, target: v, n });
    }
    const deg = new Map(); links.forEach(l => { deg.set(l.source, (deg.get(l.source) || 0) + 1); deg.set(l.target, (deg.get(l.target) || 0) + 1); });
    const r = d3.scaleSqrt().domain([0, d3.max(nodes, n => n.v) || 1]).range([2.5, W < 560 ? 11 : 15]);
    // deterministic layout: d3-force starts from a fixed phyllotaxis arrangement
    const sim = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).distance(l => 58 + 14 / l.n).strength(l => Math.min(0.9, 0.25 + 0.12 * l.n)))
      .force('charge', d3.forceManyBody().strength(-210).distanceMax(320))
      .force('collide', d3.forceCollide(n => r(n.v) + 9).strength(0.9))
      .force('x', d3.forceX(0).strength(n => deg.has(idx.get(n.i)) ? 0.04 : 0.2))
      .force('y', d3.forceY(0).strength(n => deg.has(idx.get(n.i)) ? 0.07 : 0.25))
      .stop();
    for (let t = 0; t < 320; t++) sim.tick();
    const pad = 16, labW = W < 560 ? 0 : 110;
    const xs = d3.extent(nodes, n => n.x), ys = d3.extent(nodes, n => n.y);
    const k = Math.min((W - 2 * pad - labW) / ((xs[1] - xs[0]) || 1), (H - 2 * pad) / ((ys[1] - ys[0]) || 1), 1.3);
    const ox = (W - labW - k * (xs[0] + xs[1])) / 2, oy = (H - k * (ys[0] + ys[1])) / 2;
    nodes.forEach(n => { n.px = ox + k * n.x; n.py = oy + k * n.y; });

    const svg = d3.select(chartN).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img')
      .attr('aria-label', `Co-authorship among the top ${nodes.length} ${SHORT[S.f]} contributors, ${lo} to ${hi}`);
    svg.append('rect').attr('class', 'frame').attr('width', W).attr('height', H);
    const lw = d3.scaleLinear().domain([1, d3.max(links, l => l.n) || 1]).range([0.8, 3.2]);
    const L = svg.append('g').selectAll('line').data(links).join('line').attr('class', 'nlink')
      .attr('x1', l => l.source.px).attr('y1', l => l.source.py).attr('x2', l => l.target.px).attr('y2', l => l.target.py)
      .attr('stroke-width', l => lw(l.n));
    const big = G.list[0];
    const N = svg.append('g').selectAll('g').data(nodes).join('g').attr('class', n => 'nnode' + (n.i === S.who ? ' sel' : ''))
      .attr('transform', n => `translate(${n.px},${n.py})`).attr('tabindex', 0).attr('role', 'button')
      .attr('aria-label', n => `${label(n.i)}: open profile`);
    N.append('circle').attr('r', n => r(n.v))
      .attr('class', n => n.g && n.g.m.length === 1 ? 'solo' : n.g === big ? 'big' : 'other')
      .style('fill', n => n.g === big && big.m.length > 1 ? col(S.f) : null);
    const nLabels = W < 560 ? 12 : S.rows > 30 ? 30 : nodes.length;
    const labelled = new Set(nodes.slice().sort((a, b) => b.v - a.v).slice(0, nLabels).map(n => n.i));
    N.filter(n => labelled.has(n.i)).append('text').attr('class', 'nlabel').attr('x', n => r(n.v) + 3).attr('dy', '0.34em')
      .text(n => label(n.i));
    // greedy label placement, largest first: right of the node, else left, else leave it to the tooltip
    const placed = [];
    const hit = b => placed.some(q => b.x < q.x + q.w && q.x < b.x + b.w && b.y < q.y + q.h && q.y < b.y + b.h)
      || nodes.some(m => { const rr = r(m.v); return m.px + rr > b.x && m.px - rr < b.x + b.w && m.py + rr > b.y && m.py - rr < b.y + b.h; });
    N.filter(n => labelled.has(n.i)).sort((a, b) => b.v - a.v).each(function (n) {
      const t = this.querySelector('text'), bb = t.getBBox(), rr = r(n.v);
      const cands = [
        { x: n.px + rr + 3, y: n.py + bb.y, tx: rr + 3, ty: 0, a: 'start' },
        { x: n.px - rr - 3 - bb.width, y: n.py + bb.y, tx: -rr - 3, ty: 0, a: 'end' },
        { x: n.px - bb.width / 2, y: n.py - rr - 2 - bb.height, tx: 0, ty: -rr - 2 - bb.height / 2, a: 'middle' },
        { x: n.px - bb.width / 2, y: n.py + rr + 2, tx: 0, ty: rr + 2 + bb.height / 2, a: 'middle' },
      ].map(q => ({ ...q, w: bb.width, h: bb.height }));
      const q = cands.find(q => q.x >= 2 && q.x + q.w <= W - 2 && q.y >= 2 && q.y + q.h <= H - 2 && !hit(q));
      if (q) { placed.push(q); t.setAttribute('x', q.tx); t.setAttribute('y', q.ty); t.setAttribute('text-anchor', q.a); }
      else t.remove();
    });
    const nb = new Map(nodes.map((_, k) => [k, new Set([k])]));
    links.forEach(l => { nb.get(l.source.index).add(l.target.index); nb.get(l.target.index).add(l.source.index); });
    N.on('mouseenter focus', (e, n) => {
      const s = nb.get(n.index);
      N.classed('dim', m => !s.has(m.index)); L.classed('dim', l => l.source !== n && l.target !== n).classed('hi', l => l.source === n || l.target === n);
      const g = n.g;
      tipN.show(`<div class="t-head">${esc(label(n.i))}</div>
        <div class="row"><span>paper credit, ${lo}–${hi}</span><span class="val">${f2(n.v)}</span></div>
        <div class="row"><span>co-authors shown here</span><span class="val">${s.size - 1}</span></div>
        <div class="row"><span>${g && g.m.length > 1 ? `group ${g.k + 1}: people` : 'no co-author in period'}</span><span class="val">${g && g.m.length > 1 ? g.m.length : ''}</span></div>
        ${g && g.m.length > 1 ? `<div class="row"><span>group's share of credit</span><span class="val">${pct(g.share)}</span></div>` : ''}`, n.px, n.py);
    }).on('mouseleave blur', () => { N.classed('dim', false); L.classed('dim', false).classed('hi', false); tipN.hide(); })
      .on('click', (e, n) => openProfile(n.i))
      .on('keydown', (e, n) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openProfile(n.i); } });

    $('#net-key').innerHTML = `<span><i class="k-big" style="background:${col(S.f)}"></i>largest group (${pct(big ? big.share : 0)} of credit)</span>
      <span><i class="k-other"></i>other groups</span><span><i class="k-solo"></i>no co-author in period</span>`;
    // groups table
    const multi = G.list.filter(g => g.m.length > 1), solo = G.list.length - multi.length;
    const named = g => g.m.filter(x => PEOPLE[x].n).sort((a, b) => G.credit.get(b) - G.credit.get(a));
    $('#groups').innerHTML = `<p class="groups-sum"><strong>${d3.format(',')(G.list.length)}</strong> groups among
      ${d3.format(',')(G.people)} contributors: ${d3.format(',')(multi.length)} with two or more people, and ${d3.format(',')(solo)}
      people with no co-author in this field and period. Effective number of groups: <strong>${G.eff.toFixed(1)}</strong>.</p>
      <table class="booktabs gtab"><thead><tr><th>Group</th><th>People</th><th>Credit</th><th>Best-known members</th></tr></thead><tbody>
      ${multi.slice(0, 6).map(g => {
        const nm = named(g);
        return `<tr><td>${g.k + 1}</td><td>${g.m.length}</td><td>${pct(g.share)}</td><td class="gm">${nm.slice(0, 4).map(x =>
          `<button class="bibbtn" data-p="${x}">${esc(label(x))}</button>`).join(', ') || '<span class="muted">(none named)</span>'}${nm.length > 4 ? `<span class="muted"> and ${g.m.length - 4} more</span>` : g.m.length > nm.length ? `<span class="muted"> and ${g.m.length - nm.length} not named</span>` : ''}</td></tr>`;
      }).join('')}</tbody></table>`;
    $$('#groups [data-p]').forEach(b => b.addEventListener('click', () => openProfile(+b.dataset.p)));
    refreshNetTable();
  }

  // ---------- figure 5: connectivity over time, all fields ----------
  const figK = $('#fig-conn'), chartK = $('.chart', figK);
  const tipK = tooltip(chartK);
  let connMode = 'eff', connKeys = [];
  seg('conn', connMode, v => { connMode = v; renderConn(field(S.f)); refreshConnTable(); });
  function connectivity(F) {
    if (F.conn) return F.conn;
    const out = [];
    for (let y = Y0 + 2; y <= Y1 - 2; y++) {   // full windows only: shorter ones split groups artificially
      const G = groups(F.c, y - 2, y + 2);
      if (G.papers >= 8) out.push({ y, eff: G.eff, big: G.list[0].share, n: G.list.length, people: G.people });
    }
    return (F.conn = out);
  }
  const refreshConnTable = wireFoot(figK, () => {
    const ys = [...new Set(connKeys.flatMap(k => connectivity(field(k)).map(d => d.y)))].sort((a, b) => a - b);
    const look = Object.fromEntries(connKeys.map(k => [k, new Map(connectivity(field(k)).map(d => [d.y, d]))]));
    return [['Window', ...connKeys.map(k => SHORT[k])],
      ys.map(y => [`${y - 2}–${y + 2}`, ...connKeys.map(k => { const d = look[k].get(y); return d ? (connMode === 'eff' ? d.eff.toFixed(1) : pct(d.big)) : ''; })])];
  });
  function renderConn(F) {
    chartK.querySelector('svg')?.remove();
    const W = chartK.clientWidth; if (W < 240) return;
    connKeys = MAIN.includes(S.f) ? MAIN : [...MAIN, S.f];
    const series = connKeys.map(k => ({ k, d: connectivity(field(k)) })).filter(s => s.d.length);
    const H = Math.round(Math.min(340, Math.max(230, W * 0.4))), m = { t: 10, r: W < 560 ? 12 : 92, b: 32, l: 46 };
    const w = W - m.l - m.r, h = H - m.t - m.b;
    const val = d => connMode === 'eff' ? d.eff : d.big;
    const x0 = Math.max(1990, d3.min(series, s => s.d[0].y));
    const x = d3.scaleLinear().domain([x0, Y1 - 2]).range([0, w]);
    const vis = series.map(s => ({ ...s, d: s.d.filter(d => d.y >= x0) }));
    const y = connMode === 'eff'
      ? d3.scaleLog().domain([1, Math.max(10, d3.max(vis, s => d3.max(s.d, val)))]).range([h, 0]).nice()
      : d3.scaleLinear().domain([0, 1]).range([h, 0]);
    const svg = d3.select(chartK).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img')
      .attr('aria-label', connMode === 'eff' ? 'Effective number of co-author groups by field and five-year window' : 'Share of paper credit in the largest co-author group by field and five-year window');
    const g = svg.append('g').attr('transform', `translate(${m.l},${m.t})`);
    const [lo, hi] = win(F);
    if (S.lo !== null) { const a = Math.max(lo, x0), b = Math.min(hi, Y1 - 2); if (b >= a) g.append('rect').attr('class', 'win-band').attr('x', x(a)).attr('width', Math.max(3, x(b) - x(a))).attr('y', 0).attr('height', h); }
    const yt = connMode === 'eff' ? [1, 2, 5, 10, 20, 50, 100].filter(v => v <= y.domain()[1]) : [0, 0.25, 0.5, 0.75, 1];
    yTicks(g, y, w, yt, connMode === 'eff' ? d3.format('~g') : d3.format('.0%'));
    g.append('text').attr('class', 'axis-label').attr('transform', `translate(${-34},${h / 2}) rotate(-90)`).attr('text-anchor', 'middle')
      .text(connMode === 'eff' ? 'effective groups' : 'largest group');
    const line = d3.line().x(d => x(d.y)).y(d => y(val(d))).curve(d3.curveMonotoneX);
    const ordered = vis.slice().sort((a, b) => (a.k === S.f) - (b.k === S.f));
    g.append('g').selectAll('path').data(ordered).join('path').attr('class', s => 'series-line' + (s.k === S.f ? ' focus' : ' faint'))
      .attr('stroke', s => col(s.k)).attr('d', s => line(s.d));
    g.append('rect').attr('class', 'frame').attr('width', w).attr('height', h);
    xTicks(g.append('g'), x, h, yearTicks(x0, Y1 - 2, w), String);
    if (W >= 560) {
      const labs = spread(vis.map(s => ({ k: s.k, y: y(val(s.d[s.d.length - 1])) })), 14, 0, h);
      labs.forEach(l => g.append('text').attr('class', 'dlabel' + (l.k === S.f ? '' : ' muted')).attr('x', w + 8).attr('y', l.y).attr('dy', '0.34em').text(SHORT[l.k]));
    }
    const cross = g.append('line').attr('class', 'crosshair').attr('y1', 0).attr('y2', h).attr('opacity', 0);
    g.append('rect').attr('width', w).attr('height', h).attr('fill', 'transparent')
      .on('mousemove', ev => {
        const [mx] = d3.pointer(ev), yr = Math.round(x.invert(mx));
        cross.attr('x1', x(yr)).attr('x2', x(yr)).attr('opacity', 1);
        const rows = vis.map(s => ({ k: s.k, d: s.d.find(d => d.y === yr) })).filter(r => r.d).sort((a, b) => val(b.d) - val(a.d));
        if (!rows.length) { tipK.hide(); return; }
        tipK.show(`<div class="t-head">${yr - 2}–${yr + 2}</div>` + rows.map(r =>
          `<div class="row${r.k === S.f ? ' strong' : ''}"><span class="sw" style="background:${col(r.k)}"></span>${SHORT[r.k]}<span class="val">${connMode === 'eff' ? r.d.eff.toFixed(1) : pct(r.d.big)}</span></div>`).join(''),
          x(yr) + m.l, d3.pointer(ev, chartK)[1]);
      })
      .on('mouseleave', () => { cross.attr('opacity', 0); tipK.hide(); });
  }
  function spread(labels, minGap, lo, hi) {
    labels.sort((a, b) => a.y - b.y);
    for (let it = 0; it < 60; it++) {
      let moved = false;
      for (let i = 1; i < labels.length; i++) {
        const d = labels[i].y - labels[i - 1].y;
        if (d < minGap) { const s = (minGap - d) / 2; labels[i].y += s; labels[i - 1].y -= s; moved = true; }
      }
      labels.forEach(l => { l.y = Math.max(lo, Math.min(hi, l.y)); });
      if (!moved) break;
    }
    return labels;
  }

  // ---------- profile: co-author network ----------
  function egoChart(i, el, scope) {
    el.innerHTML = '';
    const c = CI[S.f];
    const js = byPerson[i].filter(j => scope === 'all' || PAPERS[j].w[c] > 0).sort((a, b) => PAPERS[a].y - PAPERS[b].y || a - b);
    const shared = new Map(), first = new Map();
    js.forEach((j, t) => PAPERS[j].a.forEach(k => {
      if (k === i) return;
      shared.set(k, (shared.get(k) || 0) + 1);
      if (!first.has(k)) first.set(k, t);
    }));
    if (!shared.size) { el.innerHTML = `<p class="muted small">No co-authors on ${scope === 'all' ? 'counted' : SHORT[S.f]} papers.</p>`; return; }
    const W = el.clientWidth || 600, narrow = W < 560, MAXN = narrow ? 16 : 28;
    const keep = [...shared].sort((a, b) => b[1] - a[1] || first.get(a[0]) - first.get(b[0])).slice(0, MAXN).map(([k]) => k);
    // around the ring in order of first shared paper, so co-authors of the same paper sit together
    const co = keep.sort((a, b) => first.get(a) - first.get(b) || shared.get(b) - shared.get(a));
    const H = Math.max(240, Math.min(360, 120 + co.length * 9)), R = Math.max(60, Math.min(H / 2 - 22, W / 2 - (narrow ? 95 : 170)));
    const cx = W / 2, cy = H / 2;
    const r = d3.scaleSqrt().domain([1, d3.max(co, k => shared.get(k))]).range([3, 9]);
    const lw = d3.scaleLinear().domain([1, d3.max(co, k => shared.get(k))]).range([0.8, 3.4]);
    const nodes = co.map((k, t) => { const a = -Math.PI / 2 + 2 * Math.PI * (t + 0.5) / co.length; return { k, a, n: shared.get(k), x: cx + R * Math.cos(a), y: cy + R * Math.sin(a) }; });
    const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img').attr('aria-label', `Co-authors of ${PEOPLE[i].n}`);
    svg.append('g').selectAll('line').data(nodes).join('line').attr('class', 'nlink')
      .attr('x1', cx).attr('y1', cy).attr('x2', d => d.x).attr('y2', d => d.y).attr('stroke-width', d => lw(d.n));
    const N = svg.append('g').selectAll('g').data(nodes).join('g').attr('class', d => 'nnode' + (PEOPLE[d.k].n ? '' : ' anon'))
      .attr('transform', d => `translate(${d.x},${d.y})`);
    N.append('circle').attr('r', d => r(d.n)).attr('class', 'other');
    N.filter(d => PEOPLE[d.k].n).attr('tabindex', 0).attr('role', 'button').attr('aria-label', d => `${label(d.k)}: open profile`)
      .on('click', (e, d) => openProfile(d.k))
      .on('keydown', (e, d) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openProfile(d.k); } });
    // labels: each side of the ring spread apart vertically so they never overlap
    [nodes.filter(d => Math.cos(d.a) >= 0), nodes.filter(d => Math.cos(d.a) < 0)].forEach(side => {
      const labs = spread(side.map(d => ({ d, y: d.y + Math.sin(d.a) * (r(d.n) + 2) })), 13, 8, H - 6);
      labs.forEach(l => {
        const d = l.d, right = Math.cos(d.a) >= 0;
        svg.append('text').attr('class', 'nlabel' + (PEOPLE[d.k].n ? '' : ' muted')).attr('dy', '0.34em')
          .attr('x', d.x + (right ? 1 : -1) * (r(d.n) + 4)).attr('y', l.y).attr('text-anchor', right ? 'start' : 'end')
          .text(PEOPLE[d.k].n ? `${label(d.k)} (${d.n})` : `not named (${d.n})`);
      });
    });
    N.append('title').text(d => `${PEOPLE[d.k].n || 'not named'}: ${d.n} shared paper${d.n === 1 ? '' : 's'}`);
    const C = svg.append('g').attr('class', 'nnode center').attr('transform', `translate(${cx},${cy})`);
    C.append('circle').attr('r', 9).style('fill', col(S.f));
    if (shared.size > co.length) el.insertAdjacentHTML('beforeend', `<p class="muted small">Showing the ${co.length} most frequent of ${shared.size} co-authors. Numbers are shared papers.</p>`);
    else el.insertAdjacentHTML('beforeend', `<p class="muted small">Numbers are shared papers. Co-authors are placed around the ring in order of their first paper together.</p>`);
  }

  // ---------- researcher profile ----------
  const prof = $('#profile');
  function openProfile(i) { S.who = i; renderProfile(); writeHash(); const all = ranked(F_cur()); renderHeat(F_cur(), all); renderNet(F_cur(), all); prof.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); }
  function renderProfile() {
    if (S.who === null || !PEOPLE[S.who] || !PEOPLE[S.who].n) { prof.hidden = true; prof.innerHTML = ''; return; }
    const i = S.who, P = PEOPLE[i], js = byPerson[i].slice().sort((a, b) => PAPERS[b].y - PAPERS[a].y);
    const credit = CLS.map((_, c) => d3.sum(js, j => PAPERS[j].w[c] / PAPERS[j].a.length));
    const years = js.map(j => PAPERS[j].y);
    const co = new Map();
    js.forEach(j => PAPERS[j].a.forEach(k => { if (k !== i) co.set(k, (co.get(k) || 0) + 1); }));
    const coTop = [...co].sort((a, b) => b[1] - a[1] || (label(a[0]) || '').localeCompare(label(b[0]) || '')).slice(0, 12);
    const nAnon = [...co.keys()].filter(k => !PEOPLE[k].n).length;
    prof.hidden = false;
    prof.innerHTML = `
      <div class="profile-head">
        <h2>${esc(P.n)}${P.r === 'u' ? ' <span class="muted" title="Not matched to a DBLP person record">†&nbsp;unmatched name</span>' : ''}</h2>
        <button class="icon-btn" id="prof-close" aria-label="Close profile">&times;</button>
      </div>
      <div class="profile-meta">${[P.af && esc(P.af), P.pid && `<a href="https://dblp.org/pid/${esc(P.pid)}.html" rel="noopener">DBLP ${esc(P.pid)}</a>`,
        `${js.length} counted paper${js.length === 1 ? '' : 's'}, ${d3.min(years)}–${d3.max(years)}`,
        P.nm && `<span title="Papers not found in DBLP, assigned to this person because the author string matches the name">${P.nm === js.length ? 'all' : P.nm} matched by name only</span>`].filter(Boolean).join(' &middot; ')}</div>
      <div class="profile-classes">${MAIN.map(k => credit[CI[k]] > 0 ? `<span class="cls${k === S.f || COLOR[S.f] === k ? ' on' : ''}"><i style="background:${col(k)}"></i>${SHORT[k]} <b>${f2(credit[CI[k]])}</b></span>` : '').join('')}
        <span class="hint">paper credit, all years</span></div>
      <div class="chart profile-chart"></div>
      <div class="ego-head"><h3 class="caps">Co-author network</h3>
        <div class="seg" id="ego-scope" aria-label="Papers"><button data-v="field">${esc(SHORT[S.f])} papers</button><button data-v="all">all counted papers</button></div></div>
      <div class="chart ego-chart"></div>
      <div class="profile-cols">
        <div><h3 class="caps">Papers</h3><ol class="plist">${js.map(j => {
          const p = PAPERS[j];
          const dots = MAIN.filter(k => p.w[CI[k]] > 0).map(k => `<i style="background:${col(k)}" title="${SHORT[k]} ${p.w[CI[k]]}"></i>`).join('');
          return `<li><span class="py">${p.y}</span><span class="dots">${dots}</span><a href="bibliography.html#${encodeURIComponent(p.k)}">${esc(p.t)}</a>${p.a.length > 1 ? `<span class="na">${p.a.length} authors</span>` : ''}</li>`;
        }).join('')}</ol></div>
        <div><h3 class="caps">Most frequent co-authors</h3>${coTop.length ? `<ul class="colist">${coTop.map(([k, n]) =>
          `<li>${PEOPLE[k].n ? `<button class="bibbtn" data-p="${k}">${esc(label(k))}</button>` : '<span class="muted">(not named)</span>'}<span class="n">${n}</span></li>`).join('')}</ul>` : '<p class="muted">None: every counted paper is single-authored.</p>'}
          ${co.size > coTop.length ? `<p class="muted small">${co.size} co-authors in all${nAnon ? `, ${nAnon} with too few papers to be named` : ''}.</p>` : ''}</div>
      </div>`;
    $('#prof-close').addEventListener('click', () => { S.who = null; renderProfile(); writeHash(); const all = ranked(F_cur()); renderHeat(F_cur(), all); renderNet(F_cur(), all); });
    $$('.colist [data-p]', prof).forEach(b => b.addEventListener('click', () => openProfile(+b.dataset.p)));
    profileChart(js, $('.profile-chart', prof));
    const hasField = js.some(j => PAPERS[j].w[CI[S.f]] > 0);
    const scopeEl = $('#ego-scope', prof), egoEl = $('.ego-chart', prof);
    const setScope = v => { scopeEl.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', b.dataset.v === v)); egoChart(i, egoEl, v); };
    scopeEl.querySelector('[data-v="field"]').disabled = !hasField;
    scopeEl.addEventListener('click', e => { const b = e.target.closest('button'); if (b && !b.disabled) setScope(b.dataset.v); });
    setScope(hasField ? 'field' : 'all');
  }
  function profileChart(js, el) {
    const W = el.clientWidth || 600, H = 120, m = { t: 8, r: 8, b: 26, l: 36 };
    const w = W - m.l - m.r, h = H - m.t - m.b;
    const a = Math.min(...js.map(j => PAPERS[j].y)), b = Y1;
    const years = d3.range(Math.max(Y0, Math.min(a, b - 9)), b + 1);
    const rows = years.map(y => {
      const r = { y }; MAIN.forEach(k => { r[k] = 0; });
      js.forEach(j => { const p = PAPERS[j]; if (p.y === y) MAIN.forEach(k => { r[k] += p.w[CI[k]] / p.a.length; }); });
      return r;
    });
    const st = d3.stack().keys(MAIN)(rows);
    const x = d3.scaleBand().domain(years).range([0, w]).paddingInner(0.2);
    const y = d3.scaleLinear().domain([0, d3.max(rows, r => d3.sum(MAIN, k => r[k])) || 1]).nice(3).range([h, 0]);
    const svg = d3.select(el).append('svg').attr('viewBox', `0 0 ${W} ${H}`).attr('role', 'img').attr('aria-label', 'Paper credit per year, all fields');
    const g = svg.append('g').attr('transform', `translate(${m.l},${m.t})`);
    yTicks(g, y, w, y.ticks(3), d3.format('~g'));
    st.forEach(s => g.append('g').selectAll('rect').data(s).join('rect')
      .attr('x', d => x(d.data.y)).attr('width', x.bandwidth()).attr('y', d => y(d[1])).attr('height', d => y(d[0]) - y(d[1]))
      .attr('fill', col(s.key)).attr('fill-opacity', 0.85));
    g.append('rect').attr('class', 'frame').attr('width', w).attr('height', h);
    xTicks(g.append('g'), v => x(v) + x.bandwidth() / 2, h, yearTicks(years[0], b, w), String, false);
  }

  // ---------- render ----------
  function renderAll() {
    const F = field(S.f);
    chips.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', b.dataset.f === S.f));
    setMetric(S.m); setRows(S.rows); setSort(S.sort);
    const all = ranked(F);
    renderWindow(F); renderStats(F, all); renderHeat(F, all); renderNet(F, all); renderConc(F); renderConn(F); renderProfile();
    writeHash();
  }
  readHash();
  renderAll();
  let rw = 0, rt;
  new ResizeObserver(es => { const nw = Math.round(es[0].contentRect.width); if (nw !== rw) { rw = nw; clearTimeout(rt); rt = setTimeout(renderAll, 80); } }).observe($('.ppl-main'));
  addEventListener('hashchange', () => { readHash(); renderAll(); });
})();
