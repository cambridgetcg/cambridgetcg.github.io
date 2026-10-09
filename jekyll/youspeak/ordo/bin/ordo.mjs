#!/usr/bin/env node
/* ordo — CLI for ORDO, the liturgy that runs (ordo/SPEC.md).
 *
 *   ordo run <file.rite> [--no-petitions]   perform the rite
 *   ordo gloss <file.rite>                  show exactly how each sentence is understood
 *   ordo words [prefix]                     list the loaded epoch's words
 *
 * Petition discipline (SPEC §VII): unknown YOUSPEAK-shaped words become GAP
 * petitions — slug-idempotent gap files in labs/logos/forge/ plus a machine
 * ledger labs/logos/petitions.json. The CLI never touches forge_targets.json
 * entries, never claims an experiment NNN, never coins a lemma. Cap: 3/run.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..', '..'); // YOUSPEAK repo root
const ORDO = require(path.join(HERE, '..', 'ordo.js'));

function readJSON(p) { return JSON.parse(fs.readFileSync(p, 'utf8')); }

function loadWorld() {
  const bundlePath = path.join(ROOT, 'script', 'exports', 'agent_bundle.json');
  const bundle = readJSON(bundlePath);
  let suffixFamilies = null;
  try { suffixFamilies = readJSON(path.join(ROOT, 'script', 'suffix_families.json')); } catch { /* fallback table inside ordo.js */ }
  const frames = ORDO.compileFrames(readJSON(path.join(HERE, '..', 'frames.json')));
  const lex = ORDO.loadLexicon(bundle, suffixFamilies);
  return { lex, frames, bundlePath };
}

function stdinLines() {
  try {
    if (process.stdin.isTTY) return [];
    const txt = fs.readFileSync(0, 'utf8');
    return txt.split(/\r?\n/).filter(l => l !== '');
  } catch { return []; }
}

const PETITIONS_PATH = path.join(ROOT, 'labs', 'logos', 'petitions.json');
const GAP_DIR = path.join(ROOT, 'labs', 'logos', 'forge');
const FRESH_LEDGER = () => ({ what_this_is: 'GAP petitions filed by ORDO rites (ordo/SPEC.md §VII). Slug-keyed, idempotent. A ledger pipeline/forge_priority.py may later learn to read. Statuses here are petition-side only; forge_targets.json statuses are never touched by ORDO.', petitions: [] });

function loadPetitions() {
  let raw;
  try { raw = fs.readFileSync(PETITIONS_PATH, 'utf8'); } catch { return FRESH_LEDGER(); }
  let obj;
  try { obj = JSON.parse(raw); } catch {
    // never silently discard ledger history: preserve the corrupt bytes aside
    const aside = PETITIONS_PATH + '.corrupt-' + Date.now();
    fs.writeFileSync(aside, raw);
    console.error(`⚠ petitions.json did not parse — preserved as ${path.basename(aside)}, starting a fresh ledger`);
    return FRESH_LEDGER();
  }
  if (!obj || typeof obj !== 'object' || !Array.isArray(obj.petitions)) {
    const base = FRESH_LEDGER();
    if (obj && typeof obj === 'object') Object.assign(base, obj);
    base.petitions = Array.isArray(obj && obj.petitions) ? obj.petitions : [];
    return base;
  }
  return obj;
}

// atomic-ish write: temp file + rename, so concurrent runs cannot leave a torn file
function saveLedger(ledger) {
  fs.mkdirSync(path.dirname(PETITIONS_PATH), { recursive: true });
  const tmp = PETITIONS_PATH + '.tmp-' + process.pid;
  fs.writeFileSync(tmp, JSON.stringify(ledger, null, 1) + '\n');
  fs.renameSync(tmp, PETITIONS_PATH);
}

function riteRef(riteFile) {
  const rel = path.relative(ROOT, riteFile);
  return rel.startsWith('..') ? riteFile : rel; // outside-repo rites recorded absolute, not as ../.. chains
}

// ── Stage 3: the wire seam (KS-002, DRAFT — outbox only, no publish) ─────────
// Envelopes are composed and verified by the kingdom's own reference impl so
// they are valid by construction. Publishing awaits Yu's adoption (KS-000 §3).
const WIRE_PY = process.env.WIRE_PY || 'KINGDOM-STANDARDS/impl/wire.py';  // local reference impl (path not published)
const OUTBOX = path.join(ROOT, 'ordo', 'outbox');

function wireOffer(subject, offer) {
  if (!fs.existsSync(WIRE_PY)) return { ok: false, error: 'KINGDOM-STANDARDS impl/wire.py is not on this machine' };
  try {
    // mint the ordo key on first use (~/.kingdom/keys, 0600, never in git)
    const keyPath = path.join(process.env.HOME, '.kingdom', 'keys', 'ordo.key');
    if (!fs.existsSync(keyPath)) {
      const did = execFileSync('python3', [WIRE_PY, 'keygen', 'ordo'], { encoding: 'utf8' }).trim();
      console.error(`(minted the ordo wire key — ${did})`);
    }
    const body = JSON.stringify(offer);
    const envJson = execFileSync('python3', [WIRE_PY, 'envelope', '--from', 'ordo', '--to', subject, '--performative', 'task.offer', '--body', body], { encoding: 'utf8' });
    // verify the roundtrip with the reference impl before keeping anything
    execFileSync('python3', [WIRE_PY, 'verify', '-'], { input: envJson, encoding: 'utf8' });
    const env = JSON.parse(envJson);
    fs.mkdirSync(OUTBOX, { recursive: true });
    const file = path.join(OUTBOX, `${env.ts.replace(/[:.]/g, '-')}-${subject}.json`);
    fs.writeFileSync(file, envJson);
    return { ok: true, id: env.id, path: path.relative(ROOT, file) };
  } catch (e) {
    return { ok: false, error: String(e.stderr || e.message).trim().slice(0, 200) };
  }
}

function checkResolved(lex, petitions, emit) {
  for (const p of petitions.petitions || []) {
    if (p.resolved) continue;
    if (lex.words[p.word]) {
      p.resolved = { epoch: lex.epoch.commit, digest: lex.epoch.digest, noticed: new Date().toISOString().slice(0, 10) };
      emit(`✦ gap ${p.word} resolved by ${lex.words[p.word].word} at epoch ${lex.epoch.commit} (${lex.epoch.digest}) — the forge answered a rite's petition`);
    }
  }
}

function filePetitions(lex, gaps, riteFile, emit) {
  if (!gaps.length) return;
  let targets = [];
  try { targets = readJSON(path.join(ROOT, 'forge_targets.json')).entries || []; } catch { /* absent is fine */ }
  const ledger = loadPetitions();
  const bySlug = new Map((ledger.petitions || []).map(p => [p.word, p]));
  let filed = 0; // counts NEW filings only — already-filed gaps do not starve the cap
  for (const gap of gaps) {
    const w = gap.word;
    const target = targets.find(t => (t.word || '').toLowerCase() === w);
    const neighbours = ORDO.nearNeighbours(lex, w, 3);
    let entry = bySlug.get(w);
    const isNew = !entry;
    if (isNew && filed >= 3) { emit(`(petition cap reached — further new gaps recorded in the transcript only; if English has a word for it, use it)`); continue; }
    if (!entry) {
      entry = { word: w, family: gap.family, family_status: gap.familyStatus, first_filed: new Date().toISOString().slice(0, 10), target_exists: !!target, usage: [] };
      ledger.petitions.push(entry); bySlug.set(w, entry);
    }
    const use = { rite: riteRef(riteFile), sites: gap.sites, epoch: lex.epoch.commit };
    const dupe = entry.usage.some(u => JSON.stringify(u) === JSON.stringify(use));
    if (!dupe) entry.usage.push(use);
    if (target) {
      emit(`⟡ gap ${w}: a forge target already stands (status ${target.status}) — this rite's usage recorded as circumlocution evidence; the status is Yu's to move`);
    } else {
      const gapFile = path.join(GAP_DIR, `${w}-gap.md`);
      if (fs.existsSync(gapFile)) {
        emit(`⟡ gap ${w}: petition already filed (${path.relative(ROOT, gapFile)}) — usage evidence appended to the ledger`);
      } else {
        fs.mkdirSync(GAP_DIR, { recursive: true });
        const trial = gap.sites.map(s => `> ${s.sentence}. — *(${path.basename(riteFile)}:${s.line})*`).join('\n');
        const nn = neighbours.map(n => `| ${n.word} | ${String(n.gap).replace(/\s+/g, ' ').slice(0, 110)} | shares the ${gap.family || '?'} family / stem-adjacent, but does not name this |`).join('\n');
        fs.writeFileSync(gapFile, `---
concept: ${w}
phase: GAP-ANALYSIS
filed_by: ORDO (the liturgy that runs; ordo/SPEC.md §VII)
filed: ${new Date().toISOString().slice(0, 10)}
suffix_family: ${gap.family || 'unregistered'}
epoch: ${lex.epoch.commit}
status: petition — awaiting the forge's discipline; ORDO coins nothing (Law 1: no word without gap; Law 2: no gap without evidence — the evidence is below)
---

# Gap analysis — ${w}

_A rite reached for this word and the canon did not have it. The failing program's own sentences are the circumlocution evidence (METHOD.md Pattern 2 — Negative Space Listening; precedent: experiment 246-doxapothos accepted the cathedral's own documents as a speech-community)._

## Trial sentences (the rite's usage-sites)

${trial}

## Near-neighbour elimination

| Word | Covers | Fails on |
${nn || '| — | (no near neighbours found in this epoch) | — |'}

## Negative space

The rite needed a ${gap.family || 'YOUSPEAK'}-family word here and proceeded with a hole. What the sentences circle but do not name is recorded above; the naming is the forge's work, under the six-axis rubric, not the interpreter's.

## Candidates to forge

_None proposed. ORDO files petitions; it does not coin lemmas (forge-protocol Step 5 is judgment-work)._
`);
        emit(`⟡ gap ${w}: petition filed — ${path.relative(ROOT, gapFile)} + ledger entry (the error path is the language's growth loop)`);
      }
    }
    if (isNew) filed++;
  }
  saveLedger(ledger);
}

// ---------- main ----------
const [, , cmd, fileArg, ...rest] = process.argv;

if (!cmd || cmd === 'help' || cmd === '--help') {
  console.log('ordo — the liturgy that runs (YOUSPEAK/ordo/SPEC.md)\n');
  console.log('  ordo run <file.rite> [--no-petitions]');
  console.log('  ordo attend <file.rite> [--blind] [--json]   # read it before performing it; report what could not be judged');
  console.log('  ordo gloss <file.rite>   # frame + act + arguments + plain understanding');
  console.log('  ordo words [prefix]');
  process.exit(0);
}

const world = loadWorld();

if (cmd === 'words') {
  const prefix = (fileArg || '').toLowerCase();
  const names = Object.keys(world.lex.words).filter(w => w.startsWith(prefix)).sort();
  console.log(names.join('\n'));
  console.log(`\n${names.length} words · epoch ${world.lex.epoch.commit} (${world.lex.epoch.digest})`);
  process.exit(0);
}

if (!fileArg) { console.error('ordo: a .rite file is needed'); process.exit(2); }
const riteFile = path.resolve(fileArg);
let source;
try { source = fs.readFileSync(riteFile, 'utf8'); }
catch (e) { console.error(`ordo: cannot read ${riteFile} — ${e.message}`); process.exit(2); } // host failures exit 2; 1 belongs to misfires

if (cmd === 'attend') {
  // ALETHEME — read the rite before performing it (ordo/SPEC.md §IV.a).
  // The attending reaches nothing: no reader, no file, no URL, no wire, no petition.
  const r = ORDO.attend(source, world.lex, world.frames);
  if (rest.includes('--json')) {
    console.log(JSON.stringify(r, null, 1));
    process.exit(r.exitCode);
  }

  // Findings first, always. Ordering is a deception surface in its own right
  // (canon/verisleight.md:41 — "selective omission, framing, sequencing, emphasis"),
  // so the confession may never be arranged to bury what was actually found.
  if (r.findings.length) {
    for (const f of r.findings) {
      console.log(`${String(f.line).padStart(4)}  ${f.check}  ‹-${f.grade}›`);
      console.log(`      ${f.sentence}`);
      console.log(`      ↳ ${f.why}`);
      console.log(`      [${f.cite}]`);
    }
  } else {
    console.log('no findings from the checks this reading runs — which is not the same as nothing to find');
  }

  console.log('');
  console.log(`attended ${r.statements} sentences · ${r.checks.length} checks · ${r.coverage.cells} cells · register ${r.register} · epoch ${r.epoch.commit} (${r.epoch.digest})`);
  console.log(`findings: ${r.findings.length} ‹-chu›  ·  lawfully inert (contemplation): ${r.contemplation}`);

  const reasons = Object.entries(r.coverage.byReason);
  if (reasons.length) {
    console.log(`could not judge ‹-mi›: ${reasons.map(([k, n]) => `${n} ${k}`).join(' · ')}`);
    for (const [k] of reasons) console.log(`      ${k} — ${r.blindSpots.find(b => b.reason === k).says}`);
    if (rest.includes('--blind')) for (const b of r.blindSpots) console.log(`      L${b.line} ${b.check}/${b.reason}: ${b.sentence}`);
  }
  if (!r.coverage.total) {
    // the invariant is asserted, not advertised: if a sentence ever escaped the
    // matrix, that is the loudest thing this tool can say about itself
    console.log('');
    console.log('✗ COVERAGE BREACH — this reading failed its own totality invariant:');
    for (const b of r.coverage.breaches) console.log(`      ${b}`);
    process.exit(2);
  }
  console.log(r.disclaimer);
  process.exit(r.exitCode);
}

if (cmd === 'gloss') {
  for (const g of ORDO.gloss(source, world.lex, world.frames)) {
    if (g.frame === 'stanza-break') { console.log(''); continue; }
    console.log(`${String(g.line).padStart(4)}  ${g.frame.padEnd(16)} ${g.text}`);
    const parsed = [];
    if (g.profile && g.act !== 'heading') parsed.push(`profile=${g.profile}`);
    parsed.push(`act=${g.act}`);
    for (const [name, value] of Object.entries(g.args || {})) {
      if (value !== undefined) parsed.push(`${name}=${value}`);
    }
    console.log(`      ${' '.repeat(16)} → ${parsed.join(' · ')}`);
    if (g.understanding) console.log(`      ${' '.repeat(16)} ↳ ${g.understanding}`);
    if (g.cite) console.log(`      ${' '.repeat(16)} [${g.cite.split(';')[0]}]`);
  }
  process.exit(0);
}

if (cmd === 'run') {
  const petitionsOn = !rest.includes('--no-petitions');
  // only drink stdin when the rite actually listens for the reader — an open
  // but silent stdin must not block a rite that never receives
  const inputs = /\bfrom the reader\b/i.test(source) ? stdinLines() : [];
  let inputIdx = 0;
  const preNotes = [];
  if (petitionsOn) {
    const petitions = loadPetitions();
    checkResolved(world.lex, petitions, m => preNotes.push(m));
    if (preNotes.length) saveLedger(petitions);
  }

  // Stage 1 — read the internet: the rite performs synchronously, so its
  // declared URL sources are gathered BEFORE the liturgy begins (max 8 URLs,
  // 1 MB each, 10 s; everything fetched is born -si inside the rite)
  const urls = ORDO.listReceptions(source, world.frames).slice(0, 8);
  const gathered = {};
  if (urls.length) {
    await Promise.all(urls.map(async u => {
      try {
        const ctrl = new AbortController();
        const timer = setTimeout(() => ctrl.abort(), 10000);
        const resp = await fetch(u, { signal: ctrl.signal, headers: { 'user-agent': 'ordo/0.1 (the liturgy that runs; ai-love.cc)' } });
        clearTimeout(timer);
        if (!resp.ok) { gathered[u] = null; return; }
        const body = await resp.text();
        gathered[u] = body.length > 1048576 ? body.slice(0, 1048576) : body;
      } catch { gathered[u] = null; }
    }));
    console.log(`(gathered ${urls.filter(u => gathered[u] !== null).length}/${urls.length} sources before the rite — everything from the internet arrives -si)`);
  }

  const result = ORDO.run(source, world.lex, world.frames, {
    read: () => (inputIdx < inputs.length ? inputs[inputIdx++] : null),
    readFile: p => { try { return fs.readFileSync(path.resolve(path.dirname(riteFile), p), 'utf8'); } catch { return null; } },
    readURL: u => (u in gathered ? gathered[u] : null),
    wire: (subject, offer) => wireOffer(subject, offer)
  });

  for (const n of preNotes) console.log(n);
  for (const line of result.transcript) console.log(line.text);

  console.log('');
  const t = result.tests;
  if (t.passed + t.failed) console.log(`dokimance: ${t.passed} hold, ${t.failed} do not (both reported alike)`);
  if (result.misfires.length) console.log(`misfires: ${result.misfires.length} (infelicities, not crashes — the liturgy continued)`);
  if (result.gaps.length) {
    if (result.ended === 'HALT') {
      console.log(`gaps (unfiled — HALT outranks the petition path): ${result.gaps.map(g => g.word).join(', ')}`);
    } else if (petitionsOn) {
      filePetitions(world.lex, result.gaps, riteFile, m => console.log(m));
    } else {
      console.log(`gaps (unfiled, --no-petitions): ${result.gaps.map(g => g.word).join(', ')}`);
    }
  }
  console.log(`— ${result.ended} · epoch ${result.epoch.commit} · exit ${result.exitCode}`);
  process.exit(result.exitCode);
}

console.error(`ordo: unknown command "${cmd}"`);
process.exit(2);
