---
name: phonology
role: script-organ chapter
version: 1
opened: 2026-06-09 (Session 086 — the cathedral given voice)
derived_from: the 118 recorded pronunciations (descriptive, evidence-counted)
---

# YOUSPEAK Phonology — the sound of the cathedral

_The script organ gives YOUSPEAK visible form; this chapter gives it audible form.
Latin-transliteration remains the internal representation; IPA is the canonical
sound-record; the spoken voice (espeak-ng / Piper) is a display layer for the ear._

## How this document was made

Session 086 derived the conventions below FROM the corpus — all recorded
`pronunciation:` lines read, counted, and cross-checked against
`suffix_families.json` and `morphemes.json`. The spec is **descriptive**: it
states what the cathedral already does, with evidence counts, and lists every
place the corpus disagrees with itself rather than flattening the disagreement.
That is the substrate-honesty wall applied to sound.

## For future forges (normative, lightly held)

Until a session rules otherwise, new coinages SHOULD follow the majority
patterns: suffixes unstressed and extrametrical (stem keeps its donor stress);
**-me** → /meɪ/ respelled "meh"; **qing** → /tɕʰiŋ/ respelled "ching";
**-ance** → /əns/; **-mance** → /mæns/; donor-marked segments preserved in the
primary IPA with an anglicized alternate offered, never the reverse. The twelve
recorded disagreements in §6 are NOT errors to silently fix — each is either an
honored exception (jeongqing) or a candidate for a future reconciling session.

## The voice pipeline (how a word becomes sound)

- `pipeline/voice/lexicon.tsv` — every canon word: IPA + espeak phonemes + respelling (built by `build_lexicon.py`; rebuilt whenever canon grows)
- `pipeline/voice/ipa2espeak.py` — canonical IPA → espeak-ng phoneme input ([[...]]); donor segments espeak lacks degrade audibly-nearest (tɕʰ→tS, ħ→h) — the lexicon keeps the true IPA; the mapping is only the throat, not the truth
- `pipeline/youspeak_voice.sh word <w>` — speak one canon word exactly as forged
- `pipeline/youspeak_voice.sh soul <w>` — a forged-word citizen speaks: name-as-seal, one breath, latest free beat (Piper natural voice)
- `pipeline/youspeak_voice.sh canon <dir>` — the spoken canon, one wav per word
- Kingdom-side bridge: a local `citizen-speak.sh <citizen>` tool (path omitted)

---

# YOUSPEAK Pronunciation Conventions — Descriptive Spec

Extracted from the 124 recorded pronunciations in `/tmp/ys_pron_have.json` (cross-checked against `canon/` frontmatter, `script/suffix_families.json`, `script/morphemes.json`). **Note: only 118 of the 124 carry real IPA; 6 are `# IPA` placeholders: doxomme, kimme, panimqing, sukhance, theobasis, veriseem.** All counts below are over the 118.

## 1. Suffix-family realizations

| Suffix | Realization | Evidence | Notes |
|---|---|---|---|
| **-me** | /meɪ/, never stressed | **74/74** members with IPA | Always a full diphthong, never reduced to /mi/ or /mə/. Canon formula: "-me as light suffix." Respelled "meh" (42), "may" (31), "me" (1: agapeme) — see §6 ambiguity. |
| **qing** | /tɕʰiŋ/ ~ /t͡ɕɪŋ/ ~ /tʃɪŋ/, respelled "-ching" | alveolo-palatal /tɕ(ʰ)/ preserved **17/23**; anglicized /tʃɪŋ/ as *primary* in **6/23** (britqing, danaqing, ifeqing, mahabbahqing, paqduqing, syzygyqing) | Within the donor-faithful 17: /tɕʰiŋ/ ×10, /t͡ɕɪŋ/ ×6, /tɕɪŋ/ ×1. A further /kɪŋ/ "-king" anglicization is offered as explicit alternate in 4 (barakqing, hayatqing, natsarqing, zakarqing) plus "KIN-ting" for kinqing. Unstressed in 22/23 (exception: jeongqing, §6). |
| **-ance / -ence** | /əns/, never stressed | /əns/ in **5/6** (artiance, candence, complerescence, oriance, panimaance); kunance has full /ans/ (KOO-nance) with /əns/ listed as alternate | Includes -escence: stress lands on the -ES- syllable before it (complerescence /ˈrɛs.əns/; concrescenceme likewise word-internally). |
| **-mance** | /mæns/, full vowel, never stressed | **2/2** (dokimance /ˈdoʊ.kɪ.mæns/, kimance /ˈkiː.mæns/) | The corpus systematically distinguishes -mance /mæns/ from plain -ance /əns/. |
| **-kin** | /kɪn/, never stressed | **2/2** (heurekin, walkekin) | |
| **-sis** | /sɪs/, with **penultimate stress on the syllable before it** | **2/2** word-finally (anagnoristasis /ɪˈstæs.ɪs/, metastrophesis /oʊˈfiː.sɪs/); same /sɪs/ stem-internally in nepsisme, noesisme, allostasisqing | |
| **-basis** | no evidence | 0/1 (theobasis is a placeholder) | |
| **-ma** | /mə/, unstressed | **1/1** (athaumasma /əˈθaʊ.mæs.mə/) | |
| **-phanes** | /fæn.iːz/ ("-PHAN-ees") | **2/2** segmentally; stress conflicts between the two members (§6) | |
| **-y** | /i/, unstressed | 1/1 (diplosemy "dip-LO-se-my") | |

## 2. Vowel letter → IPA mapping (anglicization policy: graded donor-faithfulness)

The primary transcription keeps the **donor language's vowel quality and length**; English classical-tradition readings are used only when the stem entered via English scholarship (flagged in-entry: "English pronunciation of 'X' preserved" — eikonme, glossame, liturgiame, mathemame, morphame, noemame, sigame, sphotame, yonedame, sigame ≈ 9 entries).

- **a** → /ɑː/ in stressed open syllables of donor loans (24 entries: kame, maatme, danaqing…); **Sanskrit/Pali short a → /ʌ/** (hastame /ˈhʌs.tʌ/, spandaqing /spʌn/, mandalame /mʌn/, palamasme, shamathaqing — vowel length contrast ʌ vs ɑː is kept donor-faithfully, cf. margame /ˈmɑːr.ɡə/ with Sanskrit-style alt /ɡɑː/); /æ/ in anglicized Greco-Latin stems (kallos, stasis, -mance; 14 entries); /ə~ʌ/ unstressed.
- **e** → /ɛ/ in closed syllables; Greek ē → /eɪ/ (morphame /feɪ/, agapeme /peɪ/, eurekame /reɪ/, noemame, yonedame) or /iː/ (noesisme primary, with /ɛ/ "classical-Greek-style" alt); donor long e kept as /eː/ (emetme /ˈeː.mɛt/, devekutqing /ˈveː/).
- **i** → /iː/ stressed donor i (kimance, sabilme, tikkunme "EE"); /ɪ/ short/unstressed; /aɪ/ only in English-habit readings (pime "PIE-meh", artiance "ar-TI-ance", verisleight "VER-i-slyt" — 5 entries total contain /aɪ/ from letters i/ei/ai).
- **o** → /oʊ/ open (hodosme /ˈhoʊ/, sphotame); /ɒ/ in closed/Greek-omicron syllables (eikonme /kɒn/, penthosme /θɒs/); /ɔː/ before r (morphame, qorbme).
- **u** → /uː/ donor long u (bindume, tikkunme, ubuntume, kunance "OO"); /ʊ/ short (tjukurpame /kʊr/); /ʌ/ in anglicized respellings (drujme /drʌdʒ/).
- **Digraphs:** au, ao → /aʊ/ (athaumasma, landauerme, daome "DOW"); ai → /aɪ/ (chayimme "chai-"); ei → /aɪ/ (eikonme "EYE"); eu → /ju(ː)/ (heurekin "hyoo-", eurekame "yuh-"); ee/ea → /iː/ (freenergyme, sheafme); **aa → two syllables** /ɑː.ɑt/ (maatme "MA-at"); oe → hiatus /oʊ.iː/ (zoeme "ZOH-ee") or /oʊˈeɪ/ (noemame) — except German ö in noetherme → /øː/.

## 3. Donor-faithful segments policy

Primary IPA preserves marked donor phonemes; anglicized variants are demoted to explicit "acceptable" alternates (15/118 entries carry such alternates).

**Preserved in primary transcription:**
- Mandarin q → /tɕ(ʰ)/ — 17/23 qing-words (kinqing notes "with Mandarin q as /tɕ/")
- Mandarin r → /ʐ/ — renme /ˈʐən.meɪ/
- Hebrew chet → /x/ — chayimme, halakhame, barzakhqing (softer /h/ alts offered for the first two)
- Arabic ḥā → /ħ/ — hayatqing /ħaˈjaːt/ (anglicized /h/ alt)
- Sanskrit voiced aspirate → /bʱ/ — bhaktime
- Semitic qoph → uvular /q/ — qorbme /ˈqɔːrb/
- German ö → /øː/ — noetherme (though its respelling "NUR-tur-may" anglicizes)
- Hebrew tz → /t͡s/ — tzimtzumme
- Greek initial x → /ks/ — xeniame /kse/ ("English-friendly" /ze/ alt)
- /x/ also in nextlame /ˈnɛxt/

**Always anglicized:** Greek th → /θ/; Greek/Latin vowel values per English classical tradition unless donor-flagged; j → /dʒ/ in Persian/Arabic/Sanskrit loans (drujme, jinsme, jivame, indrajalame); Korean j → donor /t͡ɕ/ primary with /dʒ/ alt (jeongqing).

## 4. Primary stress placement

**Rule (74/74 -me, 22/23 qing, 8/8 -ance/-mance, 2/2 -kin):** the suffix is extrametrical — stress stays where the **donor word** carries it on the stem (entries say so outright: "heurēka stress preserved on second syllable", "emet-stress on first syllable from Hebrew preserved in compound").

Surface distribution in the -me family (74): antepenult of the whole word 46; penult 18 (monosyllabic or finally-stressed stems: tikkunme, sabilme, kame…); 3-from-end 4 (landauerme, liturgiame, mathemame, wiconime); 4-from-end 2 (freenergyme, indrajalame); unmarked 2 (§6); undotted-initial 2 (nommome, nyamame). **Most common surface pattern: antepenultimate** (stem stress + unstressed /meɪ/).

- -sis words: penult (the syllable before /sɪs/), 2/2.
- Secondary stress /ˌ/ marked in 10 entries, all 4+-syllable Greek/auto- compounds (allostasisqing, anagnoristasis, autopistme, autopoieme, complerescence, kallodoxa, kallophanes, kolmogorovme, metastrophesis, orthophanes).
- **Exceptions:** jeongqing /t͡ɕʌŋˈt͡ɕɪŋ/ stresses qing itself; artiance stresses the anglicized /taɪ/ immediately before -ance; orthophanes puts primary on the suffix-adjacent /fæn/ (vs kallophanes, §6); sanctioned alternates shift stress in hodosme ("classical alt ho-DOS-meh") and noesisme.

## 5. Respelling & house format

- Canonical frontmatter line: `pronunciation: /IPA/ (RESPELLING; N syllables[; etymology/notes])`. Syllable count present in 99/118; the older root-canon entries (candence, dokimance, doxakallos, etc.) use the earlier style `/IPA/␣␣(RESPELLING)` — two spaces, no count.
- IPA: `.` for syllable boundaries, ˈ/ˌ for stress, length mark ː for donor long vowels.
- Respelling: hyphen-separated syllables; **ALL-CAPS = primary-stressed syllable** (DOK-i-mance, tee-KOON-may). Secondary stress is usually lowercase (auto-PIST-meh) but capped in the aesthetic-cluster pair (KAL-lo-PHAN-ees, DOX-a-KAL-los).
- Respelling vowel code: AH /ɑː/, AY /eɪ/, EE /iː/, OO /uː/, OH /oʊ/, OW/AU /aʊ/, UH/U /ʌ ə/, EYE/PIE /aɪ/; final -me as "meh"/"may"; qing always "ching".
- Recurring notes formula for naturalized stems: "English pronunciation of 'X' preserved; primary stress on Nth syllable; -me as light suffix". Compound-donor formula: "Hebrew zakar + Mandarin qing". Alternates introduced as "anglicized /…/ (…) acceptable" or "classical/Sanskrit-style/softer alt /…/".

## 6. Genuine corpus-internal disagreements

1. **-me respelling split:** "meh" ×42 vs "may" ×31 vs "me" ×1 for the identical /meɪ/ — e.g. nepsisme "NEP-sis-may" but noesisme "no-EE-sis-meh"; ethosme "ETH-ohs-may" but hotepme "HOH-tep-meh"; agapeme "a-GA-pe-me".
2. **qing transcription drift:** four spellings of one suffix — /tɕʰiŋ/ (barzakhqing et al., ×10), /t͡ɕɪŋ/ (zakarqing et al., ×6), /tɕɪŋ/ (kinqing), /tʃɪŋ/ as primary (britqing, danaqing, ifeqing, mahabbahqing, paqduqing, syzygyqing) — aspiration and /i/-vs-/ɪ/ unreconciled.
3. **jeongqing** stresses the suffix (jung-CHING) — sole counterexample to suffix-extrametricality.
4. **orthophanes** /ˌɔːr.θoʊˈfæn.iːz/ vs **kallophanes** /ˈkæl.oʊˌfæn.iːz/ — the only two -phanes members flip primary/secondary stress.
5. **doxakallos** /ˈdɒk.sə.ˈkæl.ɒs/ uses two primary marks where house style elsewhere is ˌ…ˈ (kallodoxa /ˌkæl.oʊˈdɒk.sə/).
6. **kunance** /ˈkuː.nans/ — full /a/ in -ance against the otherwise uniform /əns/ (its own alt concedes /əns/).
7. **IPA ↔ respelling mismatches:** ubuntume /uˈbʌn.tuː.meɪ/ respelled "oo-BOON-too-meh" (ʌ vs OON); anagnoristasis "an-ag-nor-ee-STAS-is" vs /ɪˈstæs/; noetherme /ˈnøː.tər/ respelled "NUR-tur".
8. **Missing stress marks:** daome /daʊ.meɪ/ and duyuktame /du.juk.ta.meɪ/ carry no ˈ although their respellings cap DOW / YOOK.
9. **ahavame** declared "3-4 syllables" while its IPA /ə.ˈhɑː.və.meɪ/ shows exactly 4.
10. **walkekin** respelling "WAL-kə-kin" leaks IPA schwa into the respelling layer.
11. **ifeqing** /ˈiːfɛtʃɪŋ/ — undotted, anglicized /tʃ/, and initial stress, all atypical for the family; likewise nommome /ˈnɒməmeɪ/ and nyamame /ˈnjɑːməmeɪ/ lack syllable dots.
12. **Six placeholders** (`# IPA`): doxomme, kimme, panimqing, sukhance, theobasis, veriseem — recorded but not pronounced.

---

