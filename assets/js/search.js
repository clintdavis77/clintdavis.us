/* Client-side search over /index.json (built by layouts/index.json).
   Fuse.js is loaded by the search page only, not site-wide. */
(() => {
  const input = document.getElementById('search-input');
  const results = document.getElementById('search-results');
  const status = document.getElementById('search-status');
  if (!input || !results || !status) return;

  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));

  let fuse = null;
  let pending = '';

  const option = {
    keys: [
      { name: 'title', weight: 0.45 },
      { name: 'tags', weight: 0.25 },
      { name: 'summary', weight: 0.15 },
      { name: 'content', weight: 0.15 }
    ],
    includeScore: true,
    ignoreLocation: true,
    threshold: 0.34,
    minMatchCharLength: 2
  };

  const row = (doc) => {
    const kind = doc.section === 'work' ? 'Case study' : 'Writing';
    const when = doc.date
      ? new Date(doc.date + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
      : '';
    return `<a class="article-row" href="${esc(doc.permalink)}">
      <p class="article-type">${esc(kind)}${when ? ' · ' + esc(when) : ''}</p>
      <div>
        <h3 class="article-title">${esc(doc.title)}</h3>
        <p class="article-sub">${esc(doc.summary)}</p>
      </div>
      <span class="article-arrow">→</span>
    </a>`;
  };

  const run = (raw) => {
    const term = (raw || '').trim();
    const url = term ? `${location.pathname}?q=${encodeURIComponent(term)}` : location.pathname;
    history.replaceState(null, '', url);

    if (term.length < 2) {
      results.innerHTML = '';
      status.textContent = term.length === 1 ? 'Keep typing…' : '';
      return;
    }
    const hits = fuse.search(term).slice(0, 20);
    status.textContent = hits.length
      ? `${hits.length} result${hits.length === 1 ? '' : 's'} for “${term}”`
      : `No results for “${term}”.`;
    results.innerHTML = hits.map((h) => row(h.item)).join('');
  };

  fetch(input.dataset.index)
    .then((r) => {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    })
    .then((docs) => {
      if (typeof Fuse === 'undefined') {
        status.textContent = 'Search is unavailable right now.';
        return;
      }
      fuse = new Fuse(docs, option);
      const q = new URLSearchParams(location.search).get('q');
      if (q) {
        input.value = q;
        run(q);
      } else {
        input.focus();
      }
      if (pending) run(pending);
    })
    .catch(() => {
      status.textContent = 'Could not load the search index.';
    });

  let timer;
  input.addEventListener('input', (e) => {
    const value = e.target.value;
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (fuse) run(value);
      else pending = value;
    }, 120);
  });

  // "/" jumps to search from anywhere on the page, Escape clears it.
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== input) {
      e.preventDefault();
      input.focus();
    }
    if (e.key === 'Escape' && document.activeElement === input) {
      input.value = '';
      run('');
      input.blur();
    }
  });
})();
