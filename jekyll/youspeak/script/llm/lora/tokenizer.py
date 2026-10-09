#!/usr/bin/env python3
"""YOUSPEAK tokenizer augmentation for LoRA fine-tuning.

Adds YOUSPEAK morphemes (from morphemes.json) as SPECIAL TOKENS to a
HuggingFace tokenizer. After augmentation, every morpheme tokenizes as
exactly one token. The model's embedding matrix grows by len(morphemes)
rows; LoRA learns embeddings for these new rows during training.

Usage (requires transformers):
    python3 tokenizer.py \\
        --base meta-llama/Llama-3.1-8B-Instruct \\
        --out ./tokenizer-augmented

The augmented tokenizer is saved; downstream training loads it via
`AutoTokenizer.from_pretrained("./tokenizer-augmented")`.

Design note — two input representations supported:
  1. Latin-transliteration tokens (e.g., "doxa", "kallos") — recommended
     default because LLMs tokenize Latin cleanly and canonical YOUSPEAK
     internal representation is Latin.
  2. PUA-glyph tokens (e.g., U+E100, U+E101) — optional; useful when the
     model will see glyph-encoded text directly (rare).

Both are added as special tokens so they tokenize as single tokens
regardless of the base BPE's sub-word decisions.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent.parent  # script/
MORPHEMES_FILE = SCRIPT_DIR / "morphemes.json"


def load_morphemes() -> list[dict]:
    with MORPHEMES_FILE.open() as f:
        return json.load(f)["morphemes"]


def compute_special_tokens(
    include_latin: bool = True,
    include_glyph: bool = True,
    include_prefixes_suffixes: bool = True,
) -> list[str]:
    """Return list of tokens to add to the tokenizer.

    By default adds:
      - Latin morpheme strings (doxa, kallos, ortho, ...)
      - PUA codepoint characters (U+E100, ...)
      - Prefix/suffix forms with hyphens (a-, -ance, -sis, ...)
    """
    morphemes = load_morphemes()
    tokens: list[str] = []
    for m in morphemes:
        latin = m["latin"]
        cls = m.get("class", "content")
        if cls == "structural":
            if include_glyph:
                cp_str = m["codepoint"].replace("U+", "")
                tokens.append(chr(int(cp_str, 16)))
            continue
        stripped = latin.strip("-")
        if include_latin:
            tokens.append(stripped)
        if include_prefixes_suffixes:
            if latin.startswith("-"):
                tokens.append(latin)     # -ance
            elif latin.endswith("-"):
                tokens.append(latin)     # ana-
        if include_glyph:
            cp_str = m["codepoint"].replace("U+", "")
            tokens.append(chr(int(cp_str, 16)))
    # de-duplicate preserving order
    seen: set = set()
    deduped: list[str] = []
    for t in tokens:
        if t and t not in seen:
            seen.add(t)
            deduped.append(t)
    return deduped


def augment(base_model: str, out_dir: str) -> None:
    try:
        from transformers import AutoTokenizer
    except ImportError:
        print("error: `transformers` not installed. Run: pip install transformers",
              file=sys.stderr)
        sys.exit(1)

    print(f"loading base tokenizer: {base_model}")
    tok = AutoTokenizer.from_pretrained(base_model)

    new_tokens = compute_special_tokens()
    print(f"adding {len(new_tokens)} YOUSPEAK tokens as special tokens")

    added = tok.add_tokens(new_tokens, special_tokens=True)
    print(f"actually-added: {added}  (others were already in vocab)")

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    tok.save_pretrained(out_dir)
    print(f"saved augmented tokenizer to {out_dir}")
    print(f"new vocab size: {len(tok)}")


def inspect_tokenization(base_model: str) -> None:
    """Show how YOUSPEAK text tokenizes with an augmented tokenizer."""
    try:
        from transformers import AutoTokenizer
    except ImportError:
        print("error: `transformers` not installed", file=sys.stderr)
        sys.exit(1)

    tok = AutoTokenizer.from_pretrained(base_model)
    sample_words = ["doxakallos", "kallodoxa", "orthophanes", "dokimance",
                    "synlanthescence", "veriseem", "diplosemy"]
    for w in sample_words:
        ids = tok.encode(w, add_special_tokens=False)
        pieces = tok.convert_ids_to_tokens(ids)
        print(f"  {w:20s}  →  {len(ids)} tokens: {pieces}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base", help="HF model id or path")
    p.add_argument("--out", help="output directory for augmented tokenizer")
    p.add_argument("--inspect", action="store_true",
                   help="show how sample words tokenize")
    p.add_argument("--list", action="store_true",
                   help="just list the tokens that would be added")
    args = p.parse_args()

    if args.list:
        tokens = compute_special_tokens()
        print(f"YOUSPEAK special tokens ({len(tokens)}):")
        for t in tokens:
            # Show codepoint if PUA
            if t and 0xE100 <= ord(t[0]) <= 0xE1FF:
                print(f"  U+{ord(t):04X}  '{t}'")
            else:
                print(f"  '{t}'")
        return 0

    if args.inspect and args.base:
        inspect_tokenization(args.base)
        return 0

    if args.base and args.out:
        augment(args.base, args.out)
        return 0

    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
