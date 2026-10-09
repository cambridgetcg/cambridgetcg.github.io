---
title: YOUSPEAK Codepoint Assignment Table
opened: 2026-04-24
updated: 2026-06-10
data_source: morphemes.json
encoding_range: Unicode Private Use Area (PUA) U+E100–U+E1FF
---

# YOUSPEAK Codepoint Assignments

_Unicode PUA encoding for the YOUSPEAK writing system. 256 slots reserved (U+E100–U+E1FF). Structured assignment by morpheme class. Extensible to U+E200+ when the inventory exceeds 256._

---

## Design principles

1. **PUA encoding** (not full Unicode proposal) — immediate usability; future migration path to official Unicode codepoints if the script achieves institutional adoption.
2. **Range-structured** — content morphemes, grammatical morphemes, structural marks each have their own subrange. Class is inferable from codepoint.
3. **Stable** — once assigned, a morpheme's codepoint does not change. Additions go to the next available slot; nothing is rearranged.
4. **Sparse** — ample empty slots left for extension.

## Subrange structure (U+E100–U+E1FF, 256 slots)

| Subrange | Count | Class | Allocated | Reserved |
|---|---|---|---|---|
| U+E100 – U+E13F | 64 | content morphemes | 56 | 8 |
| U+E140 – U+E15F | 32 | grammatical morphemes (prefixes/suffixes) | 17 | 15 |
| U+E160 – U+E17F | 32 | structural marks (separator, annotations, determinatives, rhythm) | 20 | 12 |
| U+E180 – U+E1FF | 128 | reserved for future use (cadences/tones, ligatures, compound-atomic forms) | 0 | 128 |

## Content morphemes (U+E100 – U+E13F)

| Codepoint | Latin | Tongue | Native | Meaning |
|---|---|---|---|---|
| U+E100 | doxa | Greek | δόξα | glory, manifested-weight |
| U+E101 | kallos | Greek | κάλλος | beauty (substantive) |
| U+E102 | ortho | Greek | ὀρθός | right, straight, true |
| U+E103 | phanes | Greek | φαν- | appearing, shining-forth |
| U+E104 | algia | Greek | ἄλγος | structural ache |
| U+E105 | anagno | Greek | ἀναγνώρισις | recognition-moment |
| U+E106 | stasis | Greek | στάσις | standing-still |
| U+E107 | meta | Greek | μετά | after, beyond, complete-change |
| U+E108 | strophe | Greek | στροφή | turning |
| U+E109 | thauma | Greek | θαῦμα | wonder, marvel |
| U+E10A | syn | Greek | σύν | together-with |
| U+E10B | phora | Greek | φορά | carrying |
| U+E10C | cand | Latin | candor | luminous-warm-clear-white |
| U+E10D | dokim | Greek | δοκιμ- | testing, assaying, approving |
| U+E10E | arti | Latin/Greek | ars/arete/artios | fitted, skilled-making, excellence |
| U+E10F | veri | Latin | verum | truth |
| U+E110 | compler | Latin | com+plere | filling-together |
| U+E111 | diplos | Greek | διπλόος | twofold, double |
| U+E112 | sema | Greek | σῆμα | sign, meaning |
| U+E113 | anastro | Greek | ἀναστρο- | inversion, turning-back |
| U+E114 | kalypt | Greek | καλύπτω | enclose, enfold |
| U+E115 | haphe | Greek | ἁφή | touching |
| U+E116 | allos | Greek | ἄλλος | other, different |
| U+E117 | parallax | Greek | παράλλαξις | parallel-shift |
| U+E118 | hypo | Greek | ὑπό | under, beneath |
| U+E119 | stix | Greek | στίξις | punctuation, stopping |
| U+E11A | kairos | Greek | καιρός | right-time, time-layer |
| U+E11B | morphe | Greek | μορφή | form, shape |
| U+E11C | klimax | Greek | κλῖμαξ | ladder, scale, gradation |
| U+E11D | lanthes | Greek | λανθάν- | escape-notice, be-hidden |
| U+E11E | sleight | English | sleight | deceptive-skill |
| U+E11F | seem | English | seem | appear-as |
| U+E120 | andros | Greek | ἀνδρός | of-a-person, of-a-being |
| U+E121 | gloria | Latin | gloria | glory (creature-scale) |
| U+E122 | vide | Latin | videre | seeing, perceiving |
| U+E123 | cede | Latin | cedere | yielding, stepping-back |
| U+E124 | choro | Greek | χορός | gathered-chorus |
| U+E125 | ki | Japanese | 気 | gathered life-attention-presence |
| U+E126 | qing | Mandarin | 情 | deep emotional bond, earnestness-of-feeling |
| U+E127 | kin | English/PIE | kin | family, chosen-relation; from PIE *ǵenh₁- |
| U+E128 | tacit | Latin | tacitus | silent, wordless |
| U+E129 | mushin | Japanese | 無心 | no-mind; action without deliberative self-awareness |
| U+E12A | me | Sumerian | 𒈨 | divine-ordinance, culture-constituting-quality-gift |
| U+E12B | nam | Sumerian | 𒉆 | destiny, abstract-quality-marker |
| U+E12C | kittu | Akkadian | 𒆠𒁴 | justice, truth-rightness-as-principle |
| U+E12D | kawil | Maya | K'awil | divine empowerment-quality, royal potency |
| U+E12E | chul | Maya | ch'ul/k'uhul | sacredness, holiness |
| U+E12F | kavod | Hebrew | כָּבוֹד | manifested-weight / glory-as-presence |
| U+E130 | jamal | Arabic | جَمَال | divine beauty / intimate-aspect of the Divine |
| U+E131 | brahman | Sanskrit | ब्रह्मन् | the absolute / ground-of-being / ultimate-reality |
| U+E132 | haqq | Arabic | الحق | The Real / truth-as-ground |
| U+E133 | dhikr | Arabic | ذِكْر | remembrance-worship / recitative-attention |
| U+E134 | hesych | Greek | ἡσυχία | sacred stillness / inner silence |
| U+E135 | bhakti | Sanskrit | भक्ति | devotional-surrender-quality |
| U+E136 | sukh | Sanskrit | सुख | ordinary ease / well-being / pleasant-feeling (opposite of duḥkha) |
| U+E137 | panim | Hebrew | פָּנִים | face as presence; face-to-face register |

> **Note on U+E12A range exception**: -me is the most productive YOUSPEAK suffix (25+ members) and the source of the core theological claim of the language (Sumerian *me* = divine ordinances as gifts constituting civilization). It operates grammatically as a suffix but carries the content-weight of a theological root morpheme; its codepoint therefore sits in the content range. Glyph: descent-into-reception — downward triangle in upward-opening arc.

## Grammatical morphemes (U+E140 – U+E15F)

| Codepoint | Latin | Tongue | Native | Meaning |
|---|---|---|---|---|
| U+E140 | a- | Greek | ἀ- | privative (not, without) |
| U+E141 | -sis | Greek | -σις | state-noun suffix (state resulting from verb) |
| U+E142 | -ance | Latin | -antia | quality/state suffix |
| U+E143 | -mance | Greek/English | -mantia | quality-mode suffix (mance in English: romance, necromance) |
| U+E144 | -ence | Latin | -entia | quality/state suffix (parallel to -ance) |
| U+E145 | -ma | Greek | -μα | result-of-action suffix (phantasma, stigma, trauma) |
| U+E146 | -iance | Latin | -iantia | luminous-quality suffix (radiance, brilliance) |
| U+E147 | -escence | Latin | -escentia | becoming suffix (adolescence, luminescence) |
| U+E148 | -mia | Greek | -μία | state-noun suffix |
| U+E149 | ana- | Greek | ἀνά- | up, back, again |
| U+E14A | en- | Greek | ἐν- | in, within |
| U+E14B | com- | Latin | con- | together, with |
| U+E14C | -y | Greek/English | -y | noun-abstract suffix (in diplosemy: diplos+sema+y) |
| U+E14D | -mi | Quechua | -mi | evidential: direct witness / personal experience |
| U+E14E | -si | Quechua | -si | evidential: reported / hearsay |
| U+E14F | -chu | Quechua | -chu / -chá | evidential: inferred / deduced from evidence |
| U+E150 | -auth | YOUSPEAK+Greek | auth- | evidential: by divine authority / Scriptural basis |

> **Note on U+E14D–E150 (evidentials)**: the Quechua-inherited knowledge-source suffixes (-mi direct witness, -si reported, -chu inferred) plus the YOUSPEAK-native extension -auth (by divine authority / Scriptural basis). Glyphs share the evidential family armature: identical claim-bar below, grasping-path above whose integrity encodes the epistemic gradient (S092).

## Structural marks (U+E160 – U+E17F)

| Codepoint | Latin | Tongue | Native | Meaning |
|---|---|---|---|---|
| U+E160 | · | YOUSPEAK | — | compound-separator — thin visual space between morpheme-glyphs in a single word |
| U+E161 | 「 | YOUSPEAK | — | reading-annotation open — introduces Latin-transliteration gloss over a glyph-sequence |
| U+E162 | 」 | YOUSPEAK | — | reading-annotation close |
| U+E163 | ↔ | YOUSPEAK | — | diplosemic-pair indicator — marks a word as having an Anastrophance-sibling; rendered as a small double-headed arrow over or alongside the word |
| U+E164 | ◆ | YOUSPEAK | — | canon-mark — optional indicator for canonically-promoted words, distinguishing from refine-register |
| U+E165 | । | Sanskrit | । (daṇḍa) | phrase-end mark — minor rhythmic pause in liturgical prose; Sanskrit daṇḍa tradition |
| U+E166 | ॥ | Sanskrit | ॥ (double daṇḍa) | sentence-end mark — major rhythmic pause; Sanskrit double-daṇḍa tradition |
| U+E167 | ‧ | Greek | · (ano teleia) | breath-pause mark — breath or meditative pause within a phrase; Greek ano teleia tradition |
| U+E170 | .DIV | Egyptian | 𓊹 | determinative: divine register |
| U+E171 | .PER | Egyptian | 𓀀 | determinative: person / agent |
| U+E172 | .ACT | Egyptian | 𓂻 | determinative: act / event / process |
| U+E173 | .ABS | Egyptian | 𓏛 | determinative: abstract quality / concept |
| U+E174 | .PRC | Egyptian | 𓁹 | determinative: perception / seeing / attending |
| U+E175 | .REL | YOUSPEAK | two-linked-figures | determinative: relation / between-persons |
| U+E176 | .HID | YOUSPEAK | dashed-outline | determinative: hidden / concealed / deceptive |
| U+E177 | .TIM | Egyptian | 𓇳 | determinative: time / temporal event |
| U+E178 | .PLC | Egyptian | 𓉐 | determinative: place / locus |
| U+E179 | .QNT | Egyptian | 𓏤𓏤𓏤 | determinative: quantity / plurality / collection |
| U+E17A | [selah] | Hebrew | סלה (selah) | sacred silence marker; held pause in worship-composition |
| U+E17B | O- | Greek | ὦ | vocative particle; marks address to GoD or sacred entity |
| U+E17C | mi: | Tok Pisin | mi | anchor particle: utterance stands from my side (grammars/ankyrance/, reserved 2026-07-16) |
| U+E17D | yu: | Tok Pisin | yu | anchor particle: utterance stands from your side, as received (grammars/ankyrance/, reserved 2026-07-16) |
| U+E17E | yumi: | Tok Pisin | yumi | anchor particle: utterance stands from within the us; inclusive dyad (grammars/ankyrance/, reserved 2026-07-16) |
| U+E17F | mitakuyame: | Lakota | mitákuye | anchor particle: utterance stands from within all-my-relations; liturgical (grammars/ankyrance/, reserved 2026-07-16) |

> **Note on punctuation marks (U+E165–E167)**: proposed in `archaeology/script-mechanics/05-reading-flow.md` (S075) from Sanskrit daṇḍa tradition and Greek *ano teleia*; reserved 2026-04-30; **implemented in the font 2026-06-10 (S092)** as the rhythm-family — visual weight ascends sep-dot < breath < daṇḍa < double-daṇḍa, all stroke-built and unfilled (fill is reserved for the canon-mark).

> **Note on determinatives (U+E170–E179)**: Egyptian-inherited silent class-markers. All ten stand on an identical short plinth-bar (the family motif: 'silent class-marker, not a word'), render at subordinate weight (60 vs the 80 content default), and suppress the corner class-mark (a determinative IS a class-tag). Animate icons face left, toward the word they classify (S092).

## Example compound encodings

Each word is the codepoint-sequence of its morphemes, in compound order:

| Word | Morpheme breakdown | Codepoint sequence |
|---|---|---|
| doxakallos | doxa + kallos | U+E100 U+E101 |
| kallodoxa | kallos + doxa | U+E101 U+E100 |
| orthophanes | ortho + phanes | U+E102 U+E103 |
| doxalgia | doxa + algia | U+E100 U+E104 |
| anagnoristasis | ana + gno(risis) + stasis | U+E149 U+E105 U+E106 |
| metastrophesis | meta + strophe + -sis | U+E107 U+E108 U+E141 |
| athaumasma | a- + thauma + -ma | U+E140 U+E109 U+E145 |
| synophora | syn + phora | U+E10A U+E10B |
| kallophanes | kallos + phanes | U+E101 U+E103 |
| dokimance | dokim + -ance | U+E10D U+E142 |
| artiance | arti + -iance | U+E10E U+E146 |
| verisleight | veri + sleight | U+E10F U+E11E |
| candence | cand + -ence | U+E10C U+E144 |
| complerescence | com- + compler + -escence | (U+E14B + U+E110 + U+E147) or just U+E110 + U+E147 |
| diplosemy | diplos + sema + -y | U+E111 U+E112 U+E14C |
| veriseem | veri + seem | U+E10F U+E11F |
| **doxame** | **doxa + -me** | **U+E100 U+E12A** |
| **kallome** | **kallos + -me** | **U+E101 U+E12A** |
| **mitakuyame** | **mitakuya + -me** | **[mitakuya codepoint TBD] U+E12A** |

## Reserved-for-growth

- **U+E138–U+E13F** — 8 content morpheme slots (next: the ten codepoint-less canon morphemes — theo, proskyn, sraddh, metano, kavv, nar, rah, sat, shukh, ypso — surfaced by the S092 espanso regeneration)
- **U+E151–U+E15F** — 15 grammatical morpheme slots
- ~~U+E17C–U+E17F~~ — **claimed 2026-07-16** by the ankyrance anchor particles (see structural marks table); tone/cadence/register marks move to the U+E180 pane
- **U+E180–U+E1FF** — a full 128-slot pane reserved: ligatures for very-common compounds, cadence/tone marks (Cadences/ chapter, future), substrate-variants (Substrata/ chapter, future), or expansion past the current ranges

## Migration note — future Unicode proposal

If YOUSPEAK script achieves adoption (institutional use, public-script-community formation, documentation sufficient for Unicode Technical Committee review), a formal Unicode proposal can be made. At that point, codepoints would migrate from the PUA to officially-assigned Unicode positions. All YOUSPEAK-aware tools (the transliterator, the font, the IME) would handle the remapping. Documents encoded in PUA can be migrated by a one-pass search-and-replace.

Until then, PUA is sufficient for all private, institutional, and research use.

---

_Codepoint table opened 2026-04-24. Updated 2026-04-30 (S075): U+E12A assigned to -me; U+E165–U+E167 reserved. Updated 2026-06-10 (S092, the font made flesh): all 93 catalogued morphemes now have drawn glyphs AND live in the built font (youspeak-v1.otf/.ttf); daṇḍa rhythm-family implemented; tables regenerated from morphemes.json — the data source of truth._
