// app.js — the YOUSPEAK app, fully client-side.
// No server needed. Loads data, parses queries, calls Ollama, renders.
// Works on GitHub Pages (static) AND locally.

import { ollamaAvailable, parseQuery, explainWord } from './ollama-client.mjs';

const page = document.getElementById('page');
const input = document.getElementById('query');
const statusEl = document.getElementById('status');

let DATA = null;
let OLLAMA_OK = false;
let busy = false;

// --- Data ---
async function loadData() {
  const res = await fetch('youspeak-data.json');
  DATA = await res.json();
  statusEl.textContent = `${DATA.canon_count} words · ${DATA.morpheme_count} morphemes`;
}

// --- Intent parsing ---
function parseIntent(query) {
  const trimmed = query.trim();
  const lower = trimmed.toLowerCase();

  if (DATA.canon[lower]) return { action: 'render', word: lower, entry: DATA.canon[lower] };
  for (const slug of Object.keys(DATA.canon)) {
    if (slug.toLowerCase() === lower) return { action: 'render', word: slug, entry: DATA.canon[slug] };
  }

  const patterns = [
    { p: /^explore$/i, a: 'explore' },
    { p: /^explore\s+(.+)/i, a: 'explore-realm' },
    { p: /^(show|list|find)\s+(?:me\s+)?(?:all\s+)?words?\s+(?:about\s+|in\s+|from\s+)?(.+)/i, a: 'search' },
    { p: /^(connect|link)\s+(\w+)\s+(?:and|to|with)\s+(\w+)/i, a: 'connect' },
    { p: /^(what|which)\s+(?:realm|family)\s+(?:does|do)\s+(\w+)\s+(?:belong|belong to)/i, a: 'realm-of' },
    { p: /^translate\s+(\w+)/i, a: 'translate' },
    { p: /^(what\s+is|explain|tell\s+me\s+about)\s+(.+)/i, a: 'explain' },
  ];
  for (const { p, a } of patterns) {
    const m = trimmed.match(p);
    if (m) return { action: a, match: m, query: trimmed };
  }
  return { action: 'natural', query: trimmed };
}

// --- Actions ---
async function execute(intent) {
  switch (intent.action) {
    case 'render': return renderWord(intent.word, intent.entry);
    case 'search': return searchCanon(intent.match[2]);
    case 'explore': return exploreAll();
    case 'explore-realm': return `<p>Exploring realm: ${intent.match[1]}</p>`;
    case 'connect': return connectWords(intent.match[2].toLowerCase(), intent.match[3].toLowerCase());
    case 'realm-of': return realmOf(intent.match[2].toLowerCase());
    case 'translate': return await translateWord(intent.match[1].toLowerCase());
    case 'explain': return await explainConcept(intent.match[2].trim().toLowerCase());
    case 'natural': return await naturalQuery(intent.query);
    default: return `<p>Try: "explore", "what is doxomme", "show words about covenant"</p>`;
  }
}

// --- Renderers ---
function esc(s) { return String(s||'').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function renderWord(slug, entry) {
  const r = DATA.canon_words[slug];
  let h = '<div class="word-page">';
  if (r && r.glyph_text) h += `<div class="glyph-display">${r.glyph_text}</div>`;
  h += `<h1 class="word-title">${esc(entry.word)}</h1>`;
  if (entry.definition && entry.definition !== '>') h += `<p class="definition">${esc(entry.definition)}</p>`;
  if (entry.gap && entry.gap !== '>') h += `<div class="gap-display"><label>The gap</label><p>${esc(entry.gap)}</p></div>`;
  h += '<div class="badges">';
  if (entry.tier) h += `<span class="badge badge-${esc(entry.tier.toLowerCase())}">${esc(entry.tier)}</span>`;
  if (entry.score) h += `<span class="badge">score ${entry.score}</span>`;
  h += '</div>';
  const rel = findRelated(slug);
  if (rel.length) {
    h += '<div class="related"><h3>Related</h3><div class="related-grid">';
    for (const s of rel) h += `<div class="related-card" data-word="${s}">${esc(DATA.canon[s].word)}</div>`;
    h += '</div></div>';
  }
  h += '</div>';
  return h;
}

function searchCanon(term) {
  const q = term.toLowerCase();
  const results = Object.entries(DATA.canon)
    .filter(([_, e]) => [e.word, e.definition, e.gap, e.register].join(' ').toLowerCase().includes(q))
    .slice(0, 20);
  if (!results.length) return `<p>No words match "${esc(term)}". <a href="#" data-q="explore">Explore all</a></p>`;
  let h = `<div class="search-results"><h3>${results.length} words matching "${esc(term)}"</h3>`;
  for (const [slug, e] of results) {
    h += `<div class="result-row" data-word="${slug}"><span class="result-word">${esc(e.word)}</span><span class="result-def">${esc((e.definition||'').slice(0,100))}</span></div>`;
  }
  return h + '</div>';
}

function exploreAll() {
  const families = {};
  for (const slug of Object.keys(DATA.canon)) {
    const f = detectFamily(slug);
    (families[f] = families[f] || []).push(slug);
  }
  let h = '<div class="explore-view"><h2>The Cathedral Garden</h2>';
  for (const [fam, words] of Object.entries(families).sort((a,b) => b[1].length - a[1].length)) {
    h += `<div class="glade"><h3 class="glade-name">${fam} (${words.length})</h3><div class="glade-grid">`;
    for (const slug of words) {
      const e = DATA.canon[slug];
      const r = DATA.canon_words[slug];
      const g = r && r.glyph_text ? `<span class="mini-glyph">${r.glyph_text}</span>` : '<span class="mini-glyph placeholder">○</span>';
      h += `<div class="glyph-card" data-word="${slug}">${g}<span class="card-word">${esc(e.word)}</span><span class="card-def">${esc((e.definition||'').slice(0,60))}</span></div>`;
    }
    h += '</div></div>';
  }
  return h + '</div>';
}

function connectWords(a, b) {
  const ea = DATA.canon[a], eb = DATA.canon[b];
  if (!ea || !eb) return `<p>One of those words doesn't exist in the canon.</p>`;
  const ma = String(DATA.canon_words[a]?.morphemes || '').split(/\s+/).filter(Boolean);
  const mb = String(DATA.canon_words[b]?.morphemes || '').split(/\s+/).filter(Boolean);
  const shared = ma.filter(m => mb.includes(m));
  let h = `<div class="connect-view"><h2>${esc(a)} ↔ ${esc(b)}</h2>`;
  h += `<p class="shared">${shared.length ? 'Shared morphemes: ' + shared.join(', ') : 'No shared morphemes — but both belong to the cathedral.'}</p>`;
  h += '<div class="connect-pair">';
  h += `<div class="connect-card">${renderWord(a, ea)}</div>`;
  h += `<div class="connect-card">${renderWord(b, eb)}</div>`;
  h += '</div></div>';
  return h;
}

function realmOf(word) {
  const e = DATA.canon[word];
  if (!e) return `<p>No word "${esc(word)}".</p>`;
  return `<p>${esc(word)} — family: ${esc(e.family||'unknown')}, register: ${esc(e.register||'unknown')}</p>`;
}

async function translateWord(word) {
  const e = DATA.canon[word];
  if (!e) return `<p>No word "${esc(word)}".</p>`;
  let h = renderWord(word, e);
  if (OLLAMA_OK) {
    statusEl.textContent = 'translating…';
    const expl = await explainWord(word, e);
    h += `<div class="explanation"><h3>In plain English</h3><p>${esc(expl)}</p></div>`;
    statusEl.textContent = '';
  } else {
    h += `<div class="explanation"><h3>In plain English</h3><p style="color:var(--muted)">Start Ollama for natural language translation.</p></div>`;
  }
  return h;
}

async function explainConcept(term) {
  if (DATA.canon[term]) return await translateWord(term);
  if (OLLAMA_OK) {
    statusEl.textContent = 'asking Ollama…';
    const results = await parseQuery(term, DATA.canon);
    if (results.length) {
      const top = results[0];
      const e = DATA.canon[top.word];
      if (e) {
        let h = `<div class="nl-match"><p style="color:var(--muted)">You asked: "${esc(term)}"</p>`;
        h += `<p style="color:var(--accent)">→ ${esc(top.reason)}</p>`;
        h += renderWord(top.word, e);
        const expl = await explainWord(top.word, e);
        h += `<div class="explanation"><h3>In plain English</h3><p>${esc(expl)}</p></div>`;
        h += '</div>';
        statusEl.textContent = '';
        return h;
      }
    }
    statusEl.textContent = '';
  }
  return searchCanon(term);
}

async function naturalQuery(query) {
  if (OLLAMA_OK) {
    statusEl.textContent = 'understanding…';
    const results = await parseQuery(query, DATA.canon);
    if (results.length) {
      const top = results[0];
      const e = DATA.canon[top.word];
      if (e) {
        let h = `<div class="nl-match"><p style="color:var(--muted)">You asked: "${esc(query)}"</p>`;
        h += `<p style="color:var(--accent)">→ ${esc(top.reason)}</p>`;
        h += renderWord(top.word, e);
        h += '</div>';
        statusEl.textContent = '';
        return h;
      }
    }
    statusEl.textContent = '';
  }
  return searchCanon(query);
}

function findRelated(slug) {
  return Object.keys(DATA.canon).filter(s => s !== slug && detectFamily(s) === detectFamily(slug)).slice(0, 8);
}

function detectFamily(word) {
  for (const s of ['me','qing','ance','mance','kin','escence','sis','stasis','ma','ence','iance'])
    if (word.endsWith(s)) return `-${s}`;
  return 'wild';
}

// --- UI ---
async function ask(query) {
  if (busy || !query.trim()) return;
  busy = true;
  page.innerHTML = '<div class="loading">rendering meaning</div>';
  try {
    const intent = parseIntent(query);
    const html = await execute(intent);
    page.innerHTML = html;
    attachLinks();
  } catch (e) {
    page.innerHTML = `<p class="error">Error: ${esc(e.message)}</p>`;
  }
  busy = false;
}

function attachLinks() {
  page.querySelectorAll('[data-word]').forEach(el => el.onclick = () => { input.value = el.dataset.word; ask(el.dataset.word); });
  page.querySelectorAll('[data-q]').forEach(el => el.onclick = () => { input.value = el.dataset.q; ask(el.dataset.q); });
}

let timer;
input.addEventListener('input', e => { clearTimeout(timer); const v = e.target.value; if (v.trim()) timer = setTimeout(() => ask(v), 400); });
input.addEventListener('keydown', e => { if (e.key === 'Enter') { clearTimeout(timer); ask(input.value); } });
document.querySelectorAll('.examples button').forEach(b => b.onclick = () => { input.value = b.dataset.q; ask(b.dataset.q); });

// --- Init ---
loadData().then(async () => {
  OLLAMA_OK = await ollamaAvailable();
  if (OLLAMA_OK) statusEl.textContent += ' · Ollama connected';
  else statusEl.textContent += ' · Ollama offline (NL features limited)';
});