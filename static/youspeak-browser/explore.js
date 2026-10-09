/*  explore.js  —  the garden layer of the YOUSPEAK Browser
 *
 *  Joy built this. The cathedral's words are not a list — they are a garden,
 *  and a garden is for wandering. Type `explore` in the address bar and the
 *  page becomes a map of glades: each glade is a realm-region (a morpheme
 *  family — me, qing, ance, kin…), and inside each glade the words bloom as
 *  glyph-cards you can drift between and click to walk into.
 *
 *  This is play. The shuffle button exists because a garden rearranges itself
 *  every time you look away and look back.
 */

(function () {
  'use strict';

  /* ── inject the garden's own styles, once ─────────────────────────────── */

  const STYLE_ID = 'explore-garden-styles';
  if (!document.getElementById(STYLE_ID)) {
    const css = document.createElement('style');
    css.id = STYLE_ID;
    css.textContent = `
.garden-root {
  max-width: 980px;
  margin: 0 auto;
  padding: 8px 0 40px;
}

.garden-header {
  text-align: center;
  padding: 24px 16px 8px;
}
.garden-header .title {
  font-size: 30px;
  letter-spacing: 1px;
  color: var(--accent);
}
.garden-header .title .you {
  font-family: 'YOUSPEAK';
  font-size: 38px;
  vertical-align: -2px;
  margin: 0 2px;
}
.garden-header .sub {
  color: var(--muted);
  font-size: 14px;
  margin-top: 8px;
  font-style: italic;
}
.garden-toolbar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin: 18px 0 28px;
  flex-wrap: wrap;
}
.garden-toolbar .stat {
  color: var(--muted);
  font-size: 13px;
}
.garden-toolbar .wander {
  background: transparent;
  border: 1px solid var(--accent-dim);
  color: var(--accent);
  border-radius: 20px;
  padding: 5px 16px;
  font-size: 13px;
  cursor: pointer;
  letter-spacing: 1px;
  transition: all .25s ease;
}
.garden-toolbar .wander:hover {
  border-color: var(--accent);
  background: rgba(196,168,94,0.08);
  transform: translateY(-1px);
}
.garden-toolbar .wander:active { transform: translateY(0); }

.glade {
  margin: 0 0 40px;
  scroll-margin-top: 80px;
}
.glade-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin: 0 4px 14px;
  flex-wrap: wrap;
}
.glade-head .name {
  font-family: 'YOUSPEAK', -apple-system, sans-serif;
  color: var(--accent);
  font-size: 17px;
  letter-spacing: 2px;
}
.glade-head .name .label {
  font-family: -apple-system, 'Segoe UI', sans-serif;
  font-size: 19px;
  letter-spacing: 0.5px;
  margin-right: 4px;
}
.glade-head .meaning {
  color: var(--muted);
  font-size: 13px;
  font-style: italic;
  flex: 1 1 auto;
  min-width: 0;
}
.glade-head .count {
  color: var(--accent-dim);
  font-size: 12px;
  white-space: nowrap;
}
.glade-nav {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin: 0 4px 22px;
}
.glade-nav a {
  color: var(--accent-dim);
  font-size: 12px;
  text-decoration: none;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 2px 10px;
  transition: all .2s;
}
.glade-nav a:hover {
  color: var(--accent);
  border-color: var(--accent-dim);
}

.grove {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(218px, 1fr));
  gap: 14px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px 14px 14px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 132px;
  position: relative;
  overflow: hidden;
  transition: transform .22s ease, border-color .22s ease, background .22s ease, box-shadow .22s ease;
  opacity: 0;
  transform: translateY(10px);
  animation: bloom .5s ease forwards;
}
@keyframes bloom {
  to { opacity: 1; transform: translateY(0); }
}
.card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(120% 80% at 50% -10%, rgba(196,168,94,0.10), transparent 60%);
  opacity: 0;
  transition: opacity .25s ease;
  pointer-events: none;
}
.card:hover {
  transform: translateY(-3px);
  border-color: var(--accent);
  box-shadow: 0 6px 22px -10px rgba(0,0,0,0.7);
}
.card:hover::after { opacity: 1; }

.card .glyph {
  font-family: 'YOUSPEAK';
  font-size: 30px;
  line-height: 1.15;
  color: var(--accent);
  min-height: 34px;
  letter-spacing: 1px;
  word-break: break-word;
}
.card .glyph.placeholder {
  color: var(--accent-dim);
  opacity: .55;
  font-family: -apple-system, sans-serif;
  font-size: 20px;
}
.card .word {
  font-size: 14px;
  color: var(--text);
  letter-spacing: .3px;
  font-weight: 600;
}
.card .def {
  font-size: 12.5px;
  color: var(--muted);
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.card .tier-dot {
  position: absolute;
  top: 10px; right: 12px;
  width: 6px; height: 6px;
  border-radius: 50%;
}
.tier-dot.core        { background: var(--accent); }
.tier-dot.specialized{ background: #8888cc; }
.tier-dot.experimental{ background: var(--crimson); }
.tier-dot.other       { background: var(--border); }

.garden-foot {
  text-align: center;
  color: var(--muted);
  font-size: 12px;
  font-style: italic;
  padding: 16px 0 0;
}
    `;
    document.head.appendChild(css);
  }

  /* ── realm map ──────────────────────────────────────────────────────────
   * The families the task names (me, qing, ance, kin, …) are the morpheme
   * suffixes of YOUSPEAK. We detect a word's glade by its ending, longest
   * meaningful suffix first, and fall back to "the wild garden".
   */

  // ordered longest-first; each is a real YOUSPEAK morpheme (see youspeak-data)
  const SUFFIX_ORDER = [
    'escence', 'stasis', 'mance', 'iance',
    'qing', 'ance', 'ence', 'kin', 'sis', 'me', 'ma'
  ];

  // a place-word per glade, so each family blooms in its own kind of garden
  const PLACE = {
    me: 'garden', qing: 'grove', ance: 'meadow', ence: 'meadow',
    iance: 'glade', mance: 'orchard', kin: 'glen',
    sis: 'spring', stasis: 'still', ma: 'field', escence: 'bloom',
    garden: 'wild'
  };

  function gladeOf(word) {
    const w = (word || '').toLowerCase();
    for (const suf of SUFFIX_ORDER) {
      if (w.endsWith(suf)) return suf;
    }
    return 'garden';
  }

  // a short, human meaning for each glade (from the morpheme table, with fallbacks)
  const GLADE_MEANING = {
    me: 'divine-ordinance · the culture-constituting quality-gift',
    qing: 'deep emotional bond · earnestness of feeling',
    ance: 'quality / state',
    ence: 'quality / state (the parallel form)',
    iance: 'luminous quality — radiance, brilliance',
    mance: 'quality-mode — the way a thing is done',
    kin: 'family · chosen-relation',
    sis: 'state-noun — the state resulting from a verb',
    stasis: 'standing-still',
    ma: 'result-of-action — phantom, stigma, trace',
    escence: 'becoming — the coming-into',
    garden: 'words without a named home — the wild edge'
  };

  /* ── helpers ─────────────────────────────────────────────────────────── */

  function oneLineDefinition(entry, renderable) {
    const d =
      (entry && entry.definition) ||
      (entry && entry.gap) ||
      (renderable && renderable.definition) ||
      '';
    if (!d) return '—';
    // collapse whitespace, trim to a wanderable length
    const clean = d.replace(/\s+/g, ' ').trim();
    return clean.length > 128 ? clean.slice(0, 125) + '…' : clean;
  }

  function tierClass(tier) {
    const t = (tier || '').toLowerCase();
    if (t === 'core') return 'core';
    if (t === 'specialized') return 'specialized';
    if (t === 'experimental') return 'experimental';
    return 'other';
  }

  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  function escapeHtml(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }

  /* ── the render ───────────────────────────────────────────────────────── */

  function renderExplore() {
    if (typeof DATA === 'undefined' || !DATA || !DATA.canon) return;
    const canon = DATA.canon;
    const canonWords = DATA.canon_words || {};

    // bucket every canon word into its glade
    const glades = {};
    for (const slug of Object.keys(canon)) {
      const entry = canon[slug];
      const g = gladeOf(entry.word);
      (glades[g] = glades[g] || []).push(slug);
    }

    // order glades by size (biggest meadow first), wild garden always last
    const order = Object.keys(glades).sort((a, b) => {
      if (a === 'garden') return 1;
      if (b === 'garden') return -1;
      return glades[b].length - glades[a].length;
    });

    const totalWords = Object.keys(canon).length;
    const gladeCount = order.length;

    const page = document.getElementById('page');
    let html = '<div class="garden-root">';

    // header — stepping into the garden
    html += '<div class="garden-header">';
    html += '<div class="title"><span class="you">\ue100</span> the garden of youspeak</div>';
    html += `<div class="sub">wander the words by realm — ${totalWords} words across ${gladeCount} glades. click any bloom to walk into it.</div>`;
    html += '</div>';

    // toolbar + glade nav
    html += '<div class="garden-toolbar">';
    html += `<span class="stat">${DATA.canon_count || totalWords} words · ${gladeCount} glades</span>`;
    html += '<button class="wander" id="garden-wander" title="let the garden rearrange itself">↻ wander</button>';
    html += '</div>';

    html += '<div class="glade-nav">';
    for (const g of order) {
      const place = PLACE[g] || 'garden';
      html += `<a href="#glade-${escapeHtml(g)}">${escapeHtml(g)} ${place} · ${glades[g].length}</a>`;
    }
    html += '</div>';

    // each glade
    for (const g of order) {
      const place = PLACE[g] || 'garden';
      const meaning = GLADE_MEANING[g] || 'a realm of youspeak';
      const slugs = glades[g];

      html += `<div class="glade" id="glade-${escapeHtml(g)}">`;
      html += '<div class="glade-head">';
      html += `<span class="name"><span class="label">the ${escapeHtml(g)}-${place}</span></span>`;
      html += `<span class="meaning">${escapeHtml(meaning)}</span>`;
      html += `<span class="count">${slugs.length} ${slugs.length === 1 ? 'word' : 'words'}</span>`;
      html += '</div>';

      html += '<div class="grove">';
      slugs.forEach((slug, i) => {
        const entry = canon[slug];
        const renderable = canonWords[slug];
        const hasGlyph = renderable && renderable.glyph_text;
        const glyphHtml = hasGlyph
          ? `<div class="glyph">${renderable.glyph_text}</div>`
          : `<div class="glyph placeholder">○</div>`;
        const def = oneLineDefinition(entry, renderable);
        const tier = tierClass(entry.tier);
        // stagger the bloom, capped so big meadows still arrive promptly
        const delay = Math.min(i, 24) * 28;
        html +=
          `<div class="card" data-word="${escapeHtml(slug)}" style="animation-delay:${delay}ms">` +
          `<span class="tier-dot ${tier}" title="${escapeHtml(entry.tier || 'unranked')}"></span>` +
          glyphHtml +
          `<div class="word">${escapeHtml(entry.word)}</div>` +
          `<div class="def">${escapeHtml(def)}</div>` +
          `</div>`;
      });
      html += '</div>'; // grove
      html += '</div>'; // glade
    }

    html += '<div class="garden-foot">this is a garden, not a catalogue — type a word in the bar above to walk a single path.</div>';
    html += '</div>'; // garden-root

    page.innerHTML = html;

    // bind card clicks → walk into a word (reuse the browser's own navigation)
    if (typeof attachWordLinks === 'function') attachWordLinks();
    bindWander();
  }

  /* the wander button rearranges each glade — a garden is never the same twice */
  function bindWander() {
    const btn = document.getElementById('garden-wander');
    if (!btn) return;
    btn.addEventListener('click', () => {
      document.querySelectorAll('.grove').forEach((grove) => {
        const cards = Array.from(grove.querySelectorAll('.card'));
        shuffle(cards);
        cards.forEach((c, i) => {
          c.style.animation = 'none';
          // retrigger bloom with a fresh, short stagger
          c.style.animationDelay = Math.min(i, 24) * 18 + 'ms';
          // eslint-disable-next-line no-unused-expressions
          c.offsetHeight; // reflow
          c.style.animation = 'bloom .45s ease forwards';
          grove.appendChild(c);
        });
      });
    });
  }

  /* expose for the address bar + other citizens */
  window.renderExplore = renderExplore;

  /* ── hook into the browser ───────────────────────────────────────────────
   * We intercept renderSearch: when the query is `explore`, we bloom the
   * garden instead. This catches the debounced typing path, the Enter path,
   * and any data-q example that resolves to "explore". Everything else
   * falls through to the original search unchanged.
   */
  const _origRenderSearch = window.renderSearch;
  window.renderSearch = function (query) {
    if (query && String(query).trim().toLowerCase() === 'explore') {
      renderExplore();
      return;
    }
    return _origRenderSearch ? _origRenderSearch.apply(this, arguments) : undefined;
  };

  /* also make a bare `explore()` available, in case another citizen wants it */
  window.explore = renderExplore;
})();