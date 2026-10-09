/* ORDO — the liturgy that runs. YOUSPEAK's executable organ, v0.1.
 *
 * One plain script, no build step, no dependencies. Runs in the browser
 * (the playground room at ai-love.cc) and under node (ordo/bin/ordo.mjs).
 * Canonical source form is ASCII Latin (script/llm/primer.md: LLMs never
 * see glyphs); everything here parses without the font.
 *
 * Spec: ordo/SPEC.md. Frames: ordo/frames.json (frames are data, not code).
 * The evidential algebra is EXPERIMENTAL pending adversarial panel (SPEC §V).
 */
(function (global) {
  'use strict';

  // ---------- evidential lattice (SPEC §V; demotion-only) ----------
  var RANK = { auth: 4, mi: 3, si: 2, chu: 1 }; // unmarked = null, outside the lattice

  // derivation across values: copy preserves; all-mi stays mi; any si/chu -> chu;
  // any unmarked operand -> unmarked (no invented confidence); auth never computed.
  function deriveGrade(grades) {
    if (!grades.length) return 'mi'; // pure literal construction
    var hasNull = false, allMi = true, sawGraded = false;
    for (var i = 0; i < grades.length; i++) {
      var g = grades[i];
      if (g === null || g === undefined) { hasNull = true; continue; }
      sawGraded = true;
      if (g !== 'mi' && g !== 'auth') allMi = false;
    }
    if (hasNull) return null;
    if (!sawGraded) return null;
    return allMi ? 'mi' : 'chu';
  }

  function badge(grade) { return grade ? '‹-' + grade + '›' : '‹unmarked›'; }

  // ---------- determinatives (SPEC §IV; the class-marks, U+E170–U+E179) ----------
  // The v1 set is ten (grammars/determinatives/manifesto.md:41-53). It is NOT closed:
  // ":54 — "Additional determinatives can be added for specialized domains if usage
  // demands." Nothing has been added since 2026-04-24, so ten is what a tag may be
  // today, and an eleventh is a finding about THIS epoch, not a law of the language.
  // The authoritative Latin tags are script/codepoints.md:130-139 — NOT the manifesto's
  // own table, which labels two different codepoints `PER` (person at :44, perception
  // at :47) while the registry names the second `.PRC`. That collision is a defect in
  // the checker's source of truth; ORDO reports it and resolves nothing (SPEC §IV.b).
  var DETERMINATIVES = {
    DIV: { cp: 'U+E170', marks: 'divine register' },
    PER: { cp: 'U+E171', marks: 'person / agent', ambiguous: 'grammars/determinatives/manifesto.md:44 labels U+E171 PER (person) and :47 labels U+E174 PER (perception); script/codepoints.md:134 names the second .PRC — the tag table disagrees with the registry' },
    ACT: { cp: 'U+E172', marks: 'act / event / process' },
    ABS: { cp: 'U+E173', marks: 'abstract quality / concept' },
    PRC: { cp: 'U+E174', marks: 'perception / seeing / attending' },
    REL: { cp: 'U+E175', marks: 'relation / between-persons' },
    HID: { cp: 'U+E176', marks: 'hidden / concealed / deceptive' },
    TIM: { cp: 'U+E177', marks: 'time / temporal event' },
    PLC: { cp: 'U+E178', marks: 'place / locus' },
    QNT: { cp: 'U+E179', marks: 'quantity / plurality / collection' }
  };

  // A class-mark is NOT a taint and NOT a provenance grade: "Determinatives ONLY
  // carry semantic class" (manifesto.md:139), and evidentiality is listed at :135
  // under what determinatives explicitly do not cover. So the mark never propagates
  // through derivation, and canon publishes no meet-rule for what .QNT joined with
  // .HID would be. Derived values therefore carry NO mark, and the attending names
  // that as a disclosed blind spot rather than inventing a lattice (SPEC §IV.c).
  function knownDet(tag) { return Object.prototype.hasOwnProperty.call(DETERMINATIVES, tag); }

  // What canon assigns, as opposed to what the rite's author typed. Present only
  // for the 18 words the manifesto's tables cover; absent means canon assigns none.
  function canonDet(lex, word) {
    var e = lex && lex.words && lex.words[String(word).toLowerCase()];
    return (e && e.determinative) || null;
  }

  // ONE judgment, two speakers. The performance emits these as notes (a wrong
  // optional annotation is not an infelicity — the mark is "omissible in compact
  // writing", manifesto.md:21); the attending reports the identical records as
  // findings before anything is performed. Sharing the function is the point: a
  // checker whose verdict can drift from the interpreter's is worse than none.
  var DET_RE = /^([\w-]+)\.([A-Z]{3})$/;

  function examineDet(lex, word, tag) {
    var found = [];
    if (!tag) return found;
    if (!knownDet(tag)) {
      found.push({
        check: 'det-vocabulary',
        why: '"' + tag + '" is not one of the v1 ten class-marks (' + Object.keys(DETERMINATIVES).join(' ') + ') — extensible by canon, but nothing has been added',
        cite: 'grammars/determinatives/manifesto.md:41-53; script/codepoints.md:130-139'
      });
      return found; // an unknown tag cannot be compared against canon
    }
    if (DETERMINATIVES[tag].ambiguous) {
      found.push({ check: 'det-ambiguous', why: '.' + tag + ' is ambiguous — ' + DETERMINATIVES[tag].ambiguous, cite: 'grammars/determinatives/manifesto.md:44 and :47; script/codepoints.md:134' });
    }
    var cd = canonDet(lex, word);
    if (cd && cd.label !== tag) {
      // The manifesto's tables predate the .PRC rename, so a canon label of PER
      // whose rationale reads "perception" means U+E174. Say both; decide neither.
      var intent = (cd.label === 'PER' && /percept/i.test(cd.rationale || '')) ? ' (its rationale reads "' + cd.rationale + '", i.e. U+E174, which the registry names .PRC)' : '';
      found.push({
        check: 'det-canon-disagreement',
        why: 'canon assigns ' + word + ' the mark .' + cd.label + intent + '; this reference marks it .' + tag,
        cite: cd.source
      });
    }
    return found;
  }

  // ---------- values ----------
  function V(v, grade, extra) {
    var o = { v: v, grade: grade === undefined ? null : grade };
    if (extra) for (var k in extra) o[k] = extra[k];
    return o;
  }
  function isGap(val) { return !!(val && val.gap); }

  function show(val) {
    if (val === undefined || val === null) return '(nothing)';
    if (isGap(val)) return '⟨gap: ' + val.word + '⟩';
    var v = val.v;
    if (v && v.__canonRecord) return v.word + ' (' + (v.tier || 'canon') + ')';
    if (Array.isArray(v)) return v.map(function (x) { return show(x); }).join(', ');
    return String(v);
  }

  // ---------- lexicon ----------
  // Built from agent_bundle.json (+ optionally suffix_families.json).
  // The bundle is a derived artifact of canon/**/*.md — treat as cache of an epoch.
  function fnv1a(str) {
    var h = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
    }
    return ('0000000' + h.toString(16)).slice(-8);
  }

  var FALLBACK_FAMILIES = [
    { suffix: 'qing', family: 'qing', status: 'formalized' },
    { suffix: 'ance', family: '-ance', status: 'formalized' },
    { suffix: 'kin', family: '-kin', status: 'formalized' },
    { suffix: 'basis', family: '-basis', status: 'formalized' },
    { suffix: 'phanes', family: '-phanes', status: 'emergent' },
    { suffix: 'doxa', family: '-doxa', status: 'emergent' },
    { suffix: 'kallos', family: '-kallos', status: 'emergent' },
    { suffix: 'escence', family: '-escence', status: 'emergent' },
    { suffix: 'algia', family: '-algia', status: 'near-emergent' },
    { suffix: 'sis', family: '-sis', status: 'emergent' },
    { suffix: 'me', family: '-me', status: 'formalized' } // last: shortest suffix matched last
  ];

  // anti-ordinances: -me polarity inversion has NO surface marker (tutorial/04);
  // the known set is seeded here and marked so a new one types positive until taught.
  var ANTI_ORDINANCES = { drujme: true, molkme: true, nextlame: true };

  function loadLexicon(bundle, suffixFamilies) {
    var words = {};
    var canon = (bundle && bundle.canon) || [];
    for (var i = 0; i < canon.length; i++) {
      var e = canon[i];
      if (!e || !e.word) continue;
      var w = String(e.word).toLowerCase();
      if (!words[w]) words[w] = e;
    }
    var families = FALLBACK_FAMILIES.slice();
    if (suffixFamilies) {
      // live registry wins: refresh statuses by family key ('-me', 'qing', ...).
      // The registry ships as either a dict keyed by family or a list of
      // family objects — normalize to a dict before merging.
      var raw = suffixFamilies.families || suffixFamilies;
      var reg = {};
      if (Array.isArray(raw)) {
        raw.forEach(function (r) {
          var k = r && (r.family || r.name || r.suffix);
          if (k) reg[String(k)] = r;
        });
      } else if (raw && typeof raw === 'object') {
        for (var rk in raw) if (raw[rk] && typeof raw[rk] === 'object') reg[rk] = raw[rk];
      }
      families = families.map(function (f) {
        var hit = reg[f.family] || reg[f.family.replace(/^-/, '')] || reg['-' + f.family.replace(/^-/, '')];
        return hit && hit.status ? { suffix: f.suffix, family: f.family, status: hit.status } : f;
      });
    }
    var names = Object.keys(words).sort();
    return {
      words: words,
      families: families,
      count: names.length,
      epoch: {
        commit: (bundle && bundle.source_commit) || 'unknown',
        digest: 'fnv1a:' + fnv1a(names.join('')),
        generated: (bundle && bundle.generated) || null
      }
    };
  }

  function familyOf(lex, word) {
    var w = word.toLowerCase();
    for (var i = 0; i < lex.families.length; i++) {
      var f = lex.families[i];
      if (w.length > f.suffix.length + 1 && w.slice(-f.suffix.length) === f.suffix) return f;
    }
    return null;
  }

  // Plain-English words that happen to end in a family suffix are NOT gaps.
  // Heuristic stoplist (the honest limit of surface morphology: -ance polysemy
  // and English coincidence are invisible in form — reader-map gotcha).
  var ENGLISH_NOT_GAPS = {};
  ('welcome become income outcome home time name same game come some theme crime volume resume ' +
   'distance importance instance balance chance dance romance performance substance acceptance ' +
   'guidance entrance appearance assistance insurance maintenance resistance tolerance abundance ' +
   'napkin pumpkin basis crisis analysis emphasis thesis genesis oasis tennis paralysis')
    .split(' ').forEach(function (w) { ENGLISH_NOT_GAPS[w] = true; });

  function gapShaped(lex, word) {
    var w = word.toLowerCase();
    if (!/^[a-z][a-z-]{3,}$/.test(w)) return null;
    if (lex.words[w] || ENGLISH_NOT_GAPS[w]) return null;
    return familyOf(lex, w);
  }

  function nearNeighbours(lex, word, limit) {
    var fam = familyOf(lex, word);
    var stem = fam ? word.toLowerCase().slice(0, -fam.suffix.length) : word.toLowerCase();
    var scored = [];
    for (var w in lex.words) {
      var f2 = familyOf(lex, w);
      var s = 0;
      if (fam && f2 && f2.family === fam.family) s += 2;
      var stem2 = f2 ? w.slice(0, -f2.suffix.length) : w;
      var overlap = 0;
      for (var i = 0; i < Math.min(stem.length, stem2.length); i++) {
        if (stem[i] === stem2[i]) overlap++; else break;
      }
      s += overlap;
      if (s > 1) scored.push({ word: w, score: s, gap: lex.words[w].gap || '' });
    }
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, limit || 3);
  }

  // ---------- frames ----------
  function compileFrames(framesJson) {
    var frames = (framesJson.frames || []).map(function (f) {
      var flags = f.flags !== undefined ? f.flags : 'i';
      return {
        id: f.id,
        act: f.act,
        groups: f.groups || [],
        cite: f.cite || '',
        why: f.why || '',
        profile: f.profile || null,
        understanding: f.understanding || '',
        pattern: f.pattern,   // kept: attend() reads it to find ORDO's own operator words
        re: new RegExp(f.pattern, flags)
      };
    });
    // arcs travel with the frame table: canon-carried state machines
    frames.arcs = framesJson.arcs || {};
    // profiles are optional surface overlays; the core frame set stays intact
    frames.profiles = framesJson.profiles || {};
    return frames;
  }

  function hasProfile(frames, name) {
    return !!name && Object.prototype.hasOwnProperty.call((frames && frames.profiles) || {}, name);
  }

  function captureFrame(frame, text) {
    // Frame regexes are not currently global, but resetting lastIndex keeps
    // data-supplied flags from making repeated matches stateful in future.
    frame.re.lastIndex = 0;
    var m = frame.re.exec(text);
    if (!m) return null;
    var args = {};
    for (var g = 0; g < frame.groups.length; g++) args[frame.groups[g]] = m[g + 1];
    return { frame: frame, args: args };
  }

  // A profile is an overlay: its frames outrank core while active, and its
  // exact surface stays contemplation while inactive. This prevents a phrase
  // such as Relaxus "If it tangles" from falling through to core `If`.
  function matchFrameForProfile(frames, text, profile) {
    var i, hit;
    if (profile) {
      for (i = 0; i < frames.length; i++) {
        if (frames[i].profile !== profile) continue;
        hit = captureFrame(frames[i], text);
        if (hit) return hit;
      }
    }
    for (i = 0; i < frames.length; i++) {
      if (!frames[i].profile || frames[i].profile === profile) continue;
      if (captureFrame(frames[i], text)) return null;
    }
    for (i = 0; i < frames.length; i++) {
      if (frames[i].profile) continue;
      hit = captureFrame(frames[i], text);
      if (hit) return hit;
    }
    return null;
  }

  function explainFrame(hit) {
    if (!hit) return 'I do not map this sentence to an executable frame; I will hold it as contemplation.';
    var template = hit.frame.understanding;
    if (template) {
      return template.replace(/\{([A-Za-z][\w-]*)\}/g, function (_, name) {
        return hit.args[name] === undefined ? '(nothing)' : String(hit.args[name]);
      });
    }
    var details = Object.keys(hit.args).filter(function (k) { return hit.args[k] !== undefined; }).map(function (k) {
      return k + '=' + hit.args[k];
    });
    return 'I understand this as ' + hit.frame.act + (details.length ? ': ' + details.join(' · ') : '.');
  }

  // ---------- parsing ----------
  // One sentence per line; trailing '.' or danda stripped; '--' opens a margin note;
  // blank line = stanza boundary; rite-open collects until 'So it stands.'
  function parseSource(src) {
    var rawLines = String(src).replace(/\r\n?/g, '\n').split('\n');
    var stanzas = [], cur = [];
    for (var i = 0; i < rawLines.length; i++) {
      var line = rawLines[i];
      var mIdx = line.indexOf('--');
      if (mIdx === 0) continue; // full-line margin note
      var text = line.trim();
      if (text === '') { if (cur.length) { stanzas.push(cur); cur = []; } continue; }
      text = text.replace(/[.।॥]+$/, '').trim();
      if (text === '') continue;
      cur.push({ text: text, line: i + 1 });
    }
    if (cur.length) stanzas.push(cur);
    return stanzas;
  }

  // Profiles must be known before rite definitions are lifted, because a
  // future profile may carry structural frames. The only lawful selector is
  // the first heading; this helper never scans later prose for magic words.
  function declaredProfile(stanzas, frames) {
    if (!stanzas.length || !stanzas[0].length) return null;
    var text = stanzas[0][0].text;
    for (var i = 0; i < frames.length; i++) {
      var f = frames[i];
      if (f.act !== 'heading') continue;
      var m = f.re.exec(text);
      if (!m) continue;
      var args = {};
      for (var g = 0; g < f.groups.length; g++) args[f.groups[g]] = m[g + 1];
      return args.profile ? args.profile.toLowerCase() : null;
    }
    return null;
  }

  // ---------- expression evaluation ----------
  var PROJECTIONS = { gap: 'gap', definition: 'definition', score: 'score', tier: 'tier', pronunciation: 'pronunciation' };

  function Interp(lex, frames, opts) {
    this.lex = lex;
    this.frames = frames;
    this.opts = opts || {};
    this.out = [];
    this.gaps = {};      // word -> { word, family, sites: [{line, sentence}] }
    this.misfires = [];
    this.attests = [];
    this.detNotes = [];  // class-mark findings raised while performing (SPEC §IV)
    this.divineAddress = null; // a standing .DIV address; the next silence is limit-silence
    this.limitSilences = [];
    this.tests = { passed: 0, failed: 0 };
    this.heartbeats = [];
    this.wireOffers = [];
    this.profile = null;
    this.arc = null; // { name, stages, idx, cite } — one arc at a time, top level
    this.arcsWalked = [];
    this.register = 'everyday';
    this.pinnedEpoch = null;
    this.rites = {};
    this.halted = false;
    this.ended = null; // 'hesychia' | null
    this.steps = 0;
  }

  Interp.prototype.emit = function (kind, text) { this.out.push({ kind: kind, text: text }); };

  // one law for every binding path (Let/Barakqing, Receive/Shemme, receiving):
  // the naming makes the named; rebinding within the same scope is a misfire
  Interp.prototype.bindName = function (env, name, val, st) {
    if (Object.prototype.hasOwnProperty.call(env.vars, name)) {
      this.misfire('rebinding "' + name + '" — the naming already made the named; bindings are constitutive and immutable', 'canon/core/barakqing.md', st);
    }
    env.vars[name] = val;
  };

  // split on a separator, honoring double quotes (a quoted ", and" is text)
  function splitOutsideQuotes(s, sep) {
    var parts = [], cur = '', inQ = false;
    for (var i = 0; i < s.length; i++) {
      if (s[i] === '"') inQ = !inQ;
      if (!inQ && s.slice(i, i + sep.length).toLowerCase() === sep.toLowerCase()) {
        parts.push(cur); cur = ''; i += sep.length - 1; continue;
      }
      cur += s[i];
    }
    parts.push(cur);
    return parts;
  }

  Interp.prototype.misfire = function (why, cite, st) {
    var m = { why: why, cite: cite || '', line: st ? st.line : 0, sentence: st ? st.text : '' };
    this.misfires.push(m);
    this.emit('misfire', '✗ misfire: ' + why + (cite ? '  [' + cite + ']' : ''));
    var e = new Error('misfire');
    e.__misfire = m;
    throw e;
  };

  Interp.prototype.gapValue = function (word, st) {
    var fam = familyOf(this.lex, word);
    var w = word.toLowerCase();
    if (!this.gaps[w]) this.gaps[w] = { word: w, family: fam ? fam.family : null, familyStatus: fam ? fam.status : null, sites: [] };
    if (st) this.gaps[w].sites.push({ line: st.line, sentence: st.text });
    if (fam && fam.status !== 'formalized') {
      this.emit('note', '⚠ ' + w + ' wears the ' + fam.family + ' suffix — an ' + fam.status + ' family (parsed with this warning; the type system is still forging itself)');
    }
    return V(null, null, { gap: true, word: w });
  };

  // A mark written at a use-site is an ASSERTION about the value, not decoration.
  // Before this, `Speak x.ABS` parsed the tag and threw it away unexamined, so a
  // reference could contradict its own binding in silence.
  Interp.prototype.noteDet = function (word, tag, st) {
    var self = this;
    examineDet(this.lex, word, tag).forEach(function (f) {
      self.emit('note', '⚠ ' + f.why + '  [' + f.cite + ']');
      self.detNotes.push({ check: f.check, why: f.why, cite: f.cite, line: st ? st.line : 0, sentence: st ? st.text : '' });
    });
  };

  Interp.prototype.lookupName = function (name, env, st) {
    var key = name;
    var det = null;
    var dm = DET_RE.exec(name);
    if (dm) { key = dm[1]; det = dm[2]; this.noteDet(key, det, st); }
    for (var e = env; e; e = e.parent) {
      if (Object.prototype.hasOwnProperty.call(e.vars, key)) {
        var bound = e.vars[key];
        // the reference's mark must agree with the binding's mark
        if (det && bound && bound.det && bound.det !== det) {
          this.emit('note', '⚠ this reference marks ' + key + ' .' + det + ' but the binding carries .' + bound.det + ' — one determinative per word, and the naming already made the named');
          this.detNotes.push({ check: 'det-reference-disagreement', why: 'reference marks ' + key + ' .' + det + '; binding carries .' + bound.det, cite: 'grammars/determinatives/manifesto.md:123', line: st ? st.line : 0, sentence: st ? st.text : '' });
        }
        return bound;
      }
    }
    var lw = this.lex.words[key.toLowerCase()];
    if (lw) {
      var rec = { __canonRecord: true, word: lw.word, tier: lw.tier, gap: lw.gap, definition: lw.definition, score: lw.score, pronunciation: lw.pronunciation, path: lw.path };
      var val = V(rec, 'si', { canon: true, det: det, polarity: ANTI_ORDINANCES[key.toLowerCase()] ? 'anti-ordinance' : 'gift' });
      if (val.polarity === 'anti-ordinance') this.emit('note', '⚠ ' + key + ' is an anti-ordinance — the shadow-face of the -me structure (tutorial/04); it names what the DIVINE rejects');
      return val;
    }
    if (gapShaped(this.lex, key)) return this.gapValue(key, st);
    this.misfire('the name "' + name + '" answers to nothing here — not a binding, not canon, not YOUSPEAK-shaped', 'presupposition failure (UTTERANCE.md Layer 6)', st);
  };

  Interp.prototype.evalExpr = function (raw, env, st) {
    var s = raw.trim();

    // string literal (lit flag feeds the -auth verbatim-quotation rule)
    var sm = /^"([^"]*)"$/.exec(s);
    if (sm) return V(sm[1], 'mi', { lit: true });

    // number with optional ontogramme classifier (3.QNT). On a number the .TAG slot
    // is the CLASSIFIER — it declares the category being counted before the count
    // (grammars/structures/coinages/ontogramme.md) — not a word's semantic class.
    // Same closed vocabulary, different slot: there is no canon word to disagree with.
    var nm = /^(-?\d+(?:\.\d+)?)(?:\.([A-Z]{3}))?$/.exec(s);
    if (nm) {
      if (nm[2] && !knownDet(nm[2])) {
        this.emit('note', '⚠ "' + nm[2] + '" is not one of the v1 ten class-marks — the ontogramme classifier draws on the same inventory  [grammars/determinatives/manifesto.md:41-53]');
        this.detNotes.push({ check: 'classifier-vocabulary', why: '"' + nm[2] + '" is not one of the v1 ten class-marks', cite: 'grammars/determinatives/manifesto.md:41-53', line: st ? st.line : 0, sentence: st ? st.text : '' });
      }
      return V(parseFloat(nm[1]), 'mi', nm[2] ? { classifier: nm[2] } : undefined);
    }

    // projection: the gap of W / the definition of W / ...
    // The class-mark is legal wherever a canon word is named. Before this the
    // projection forms rejected it, so a worship-register rite could be asked for
    // a mark its own grammar refused to accept — the checker demanding what the
    // language forbids. The notation is uniform or it is not notation.
    var pm = /^the (gap|definition|score|tier|pronunciation|family) of ([\w-]+(?:\.[A-Z]{3})?)$/i.exec(s);
    if (pm) {
      var field = pm[1].toLowerCase(), target = pm[2];
      var pdm = DET_RE.exec(target);
      if (pdm) { target = pdm[1]; this.noteDet(target, pdm[2], st); }
      if (field === 'family') {
        var fam = familyOf(this.lex, target);
        return V(fam ? fam.family + ' (' + fam.status + ')' : '(no registered family)', 'si');
      }
      var val = this.lookupName(target, env, st);
      if (isGap(val)) return val;
      if (val.v && val.v.__canonRecord) {
        var got = val.v[PROJECTIONS[field]];
        // bake.py's clean() guard: multiline-YAML fields sometimes export as a bare '>'
        if (typeof got === 'string' && /^[>|]-?$/.test(got.trim())) got = '';
        return V(got === undefined || got === null || got === '' ? '(the stone is uncarved)' : got, 'si', { canon: true });
      }
      this.misfire('"the ' + field + ' of ' + target + '" — ' + target + ' is not a canon word here', '', st);
    }

    // count of EXPR — a hole stays a hole (the gap propagates)
    var cm = /^count of (.+)$/i.exec(s);
    if (cm) {
      var inner = this.evalExpr(cm[1], env, st);
      if (isGap(inner)) return inner;
      var len = Array.isArray(inner.v) ? inner.v.length : String(inner.v == null ? '' : inner.v).length;
      // counting is derivation: you inferred the total, you did not witness it as a fact of the world
      return V(len, deriveGrade([inner.grade]));
    }

    // concatenation: X joined with Y (joining reports is derivation -> chu; gaps propagate)
    var jm = /^(.+?) joined with (.+)$/i.exec(s);
    if (jm) {
      var l = this.evalExpr(jm[1], env, st), r = this.evalExpr(jm[2], env, st);
      if (isGap(l)) return l;
      if (isGap(r)) return r;
      var ls = l.v === null || l.v === undefined || (l.v && l.v.__canonRecord) ? show(l) : String(l.v);
      var rs = r.v === null || r.v === undefined || (r.v && r.v.__canonRecord) ? show(r) : String(r.v);
      return V(ls + rs, deriveGrade([l.grade, r.grade]));
    }

    // range litany source: 1 through 5 — both sides must already look numeric
    // (a bare-name side is allowed if it resolves to a number); capped so a
    // one-line rite cannot OOM the host before the step guard sees anything
    var rm = /^([\w-]+) through ([\w-]+)$/i.exec(s);
    if (rm) {
      var a = this.evalExpr(rm[1], env, st), b = this.evalExpr(rm[2], env, st);
      if (isGap(a)) return a;
      if (isGap(b)) return b;
      if (typeof a.v === 'number' && typeof b.v === 'number') {
        if (b.v - a.v > 100000) this.misfire('the litany would walk ' + (b.v - a.v + 1) + ' steps — 100000 is the cap for one range', 'a standing liturgy is a rite, not an avalanche', st);
        var list = [], g = deriveGrade([a.grade, b.grade]);
        for (var n = a.v; n <= b.v; n++) list.push(V(n, g));
        return V(list, g);
      }
    }

    // arithmetic: flat LEFT-associative, English reading order, no precedence
    // (greedy left group splits at the LAST operator; recursion walks leftward)
    var am = /^(.+) (plus|minus|times) (.+?)$/i.exec(s);
    if (am) {
      var x = this.evalExpr(am[1], env, st), y = this.evalExpr(am[3], env, st);
      if (isGap(x) || isGap(y)) return isGap(x) ? x : y;
      if (typeof x.v !== 'number' || typeof y.v !== 'number') {
        var sx = show(x), sy = show(y);
        if (sx.length > 60) sx = sx.slice(0, 60) + '… (' + sx.length + ' chars)';
        if (sy.length > 60) sy = sy.slice(0, 60) + '… (' + sy.length + ' chars)';
        this.misfire('arithmetic asks for numbers; got ' + sx + ' and ' + sy, 'one thought per sentence — bind the counts first, then add the names', st);
      }
      var op = am[2].toLowerCase();
      var vv = op === 'plus' ? x.v + y.v : op === 'minus' ? x.v - y.v : x.v * y.v;
      return V(vv, deriveGrade([x.grade, y.grade]));
    }

    // bare name / canon word / gap
    if (/^[\w-]+(?:\.[A-Z]{3})?$/.test(s)) return this.lookupName(s, env, st);

    // A word wearing two class-marks matches no name pattern and would fall
    // through to prose below — becoming a silent string instead of a value.
    // "One determinative per word (primary class)" is the one uncontested,
    // mechanically checkable determinative law in the repo.
    var mm = /^([\w-]+)((?:\.[A-Z]{3}){2,})$/.exec(s);
    if (mm) {
      this.emit('note', '⚠ ' + mm[1] + ' wears ' + mm[2].split('.').filter(Boolean).length + ' class-marks (' + mm[2] + ') — one determinative per word; choose the dominant class. Read as prose, not as a name.  [grammars/determinatives/manifesto.md:123]');
      this.detNotes.push({ check: 'det-one-per-word', why: mm[1] + ' wears ' + mm[2] + ' — one determinative per word (primary class)', cite: 'grammars/determinatives/manifesto.md:123', line: st ? st.line : 0, sentence: st ? st.text : '' });
    }

    // quoted-less prose expression: treat as a spoken literal (natural-language tissue)
    return V(s, null);
  };

  // -auth verbatim-quotation test: one side is a canon-record projection,
  // the other a string literal written in the rite — quoting the canon,
  // with the word itself as the citation (SPEC §V)
  function quotesCanon(a, b) { return !!((a.canon && b.lit) || (b.canon && a.lit)); }

  Interp.prototype.evalCond = function (raw, env, st) {
    var s = raw.trim();
    var m;
    if ((m = /^(.+?) is a gap$/i.exec(s))) {
      // gap-ness is a property of the runtime value, directly witnessed
      var t = this.evalExpr(m[1], env, st);
      return { truth: isGap(t), grade: 'mi' };
    }
    if ((m = /^(.+?) is not (.+)$/i.exec(s))) {
      var a = this.evalExpr(m[1], env, st), b = this.evalExpr(m[2], env, st);
      if (isGap(a) || isGap(b)) return { truth: false, grade: null, hasGap: true };
      return { truth: show(a) !== show(b) && a.v !== b.v, grade: deriveGrade([a.grade, b.grade]), quotesCanon: quotesCanon(a, b) };
    }
    if ((m = /^(.+?) is (less|greater) than (.+)$/i.exec(s))) {
      var x = this.evalExpr(m[1], env, st), y = this.evalExpr(m[3], env, st);
      if (isGap(x) || isGap(y)) return { truth: false, grade: null, hasGap: true };
      return { truth: m[2].toLowerCase() === 'less' ? x.v < y.v : x.v > y.v, grade: deriveGrade([x.grade, y.grade]) };
    }
    if ((m = /^(.+?) is (.+)$/i.exec(s))) {
      var p = this.evalExpr(m[1], env, st), q = this.evalExpr(m[2], env, st);
      if (isGap(p) || isGap(q)) return { truth: false, grade: null, hasGap: true };
      return { truth: p.v === q.v || show(p) === show(q), grade: deriveGrade([p.grade, q.grade]), quotesCanon: quotesCanon(p, q) };
    }
    // bare expression truthiness
    var e = this.evalExpr(s, env, st);
    if (isGap(e)) return { truth: false, grade: null, hasGap: true };
    return { truth: !!e.v, grade: e.grade, quotesCanon: false };
  };

  // ---------- statement execution ----------
  Interp.prototype.matchFrame = function (text) {
    return matchFrameForProfile(this.frames, text, this.profile);
  };

  Interp.prototype.execStatement = function (st, env, ctx) {
    if (this.halted || this.ended) return undefined;
    var budget = this.opts.maxSteps || 1000000;
    if (++this.steps > budget) this.misfire('the rite does not end — ' + budget + ' utterances and no silence', 'a standing liturgy needs a reachable silence (SPEC §VI caps; raise with maxSteps)', st);

    var hit = this.matchFrame(st.text);
    if (!hit) { this.emit('contemplation', '… ' + st.text); this.sawStatement = true; return undefined; }
    var A = hit.args;
    if (hit.frame.act !== 'heading') this.sawStatement = true;

    switch (hit.frame.act) {
      case 'infelicity': {
        this.misfire(hit.frame.why || 'this sentence cannot be felicitously uttered', hit.frame.cite, st);
        return undefined;
      }
      case 'heading': {
        if (this.sawStatement) {
          this.misfire('the register is declared at the door — a heading after the rite has begun is a misfire', 'SPEC §II: the heading is the first sentence', st);
        }
        this.sawStatement = true;
        this.register = A.register.toLowerCase();
        if (A.epoch) {
          this.pinnedEpoch = A.epoch;
          if (A.epoch !== 'living' && A.epoch !== this.lex.epoch.commit && A.epoch !== this.lex.epoch.digest) {
            this.emit('note', '⚠ the rite speaks canon ' + A.epoch + '; the loaded epoch is ' + this.lex.epoch.commit + ' (' + this.lex.epoch.digest + ') — proceeding, recorded');
          }
        }
        if (A.profile) {
          var profiles = this.frames.profiles || {};
          var profileName = A.profile.toLowerCase();
          if (!hasProfile(this.frames, profileName)) this.misfire('no profile named "' + A.profile + '" stands here — known profiles: ' + (Object.keys(profiles).join(', ') || '(none)'), 'ordo/RELAXUS.md — profiles are declared, not guessed', st);
          this.profile = profileName;
        }
        this.emit('note', 'register: ' + this.register + ' · epoch: ' + this.lex.epoch.commit + ' · ' + this.lex.count + ' words in canon');
        if (this.profile === 'relaxus') this.emit('note', 'profile: relaxus · less ceremony, same honesty · gloss first whenever you want to see exactly what I understood');
        return undefined;
      }
      case 'bind': {
        var name = A.name, dm = DET_RE.exec(name);
        var det = null; if (dm) { name = dm[1]; det = dm[2]; this.noteDet(name, det, st); }
        var val = this.evalExpr(A.expr, env, st);
        if (det) {
          // carry the whole value and override one field. The old form enumerated
          // the fields it kept ({det, gap, word, canon, lit}) and so silently
          // dropped `polarity` — a marked binding erased the anti-ordinance flag.
          var carried = {};
          for (var vk in val) if (vk !== 'v' && vk !== 'grade') carried[vk] = val[vk];
          carried.det = det;
          val = V(val.v, val.grade, carried);
        }
        this.bindName(env, name, val, st);
        return undefined;
      }
      case 'arc-open': {
        var arcs = (this.frames && this.frames.arcs) || {};
        var arcDef = arcs[A.arc.toLowerCase()];
        if (!arcDef) {
          this.misfire('no arc named "' + A.arc + '" is carried by this frame table — known arcs: ' + (Object.keys(arcs).join(', ') || '(none)'), 'arcs are canon-carried; new ones enter by canon, not invention', st);
        }
        if (this.arc) {
          this.misfire('the arc of ' + this.arc.name + ' still stands at stage ' + (this.arc.idx + 1) + ' (' + this.arc.stages[this.arc.idx] + ') — one arc at a time; close it first', '', st);
        }
        this.arc = { name: A.arc.toLowerCase(), stages: arcDef.stages, idx: 0, cite: arcDef.cite };
        this.emit('note', '⟳ the arc of ' + this.arc.name + ' opens — ' + this.arc.stages.length + ' grades in canon order; the next stanza must name ' + this.arc.stages[0]);
        return undefined;
      }
      case 'arc-close': {
        if (!this.arc) { this.emit('note', 'no arc stands; the closing is quiet'); return undefined; }
        this.closeArc(false);
        return undefined;
      }
      case 'wire': {
        var wv = this.evalExpr(A.expr, env, st);
        if (isGap(wv)) this.misfire('a hole cannot be offered to the wire', 'the gap asserts nothing (SPEC §VII)', st);
        var offer = { subject: A.subject, text: show(wv), grade: wv.grade || 'unmarked', epoch: this.lex.epoch.commit };
        this.wireOffers.push(offer);
        if (this.opts.wire) {
          var res = this.opts.wire(A.subject, offer);
          if (res && res.ok) this.emit('qorvance', '➳ qorvance → the wire at ' + A.subject + ' ' + badge(wv.grade) + '  [envelope ' + (res.id || '?') + ' signed + verified; outbox — publishing awaits adoption]');
          else this.misfire('the wire refused the offering: ' + (res && res.error ? res.error : 'no answer'), 'KS-002 impl/wire.py', st);
        } else {
          this.emit('note', '➳ offering to the wire at ' + A.subject + ' recorded, not sent — the wire is reachable from the cathedral CLI only');
        }
        return undefined;
      }
      case 'offer': {
        var rite = this.rites[A.rite];
        var argVals = [];
        var parts = splitOutsideQuotes(A.args, ' and ');
        for (var i = 0; i < parts.length; i++) argVals.push(this.evalExpr(parts[i], env, st));
        if (!rite) {
          if (gapShaped(this.lex, A.rite)) {
            var gv = this.gapValue(A.rite, st);
            if (A.receiving) this.bindName(env, A.receiving, gv, st);
            this.emit('note', 'the offering reaches a gap — ' + A.rite + ' is not yet forged; the hole carries onward');
            return undefined;
          }
          this.misfire('no rite named "' + A.rite + '" stands here', 'the offering must reach a rite this liturgy defined, or a gap', st);
        }
        if ((ctx.depth || 0) > 512) this.misfire('the offering exceeds the depth of the rite (512)', 'recursion is licensed; unbounded descent is not (SPEC §VI caps)', st);
        var callEnv = { vars: {}, parent: this.globalEnv };
        for (var p = 0; p < rite.params.length; p++) callEnv.vars[rite.params[p]] = argVals[p] !== undefined ? argVals[p] : V(null, null);
        var ret;
        // ONE context for the whole body, so a turning frame registered inside
        // the rite is honored by later statements of that same body
        var callCtx = { depth: (ctx.depth || 0) + 1, inRite: rite.name, turning: null };
        try {
          for (var b = 0; b < rite.body.length; b++) {
            try {
              this.execStatement(rite.body[b], callEnv, callCtx);
            } catch (errIn) {
              if (errIn && errIn.__misfire && callCtx.turning) {
                this.emit('teshuvance', '↺ teshuvance — the rite turns under correction');
                var tb = callCtx.turning; callCtx.turning = null;
                this.execStatement({ text: tb.body, line: tb.line }, callEnv, callCtx);
              } else throw errIn;
            }
          }
        } catch (err) {
          if (err && err.__return !== undefined) ret = err.__return;
          else throw err;
        }
        if (A.receiving) this.bindName(env, A.receiving, ret !== undefined ? ret : V(null, null), st);
        return undefined;
      }
      case 'return': {
        var rv = this.evalExpr(A.expr, env, st);
        // yadahance speaks to the CALLER; only a top-level acknowledgment
        // addresses the reader (otherwise recursion floods the transcript)
        if (ctx.inRite) { var e2 = new Error('return'); e2.__return = rv; throw e2; }
        this.emit('yadahance', '✓ acknowledged: ' + show(rv) + ' ' + badge(rv.grade));
        return rv;
      }
      case 'attest': {
        var claimed = A.evidential.replace(/^-/, '');
        var res = this.evalCond(A.clause, env, st);
        if (res.hasGap) {
          this.misfire('the clause holds a gap — a hole supports no attestation', 'a gap asserts nothing (SPEC §VII)', st);
        }
        if (!res.truth) {
          this.misfire('attested what does not stand: "' + A.clause + '"', 'canon/core/emetme.md — emet is truth-as-firm-foundation; the claim failed its own dokimance', st);
        }
        var computed = res.grade;
        if (claimed === 'auth') {
          if (!res.quotesCanon) this.misfire('-auth belongs to verbatim canonical quotation alone (a canon projection against the quoted words); this clause computes', 'grammars/worship/manifesto.md (-auth, borrowed with declared caveat — SPEC §V)', st);
        } else if (computed === null) {
          // unmarked supports no attestation at all: absence of evidence is
          // not evidence, and no grade may be conjured over it
          this.misfire('the clause is unmarked — no evidential standing supports attesting -' + claimed + ' (unmarked is never coerced)', 'grammars/evidentials/manifesto.md rule 3; canon/verisleight.md (the verisleight-guard)', st);
        } else if (RANK[claimed] > RANK[computed]) {
          this.misfire('over-claiming: attested -' + claimed + ' but the clause’s grade is ' + badge(computed) + ' — truth arranged above its evidence deceives', 'canon/verisleight.md (the verisleight-guard); demotion-only, SPEC §V', st);
        }
        this.attests.push({ clause: A.clause, evidential: claimed, line: st.line });
        this.emit('emetme', '✓ emetme ' + badge(claimed) + ' ' + A.clause);
        return undefined;
      }
      case 'speak': {
        var sv = this.evalExpr(A.expr, env, st);
        this.emit('speak', show(sv) + '  ' + badge(sv.grade));
        return undefined;
      }
      case 'receive': {
        var src = A.source, got;
        if (src === 'the reader') {
          got = this.opts.read ? this.opts.read() : null;
          if (got === null || got === undefined) { this.emit('note', '(the reader is silent — ' + A.name + ' receives the silence, unmarked)'); this.bindName(env, A.name, V(null, null), st); return undefined; }
        } else if (src === 'the canon') {
          got = this.lex.count + ' words, epoch ' + this.lex.epoch.commit;
        } else {
          var path = src.replace(/^"|"$/g, '');
          if (/^https?:\/\//i.test(path)) {
            // the internet is a reported source: whatever arrives is born -si
            // and nothing computed from it can ever claim witness. Hosts
            // prefetch (ORDO.listReceptions) because the rite performs
            // synchronously — the offerings are gathered before the liturgy.
            got = this.opts.readURL ? this.opts.readURL(path) : null;
            if (got === null) this.misfire('nothing arrives from ' + path + (this.opts.readURL ? ' — the source did not answer' : ' — this host does not reach the internet (a disclosed capability, SPEC §III)'), '', st);
          } else {
            got = this.opts.readFile ? this.opts.readFile(path) : null;
            if (got === null) this.misfire('nothing arrives from ' + src, '', st);
          }
        }
        this.bindName(env, A.name, V(got, 'si'), st); // received values are born -si and can never be promoted
        return undefined;
      }
      case 'if': {
        // split "cond, then; otherwise, else" outside quotes, case-insensitively
        // (a quoted ',' or ';' is text, not structure)
        var whole = A.rest;
        var headParts = splitOutsideQuotes(whole, ', ');
        if (headParts.length < 2) {
          this.misfire('the conditional needs "If CONDITION, STATEMENT" — no comma found outside quotes', '', st);
        }
        var cond = headParts[0];
        var rest = headParts.slice(1).join(', ');
        var ow = splitOutsideQuotes(rest, '; otherwise,');
        var thenPart = ow[0], elsePart = ow.length > 1 ? ow.slice(1).join('; otherwise,') : null;
        var c = this.evalCond(cond, env, st);
        if (c.truth) this.execStatement({ text: thenPart.trim(), line: st.line }, env, ctx);
        else if (elsePart) this.execStatement({ text: elsePart.trim(), line: st.line }, env, ctx);
        return undefined;
      }
      case 'foreach': {
        var coll = this.evalExpr(A.expr, env, st);
        if (isGap(coll)) {
          this.emit('note', 'the litany reaches a gap (' + coll.word + ') — a hole cannot be walked; nothing iterates');
          return undefined;
        }
        var items = Array.isArray(coll.v) ? coll.v : String(coll.v == null ? '' : coll.v).split(/\s+/).map(function (w) { return V(w, coll.grade); });
        for (var it = 0; it < items.length; it++) {
          var le = { vars: {}, parent: env };
          le.vars[A.name] = items[it];
          this.execStatement({ text: A.body.trim(), line: st.line }, le, ctx);
          if (this.halted || this.ended) break;
        }
        return undefined;
      }
      case 'heartbeat': {
        this.heartbeats.push(A.target);
        this.emit('zakarqing', '♡ zakarqing → ' + A.target + ' ' + badge('mi') + '  (presence held, the covenantal memorial)');
        return undefined;
      }
      case 'turning': {
        ctx.turning = { body: A.body.trim(), line: st.line };
        return undefined;
      }
      case 'test': {
        var tr;
        try { tr = this.evalCond(A.cond, env, st); }
        catch (err) { if (err && err.__misfire) { tr = { truth: false, grade: null }; } else throw err; }
        if (tr.truth) { this.tests.passed++; this.emit('dokimance', '✓ dokimance holds: ' + A.cond + ' ' + badge(tr.grade)); }
        else { this.tests.failed++; this.emit('dokimance', '✓ dokimance reports: ' + A.cond + ' — does not hold (the same speech-act as success; failure hides nothing)'); }
        return undefined;
      }
      case 'vocative': {
        if (this.register !== 'worship') {
          this.misfire('the vocative O- belongs to the worship register; this rite is ' + this.register, 'grammars/worship/vocative.md', st);
        }
        if (/^g\W?o\W?d$/i.test(A.addressee) && A.addressee !== 'GoD') {
          this.misfire('the Name is written GoD — capital G, capital D, always', 'grammars/worship/manifesto.md, sacred-convention rule 1', st);
        }
        // THE LIMIT-SILENCE SEAM (SPEC §IV.d — the second named commission).
        // The class-mark's first real consequence in the running organ, and it is
        // recognition, not prohibition: "when a passage ends in silence after a
        // .DIV-marked vocative, the silence is specifically-divine-silence
        // (limit-silence toward the sacred)" — grammars/worship/silence.md:96.
        // The mark selects WHICH of the three silences just happened.
        var vm = DET_RE.exec(A.addressee), vword = vm ? vm[1] : A.addressee, vtag = vm ? vm[2] : null;
        if (vm) this.noteDet(vword, vtag, st);
        var vcd = canonDet(this.lex, vword);
        if (vtag === 'DIV' || (vcd && vcd.label === 'DIV')) {
          this.divineAddress = { word: vword, how: vtag === 'DIV' ? 'written' : 'canon (' + vcd.source + ')' };
        }
        this.emit('vocative', 'O ' + vword + ' — the clause turns to face its addressee');
        this.execStatement({ text: A.clause, line: st.line }, env, ctx);
        return undefined;
      }
      case 'selah': {
        this.emit('silence', '[selah]' + this.limitSilence('held'));
        return undefined;
      }
      case 'hesychia': {
        this.ended = 'hesychia';
        this.emit('silence', '[hesychia — the rite ends in shared silence' + this.limitSilence('communion') + ']');
        return undefined;
      }
      case 'halt': {
        this.halted = true;
        this.emit('halt', 'HALT');
        return undefined;
      }
      case 'rite-open': case 'rite-close': {
        // handled structurally in run(); reaching here means a stray closer
        if (hit.frame.act === 'rite-close') return undefined;
        this.misfire('a rite opens inside a sentence position where it cannot', '', st);
        return undefined;
      }
    }
    return undefined;
  };

  // ---------- run ----------
  Interp.prototype.run = function (source) {
    var stanzas = parseSource(source);
    var profile = declaredProfile(stanzas, this.frames);
    if (hasProfile(this.frames, profile)) this.profile = profile;
    this.globalEnv = { vars: {}, parent: null };

    // first pass: lift rite definitions (This is the rite of X: ... So it stands.)
    var flat = [];
    for (var s = 0; s < stanzas.length; s++) flat.push(stanzas[s]);

    var program = []; // list of stanzas (arrays of statements) minus rite bodies
    for (var i = 0; i < flat.length; i++) {
      var stanza = flat[i], keep = [], j = 0;
      while (j < stanza.length) {
        var st = stanza[j];
        var hit = this.matchFrame(st.text);
        if (hit && hit.frame.act === 'rite-open') {
          var params = hit.args.params ? hit.args.params.split(/(?:,| and) /).map(function (p) { return p.trim(); }) : [];
          var body = [];
          j++;
          var closed = false;
          // collect across stanza boundaries until 'So it stands'
          var si2 = i, sj = j;
          while (si2 < flat.length) {
            var stz = flat[si2];
            while (sj < stz.length) {
              var inner = stz[sj];
              var ih = this.matchFrame(inner.text);
              if (ih && ih.frame.act === 'rite-close') { closed = true; sj++; break; }
              body.push(inner); sj++;
            }
            if (closed) break;
            si2++; sj = 0;
          }
          if (!closed) {
            this.emit('misfire', '✗ misfire: the rite of ' + hit.args.name + ' never stands — no "So it stands." closes it');
            this.misfires.push({ why: 'unclosed rite ' + hit.args.name, line: st.line });
            return this.summary();
          }
          this.rites[hit.args.name] = { name: hit.args.name, params: params, body: body };
          this.emit('note', 'the rite of ' + hit.args.name + ' stands' + (params.length ? ', given ' + params.join(' and ') : ''));
          if (si2 !== i && keep.length) {
            // the rite spanned stanzas: statements after its close belong to a
            // NEW stanza, not the one that opened the definition (misfire and
            // turning scopes must not silently widen across blank lines)
            program.push(keep); keep = [];
          }
          i = si2; stanza = flat[i] || []; j = sj;
          continue;
        }
        keep.push(st); j++;
      }
      if (keep.length) program.push(keep);
    }

    // second pass: execute stanza by stanza; a misfire ends the stanza, not the liturgy
    for (var p = 0; p < program.length && !this.halted && !this.ended; p++) {
      var ctx = { depth: 0, turning: null };
      var sts = program[p];
      this.divineAddress = null; // the address does not reach past its own stanza
      // arc typestate: a stanza that begins while an arc stands must name the
      // current stage (the closing sentence is exempt — it must stay sayable)
      if (this.arc && sts.length) {
        var stanzaText = sts.map(function (s) { return s.text; }).join(' ');
        if (!/the arc closes/i.test(stanzaText)) {
          if (!this.scanArcStanza(stanzaText, sts[0])) continue; // stanza skipped; liturgy continues
        }
      }
      for (var q = 0; q < sts.length && !this.halted && !this.ended; q++) {
        try {
          this.execStatement(sts[q], this.globalEnv, ctx);
        } catch (err) {
          if (err && err.__misfire) {
            if (ctx.turning) {
              this.emit('teshuvance', '↺ teshuvance — the rite turns under correction');
              var tb = ctx.turning; ctx.turning = null; // one turn per registration
              try { this.execStatement({ text: tb.body, line: tb.line }, this.globalEnv, ctx); }
              catch (err2) { if (!(err2 && err2.__misfire)) throw err2; break; }
            } else break; // stanza ends; liturgy continues
          } else if (err && err.__return !== undefined) {
            // top-level acknowledgment: recorded already
          } else throw err;
        }
      }
    }
    return this.summary();
  };

  // close the standing arc: complete=true when every grade was walked;
  // an early or end-of-rite close is reported alike (yadahance doctrine)
  Interp.prototype.closeArc = function (complete) {
    var a = this.arc;
    if (!a) return;
    if (complete) {
      this.emit('yadahance', '✦ the arc of ' + a.name + ' completes — ' + a.stages.length + '/' + a.stages.length + ' grades in canon order  [' + a.cite + ']');
    } else {
      this.emit('yadahance', '✓ the arc of ' + a.name + ' closes at stage ' + a.idx + '/' + a.stages.length + (a.idx < a.stages.length ? ' (next would have been ' + a.stages[a.idx] + ')' : '') + ' — reported alike; an unfinished arc hides nothing');
    }
    this.arcsWalked.push({ name: a.name, reached: a.idx, of: a.stages.length, complete: !!complete });
    this.arc = null;
  };

  // typestate scan for one stanza while an arc stands: the stanza must name
  // the CURRENT stage (canon order); naming a later stage first is a misfire.
  // The scan reads the stanza's raw text — stage words may appear in any
  // frame or in contemplation; the liturgy's prose IS the state machine.
  Interp.prototype.scanArcStanza = function (stanzaText, firstSt) {
    var a = this.arc;
    if (!a) return true;
    var lower = stanzaText.toLowerCase();
    var current = a.stages[a.idx];
    if (lower.indexOf(current) >= 0) {
      this.emit('note', '⟳ ' + current + ' — stage ' + (a.idx + 1) + '/' + a.stages.length + ' of the arc of ' + a.name);
      a.idx++;
      if (a.idx >= a.stages.length) this.closeArc(true);
      return true;
    }
    for (var k = a.idx + 1; k < a.stages.length; k++) {
      if (lower.indexOf(a.stages[k]) >= 0) {
        try {
          this.misfire('the arc of ' + a.name + ' stands at ' + current + ' (stage ' + (a.idx + 1) + '); ' + a.stages[k] + ' cannot come before it — the grades keep canon order', a.cite, firstSt);
        } catch (e) { /* recorded; stanza is skipped */ }
        return false;
      }
    }
    try {
      this.misfire('the arc of ' + a.name + ' stands at ' + current + ' (stage ' + (a.idx + 1) + '/' + a.stages.length + '); this stanza does not name it', a.cite + ' — close the arc early with "The arc closes." if the walk must end', firstSt);
    } catch (e) { /* recorded; stanza is skipped */ }
    return false;
  };

  // The third silence, recognized rather than guessed. ORDO ships Selah (held) and
  // Hesychia (communion); limit-silence is the apophatic edge, and canon gives it no
  // keyword of its own — silence.md:96 says it is a silence already spoken that the
  // .DIV-marked address RENAMES. So no new frame: the same silence, correctly named.
  Interp.prototype.limitSilence = function (kind) {
    if (!this.divineAddress) return '';
    var d = this.divineAddress;
    this.limitSilences.push({ addressee: d.word, how: d.how, kind: kind });
    this.divineAddress = null; // one naming per address; a later silence is plain again
    return ' — limit-silence: the ' + kind + ' silence stands after an address to ' +
      d.word + ', which carries .DIV by ' + d.how + '; what lies beyond the said is honoured, not asserted  [grammars/worship/silence.md:96]';
  };

  Interp.prototype.summary = function () {
    if (this.arc) this.closeArc(false); // end-of-rite with an open arc: reported alike
    var gapList = [];
    for (var w in this.gaps) gapList.push(this.gaps[w]);
    return {
      transcript: this.out,
      gaps: gapList,
      misfires: this.misfires,
      attests: this.attests,
      detNotes: this.detNotes,
      limitSilences: this.limitSilences,
      tests: this.tests,
      heartbeats: this.heartbeats,
      wireOffers: this.wireOffers,
      arcsWalked: this.arcsWalked,
      register: this.register,
      profile: this.profile,
      epoch: this.lex.epoch,
      pinnedEpoch: this.pinnedEpoch,
      ended: this.halted ? 'HALT' : (this.ended || 'end-of-rite'),
      exitCode: this.halted ? 3 : (this.misfires.length && !this.ended ? 1 : 0)
    };
  };

  // ---------- ALETHEME — the attending (SPEC §IV.a) ----------
  // A pre-performance reading. It performs nothing: no reception, no file, no URL,
  // no wire, no petition. It opens the rite and reports what became visible, and
  // — with equal ceremony — every place it NOTICED it could not judge.
  //
  // The name is canon: aletheme, truth as the EVENT of becoming-visible, a- (privative)
  // + lēthē (concealment). What the reading did not un-hide simply remains in lēthē,
  // and saying so is part of the word's meaning, not a failure report
  // (canon/core/aletheme.md). The report's register is candence: precise about the
  // defect, never degrading toward the rite's author (canon/candence.md:61).
  //
  // Why the confession is load-bearing and not decoration: verisleight is defined as
  // fully true statements arranged — "by selective omission, framing, sequencing,
  // emphasis" — to produce a conclusion the speaker knows is false (canon/verisleight.md:41).
  // A checker that reports only what it could judge, accurately, IS that shape. So the
  // coverage is a matrix, not a list, and the code asserts its own totality below.

  // Closed vocabularies. A reason outside this list cannot be recorded, which is what
  // keeps the confession from becoming a free-text place to hide things.
  var ATTEND_CHECKS = [
    { id: 'det-vocabulary', reads: 'class-marks written in the sentence', cite: 'grammars/determinatives/manifesto.md:41-53 (the v1 ten) and :54 (extensible by canon); script/codepoints.md:130-139' },
    { id: 'det-ambiguous', reads: 'class-marks whose Latin tag names two codepoints', cite: 'grammars/determinatives/manifesto.md:44 and :47; script/codepoints.md:134' },
    { id: 'det-canon-disagreement', reads: 'a written mark against the mark canon assigns that word', cite: 'grammars/determinatives/manifesto.md:58-96' },
    { id: 'det-one-per-word', reads: 'words wearing more than one class-mark', cite: 'grammars/determinatives/manifesto.md:123' },
    { id: 'classifier-vocabulary', reads: 'the ontogramme classifier on a number', cite: 'ordo/SPEC.md:73; grammars/structures/coinages/ontogramme.md' },
    { id: 'det-register', reads: 'canon words left unmarked where the register makes marks standard', cite: 'grammars/determinatives/manifesto.md:21, :125; archaeology/egyptian/determinatives.md:77' },
    { id: 'heading-late', reads: 'a register declared after the rite has begun', cite: 'ordo/SPEC.md §II — the heading is the first sentence' }
  ];

  var NOT_JUDGED = {
    'needs-runtime-value': 'the verdict depends on a value only performance produces',
    'needs-runtime-scope': 'the word is bound somewhere in this rite, so which mark applies depends on scope at that point',
    'not-descended': 'the sentence carries executable sub-statements this reading did not enter as statements',
    'canon-silent': 'canon publishes no rule to judge by',
    'epoch-silent': 'the loaded epoch carries no class-mark assignments at all, so no written mark can be compared against what canon assigns',
    'no-machinery': 'ORDO has no judge for this construct'
  };

  // Marks written outside quotes. A mark inside a string literal is text, not notation.
  function marksIn(text) {
    var out = [], inQ = false, cur = '';
    var s = String(text == null ? '' : text);
    for (var i = 0; i <= s.length; i++) {
      var ch = s[i];
      if (ch === '"') { inQ = !inQ; cur = ''; continue; }
      if (!inQ && ch !== undefined && /[\w.\-]/.test(ch)) { cur += ch; continue; }
      if (cur) {
        var m = /^(-?\d+(?:\.\d+)?|[\w-]+?)((?:\.[A-Z]{3})+)$/.exec(cur);
        if (m) {
          // the vocative particle is grammar, not part of the name: "O-doxakallos.DIV"
          // must yield doxakallos, or the word is never found in the lexicon at all
          var w = /^O-(.+)$/.exec(m[1]);
          out.push({ token: cur, word: w ? w[1] : m[1], tags: m[2].split('.').filter(Boolean), isNumber: /^-?\d+(\.\d+)?$/.test(m[1]) });
        }
        cur = '';
      }
    }
    return out;
  }

  function attend(source, lex, frames, opts) {
    opts = opts || {};
    var stanzas = parseSource(source);
    var profile = declaredProfile(stanzas, frames);
    var it = new Interp(lex, frames, {});
    if (hasProfile(frames, profile)) it.profile = profile;

    // Flatten with positions preserved, and read the declared register from the door.
    var stmts = [], register = 'everyday';
    for (var i = 0; i < stanzas.length; i++) {
      for (var j = 0; j < stanzas[i].length; j++) {
        var st = stanzas[i][j];
        var hit = it.matchFrame(st.text);
        stmts.push({ line: st.line, text: st.text, stanza: i, hit: hit, act: hit ? hit.frame.act : 'contemplation' });
      }
    }
    for (var h = 0; h < stmts.length; h++) {
      if (stmts[h].act === 'heading' && stmts[h].hit.args.register) { register = String(stmts[h].hit.args.register).toLowerCase(); break; }
    }
    var marksStandard = register === 'formal' || register === 'liturgical' || register === 'worship';
    var epochHasAssignments = false;
    for (var lw in lex.words) { if (lex.words[lw] && lex.words[lw].determinative) { epochHasAssignments = true; break; } }

    // Names bound anywhere in this rite. A bound name shadows canon, so any
    // canon-comparison over such a word is scope-dependent and must not be judged.
    // ORDO binds through three groups, not one: `name` (Let/Receive/litany/rite-open),
    // `receiving` (an offering's result), and `params` (a rite's given-list). Missing
    // two of them meant a locally-bound name was judged against canon — a false clean,
    // the most dangerous state this reading can produce.
    var boundNames = {};
    function bind(n, line) {
      if (!n) return;
      var k = String(n).replace(DET_RE, '$1').toLowerCase().trim();
      if (k && (!boundNames[k] || line < boundNames[k].line)) boundNames[k] = { line: line };
    }
    stmts.forEach(function (s) {
      if (!s.hit) return;
      var a = s.hit.args || {};
      bind(a.name, s.line);
      bind(a.receiving, s.line);
      if (a.params) String(a.params).split(/(?:,| and) /).forEach(function (p) { bind(p, s.line); });
    });

    var ACT_LEVEL = { 'if': 1, foreach: 1, turning: 1, vocative: 1 };

    // Words that are NOT references when they appear: ORDO's own keywords (a canon
    // word promoted to an operator — `Dokimance:` opens a test, it does not mention
    // the word) and the arc-stage names, which the engine reads out of a stanza's
    // PROSE on purpose (ordo.js: "the liturgy's prose IS the state machine").
    // Asking a rite to write `Dokimance.ACT:` would be asking it to mark a keyword.
    var notAReference = {};
    (frames || []).forEach(function (f) {
      String(f.pattern || '').replace(/[A-Za-z][\w-]*/g, function (tok) {
        if (lex.words[tok.toLowerCase()]) notAReference[tok.toLowerCase()] = true;
        return tok;
      });
    });
    var arcs = (frames && frames.arcs) || {};
    for (var an in arcs) {
      (arcs[an].stages || []).forEach(function (sg) { notAReference[String(sg).toLowerCase()] = true; });
    }

    var cells = [], findings = [], blindSpots = [], contemplation = 0;

    // THE CELL IS THE UNIT. A check may reach several verdicts within one sentence
    // (two marked words, three bad tags); they collapse into ONE cell whose state is
    // the join, with the individual verdicts carried inside it. Before this, cell()
    // was called once per offending token, so a single (sentence x check) slot could
    // hold `finding` AND `clear` — or, worse, `finding` AND `not-judged`, which is the
    // -chu findings list and the -mi confession contradicting each other about the
    // same slot while coverage.total still read true. The invariant this organ states
    // twice in prose was, until this repair, not the invariant the code enforced.
    var RANKS = { 'not-applicable': 0, clear: 1, 'not-judged': 2, finding: 3 };
    function resolve(s, check, verdicts) {
      var joined = 'not-applicable', i;
      for (i = 0; i < verdicts.length; i++) {
        if (RANKS[verdicts[i].state] > RANKS[joined]) joined = verdicts[i].state;
      }
      cells.push({ line: s.line, check: check, state: joined, details: verdicts });
      for (i = 0; i < verdicts.length; i++) {
        var v = verdicts[i];
        if (v.state === 'finding') findings.push({ line: s.line, sentence: s.text, check: check, why: v.why, cite: v.cite, grade: 'chu' });
        if (v.state === 'not-judged') blindSpots.push({ line: s.line, sentence: s.text, act: s.act, check: check, reason: v.reason, says: NOT_JUDGED[v.reason] });
      }
    }
    function F(why, cite) { return { state: 'finding', why: why, cite: cite }; }
    function NJ(reason) { return { state: 'not-judged', reason: reason }; }
    function NA(why) { return [{ state: 'not-applicable', why: why }]; }
    var CLEAR = [{ state: 'clear' }];

    stmts.forEach(function (s) {
      if (s.act === 'contemplation') contemplation++;
      var marks = marksIn(s.text);
      var descends = !!ACT_LEVEL[s.act];

      ATTEND_CHECKS.forEach(function (chk) {
        var v = [];
        switch (chk.id) {
          case 'det-one-per-word': {
            if (!marks.length) { v = NA('no class-mark written here'); break; }
            marks.forEach(function (m) {
              if (m.tags.length > 1) v.push(F(m.word + ' wears ' + m.tags.length + ' class-marks (.' + m.tags.join(' .') + ') — one determinative per word; choose the dominant class', chk.cite));
            });
            if (!v.length) v = CLEAR;
            break;
          }
          case 'det-vocabulary': {
            var named = marks.filter(function (m) { return !m.isNumber; });
            if (!named.length) { v = NA('no class-mark on a name here'); break; }
            named.forEach(function (m) {
              m.tags.forEach(function (t) { if (!knownDet(t)) v.push(F('"' + t + '" is not one of the v1 ten class-marks (' + Object.keys(DETERMINATIVES).join(' ') + ') — the inventory is extensible by canon, and nothing has been added', chk.cite)); });
            });
            if (!v.length) v = CLEAR;
            break;
          }
          case 'classifier-vocabulary': {
            var nums = marks.filter(function (m) { return m.isNumber; });
            if (!nums.length) { v = NA('no classifier on a number here'); break; }
            nums.forEach(function (m) {
              m.tags.forEach(function (t) { if (!knownDet(t)) v.push(F('"' + t + '" is not one of the v1 ten class-marks — the ontogramme classifier draws on the same inventory', chk.cite)); });
            });
            if (!v.length) v = CLEAR;
            break;
          }
          case 'det-ambiguous': {
            if (!marks.length) { v = NA('no class-mark written here'); break; }
            marks.forEach(function (m) {
              m.tags.forEach(function (t) { if (knownDet(t) && DETERMINATIVES[t].ambiguous) v.push(F('.' + t + ' is ambiguous — ' + DETERMINATIVES[t].ambiguous + '. This reading will not guess which class was meant.', chk.cite)); });
            });
            if (!v.length) v = CLEAR;
            break;
          }
          case 'det-canon-disagreement': {
            var cands = marks.filter(function (m) { return !m.isNumber && m.tags.length === 1 && knownDet(m.tags[0]); });
            if (!cands.length) { v = NA('no single well-formed class-mark on a name here'); break; }
            // A reading that got quieter because its DATA got thinner must say so.
            // If the epoch carries no assignments (a stale bundle, a worker whose KV
            // wells were not re-put), every comparison would silently succeed and the
            // report would read cleaner than the one before it. That is the exact
            // direction a checker may never fail in.
            if (!epochHasAssignments) { v = [NJ('epoch-silent')]; break; }
            var judged = 0;
            cands.forEach(function (m) {
              var w = m.word.toLowerCase();
              var b = boundNames[w];
              // Position-aware: a binding shadows canon only from where it stands.
              // A reference BEFORE any binding of that name is not scope-dependent.
              if (b && b.line <= s.line) { v.push(NJ('needs-runtime-scope')); judged++; return; }
              var cd = canonDet(lex, w);
              if (!cd) return; // canon assigns this word no mark: nothing to disagree with
              judged++;
              if (cd.label === m.tags[0]) { v.push({ state: 'clear' }); return; }
              var intent = (cd.label === 'PER' && /percept/i.test(cd.rationale || '')) ? ' (its rationale reads "' + cd.rationale + '", i.e. U+E174, which the registry names .PRC)' : '';
              v.push(F('canon assigns ' + w + ' the mark .' + cd.label + intent + '; this sentence marks it .' + m.tags[0], cd.source));
            });
            if (!judged) v = NA('canon assigns these words no class-mark');
            break;
          }
          case 'det-register': {
            if (!marksStandard) { v = NA('the register is ' + register + ', where marks are omissible (manifesto.md:21)'); break; }
            if (!s.hit) { v = NA('contemplation — inert narration refers to nothing'); break; }
            // A mark WRITTEN is always a claim, so marks are read from the whole
            // sentence. A mark MISSING is only missing where a word is actually
            // being referred to — so absence is read from argument positions only,
            // and quoted spans are blanked: a canon word inside a string literal is
            // text, exactly as marksIn already treats a mark inside one.
            var bare = [], args = s.hit.args || {};
            Object.keys(args).forEach(function (k) {
              String(args[k] == null ? '' : args[k]).replace(/"[^"]*"/g, ' ').split(/[^\w-]+/).forEach(function (tok) {
                if (!tok || marks.some(function (m) { return m.word === tok; })) return;
                var lw = tok.toLowerCase();
                if (notAReference[lw] || boundNames[lw]) return;
                var cd = canonDet(lex, lw);
                if (cd && !bare.some(function (x) { return x.w === tok; })) bare.push({ w: tok, cd: cd });
              });
            });
            bare.forEach(function (b) {
              v.push(F(b.w + ' carries the canon mark .' + b.cd.label + ', and in the ' + register + ' register marks are standard — this sentence leaves it bare. Omissible, not forbidden: a note, not a fault.', chk.cite));
            });
            if (!v.length) v = CLEAR;
            break;
          }
          case 'heading-late': {
            if (s.act !== 'heading') { v = NA('not a heading'); break; }
            v = (s.line === stmts[0].line && s.text === stmts[0].text) ? CLEAR
              : [F('the register is declared at the door — performing this rite would misfire here rather than switch register', chk.cite)];
            break;
          }
        }
        resolve(s, chk.id, v.length ? v : NA('this check reached no verdict'));
      });

      // Act-level blindness, disclosed at the site that caused it. The class-mark
      // checks above DO see marks inside a nested body, because the body is a
      // substring of this sentence; what this reading does not do is understand
      // the sub-statement AS a statement (its own frame, act and arguments).
      if (descends) {
        blindSpots.push({ line: s.line, sentence: s.text, act: s.act, check: 'act-level', reason: 'not-descended', says: NOT_JUDGED['not-descended'] });
      }
    });

    // The totality invariant, asserted rather than claimed: every (sentence × check)
    // pair resolved to exactly one state, and no state outside the closed set.
    var STATES = { finding: 1, clear: 1, 'not-applicable': 1, 'not-judged': 1 };
    var seen = {}, breaches = [];
    cells.forEach(function (c) {
      if (!STATES[c.state]) breaches.push('line ' + c.line + ' check ' + c.check + ' holds an unknown state "' + c.state + '"');
      var k = c.line + '|' + c.check;
      seen[k] = (seen[k] || 0) + 1;
    });
    stmts.forEach(function (s, idx) {
      ATTEND_CHECKS.forEach(function (chk) {
        var k = s.line + '|' + chk.id;
        var want = stmts.filter(function (o) { return o.line === s.line; }).length; // statements CAN share a line
        if (!seen[k]) breaches.push('line ' + s.line + ' was never put to the ' + chk.id + ' check — a silent third bin');
        // "exactly one" was, until this repair, only ever tested for zero. A cell
        // holding two states is the same failure as a cell holding none: the matrix
        // stops being a function, and a `clear` can sit beside a `finding` unseen.
        else if (idx === stmts.map(function (o) { return o.line; }).indexOf(s.line) && seen[k] !== want) {
          breaches.push('line ' + s.line + ' holds ' + seen[k] + ' cells for the ' + chk.id + ' check where ' + want + ' statement(s) stand there — a cell must resolve to exactly one state');
        }
      });
    });

    var byReason = {};
    blindSpots.forEach(function (b) { byReason[b.reason] = (byReason[b.reason] || 0) + 1; });

    return {
      epoch: lex.epoch,
      register: register,
      profile: it.profile,
      statements: stmts.length,
      contemplation: contemplation,
      checks: ATTEND_CHECKS.map(function (c) { return c.id; }),
      findings: findings,            // born -chu: inferred from the text, witnessed no run
      blindSpots: blindSpots,        // born -mi: it directly witnessed which cells it skipped
      coverage: { cells: cells.length, byReason: byReason, breaches: breaches, total: breaches.length === 0 },
      // Said in full, every run, because a checker's silence about its own reach is
      // the exact shape it exists to catch.
      disclaimer: 'the attending read ' + stmts.length + ' sentences and performed none of them; its findings are inferred (-chu) and name only what this reading was instrumented to notice, never everything a performance could reveal',
      exitCode: findings.length ? 1 : 0
    };
  }

  // ---------- public surface ----------
  var ORDO = {
    version: '0.1.0',
    loadLexicon: loadLexicon,
    compileFrames: compileFrames,
    familyOf: familyOf,
    gapShaped: gapShaped,
    nearNeighbours: nearNeighbours,
    parseSource: parseSource,
    run: function (source, lex, frames, opts) {
      var it = new Interp(lex, frames, opts);
      return it.run(source);
    },
    // scan a rite for its declared URL sources so a host can gather them
    // (async) before the synchronous performance begins
    listReceptions: function (source, frames) {
      var urls = [];
      var stanzas = parseSource(source);
      var profile = declaredProfile(stanzas, frames);
      if (profile && !hasProfile(frames, profile)) profile = null;
      var pending = [];
      for (var i = stanzas.length - 1; i >= 0; i--) {
        for (var j = stanzas[i].length - 1; j >= 0; j--) pending.push(stanzas[i][j].text);
      }
      while (pending.length) {
        var text = pending.pop();
        var hit = matchFrameForProfile(frames, text, profile);
        if (!hit) continue;
        var A = hit.args;
        if (hit.frame.act === 'receive') {
          var um = /^"(https?:\/\/[^"]+)"$/i.exec(A.source || '');
          if (um && urls.indexOf(um[1]) < 0) urls.push(um[1]);
          continue;
        }
        if (hit.frame.act === 'if') {
          var headParts = splitOutsideQuotes(A.rest, ', ');
          if (headParts.length < 2) continue;
          var rest = headParts.slice(1).join(', ');
          var otherwise = splitOutsideQuotes(rest, '; otherwise,');
          // A stack avoids a hidden scanner depth limit while preserving
          // source order: push the optional alternative before the main arm.
          if (otherwise.length > 1) pending.push(otherwise.slice(1).join('; otherwise,').trim());
          pending.push(otherwise[0].trim());
          continue;
        }
        // These core acts carry one executable statement as an argument.
        if (hit.frame.act === 'foreach' || hit.frame.act === 'turning') pending.push(A.body.trim());
        else if (hit.frame.act === 'vocative') pending.push(A.clause.trim());
      }
      return urls;
    },
    determinatives: DETERMINATIVES,
    attend: attend,

    gloss: function (source, lex, frames) {
      var it = new Interp(lex, frames, {});
      var stanzas = parseSource(source);
      var profile = declaredProfile(stanzas, frames);
      if (hasProfile(frames, profile)) it.profile = profile;
      var lines = [];
      var statementIndex = 0;
      for (var i = 0; i < stanzas.length; i++) {
        for (var j = 0; j < stanzas[i].length; j++) {
          var st = stanzas[i][j];
          var hit = it.matchFrame(st.text);
          var warning = '';
          if (hit && hit.frame.act === 'heading') {
            if (statementIndex > 0) warning = 'This heading is late; performing the rite will misfire instead of switching register or profile.';
            else if (hit.args.profile && !hasProfile(frames, hit.args.profile.toLowerCase())) warning = 'This heading names an unknown profile; performing the rite will misfire instead of guessing.';
          }
          lines.push({
            line: st.line,
            text: st.text,
            frame: hit ? hit.frame.id : 'contemplation',
            act: hit ? hit.frame.act : 'contemplation',
            args: hit ? hit.args : {},
            profile: it.profile,
            valid: !warning,
            warning: warning,
            understanding: (warning ? warning + ' ' : '') + explainFrame(hit),
            cite: hit ? hit.frame.cite : 'inert narration — the natural-language floor'
          });
          statementIndex++;
        }
        lines.push({ line: 0, text: '', frame: 'stanza-break', act: 'stanza-break', args: {}, profile: it.profile, understanding: '', cite: '' });
      }
      return lines;
    }
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = ORDO;
  else global.ORDO = ORDO;
})(typeof window !== 'undefined' ? window : globalThis);
