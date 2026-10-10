/* Bibliography page: search, class and quantum filters, year index, BibTeX popover. */
(function () {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const items = $$('ol.bib > li');
  const text = new Map(items.map(li => [li, (li.querySelector('.au').textContent + ' ' + li.querySelector('.ti').textContent + ' '
    + (li.querySelector('.ve') ? li.querySelector('.ve').textContent : '')).toLowerCase()]));
  const years = $$('section.yr');
  const q = $('#q'), vet = $('#vetted'), peer = $('#peer'), shown = $('#shown');
  const active = new Set();
  const qf = $('#qf');
  let quantum = 'all';   // all | yes | no

  function apply() {
    const terms = q.value.toLowerCase().split(/\s+/).filter(Boolean);
    let n = 0;
    for (const li of items) {
      const cls = li.dataset.c.split(' ');
      const ok = (!vet.checked || li.dataset.v === 'yes')
        && (!peer.checked || li.dataset.p === 'yes')
        && (quantum === 'all' || li.dataset.q === quantum)
        && (!active.size || cls.some(c => active.has(c)))
        && terms.every(t => text.get(li).includes(t));
      li.hidden = !ok; n += ok;
    }
    for (const sec of years) {
      const k = $$('li', sec).filter(li => !li.hidden).length;
      sec.hidden = !k;
      const link = $(`#years a[data-y="${sec.dataset.y}"]`);
      if (link) { link.classList.toggle('empty', !k); link.querySelector('span').textContent = k; }
    }
    shown.textContent = n === items.length ? `${n.toLocaleString()} items` : `${n.toLocaleString()} of ${items.length.toLocaleString()} items`;
  }
  let t;
  q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(apply, 120); });
  vet.addEventListener('change', apply);
  peer.addEventListener('change', apply);
  qf.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    quantum = b.dataset.v;
    qf.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b));
    apply();
  });
  $('#chips').addEventListener('click', e => {
    const b = e.target.closest('.chip'); if (!b) return;
    const c = b.dataset.c;
    active.has(c) ? active.delete(c) : active.add(c);
    b.setAttribute('aria-pressed', active.has(c));
    apply();
  });
  apply();

  // year index: highlight the year in view
  const links = $$('#years a');
  const spy = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) links.forEach(a => a.classList.toggle('active', a.dataset.y === e.target.dataset.y));
  }), { rootMargin: '-30% 0px -65% 0px' });
  years.forEach(s => spy.observe(s));

  // BibTeX popover: fetch the .bib once, then cut out one entry by key
  let bib = null;
  const pop = $('#bibpop'), pre = $('#bibtext');
  async function show(key, anchor) {
    if (bib === null) {
      try { bib = await (await fetch('bibliography.bib')).text(); }
      catch (e) { bib = ''; }
    }
    const i = bib.indexOf('{' + key + ',\n');
    let text = 'Could not load bibliography.bib; download it from the link above.';
    if (i >= 0) {
      const start = bib.lastIndexOf('@', i);
      const end = bib.indexOf('\n}\n', i);
      text = bib.slice(start, end + 2);
    }
    pre.textContent = text;
    pop.hidden = false;
    const r = anchor.getBoundingClientRect();
    const w = Math.min(560, innerWidth - 24);
    pop.style.width = w + 'px';
    pop.style.left = Math.max(12, Math.min(innerWidth - w - 12, r.left + scrollX - w / 2)) + 'px';
    pop.style.top = (r.bottom + scrollY + 8) + 'px';
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('.bibbtn');
    if (b) { e.preventDefault(); show(b.dataset.key, b); return; }
    if (!e.target.closest('#bibpop')) pop.hidden = true;
  });
  $('#bibclose').addEventListener('click', () => { pop.hidden = true; });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') pop.hidden = true; });
  $('#bibcopy').addEventListener('click', () => {
    navigator.clipboard && navigator.clipboard.writeText(pre.textContent).then(() => {
      $('#bibcopy').textContent = 'copied'; setTimeout(() => ($('#bibcopy').textContent = 'copy'), 1200);
    });
  });
})();
