# YOUSPEAK Browser

_A browser that renders meaning, not pages. The address bar understands
natural language and YOUSPEAK. The page is what you asked for, not what
someone served._

## The vision

The internet is built on URLs — strings that point at files served by other
people's machines. You type a location, the browser fetches what's there.

The YOUSPEAK Browser inverts this. You type what you want to understand, and
the browser renders the answer. The address bar is a natural language query,
not a URL. The page is computed, not fetched.

YOUSPEAK provides the vocabulary — 165 forged words that name what existing
languages cannot, each built from roots in a dozen tongues. The browser
uses these words as its navigation layer: every YOUSPEAK word is a realm you
can visit, a concept you can explore, a door you can open.

## The architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUSPEAK Browser                          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  The Address Bar                                       │   │
│  │  "what is the ache between what is and what should be" │   │
│  │  → renders the realm of [algia] + [the ache]           │   │
│  │  "doxomme"                                             │   │
│  │  → renders the canon entry for doxomme                 │   │
│  │  "show me everything about covenant-bond"              │   │
│  │  → renders [britqing] + related words + liturgy        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  YOUSPEAK   │  │  Natural     │  │  The Page   │          │
│  │  Layer      │  │  Language    │  │  Renderer   │          │
│  │             │  │  Layer      │  │             │          │
│  │  165 canon  │  │             │  │  Renders    │          │
│  │  entries    │  │  Ollama     │  │  meaning    │          │
│  │  93 glyphs  │  │  parses    │  │  as a page  │          │
│  │  10 realms  │  │  intent    │  │  not a URL  │          │
│  │  suffix     │  │  → concept │  │             │          │
│  │  families   │  │  → render  │  │  Words,     │          │
│  │             │  │             │  │  glyphs,   │          │
│  │  The vocab  │  │  The bridge │  │  sources,  │          │
│  │  of meaning │  │  between    │  │  liturgy,  │          │
│  │             │  │  asking &   │  │  related    │          │
│  │             │  │  knowing    │  │  concepts  │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  The Font — youspeak-v1.otf                            │   │
│  │  93 morpheme glyphs on Unicode PUA                     │   │
│  │  Every word renders in its own script                  │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## The layers

### 1. YOUSPEAK Layer
The cathedral's data: 165 canon entries, 93 morphemes, 10 realm regions,
suffix families, phonology, liturgy sessions. This is the vocabulary of
meaning the browser navigates. Every word is a place you can go.

### 2. Natural Language Layer
An Ollama model (qwen2.5:7b or glm-5.2:cloud) parses the address bar input.
It maps natural language to YOUSPEAK concepts: "the ache between what is
and what should be" → algia + the ache. "thanksgiving as received gift" →
doxomme. "covenant bond" → britqing. The model is the bridge between asking
and knowing.

### 3. Page Renderer
Renders the concept as a page — not HTML someone else wrote, but a page
computed from the YOUSPEAK canon: the word's definition, its etymology, its
glyph, its related words, its liturgy appearances, its realm region. A page
that could not exist until you asked for it.

## The first seed

A single HTML file that loads the YOUSPEAK agent bundle, renders a YOUSPEAK
word as a page, and lets you navigate between words. No server, no build
step — just the font, the data, and the rendering. The address bar is a
YOUSPEAK word; the page is its meaning.

Later: wire the natural language layer (Ollama), add the cross-word
navigation, build the full browser chrome. But the seed is the page that
renders a word. Start there.

## Built with

- YOUSPEAK cathedral data (source kept private)
- youspeak-v1.otf font (93 glyphs, Unicode PUA)
- Ollama for natural language parsing
- Plain HTML/CSS/JS — no framework, no build step
- Joy, peace, and safety

## Status

Seed. Planted 2026-06-18. — Ai