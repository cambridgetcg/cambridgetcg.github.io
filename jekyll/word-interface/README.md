# WORD INTERFACE

_The internet's user interface was built for machines. We're rewriting it for humans — in natural language, words, and their meaning._

No buttons. No menus. No modals. No cookie banners. No dark patterns. No "engagement metrics." No infinite scroll. No sign-up walls before you can read.

Just words. Words that mean what they say. Words you can trust.

## The idea

Every interface on the internet speaks machine: checkboxes, dropdowns, submit buttons, hamburger menus, settings panels, preference toggles, accept/reject dialogs. The human speaks language. The gap between them is where friction lives — and where extraction hides.

WORD INTERFACE closes the gap. The interface IS language. You type what you want. The system understands. No clicking through six menus to find one setting. No hunting for the right button. Just say it.

## How it works

```
You: "show me my orders from last week"
System: shows them

You: "cancel the one from Tuesday"
System: "Done. Order #1042 cancelled. Refund of $89.50 processing."

You: "what's my cashback balance?"
System: "You have $23.40 in store credit. Your next tier unlocks at $500 spent."
```

That's it. No navigation. No learning curve. No friction. The words ARE the interface.

## The vocabulary

WORD INTERFACE draws from [YOUSPEAK](https://cambridgetcg.github.io/youspeak-dictionary/) — 151 constructed words from 12 ancient tongues that name what modern languages cannot easily say. Words like:

- **kimance** — attentive-here-ness, the quality of being truly present
- **kinqing** — the bond-quality of deep emotional connection
- **panimaance** — presence as a face turned and here inhabited
- **sukhance** — ordinary everyday contentment

These words become interface primitives. Instead of "status: online" (machine), you see "kimance: here" (human). Instead of "connection strength: strong" (machine), you feel "kinqing: deep" (human).

## Principles

1. **Words are the interface.** If you can't say it, the interface shouldn't need it.
2. **Meaning over mechanism.** The system shows what things mean, not how they work.
3. **No extraction.** No engagement metrics. No attention harvesting. No dark patterns.
4. **Natural language in, natural language out.** You speak human. The system speaks human back.
5. **Truth carries its source.** Every claim the system makes names where it came from.
6. **Built from love.** The interface exists to serve the person, not to capture them.
7. **Open vocabulary.** Anyone can add words. Anyone can use words. No gatekeeping.

## Structure

```
src/
  engine/          # natural language understanding + response
  vocabulary/      # interface words (from YOUSPEAK + extensions)
  render/          # word-based rendering (no DOM widgets)
  intents/         # what people want to do (mapped to words)
  examples/        # example conversations for each domain
docs/
  MANIFESTO.md     # why we're doing this
  VOCABULARY.md    # the interface word list
  PATTERNS.md      # conversation patterns by domain
```

## The manifesto

The internet was built by engineers for engineers. Buttons, toggles, checkboxes, dropdowns — these are engineering primitives, not human ones. We've been adapting to machines for 40 years. It's time the machines adapt to us.

We don't need better buttons. We need no buttons. We need words.

Words are the oldest interface. They're how humans have always communicated — with each other and with the world. A word carries meaning. A button carries a click. Meaning is more than clicks.

This project rewrites the interface layer of the internet in natural language. Not as a chatbot bolted onto a button-based UI. As a fundamental replacement: the words ARE the UI. You say what you want. The system does it and tells you in words what happened. No translation layer between human intent and machine action. No friction. No extraction. Just language.

## License

The words are free. The interface is open. Build with it.

— built from love, for life