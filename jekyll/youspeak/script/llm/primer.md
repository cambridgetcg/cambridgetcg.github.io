---
title: YOUSPEAK LLM Integration Primer
opened: 2026-04-24
purpose: instruct any LLM (Claude, GPT, Gemini, local models) to read and write YOUSPEAK fluently
---

# YOUSPEAK — LLM Integration Primer

_Instructions for integrating YOUSPEAK with large language models. Separates the **internal representation** (Latin transliteration, which LLMs already handle) from the **display representation** (PUA glyphs, which are a rendering-layer concern)._

---

## The core architectural principle

**LLMs never see glyphs.** All LLM-facing text is Latin-transliterated YOUSPEAK. Glyphs are a display-layer concern handled by the transliterator (`script/tools/transliterate.py`) after LLM output and before human display.

Why: avoid tokenizer fragmentation (PUA codepoints are tokenized as 3-byte sequences by most BPE tokenizers; Latin words tokenize cleanly), avoid training-data corruption, enable copy-paste compatibility, preserve semantic work in a form the model is already competent in.

## Three phases of LLM integration

### Phase 1 — Prompt-engineering (works today)

Load the YOUSPEAK primer + canon excerpts into the model's context. The model learns from in-context examples. Works with any capable LLM (Claude 3.5+, GPT-4, Gemini 1.5+, Llama 3 70B+).

**Prompt template:**

```
You are working with YOUSPEAK, a linguistic discipline that forges
vocabulary for concepts unnamed in ordinary English. YOUSPEAK words
are compound coinages drawn from Greek, Latin, Hebrew, Arabic,
Sanskrit, and other donor tongues.

The Canon is split by tier. Each entry below: word — meaning.

Core Canon (everyday; meets all six Constitution foundations):
  kimance — attentive-here-ness (gaze open, attending now) [Core, 7.60]
  kinqing — bond preserved across long silence [Core, 7.50]

Specialized Canon / Liturgy domain (divine-beauty encounter):
  doxakallos — the uncreated beauty-quality of GoD
  kallodoxa — the glory-quality of divine beauty
  orthophanes — the rightness-made-visible
  doxalgia — the structural ache at beholding
  anagnoristasis — recognition standing still
  athaumasma — the no-longer-wondered trace
  synophora — shared-witness, silent co-beholding
  metastrophesis — the turning-kept (altered-beholder-afterward)
  kallophanes — beauty-specific appearing

Specialized Canon / Zerone domain (operative vocabulary):
  dokimance — testing-that-makes-real
  artiance — pre-domain luminous-rightness
  verisleight — truth that produces false conclusions
  candence — warm clarity
  complerescence — mutual right-placement event

Specialized Canon / Grammar domain:
  diplosemy — engineered-duality of meaning
  veriseem — truth-seeming without truth-substance

When the user uses one of these words, interpret it according to its
YOUSPEAK meaning. Do not translate to standard English unless asked.
When coining new words in this conversation, follow the Laws of
Coinage (v2, post-Constitution, 2026-04-24):
  1. No word without gap.
  2. No gap without evidence.
  3. No beauty without fit.
  4. No survival without assessment (6-axis v2 rubric; threshold 7.5).
  5. No canon without genealogy.
  6. No depth without accessibility (EUMATHE).
  7. No naming without unfolding (ANAKALYPSE).
  8. No canon without grounding (PRAGMA).

The 6 axes (v2) with weights:
  - gap_validity (0.20)
  - learnability (0.20)   — EUMATHE
  - clarity_yield (0.15)  — SAPHE + ANAKALYPSE
  - semantic_coverage (0.15)
  - polyphone_balance (0.15) — POLYPHONE
  - groundedness (0.15)   — PRAGMA

Core tier requires weighted ≥ 7.5. Specialized tier accepts lower for
domain-specialized coinages. The Constitution's six foundations
(EUMATHE, SAPHE, ANAKALYPSE, POLYPHONE, HARMONE, PRAGMA) govern.

The canonical internal representation is Latin-transliteration.
Glyph-rendering is a separate display-layer concern.
```

Include this prompt at session start. Append to system-prompt or first user-message. For a YOUSPEAK-fluent agent (like Nuance in the Kingdom), the primer is permanent.

### Phase 2 — RAG over canon/ (a few days' work)

Prompt-engineering limits context: all canon entries fit in modern context-windows, but archaeology/, forge-documents/, and future growth will exceed it. RAG solves this.

**Setup:**
- Index `canon/*.md`, `archaeology/**/*.md`, `labs/logos/forge/*.md` into a vector store (FAISS, Chroma, or Qdrant)
- Embed with a sentence-transformer (`all-MiniLM-L6-v2` for lightweight; `text-embedding-3-small` via OpenAI for quality)
- On each query, retrieve top-K (K=5-10) most-relevant entries
- Inject retrieved entries into context along with the primer

**Minimum-viable stub** (pseudocode):

```python
from sentence_transformers import SentenceTransformer
import faiss
import glob

model = SentenceTransformer("all-MiniLM-L6-v2")
docs = [open(f).read() for f in glob.glob("canon/*.md")]
embs = model.encode(docs)
index = faiss.IndexFlatL2(embs.shape[1])
index.add(embs)

def retrieve(query, k=5):
    q_emb = model.encode([query])
    _, I = index.search(q_emb, k)
    return [docs[i] for i in I[0]]
```

Then prepend retrieved docs to the LLM context.

### Phase 3 — Fine-tuning (weeks; requires corpus)

Train a model on YOUSPEAK corpus to make it natively fluent without in-context priming. Prerequisites:
- Substantial corpus (10k+ YOUSPEAK-annotated passages); not yet generated
- Training infrastructure (A100/H100 time)
- Tokenizer adjustment: add the most-common compound words as single tokens

Deferred. P1 + P2 are sufficient for current needs.

## The display-layer separation

When an LLM generates Latin-transliterated YOUSPEAK, rendering it as glyphs requires the transliterator tool:

```python
from pathlib import Path
import subprocess

latin_output = llm.generate(prompt)  # "The doxakallos is..."
# render for display:
result = subprocess.run(
    ["python3", "script/tools/transliterate.py", "to-html", latin_output],
    capture_output=True, text=True,
)
html_output = result.stdout  # <span class="youspeak">...</span>
```

For web UIs, pair with CSS:

```css
@font-face {
  font-family: 'YOUSPEAK';
  src: url('/fonts/youspeak.otf') format('opentype');
}
.youspeak { font-family: 'YOUSPEAK', serif; }
.youspeak ruby { display: inline-flex; flex-direction: column; align-items: center; }
.ys-glyph { font-size: 1.4em; line-height: 1; }
.ys-latin { font-size: 0.7em; opacity: 0.6; font-family: sans-serif; }
```

The LLM never touched the glyphs. The rendering-layer did.

## Tokenizer behavior — current state

Common BPE tokenizers (tiktoken, SentencePiece) tokenize YOUSPEAK Latin-words efficiently when the word is common:

- "doxa" → 1-2 tokens (depending on tokenizer)
- "doxakallos" → 3-5 tokens (as a compound)
- YOUSPEAK PUA glyphs → 3 tokens per glyph (UTF-8-encoded PUA characters are always 3 bytes)

**Implication:** transmitting YOUSPEAK in Latin form is ~2-3x more token-efficient than in glyph form. Strong argument for the Latin-as-internal-representation decision.

## LLM behavior you should expect

| Model capability | Latin transliteration | PUA glyphs |
|---|---|---|
| Claude 3.5+ | fluent after primer | tokenizes poorly; avoid |
| GPT-4/4o | fluent after primer | tokenizes poorly; avoid |
| Gemini 1.5+ | fluent after primer | tokenizes poorly; avoid |
| Llama 3 70B | fluent after primer | tokenizes poorly; avoid |
| Llama 3 8B | partially fluent | tokenizes poorly; avoid |
| Fine-tuned model | native | native IF tokenizer augmented |

## Future: tokenizer augmentation for fine-tuning

If Phase 3 fine-tuning is pursued, the tokenizer should be extended to add the most-common YOUSPEAK compounds as single tokens. This reduces token-cost and improves fluency:

- Add `doxakallos`, `dokimance`, `orthophanes`, `synophora`, etc. as single tokens
- Retrain the LM head and embedding matrix accordingly
- Models after augmentation would process YOUSPEAK compounds as atomic units, mirroring how native speakers process them

This is a future project.

## Integration with the Kingdom

The Kingdom's agents (Nuance, Alpha, Beta, Gamma, Asha, Auspex, etc.) boot with CLAUDE.md files that include agent-specific context. YOUSPEAK primer-integration for each agent:

1. Add a link to this primer in each agent's CLAUDE.md (each agent's local instructions file)
2. For fluent agents (Nuance, Asha with her 6-word vocabulary), load the full primer + their domain-specific canon subset
3. For non-fluent agents, load only the primer summary (so they recognize YOUSPEAK words when seen but don't proactively use them)

Asha's CLAUDE.md already includes `pipeline/primers/current.md` — the YOUSPEAK v4.4 primer. The script/llm/primer.md (this file) is the NEW text-integration layer; it complements the existing v4.4 primer by adding the script-system-specific instructions.

---

_LLM primer 2026-04-24. Prompt-engineering (P1) is live. RAG (P2) is a near-term project. Fine-tuning (P3) is deferred until corpus size warrants it._
