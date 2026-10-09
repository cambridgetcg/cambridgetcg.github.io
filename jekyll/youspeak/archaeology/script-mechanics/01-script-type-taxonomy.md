---
chapter: 1
title: Script-type taxonomy
parent: archaeology/script-mechanics/
---

# Chapter 1 — Script-type taxonomy

_What does each script-type encode, sacrifice, and reveal about the reading experience it creates?_

Writing systems are not neutral delivery-channels. Each type encodes a particular theory about what language IS — what units matter, what should be marked, what can be left to context. When a culture adopts a writing system, it is also adopting an epistemological stance.

YOUSPEAK is designing a new writing system. To do this well, we need to understand the full design-space — not to imitate any single tradition, but to choose consciously where on each axis we want to stand.

---

## The taxonomy (seven types)

The conventional linguistics classification has seven major script-types. Real historical scripts often blend types (Egyptian is logographic + phonographic + determinative; Maya is logographic + syllabic). The taxonomy names the *primary encoding unit* — what the glyph fundamentally represents.

---

### Type 1 — Logography (morpheme-writing)

**Principle**: One glyph = one morpheme (a meaningful unit of language).

**Primary examples**: Chinese *hanzi*, Egyptian hieroglyphs (logographic layer), Sumerian cuneiform (earliest phase), Maya glyphs (main signs), Yi script.

**What it encodes**: Meaning directly. You do not need to know how to *pronounce* a logograph to understand it. A Chinese-speaker and a Japanese-speaker can read the same hanzi and understand the same meaning even though they pronounce it completely differently (*mù* vs. *ki* for 木, tree). The glyph encodes the concept, not the sound.

**What it sacrifices**: Efficiency for new words. Pure logographic systems require one new glyph per morpheme. Classical Chinese required ~50,000 characters for full literacy; practical literacy required 3,000-5,000. This is a high acquisition barrier. And logographic systems cannot easily represent proper nouns, foreign borrowings, or neologisms without phonetic supplements.

**The reader's experience**: A logographic reader is *recognizing patterns*, not *assembling sounds*. This is fundamentally different from alphabetic reading. Skilled Chinese readers process hanzi holistically — the glyph as a gestalt, not as its component strokes. The glyph is an icon. Reading logographically is more like looking at faces than like decoding a cipher. 

**Historical evidence for this**: Brain imaging studies (Tan et al., 2001; Liu et al., 2007) show that Chinese character-reading activates stronger visuospatial processing areas (inferior temporal gyrus, fusiform face area region) than alphabetic reading, which activates stronger phonological processing areas. Chinese readers *see* meaning; alphabetic readers *hear* it (internally).

**Why this matters for YOUSPEAK**: YOUSPEAK is explicitly **morpheme-logographic** — one codepoint per morpheme, glyphs represent meanings. This is by design and is theologically motivated (each morpheme comes from a tradition that carries its own semantic field; the glyph should evoke that field). YOUSPEAK is building in the logographic tradition, not the alphabetic tradition. We need to understand what this commits us to:

- Glyph-designs must be *visually distinct* at the morpheme level (not the phoneme level)
- Acquisition involves *learning icons*, not *learning phonological rules*
- The reading experience should be *contemplative recognition*, not rapid phonological assembly
- This is appropriate for a liturgical/theological language where *dwelling in a word's meaning* is the point

---

### Type 2 — Syllabary (syllable-writing)

**Principle**: One glyph = one syllable.

**Primary examples**: Japanese *hiragana* and *katakana*, Cherokee (invented 1821 by Sequoyah), Linear B (Mycenaean Greek), Vai (West African), Kana in modern Japanese use.

**What it encodes**: Sound at the syllable level. A syllabary needs ~80-150 signs (depending on the language's syllable structure) compared to ~1000+ for a full logography, but more than the ~26-30 of an alphabet.

**What it sacrifices**: Handling of syllable-final consonants. Many syllabaries work best with CV (consonant-vowel) syllables; languages with complex consonant clusters (like English's "strengths" or Japanese's loan-adaptation of "McDonald's" → *makudonarudo*) strain the system. Japanese kana works well because Japanese syllables are almost exclusively CV; hiragana handles Japanese phonology elegantly because Japanese phonology is simple enough to fit.

**The reader's experience**: Syllabic reading is faster than alphabetic reading for the languages it suits. The reading unit (syllable) corresponds to the *natural spoken unit* — we speak in syllable-bursts. Japanese hiragana-readers process syllable-glyphs at approximately the same speed as English letter-readers process individual letters, but since each kana-glyph carries *more information* (a full syllable-sound), Japanese readers can cover more linguistic ground per fixation.

**Cherokee as a designed system**: Sequoyah's invention of Cherokee syllabary (1821) is one of history's most remarkable achievements — he designed 85 signs from scratch, in a single lifetime, for a specific language. He adapted shapes from sources he could see (English letters, some numerals) but assigned them entirely new sound-values. Cherokee literacy spread to 90% of the Cherokee population within a decade of the system's introduction — a rate unprecedented in literacy history. This tells us something about the *matchedness* of script-to-language: the Cherokee syllabary fit Cherokee phonology so well that it was *learnable within a few days by adult speakers*. The match between the language's natural units and the script's encoding units determines acquisition speed.

**Why this matters for YOUSPEAK**: YOUSPEAK is not a syllabary — it's morphemic. But the Cherokee example is instructive for the **-me** suffix design: -me carries significant semantic load AND it functions as a suffix (it always follows a content morpheme). This is analogous to a kana-use pattern in Japanese where content-words (written in kanji/logograms) are followed by grammatical particles and inflections (written in hiragana/syllabary). The visual distinction between *content* (large, iconic) and *grammar* (smaller, lighter) is a design pattern we can learn from Japanese mixed writing.

---

### Type 3 — Abjad (consonant-writing)

**Principle**: One glyph = one consonant. Vowels are either omitted or marked with optional diacritics.

**Primary examples**: Hebrew, Arabic, Aramaic, Phoenician, Syriac, Tigrinya (partially). These are the classic Semitic abjads.

**What it encodes**: Consonantal skeleton. In Semitic languages, the consonants carry the basic semantic field; vowels mark grammatical function (tense, number, case, person). An abjad is *designed for this language structure* — it encodes what carries meaning (consonants) and relies on reader-knowledge for what shifts meaning (vowels). A skilled Hebrew reader of an unvoweled text knows from context and root-familiarity what vowels to supply; beginning readers use vowel-marks (nikkud).

**What it sacrifices**: Transparency for learners and for foreign words. An Arabic-speaker reading Arabic without vowel-marks relies on deep familiarity with the language's root-pattern system. Foreigners learning Arabic must first acquire that root-knowledge before the abjad becomes navigable. The system is efficient for the native speaker but opaque to the outsider.

**The theological encoding of abjads**: The abjad encodes the Semitic theological intuition that the **consonantal root is primary** — the divine name, the divine action, the theological concepts all live in the root. The vowels modulate the root but do not carry the theological-payload. Written Hebrew without vowels (as the Torah was originally written) presents the theology *in skeleton form* — the bare bones of the divine word, which the reader clothes with breath (vowels) through their knowledge of the tradition. Reading the Torah is thus an act of *co-creation* — the reader supplies what is not written, drawing on tradition.

YOUSPEAK's grammars/structures/coinages/radikance.md names this pattern as **RADIKANCE** — the consonantal-root as theological-skeleton.

**Why this matters for YOUSPEAK**: YOUSPEAK does not use an abjad (it has no vowel-dropping; EUMATHE principle demands transparency). But abjads teach us that *what you mark and what you omit* is a design decision that encodes a theory of meaning. YOUSPEAK's design decision: *every* morpheme gets a glyph, including suffixes — there is no silent or optional layer. This encodes a different theory: that the grammatical layer is as important as the lexical layer. The -me suffix is NOT silent; it is the theological payload.

---

### Type 4 — Abugida (consonant-diacritic writing, with inherent vowel)

**Principle**: One glyph = one consonant with an *inherent vowel* (usually /a/). Other vowels are marked by modifying the base glyph.

**Primary examples**: Devanagari (Sanskrit, Hindi, Nepali, Marathi), Ge'ez/Ethiopic (Amharic, Tigrinya, Ethiopian liturgical), Tamil, Thai, Tibetan, Khmer, Sinhala, most scripts derived from Brahmi (~300 BCE), Canadian Aboriginal Syllabics (Cree, Inuktitut).

**What it encodes**: Syllable structure, but by modifying a base-consonant glyph rather than using an independent glyph per syllable. This is more compact than a full syllabary and more expressive than an abjad. The base-consonant carries the meaning-anchor; the vowel modification adjusts the syllable.

**Devanagari's engineering**: The script was systematically designed (or systematized by Paninian grammarians, ~4th century BCE) around articulatory phonology. The consonant-table is organized by place and manner of articulation:
- Gutturals (throat): क (ka), ख (kha), ग (ga), घ (gha)
- Palatals: च (ca), छ (cha), ज (ja), झ (jha)
- Retroflex: ट (ṭa), ठ (ṭha), ड (ḍa), ढ (ḍha)
- Dentals: त (ta), थ (tha), द (da), ध (dha)
- Labials: प (pa), फ (pha), ब (ba), भ (bha)

This is *phonologically systematic* — the layout of the consonant-table encodes the articulation system of the human vocal tract. A person who learns Devanagari is simultaneously learning the phonological categories of Sanskrit phonetics. The script *is* the grammar of articulation. This is the parallel of Hangul's featural design (see below) — both scripts encode phonological structure in the script's structure.

**Ge'ez and the liturgical abugida**: Ethiopian Orthodox Christianity uses Ge'ez in its liturgy — one of the oldest continuously-used Christian liturgical languages. The Ge'ez script (Ethiopic) is an abugida with 33 base consonants, each with 7 vowel-modifications (forms). Learning Ge'ez means learning 231 distinct glyph-forms — but because they derive systematically from 33 base-forms with predictable modifications, acquisition is faster than 231 independent glyphs would suggest. The system is internally coherent.

**The Śiroreka (head-line) of Devanagari**: Devanagari letters hang from a horizontal head-line (śiroreka) at the top. Words are written with letters hanging below this continuous line; the line itself is a visual device that links letters into words, showing syllable-grouping. The head-line encodes the idea that letters are *supported from above* — a subtle theological-visual metaphor that scholars have noted aligns with the script's use for sacred texts. The line is the sky; the letters hang from it. Sanskrit is written as if the words descend from the cosmic order.

**Why this matters for YOUSPEAK**: YOUSPEAK does not use an abugida, but two lessons transfer:
1. **Systematic base + modification**: YOUSPEAK's suffix-glyphs (like -me) relate to content-morpheme glyphs. We can design them with a systematic relationship — the suffix modifies or completes the content morpheme visually, the way vowel-marks modify base-consonants in an abugida.
2. **The head-line as visual connector**: In YOUSPEAK compounds, we need a visual principle that shows which glyphs belong together as one word. Devanagari's śiroreka is one solution; YOUSPEAK uses compound-separator (U+E160) as another. But we could also *design the glyph-box* so that compound-glyphs visually lean toward each other — a gravity-toward-the-right in each glyph's composition, so that a compound reads as a connected unit.

---

### Type 5 — Alphabet (phoneme-writing)

**Principle**: One glyph = one phoneme (consonant or vowel).

**Primary examples**: Latin/Roman alphabet (English, French, Spanish, Italian, Portuguese, etc.), Greek, Cyrillic, Armenian, Georgian, Coptic.

**What it encodes**: Individual sounds (phonemes). With ~26-30 letters, any word in the language can be spelled. The system is maximally general — any word, proper noun, neologism, or foreign borrowing can be encoded phonetically.

**What it sacrifices**: Meaning-density. An alphabetic reader must assemble phonemes into syllables, syllables into morphemes, morphemes into words — a three-step assembly process that logographic readers don't need. Alphabetic reading involves more phonological processing and more serial assembly. The benefit is maximum flexibility; the cost is that the glyph tells you nothing about meaning directly — you must know the language.

**The Greek contribution**: The Greek alphabet (developed ~800 BCE from Phoenician abjad) made the crucial innovation of using letters to represent *vowels* — the Phoenician abjad had no vowel letters. This produced the first *full* alphabet in the sense we now mean. Greek had letters that were not present in Phoenician (Α, Ε, Η, Ι, Ο, Υ, Ω — the vowels) — these were Phoenician letters that represented sounds Greek didn't have, repurposed by Greek-speakers as vowel-marks. The result was a system that could represent Greek more precisely than any abjad could.

**The Roman spread**: The Latin alphabet (from Greek via Etruscan, ~700-500 BCE) became the most widely distributed writing system in human history — now used by ~70% of the world's written languages. Its spread follows Roman military expansion, Christian missionary activity, and colonial-era language-replacement. The alphabet's spread was not because of inherent superiority but because of the political power of those who used it.

**Why this matters for YOUSPEAK**: YOUSPEAK uses the Latin alphabet as its *transliteration layer* — the internal representation, the fallback display. This is the right choice for machine-readability and cross-platform compatibility. But the YOUSPEAK *glyph layer* is not alphabetic — it is morpheme-logographic. We are designing two encoding systems simultaneously: an efficient machine-readable transliteration (Latin) and a meaning-dense glyph-display (YOUSPEAK script). This dual-layer is like Japanese mixed writing (kanji + kana + rōmaji), where different encoding systems serve different purposes within the same text.

---

### Type 6 — Syllabic-logographic mixed systems (the most common in sacred-script traditions)

**Principle**: A single script combines logographic (meaning-glyphs) and phonographic (sound-glyphs) principles. Different glyphs serve different functions; context and position determine which reading is intended.

**Primary examples**: Egyptian hieroglyphs, Maya glyphs, Sumerian cuneiform (mixed period), Japanese mixed writing (kanji + hiragana + katakana), modern Chinese (hanzi + pinyin), Korean (hangul + hanja in formal use).

**Egyptian mixed system in detail**: Every Egyptian word is typically written with:
1. A **phonogram** (one or more consonant-signs that spell the sound of the word)
2. A **determinative** (a silent logogram appended at the end that categorizes the word's semantic domain)

Example: the word *nefer* (𓄤𓆑𓂋, beautiful/good) is written with:
- Phonograms: nfr consonants (voiced by the three phonogram signs)
- The nefer-glyph itself (the trachea-with-heart sign, 𓄤) also serves as the word's determinative — it silently classifies the word as belonging to the semantic domain of "beauty/goodness"
- In some contexts, the nefer-glyph functions as a pure phonogram (nfr sounds); in others, as a pure logogram (the meaning "beautiful")

This means a single glyph can carry meaning in two simultaneous registers: as a sound-value AND as a meaning-indicator. Egyptian readers learned to read both layers simultaneously — a cognitive sophistication that required years of scribal training.

**Maya glyphs as mixed system**: Each Maya glyph-block is a compound of a main sign (logographic — represents a morpheme-meaning) with affixes (syllabic — can provide phonetic complements that spell the pronunciation, or serve as grammatical markers). A single glyph-block can contain 3-4 sub-signs arranged in a conventionalized spatial pattern. The scribe chose whether to spell a word logographically or syllabically (or both simultaneously) based on what would be most elegant and clear. Scribes had artistic freedom within a strict system — a combination of rule and creativity that is aesthetically beautiful.

**Why this matters for YOUSPEAK**: YOUSPEAK's morpheme-glyphs already function as logographs (doxa = glory, not just "a D-sound"). The design_philosophy.md adds *donor-tongue sigils* (small marks that indicate which tradition a morpheme comes from — Greek, Latin, Hebrew, etc.) to the glyph's corner. This creates a **mixed system**: the glyph body is logographic (encodes meaning), the sigil is categorical (encodes tradition-origin). This is structurally similar to Egyptian's determinative system — a layer of categorical information added to the primary glyph.

The YOUSPEAK design question this raises: should the donor-tongue sigil be *inside* the glyph body (integrated), or *outside* it (as a separate mark in the corner)? Egyptian determinatives come AFTER the phonographic spelling; Japanese furigana comes ABOVE the kanji. Both are external. YOUSPEAK's design_philosophy.md opts for a corner-sigil (external), which is the right choice for cognitive load — it doesn't compete with the main iconic shape.

---

### Type 7 — Featural systems (the most consciously engineered)

**Principle**: The glyph's *shape* systematically encodes phonological or semantic features. Glyphs that represent phonologically similar sounds look visually similar.

**Primary examples**: Korean Hangul, Pitman shorthand, Bell's Visible Speech (1867), International Phonetic Alphabet (IPA), UNIFON (English phonemic alphabet, 1959).

**Hangul as the paradigm case**: Hangul (1443 CE) was consciously designed by King Sejong and his scholars. Its design axioms:

1. **Consonant-glyphs encode articulation**: Each consonant-letter visually depicts the position or movement of the vocal organs when producing that sound.
   - ㄱ (g/k) — the back of the tongue touching the roof of the mouth (a side-view of the tongue-root blocking the throat)
   - ㄴ (n) — the tongue touching the roof of the mouth at the teeth-ridge (a side-view of the tongue-tip in alveolar position)
   - ㅁ (m) — the lips closed (a side-view of a closed mouth)
   - ㅅ (s) — teeth together (two strokes like front teeth)
   - ㅇ (ng/silent) — the throat (a circle = the open throat or the ring of the vocal cords)
   
2. **Aspiration is marked geometrically**: Aspirated consonants (k, t, p, ch) are formed by adding an extra stroke to their unaspirated bases (g/k, d/t, b/p, j/ch). The extra stroke = extra breath.

3. **Vowels encode orientation to heaven/earth/human**: The three primary vowel-strokes are:
   - ㆍ (aɾae-a, the ancient vowel) — a single dot = Heaven (yang)
   - ― (eu) — a horizontal stroke = Earth (yin)
   - ㅣ (i) — a vertical stroke = Human (the mediator between heaven and earth)
   All other vowels are combinations of these three elements. The vowel-system encodes a cosmological-anthropology.

4. **Syllable-blocks**: Hangul letters are combined into square syllable-blocks. The syllable block contains initial consonant (top-left), vowel (right or bottom), and optional final consonant (bottom). The block is read top-to-bottom, left-to-right within the block. Words are sequences of blocks.

**Hangul's theological significance**: Sejong's preface (*Hunminjeongeum*, 1446) declares that the script was created "to help the people" — those who could not access literacy through Chinese hanja (which required years of classical education). Hangul is a **democratizing** script. It can be learned in a day (the famous claim). Its design is so well-matched to Korean phonology that the learning curve is almost zero for Korean speakers. The alphabetic principle of Hangul — that you can represent *any* word with a small set of phonological primitives — is the same as Greek/Latin, but Hangul's execution is more elegant because the glyph-shapes *teach the phonological system* rather than requiring it to be memorized separately.

**Why this matters for YOUSPEAK**: YOUSPEAK does not need to be featural in the phonological sense (we're morpheme-logographic, not phonemic). But the **design principle** of Hangul is directly applicable: *the shape of a glyph should encode something about its function or meaning*. Hangul's consonant-glyphs look like the articulation they represent. YOUSPEAK's morpheme-glyphs should look like — or at least evoke — the concepts they represent. The *pictographic motivation* chapter (Chapter 3) develops this directly. The Hangul insight: **every design element is justified; nothing is arbitrary**.

---

## Comparison table

| Type | Encoding unit | Example scripts | Glyph count | Meaning from glyph? | Sound from glyph? |
|---|---|---|---|---|---|
| Logography | Morpheme | Chinese hanzi, Egyptian | 3,000–50,000 | Direct | No (or indirect) |
| Syllabary | Syllable | Hiragana, Cherokee | ~80–150 | No | Syllable |
| Abjad | Consonant | Hebrew, Arabic | ~22–28 | No | Consonant only |
| Abugida | Consonant + inherent vowel | Devanagari, Ge'ez, Tibetan | ~50–300 | No | Consonant + vowel |
| Alphabet | Phoneme | Latin, Greek, Cyrillic | ~24–35 | No | Full phoneme |
| Mixed | Multiple | Egyptian, Maya, Japanese | 50–50,000 | Partially | Partially |
| Featural | Phonological feature | Hangul | ~24 + 14 | No (phonological) | Feature-by-feature |

---

## YOUSPEAK positioning

YOUSPEAK's script is:

- **Logographic** in its primary encoding unit (one glyph per morpheme = one glyph per meaning-unit)
- **Compositional** in word-formation (compound words = sequence of morpheme-glyphs)
- **Mixed** in its meta-information (donor-tongue sigils encode tradition-of-origin; class-marks encode grammatical function)
- **Featural** in aspiration (the design_philosophy.md uses shape-families that group morphemes by semantic domain — curves for beauty-domain, crosses for truth-domain, rays for appearing-domain; this is featural encoding at the semantic level)
- **Not phonographic** — the glyph tells you nothing about how to pronounce the morpheme (pronunciation is handled by the Latin transliteration layer)

This positioning is principled. YOUSPEAK is a **liturgical/contemplative language** — speed-of-phonological-decoding is less important than *depth of semantic encounter*. A person who sees the doxa-glyph (weight-that-manifests, the downward triangle with horizontal bar) should *feel the concept* before they hear the word. The glyph precedes the sound; the concept precedes the utterance. This is the appropriate sequence for a language designed for worship.

---

_Chapter 1 complete. → [Chapter 2: Letterform anatomy](02-letterform-anatomy.md)_
