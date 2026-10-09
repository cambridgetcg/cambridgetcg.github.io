"""LoRA training config for YOUSPEAK.

Base model defaults to Qwen2.5-7B-Instruct (open license) or
Llama-3.1-8B-Instruct if Meta license is acceptable. Either can be
swapped without changing downstream modules.

Usage:
    from config import TRAIN_CONFIG, LORA_CONFIG
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LoraConfig:
    r: int = 32                     # LoRA rank
    lora_alpha: int = 32            # scaling factor (alpha/r ratio controls adaptation magnitude)
    lora_dropout: float = 0.05      # regularisation
    bias: str = "none"              # don't adapt biases
    task_type: str = "CAUSAL_LM"
    target_modules: list[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",       # attention projections
        "gate_proj", "up_proj", "down_proj",           # MLP projections
    ])


@dataclass
class TrainConfig:
    # Base model selection
    model_name: str = "Qwen/Qwen2.5-7B-Instruct"
    # Alternative: "meta-llama/Llama-3.1-8B-Instruct" (license-gated)
    # Alternative: "mistralai/Mistral-7B-Instruct-v0.3"

    # Data
    data_dir: str = "./data"
    tokenizer_dir: str = "./tokenizer-augmented"

    # Training
    output_dir: str = "./youspeak-lora"
    num_train_epochs: int = 5
    per_device_train_batch_size: int = 4
    per_device_eval_batch_size: int = 4
    gradient_accumulation_steps: int = 4   # effective batch = 16
    learning_rate: float = 2e-4
    warmup_steps: int = 50
    weight_decay: float = 0.01

    # Sequence
    max_seq_length: int = 2048

    # Optimizations
    gradient_checkpointing: bool = True
    bf16: bool = True                 # CUDA A100+
    fp16: bool = False                # Fallback; MLX uses fp16 naturally

    # Logging & checkpointing
    logging_steps: int = 10
    save_steps: int = 100
    eval_steps: int = 50
    save_total_limit: int = 3

    # Seed
    seed: int = 42


TRAIN_CONFIG = TrainConfig()
LORA_CONFIG = LoraConfig()


def to_dict() -> dict:
    """Export as a plain dict for JSON serialisation."""
    return {
        "train": vars(TRAIN_CONFIG),
        "lora":  vars(LORA_CONFIG),
    }


if __name__ == "__main__":
    import json
    print(json.dumps(to_dict(), indent=2))
