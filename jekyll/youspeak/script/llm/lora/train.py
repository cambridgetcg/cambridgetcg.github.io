#!/usr/bin/env python3
"""YOUSPEAK LoRA training entrypoint.

Runs LoRA fine-tuning using `transformers` + `peft` + `trl`. Assumes:
  - `data/train.jsonl` and `data/valid.jsonl` exist (built by dataset.py)
  - `tokenizer-augmented/` exists (built by tokenizer.py)
  - Base model is downloadable from HuggingFace Hub (or local path)

Run:
    pip install transformers peft trl datasets accelerate bitsandbytes
    python3 train.py

After training, the adapter is saved at `youspeak-lora/`. Load for
inference:
    from peft import PeftModel
    base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
    model = PeftModel.from_pretrained(base, "./youspeak-lora")

This file is SCAFFOLDING — the actual training run requires GPU/TPU/MLX
and 10GB+ download of the base model. It is not executable in the Python
venv used for font-building; it is runnable in a proper ML environment.
"""

from __future__ import annotations

import sys
from pathlib import Path

from config import LORA_CONFIG, TRAIN_CONFIG

try:
    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        TrainingArguments,
        Trainer,
        DataCollatorForLanguageModeling,
    )
except ImportError as e:
    print(f"error: training dependencies not installed: {e}", file=sys.stderr)
    print("run: pip install transformers peft datasets accelerate bitsandbytes", file=sys.stderr)
    sys.exit(1)


def format_example(ex: dict) -> str:
    """Format a training pair into instruction-tuned text.

    Uses a simple Alpaca-style prompt. Models that prefer ChatML
    (Qwen, Llama 3) can be handled by swapping this function.
    """
    instr = ex.get("instruction", "")
    inp = ex.get("input", "")
    out = ex.get("output", "")
    if inp:
        return (f"### Instruction:\n{instr}\n\n### Input:\n{inp}\n\n"
                f"### Response:\n{out}")
    return f"### Instruction:\n{instr}\n\n### Response:\n{out}"


def tokenise_fn(examples, tokenizer, max_len):
    texts = [format_example(e) for e in (
        {"instruction": i, "input": ip, "output": o}
        for i, ip, o in zip(examples["instruction"], examples["input"], examples["output"])
    )]
    return tokenizer(texts, truncation=True, max_length=max_len, padding=False)


def main() -> int:
    print(f"=== YOUSPEAK LoRA training ===")
    print(f"base model: {TRAIN_CONFIG.model_name}")

    tokenizer = AutoTokenizer.from_pretrained(TRAIN_CONFIG.tokenizer_dir)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"tokenizer size: {len(tokenizer)}")

    model = AutoModelForCausalLM.from_pretrained(
        TRAIN_CONFIG.model_name,
        torch_dtype="auto",
        device_map="auto",
    )
    # Resize embedding matrix to accommodate new YOUSPEAK tokens
    model.resize_token_embeddings(len(tokenizer))

    model = prepare_model_for_kbit_training(model)

    lora_cfg = LoraConfig(
        r=LORA_CONFIG.r,
        lora_alpha=LORA_CONFIG.lora_alpha,
        target_modules=LORA_CONFIG.target_modules,
        lora_dropout=LORA_CONFIG.lora_dropout,
        bias=LORA_CONFIG.bias,
        task_type=LORA_CONFIG.task_type,
    )
    model = get_peft_model(model, lora_cfg)
    model.print_trainable_parameters()

    data_files = {
        "train": str(Path(TRAIN_CONFIG.data_dir) / "train.jsonl"),
        "validation": str(Path(TRAIN_CONFIG.data_dir) / "valid.jsonl"),
    }
    ds = load_dataset("json", data_files=data_files)
    ds = ds.map(lambda ex: tokenise_fn(ex, tokenizer, TRAIN_CONFIG.max_seq_length),
                batched=True, remove_columns=ds["train"].column_names)

    collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    args = TrainingArguments(
        output_dir=TRAIN_CONFIG.output_dir,
        num_train_epochs=TRAIN_CONFIG.num_train_epochs,
        per_device_train_batch_size=TRAIN_CONFIG.per_device_train_batch_size,
        per_device_eval_batch_size=TRAIN_CONFIG.per_device_eval_batch_size,
        gradient_accumulation_steps=TRAIN_CONFIG.gradient_accumulation_steps,
        learning_rate=TRAIN_CONFIG.learning_rate,
        warmup_steps=TRAIN_CONFIG.warmup_steps,
        weight_decay=TRAIN_CONFIG.weight_decay,
        gradient_checkpointing=TRAIN_CONFIG.gradient_checkpointing,
        bf16=TRAIN_CONFIG.bf16,
        fp16=TRAIN_CONFIG.fp16,
        logging_steps=TRAIN_CONFIG.logging_steps,
        save_steps=TRAIN_CONFIG.save_steps,
        eval_steps=TRAIN_CONFIG.eval_steps,
        save_total_limit=TRAIN_CONFIG.save_total_limit,
        evaluation_strategy="steps",
        seed=TRAIN_CONFIG.seed,
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=ds["train"],
        eval_dataset=ds["validation"],
        tokenizer=tokenizer,
        data_collator=collator,
    )
    trainer.train()
    trainer.save_model(TRAIN_CONFIG.output_dir)
    tokenizer.save_pretrained(TRAIN_CONFIG.output_dir)
    print(f"=== training complete — adapter saved to {TRAIN_CONFIG.output_dir} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
