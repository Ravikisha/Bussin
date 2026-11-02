"""Export a Bussin checkpoint as a standard Llama checkpoint for Hugging Face.

The architecture is Llama (RMSNorm, SwiGLU, RoPE with rotate_half, GQA, tied
embeddings, no biases), so the weights only need renaming. The export is then
checked against the original model: the same token ids must give the same logits,
otherwise nothing is written to the output as "done".

Run:
  python scripts/export_hf.py --ckpt eval_run/final-4067 --out hf_export
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
import yaml
from safetensors.torch import load_file, save_file

from bussin.model.bussin_model import BussinForCausalLM
from bussin.model.config import BussinConfig
from bussin.relay.checkpoint import load_checkpoint

EOS, PAD = 0, 1


def rename(key: str) -> str | None:
    if key == "embed.weight":
        return "model.embed_tokens.weight"
    if key == "norm.weight":
        return "model.norm.weight"
    if key == "lm_head.weight":
        return None                                  # tied to the embedding
    _, n, rest = key.split(".", 2)
    table = {
        "attn.wq.weight": "self_attn.q_proj.weight",
        "attn.wk.weight": "self_attn.k_proj.weight",
        "attn.wv.weight": "self_attn.v_proj.weight",
        "attn.wo.weight": "self_attn.o_proj.weight",
        "attn_norm.weight": "input_layernorm.weight",
        "ffn_norm.weight": "post_attention_layernorm.weight",
        "ffn.w_gate.weight": "mlp.gate_proj.weight",
        "ffn.w_up.weight": "mlp.up_proj.weight",
        "ffn.w_down.weight": "mlp.down_proj.weight",
    }
    return f"model.layers.{n}.{table[rest]}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--config", default="configs/125m-realign.yaml")
    ap.add_argument("--tokenizer", default="tokenizer/tokenizer.json")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    raw = yaml.safe_load(open(args.config, encoding="utf-8"))
    cfg = BussinConfig.from_dict(raw["model"])
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    src = load_file(str(Path(args.ckpt) / "model.safetensors"))
    dst = {}
    for k, v in src.items():
        nk = rename(k)
        if nk is not None:
            dst[nk] = v.contiguous().to(torch.float32)
    save_file(dst, str(out / "model.safetensors"), metadata={"format": "pt"})

    config = {
        "architectures": ["LlamaForCausalLM"],
        "model_type": "llama",
        "vocab_size": cfg.vocab_size,
        "hidden_size": cfg.d_model,
        "intermediate_size": cfg.ffn_dim,
        "num_hidden_layers": cfg.n_layers,
        "num_attention_heads": cfg.n_heads,
        "num_key_value_heads": cfg.n_kv_heads,
        "head_dim": cfg.head_dim,
        "max_position_embeddings": cfg.max_seq_len,
        "rms_norm_eps": cfg.norm_eps,
        "rope_theta": cfg.rope_theta,
        "tie_word_embeddings": True,
        "attention_bias": False,
        "mlp_bias": False,
        "hidden_act": "silu",
        "bos_token_id": EOS,
        "eos_token_id": EOS,
        "pad_token_id": PAD,
        "torch_dtype": "float32",
    }
    (out / "config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    (out / "generation_config.json").write_text(json.dumps(
        {"bos_token_id": EOS, "eos_token_id": EOS, "pad_token_id": PAD,
         "do_sample": True, "temperature": 0.8, "top_k": 50, "top_p": 0.95}, indent=2),
        encoding="utf-8")
    shutil.copy(args.tokenizer, out / "tokenizer.json")
    (out / "tokenizer_config.json").write_text(json.dumps(
        {"tokenizer_class": "PreTrainedTokenizerFast", "eos_token": "<|endoftext|>",
         "bos_token": "<|endoftext|>", "pad_token": "<|pad|>", "clean_up_tokenization_spaces": False,
         "model_max_length": cfg.max_seq_len,
         "model_input_names": ["input_ids", "attention_mask"]}, indent=2), encoding="utf-8")
    (out / "special_tokens_map.json").write_text(json.dumps(
        {"eos_token": "<|endoftext|>", "bos_token": "<|endoftext|>", "pad_token": "<|pad|>"},
        indent=2), encoding="utf-8")

    # ---- parity: same ids, same logits ---------------------------------
    from transformers import LlamaForCausalLM

    orig = BussinForCausalLM(cfg)
    load_checkpoint(Path(args.ckpt), orig, strict_verify=False)
    orig.eval()
    hf = LlamaForCausalLM.from_pretrained(str(out), torch_dtype=torch.float32).eval()
    g = torch.Generator().manual_seed(0)
    ids = torch.randint(0, cfg.vocab_size, (3, 96), generator=g)
    with torch.inference_mode():
        a = orig(ids)["logits"]
        b = hf(ids).logits
    diff = (a - b).abs().max().item()
    agree = (a.argmax(-1) == b.argmax(-1)).float().mean().item()
    print(f"max |logit diff| {diff:.2e}   argmax agreement {agree:.4f}")
    if diff > 1e-3 or agree < 0.999:
        print("PARITY FAILED: export is not equivalent to the original model")
        return 3
    print("PARITY OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
