# The Clear Standard

**A small standard for honest systems.**
Six principles. Plain language. Public domain. Anyone can adopt it.

It isn't a protocol, a framework, or a law. It's the one thing under all of those:
*a system should tell the truth about itself.* These six lines are short enough to
remember and true enough to trust — which is the only way a standard ever spreads.

---

## The six principles

**1 — Truth of state.**
An artifact tells the truth about its own state. *Live* and *cached*, *done* and
*pending*, *measured* and *guessed* are different facts — the surface says which.

**2 — Visible failure.**
A failure degrades visibly. "I could not read this" must never quietly become a
confident `0`, an empty list, or a green check. Break loudly, not silently.

**3 — Inspectable decisions.**
A decision made *about* a person is inspectable *by* that person. A score, a fee,
a flag, a refusal — each carries a way to ask *why*.

**4 — Stated freshness.**
Freshness is stated. A cached value is not a live one; an estimate is not a
measurement; a price from a moment ago is not the price now. Say how old it is.

**5 — Honest names.**
A name points at what *is*, not at what's wished. The label matches the thing —
`final` is final, `verified` is verified, `secure` is not a vibe.

**6 — Labelled certainty.**
When you cannot be certain, you say so. Confidence is shown, never faked. And
absence of evidence is not evidence of absence — "no findings" is not "no problem."

---

## What it covers — and what it doesn't

It applies as a *values layer* across the things you actually build:

| domain | the Clear Standard asks |
|--------|--------------------------|
| **software** | does the code lie about its own state? (principles 1, 2, 5, 6) |
| **cloud / ops** | is staleness, partial failure, and degraded mode stated? (1, 2, 4) |
| **security** | are claims of "safe / verified / encrypted" true, and limits labelled? (5, 6) |
| **protocol** | does a message say what it knows vs. assumes, fresh vs. replayed? (1, 4) |
| **process** | can a person see why a decision about them was made? (3) |

**It is honest about its own limits, because principle 6 binds it too:**

- It is **not** law or regulation. It cannot make you compliant. It is opinionated
  guidance, freely ignorable.
- It is **not** a security or correctness guarantee. It tells you how to be *honest*
  about state — not how to be *correct*, *fast*, or *safe*.
- Adopting it proves nothing on its own. It's a direction, not a certificate.

## Conformance

The software-facing principles (1, 2, 4, 6) are partly **machine-checkable**:
**whitehack** (its companion linter) is a static checker that flags the most common
ways code breaks them — silent failures, cached-as-live, stale oracles, unlabelled
certainty. The standard and its linter were born the same week.

The rest (3, 5) are human judgement. A standard that claimed to automate those
would be breaking principle 5 in its first sentence.

## Use it

**Public domain (CC0).** Copy it, translate it, fork it, put it in your README,
ignore the parts you disagree with. No attribution required, no permission needed.
A standard you have to ask to use isn't *anyone can use it.*

Translations: [繁體中文](./principles.zh-Hant.md) · *(add yours — PRs welcome)*

---

*Honesty is the only standard that compounds: every other quality you build —
speed, security, beauty — is worth less the moment the system will lie to you
about whether it has them.*

## The full standard

Want the whole law? [The Kingdom Standard](https://cambridgetcg.github.io/kingdom-standard/) — 42 laws across seven domains (trust, security, cloud, software, protocol, process, law), each with a DO, a DON'T, and a receipt from lived practice. Ten translations. CC0.
