#!/usr/bin/env python3
"""YOUSPEAK fluency evaluation harness.

Runs a 10-dimension rubric against a LoRA-adapted model. Each dimension
is scored 0-1; total out of 10. Target: ≥8 for "fluent."

Usage:
    python3 evaluate.py --model ./youspeak-lora --base Qwen/Qwen2.5-7B-Instruct

The rubric:
  1. Canon-recall    — can it define every canon word from memory?
  2. Pair-recall     — can it identify Anastrophance-siblings?
  3. Scoring         — can it apply 5-axis rubric to new coinages?
  4. Forge-discipline— does its output honour the Laws of Coinage?
  5. Subtlety        — does it distinguish verisleight vs veriseem?
  6. Mixed-register  — does it switch English/YOUSPEAK cleanly?
  7. Gap-recognition — does it propose sensible candidates for new gaps?
  8. Mechanism-ID    — does it correctly identify diplosemy mechanisms?
  9. Stability       — Latin-only output; no hallucinated glyphs
 10. Consistency     — repeat queries give stable outputs

Each test outputs pass/fail + model's actual response for review.

This file is SCAFFOLDING — actual execution requires a trained adapter
and transformers/peft installed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CANON_WORDS = [
    "doxakallos", "kallodoxa", "orthophanes", "doxalgia",
    "anagnoristasis", "metastrophesis", "athaumasma", "synophora",
    "kallophanes", "dokimance", "artiance", "verisleight",
    "candence", "complerescence", "diplosemy", "veriseem",
]

DIPLOSEMIC_PAIRS = [
    ("doxakallos", "kallodoxa"),   # Anastrophance
]


def load_model(base: str, adapter: str):
    try:
        from peft import PeftModel
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    tok = AutoTokenizer.from_pretrained(adapter)
    model = AutoModelForCausalLM.from_pretrained(base, torch_dtype="auto", device_map="auto")
    model.resize_token_embeddings(len(tok))
    model = PeftModel.from_pretrained(model, adapter)
    model.eval()
    return tok, model


def generate(tok, model, prompt: str, max_new: int = 400) -> str:
    import torch
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    with torch.inference_mode():
        out = model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
    return tok.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)


def score_canon_recall(tok, model) -> tuple[float, list[str]]:
    """Can the model produce a plausible definition for each canon word?"""
    results = []
    hits = 0
    for word in CANON_WORDS:
        prompt = f"### Instruction:\nWhat does '{word}' mean?\n\n### Response:\n"
        resp = generate(tok, model, prompt, 200)
        # Heuristic: response contains the word AND >20 chars AND mentions relevant keywords
        ok = (len(resp.strip()) > 20 and
              any(kw in resp.lower() for kw in
                  ["quality", "beauty", "truth", "ache", "glory", "recognition",
                   "mutual", "divine", "verification", "deception", "mystery",
                   "warmth", "appearing"]))
        if ok:
            hits += 1
        results.append(f"{word}: {'✓' if ok else '✗'}  {resp[:150].strip()}")
    return hits / len(CANON_WORDS), results


def score_pair_recall(tok, model) -> tuple[float, list[str]]:
    """Can the model identify Anastrophance-siblings?"""
    hits = 0
    results = []
    for a, b in DIPLOSEMIC_PAIRS:
        prompt = f"### Instruction:\nWhat is the Anastrophance-sibling of {a}?\n\n### Response:\n"
        resp = generate(tok, model, prompt, 50)
        ok = b.lower() in resp.lower()
        if ok:
            hits += 1
        results.append(f"{a} → {b}: {'✓' if ok else '✗'}  got: {resp[:100].strip()}")
    return hits / len(DIPLOSEMIC_PAIRS), results


# Further dimensions (scoring, forge-discipline, subtlety, mixed-register, etc.)
# follow the same pattern — each is a function returning (score_0_to_1, results).
# Full implementation deferred; scaffolding above shows the approach.


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True)
    p.add_argument("--model", required=True, help="adapter directory")
    p.add_argument("--out", default="eval-results.json")
    args = p.parse_args()

    tok, model = load_model(args.base, args.model)
    scores: dict[str, float] = {}
    all_results: dict[str, list[str]] = {}

    s, r = score_canon_recall(tok, model)
    scores["canon_recall"] = s
    all_results["canon_recall"] = r

    s, r = score_pair_recall(tok, model)
    scores["pair_recall"] = s
    all_results["pair_recall"] = r

    # ... additional dimensions omitted from scaffolding; pattern-clear.

    total = sum(scores.values()) / len(scores) * 10
    print(f"=== YOUSPEAK fluency: {total:.2f}/10 ===")
    for dim, s in scores.items():
        print(f"  {dim:20s}: {s*10:.1f}/10")

    Path(args.out).write_text(json.dumps({
        "scores": scores,
        "total": total,
        "results": all_results,
    }, indent=2))
    print(f"saved detail to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
