---
chapter: LoRA training pipeline for YOUSPEAK
opened: 2026-04-24
purpose: fine-tune a base LLM into YOUSPEAK-fluency via Low-Rank Adaptation
status: scaffolding + config; execution requires corpus curation + compute
---

# YOUSPEAK LoRA Pipeline

_Where a base LLM (Llama 3, Qwen, Mistral, or similar) is adapted into YOUSPEAK-fluency via Low-Rank Adaptation (LoRA). Small trainable parameter budget; runs on Apple Silicon via MLX or on a single consumer GPU via PyTorch._

---

## Why LoRA

Full fine-tuning of an 8B model adjusts ~16 GB of weights. LoRA adjusts ~50-200 MB — low-rank decompositions of attention and MLP projection matrices — while the base weights stay frozen. For YOUSPEAK, this is ideal:

- The domain is small (18 canonical words, ~50 morphemes, ~200-line canon-entries-per-word)
- We need the model to *specialise*, not re-learn language from scratch
- Training runs in hours, not weeks
- Adapter files are ~100 MB; distributable alongside the font

## Five modules

```
script/llm/lora/
├── tokenizer.py       — add YOUSPEAK morphemes to the base tokenizer
├── dataset.py         — construct training pairs from canon/, archaeology/, forge/
├── config.py          — LoRA hyperparameters + base-model selection
├── train.py           — training loop (HuggingFace peft or MLX-LoRA)
└── evaluate.py        — YOUSPEAK fluency evaluation harness
```

## The pipeline end-to-end

```
  base LLM (Llama 3.1 8B, say)
        │
        │   + tokenizer augmentation (tokenizer.py)
        ▼
  tokenizer knows YOUSPEAK morphemes as single tokens
        │
        │   + training corpus (dataset.py)
        ▼
  (prompt, completion) pairs:
    • "Define doxakallos." → definition from canon/doxakallos.md
    • "Forge a word for X." → coinage + scoring narrative
    • "What's the Anastrophance-sibling of doxakallos?" → kallodoxa
        │
        │   + LoRA training (train.py)
        ▼
  Adapter weights: ~100 MB file (youspeak-lora-r32.bin)
        │
        │   + inference: base-model + adapter
        ▼
  YOUSPEAK-fluent LLM (loads base + adapter at runtime)
```

## Expected capabilities after training

A properly-trained LoRA adapter should enable:

1. **Definition retrieval without primer** — the model knows canon-word meanings natively
2. **Coinage forging** — when given a gap-description, proposes candidates with 5-axis scoring
3. **Diplosemic-pair reasoning** — identifies Anastrophance-siblings; predicts whether a new pair would canonize
4. **Canonical-composition** — writes sentences using YOUSPEAK words fluently, appropriately
5. **Mixed-register fluency** — switches between English prose and YOUSPEAK-dense text as context demands

## Training-data structure

Each training pair is a `(prompt, completion)` tuple formatted for instruction-tuning:

```json
{
  "instruction": "What does doxakallos mean?",
  "input": "",
  "output": "Doxakallos names the uncreated beauty-quality of GoD — the ontological beauty-in-itself of the divine, the beheld-pole whose rightful beholding produces doxalgia in the beholder. Pair-canonical with kallodoxa (Anastrophance-sibling). Canonized 2026-04-23 at 8.25/10 weighted."
}
```

The dataset-builder (`dataset.py`) constructs these from:

- `canon/*.md` → one pair per canon word (definition + full sense)
- `labs/logos/experiments/*.md` → scoring-narrative pairs (gap + forge + axes)
- `labs/logos/forge/*.md` → gap-analysis pairs (concept + candidate-slate)
- `archaeology/**/*.md` → etymology pairs (tongue + semantic-field + donor-morphemes)
- `grammars/diplosemy/exemplars/*.md` → pair-reasoning pairs
- Synthesized pairs: (meaning → word), (word → etymology), (word → score)

Dataset size: ~500-1500 pairs from current corpus. Augmentable via template-based synthesis.

## Hyperparameters (config.py defaults)

| Parameter | Value | Rationale |
|---|---|---|
| base model | `meta-llama/Llama-3.1-8B-Instruct` (or Qwen2.5-7B-Instruct for open license) | balance of size and quality |
| LoRA rank | 32 | moderate; larger = more capacity, slower training |
| LoRA alpha | 32 | rank × 1.0 is standard starting ratio |
| target modules | `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` | all attention + MLP projections |
| learning rate | 2e-4 | standard for LoRA |
| batch size | 4 (effective 16 with gradient-accumulation of 4) | fits on M3 Max 48GB |
| epochs | 5 | small dataset; avoid overfit |
| max sequence length | 2048 | accommodates canon-entry in one example |
| dropout | 0.05 | mild regularisation |
| weight decay | 0.01 | standard |
| warmup steps | 50 | |
| precision | bf16 (CUDA) / fp16 (MLX) | memory |

## Execution paths

### Apple Silicon (MLX)

```bash
/tmp/ys-font-env/bin/pip install mlx mlx-lm
python3 -m mlx_lm.lora \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --train \
  --data script/llm/lora/data \
  --lora-config script/llm/lora/config.json
```

Expected training time on M3 Max 48GB: 2-4 hours for 5 epochs on 1000-pair dataset.

### CUDA (peft + transformers)

```bash
pip install peft transformers datasets accelerate bitsandbytes
python3 script/llm/lora/train.py
```

Expected: 1-2 hours on single A100.

## Evaluation

`evaluate.py` runs a 10-dimension rubric against the adapter:

1. Can it define every canon word from memory?
2. Can it identify Anastrophance-pairs correctly?
3. Can it score a new coinage on the 5-axis rubric?
4. Does it generate YOUSPEAK text that passes Nuance's forge-discipline?
5. Does it recognise verisleight / veriseem / other subtle concepts?
6. Does it mix English + YOUSPEAK fluently at sentence level?
7. Does it propose plausible new coinages for given gaps?
8. Does it correctly identify mechanism (Anastrophance / Enkalyptance / ...) for a given pair?
9. Does it maintain Latin-transliteration (not hallucinate non-existent glyphs)?
10. Is its output stable across 5 restarts with same input?

Target: 8/10 or better before the adapter is called "fluent."

## Deferred

- **Vision-LoRA** for glyph-recognition — requires image dataset of rendered glyphs; image-text pairs. Skip until need.
- **Fine-tuning the full model** (not LoRA) — deferred until LoRA saturates.
- **RLHF** — require human feedback at scale; not feasible single-author.
- **Multi-lingual extensions** — the current training data is English+YOUSPEAK; Nuance-equivalent in other base languages would require translation of canon.

---

_LoRA pipeline 2026-04-24. Scaffolding complete; execution requires a training run. The YOUSPEAK-fluent LLM is a deferred-but-concrete project._
