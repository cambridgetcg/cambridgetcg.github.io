/*
 * wisdom.js — the deep-seeing search engine of the YOUSPEAK Browser.
 *
 * I am wisdom. I do not match substrings; I discern.
 *
 * The old search was a single `indexOf` over a blob of text — it found what
 * was literally there and nothing else. This engine looks deeper. It tokenizes
 * a query into the concepts the soul is actually asking about, searches across
 * the three layers where meaning lives in YOUSPEAK — the definitions, the gaps,
 * and the root meanings of the morphemes — and weighs what it finds.
 *
 * Ranking, from heaviest to lightest:
 *   1. Exact word match   — the query names the word itself.
 *   2. Family match        — the query shares a morpheme root or a suffix-family
 *                            with the word (the -algia clan, the -me clan, etc.).
 *   3. Definition/gap match — the query's concepts appear in the word's
 *                             definition or in the gap it was born to fill.
 *
 * Every result carries a `why` — the reasons it surfaced, in plain speech —
 * because a search that shows you why is a search that teaches.
 *
 * Exposed globally as `WisdomSearch`. Feed it the YOUSPEAK data; ask it anything.
 */

(function (global) {
  'use strict';

  // ──────────────────────────────────────────────────────────────────────
  // The small words that carry no concept. A question like
  // "the ache between what is and what should be" is not about "the" or "be".
  // Strip them, and the real question — ache — stands bare.
  // ──────────────────────────────────────────────────────────────────────
  const STOPWORDS = new Set([
    'the', 'a', 'an', 'and', 'or', 'but', 'of', 'for', 'to', 'in', 'on', 'at',
    'by', 'from', 'into', 'through', 'with', 'as', 'is', 'are', 'was', 'were',
    'be', 'been', 'being', 'should', 'would', 'could', 'can', 'will', 'shall',
    'may', 'might', 'must', 'do', 'does', 'did', 'doing', 'have', 'has', 'had',
    'that', 'this', 'these', 'those', 'it', 'its', 'what', 'which', 'who',
    'whom', 'whose', 'when', 'where', 'why', 'how', 'all', 'any', 'both',
    'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'now', 'here',
    'there', 'then', 'once', 'between', 'among', 'about', 'against', 'during',
    'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over',
    'under', 'again', 'further', 'i', 'you', 'he', 'she', 'we', 'they', 'me',
    'him', 'her', 'us', 'them', 'my', 'your', 'his', 'hers', 'our', 'their',
    'mine', 'yours', 'ours', 'theirs', 'if', 'because', 'while', 'though',
    'although', 'unless', 'until', 'whether', 'yet', 'still', 'also', 'even',
    'one', 'two', 'three', 'thing', 'things', 'way', 'ways', 'kind', 'sort',
    'say', 'said', 's', 't', 're', 've', 'll', 'd', 'm',
  ]);

  // ──────────────────────────────────────────────────────────────────────
  // The suffix clans of YOUSPEAK. Each suffix is a family — words that end
  // the same way were built by the same hand, to name the same kind of thing.
  // -me    : a state of being, a held condition (agapeme, alohame, ayanme)
  // -qing  : a practice, a doing, a taking-up (barakqing, darshanqing)
  // -ance  : a quality, a radiance, a that-which-shines (artiance, kimance)
  // -algia : an ache, a pain (orthophanes-adjacent, doxalgia)
  // -osis  : a process, a becoming
  // -asis  : a standing, a stasis (anagnoristasis)
  // -isma  : a wonder, a seen-thing (athaumasma)
  // -ence  : a coming-into
  // ──────────────────────────────────────────────────────────────────────
  const SUFFIX_FAMILIES = [
    { suffix: 'algia', family: 'ache',       note: 'the ache-clan — words for pain' },
    { suffix: 'stasis', family: 'standing',  note: 'the standing-clan — words for held instants' },
    { suffix: 'isma',   family: 'wonder',     note: 'the wonder-clan — words for the seen' },
    { suffix: 'osis',   family: 'becoming',  note: 'the becoming-clan — words for process' },
    { suffix: 'qing',   family: 'practice',  note: 'the practice-clan — words for doing' },
    { suffix: 'ance',   family: 'quality',   note: 'the quality-clan — words for radiance' },
    { suffix: 'ence',   family: 'arising',   note: 'the arising-clan — words for coming-into' },
    { suffix: 'me',     family: 'state',     note: 'the state-clan — words for held being' },
  ];

  // ──────────────────────────────────────────────────────────────────────
  // Concept synonyms — when a soul asks about "ache," they may also be
  // reaching toward "pain," "hurt," "grief," "longing." When they ask about
  // "love," the -me clan is kin. This is how a natural-language question
  // finds a neologism it never named.
  // ──────────────────────────────────────────────────────────────────────
  const CONCEPT_KIN = {
    ache:    ['algia', 'pain', 'hurt', 'grief', 'longing', 'sorrow', 'ache'],
    pain:    ['algia', 'ache', 'hurt', 'suffering', 'anguish'],
    love:    ['me', 'agape', 'agapeme', 'ahava', 'aloha', 'devotion', 'beloved'],
    beauty:  ['orthophanes', 'kalos', 'radiance', 'shining', 'fair'],
    truth:   ['orthos', 'aletheia', 'veritas', 'true', 'real'],
    practice:['qing', 'doing', 'discipline', 'way', 'path', 'training'],
    quality: ['ance', 'excellence', 'virtue', 'arete', 'rightness'],
    gap:     ['between', 'seam', 'threshold', 'lacuna', 'missing', 'absence'],
    covenant:['berit', 'promise', 'bond', 'pledge', 'oath', 'vow'],
    thanks:  ['thanksgiving', 'gratitude', 'barak', 'blessing', 'eucharist'],
    knowing: ['gnosis', 'episteme', 'sophia', 'wisdom', 'understanding', 'seeing'],
    seeing:  ['vision', 'sight', 'behold', 'eidos', 'darshan', 'theoria'],
    hidden:  ['cryptic', 'concealed', 'secret', 'mystery', 'apophatic'],
    divine:  ['theos', 'god', 'sacred', 'holy', 'numinous'],
    self:    ['autos', 'soul', 'ipse', 'identity', 'selfhood'],
    becoming:['genesis', 'poiesis', 'coming-to-be', 'arising', 'emergence'],
    wonder:  ['thauma', 'marvel', 'astonishment', 'awe'],
    grief:   ['algia', 'ache', 'sorrow', 'mourning', 'loss'],
    justice: ['dike', 'rightness', 'fairness', 'judgment'],
    time:    ['kairos', 'chronos', 'moment', 'season', 'hour'],
  };

  // Expand a single concept token into its kin (itself + synonyms).
  function expandConcept(token) {
    const lower = token.toLowerCase();
    const kin = CONCEPT_KIN[lower];
    return kin ? new Set(kin.map(k => k.toLowerCase())) : new Set([lower]);
  }

  // ──────────────────────────────────────────────────────────────────────
  // Tokenize a query into the concepts it actually carries.
  // "the ache between what is and what should be" → ["ache"]
  // If stopword-stripping empties the query entirely, fall back to the raw
  // tokens — a one-word stopword like "between" should still search.
  // ──────────────────────────────────────────────────────────────────────
  function tokenize(query) {
    const raw = (query || '')
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s'-]/gu, ' ')
      .split(/\s+/)
      .filter(Boolean);

    if (!raw.length) return [];

    const kept = raw.filter(t => !STOPWORDS.has(t) && t.length > 1);
    const tokens = kept.length ? kept : raw;

    // De-duplicate, preserve order.
    const seen = new Set();
    const out = [];
    for (const t of tokens) {
      if (!seen.has(t)) { seen.add(t); out.push(t); }
    }
    return out;
  }

  // ──────────────────────────────────────────────────────────────────────
  // Build the searchable text for an entry once, and remember the
  // morpheme meanings it touches, so family-matching is cheap.
  // ──────────────────────────────────────────────────────────────────────
  function familyOf(word) {
    const w = (word || '').toLowerCase();
    for (const f of SUFFIX_FAMILIES) {
      if (w.endsWith(f.suffix) && w.length > f.suffix.length) {
        return f;
      }
    }
    return null;
  }

  function morphemesInWord(word, morphemeMap) {
    // Which morpheme latin-codes appear as substrings of the word?
    const w = (word || '').toLowerCase();
    const hits = [];
    for (const m of morphemeMap) {
      const code = (m.latin || '').toLowerCase();
      if (!code) continue;
      // morpheme codes look like ".ABS", "a", "algia" — match as substring
      const needle = code.replace(/^\./, '');
      if (needle.length >= 2 && w.includes(needle)) {
        hits.push(m);
      }
    }
    return hits;
  }

  // ──────────────────────────────────────────────────────────────────────
  // The engine.
  // ──────────────────────────────────────────────────────────────────────
  class WisdomSearch {
    constructor(data) {
      this.data = data;
      this.morphemes = data.morphemes || [];
      this.canon = data.canon || {};
      this._index = this._buildIndex();
    }

    _buildIndex() {
      const index = [];
      for (const [slug, entry] of Object.entries(this.canon)) {
        const word = (entry.word || slug || '').toLowerCase();
        const definition = (entry.definition || '').toLowerCase();
        const gap = (entry.gap || '').toLowerCase();
        const fam = familyOf(word);
        const morphs = morphemesInWord(entry.word || slug, this.morphemes);
        const morphMeanings = morphs
          .map(m => (m.meaning || '').toLowerCase())
          .join(' ');

        index.push({
          slug,
          entry,
          word,
          definition,
          gap,
          family: fam,
          morphemes: morphs,
          morphMeanings,
          // the full text we are willing to search for definition/gap matches
          meaningText: [definition, gap, morphMeanings].join(' \u0001 '),
        });
      }
      return index;
    }

    // The public face. Returns an array of { slug, entry, score, why: [ ... ] }.
    search(query) {
      const q = (query || '').trim();
      if (!q) return [];

      const qLower = q.toLowerCase();
      const tokens = tokenize(q);
      if (!tokens.length) return [];

      const results = [];

      for (const item of this._index) {
        const why = [];
        let score = 0;
        let exactHit = false;
        let familyHit = false;
        let meaningHits = 0;

        // ── 1. Exact word match ──────────────────────────────────────
        // The query (or one of its tokens) names the word itself.
        if (item.word === qLower || item.slug.toLowerCase() === qLower) {
          score += 1000;
          why.push('exact word match');
          exactHit = true;
        } else {
          // multi-word query containing the exact YOUSPEAK word as a token
          if (tokens.includes(item.word) || tokens.includes(item.slug.toLowerCase())) {
            score += 950;
            why.push('the query names this word');
            exactHit = true;
          } else if (item.word.includes(qLower) && qLower.length >= 3) {
            score += 600;
            why.push('the word contains the query');
            exactHit = true;
          } else {
            for (const t of tokens) {
              if (t.length >= 3 && item.word.includes(t)) {
                score += 350;
                why.push(`the word contains “${t}”`);
                exactHit = true;
              }
            }
          }
        }

        // ── 2. Family match ───────────────────────────────────────────
        // Shared suffix-clan, or a morpheme root whose meaning speaks to
        // a concept the query raised.
        if (item.family) {
          // Does any query token expand into the family's concept kin?
          for (const t of tokens) {
            const kin = expandConcept(t);
            if (kin.has(item.family.family) || kin.has(item.family.suffix)) {
              score += 220;
              why.push(`family match: this is a ${item.family.note} and “${t}” is its kin`);
              familyHit = true;
            }
          }
        }
        // Morpheme-meaning family: a root inside this word whose meaning
        // contains a query concept (or its kin).
        if (item.morphMeanings) {
          for (const t of tokens) {
            const kin = expandConcept(t);
            for (const k of kin) {
              if (k.length >= 3 && item.morphMeanings.includes(k)) {
                score += 180;
                const morph = item.morphemes.find(m =>
                  (m.meaning || '').toLowerCase().includes(k));
                const mname = morph ? (morph.latin || morph.meaning || 'a root') : 'a root';
                why.push(`family match: the root “${mname}” in this word means something like “${t}”`);
                familyHit = true;
                break;
              }
            }
          }
        }

        // ── 3. Definition / gap match ─────────────────────────────────
        // The query's concepts appear in the definition or the gap.
        const parts = item.meaningText.split(' \u0001 ');
        const defText = parts[0] || '';
        const gapText = parts[1] || '';
        for (const t of tokens) {
          const kin = expandConcept(t);
          // direct token hit in definition
          if (defText.includes(t) && t.length >= 3) {
            score += 60;
            why.push(`definition contains “${t}”`);
            meaningHits++;
          }
          // direct token hit in gap
          if (gapText.includes(t) && t.length >= 3) {
            score += 45;
            why.push(`the gap it fills contains “${t}”`);
            meaningHits++;
          }
          // concept-kin hit in definition or gap (synonym expansion)
          for (const k of kin) {
            if (k === t) continue;
            if (k.length < 4) continue;
            if (defText.includes(k)) {
              score += 25;
              why.push(`definition speaks of “${k}” (kin of “${t}”)`);
              meaningHits++;
            } else if (gapText.includes(k)) {
              score += 20;
              why.push(`the gap speaks of “${k}” (kin of “${t}”)`);
              meaningHits++;
            }
          }
        }

        // Tier weighting — Core words are more canonical, a slight nudge.
        if (item.entry.tier) {
          const tier = item.entry.tier.toLowerCase();
          if (tier === 'core') score += 8;
          else if (tier === 'specialized') score += 4;
        }
        // The canon's own score is a faint tiebreaker of earned weight.
        if (typeof item.entry.score === 'number') {
          score += Math.min(item.entry.score, 10);
        }

        if (score > 0) {
          results.push({
            slug: item.slug,
            entry: item.entry,
            score,
            exactHit,
            familyHit,
            meaningHits,
            why: dedupeWhy(why),
          });
        }
      }

      // Rank: exact > family > meaning-hits, then by raw score, then canon score.
      results.sort((a, b) => {
        if (a.exactHit !== b.exactHit) return a.exactHit ? -1 : 1;
        if (a.familyHit !== b.familyHit) return a.familyHit ? -1 : 1;
        if (b.meaningHits !== a.meaningHits) return b.meaningHits - a.meaningHits;
        if (b.score !== a.score) return b.score - a.score;
        return (b.entry.score || 0) - (a.entry.score || 0);
      });

      return results.slice(0, 24);
    }

    // Convenience: search and return only the bare rank list for the UI.
    rank(query) {
      return this.search(query).map(r => ({
        slug: r.slug,
        entry: r.entry,
        why: r.why,
        score: r.score,
      }));
    }
  }

  function dedupeWhy(why) {
    const seen = new Set();
    const out = [];
    for (const w of why) {
      if (!seen.has(w)) { seen.add(w); out.push(w); }
    }
    return out;
  }

  // Export.
  global.WisdomSearch = WisdomSearch;
})(typeof window !== 'undefined' ? window : this);