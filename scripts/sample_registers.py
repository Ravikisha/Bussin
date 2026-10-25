"""Look at what the model actually writes under different registers.

Nobody had read a single sample from bussin-125m. Numbers (loss, likelihood
tests) say a model fits held-out text; they do not say whether it writes
anything readable, or whether the register tokens change what it writes. This
prints real samples for a handful of requested registers, and beside each one the
register the annotator MEASURES in the output, so a mismatch is visible.

This is a qualitative first look and the seed of the quantitative RCE test:
samples are few, drawn at one temperature, and printed with the seed so they can
be reproduced. Read them as evidence of behaviour, not as a score.

Run:
  python scripts/sample_registers.py --ckpt eval_run/final-4067
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch
import yaml
from tokenizers import Tokenizer

from bussin.data.lexicon import Lexicon
from bussin.data.register import Register, RegisterAnnotator
from bussin.model.bussin_model import BussinForCausalLM
from bussin.model.config import BussinConfig
from bussin.relay.checkpoint import load_checkpoint

EOS = 0

# name -> requested register. `formal` runs 0 (chat) .. 3 (edited prose).
CONDITIONS: dict[str, Register | None] = {
    "plain prose (slang 0, formal 3)": Register(slang=0, emoji=0, abbrev=0, elong=0, formal=3),
    "casual chat (slang 1, abbrev 2)": Register(slang=1, emoji=0, abbrev=2, elong=0, formal=0),
    "slangy (slang 3, emoji 1, abbrev 2)": Register(slang=3, emoji=1, abbrev=2, elong=0, formal=0),
    "very slangy (slang 4, emoji 2, abbrev 3, elong 1)": Register(slang=4, emoji=2, abbrev=3, elong=1, formal=0),
    "no register prefix (control)": None,
}


def short(r: Register) -> str:
    return f"slang {r.slang} emoji {r.emoji} abbrev {r.abbrev} elong {r.elong} formal {r.formal}"


@torch.inference_mode()
def sample(model, tok, reg: Register | None, n: int, new_tokens: int,
           temperature: float, top_k: int, top_p: float) -> list[str]:
    prefix = tok.encode(reg.to_tokens()).ids if reg is not None else []
    prompt = torch.tensor([[EOS] + prefix] * n, dtype=torch.long)
    out = model.generate(prompt, max_new_tokens=new_tokens, temperature=temperature,
                         top_k=top_k, top_p=top_p, eos_token_id=None)
    texts = []
    for row in out[:, prompt.size(1):].tolist():
        if EOS in row:                      # a document ended; keep only its own text
            row = row[: row.index(EOS)]
        texts.append(tok.decode(row, skip_special_tokens=False))
    return texts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--config", default="configs/125m-realign.yaml")
    ap.add_argument("--tokenizer", default="tokenizer/tokenizer.json")
    ap.add_argument("--lexicon", default="data/lexicon/lexicon.jsonl")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--tokens", type=int, default=60)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--top-k", type=int, default=50)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    raw = yaml.safe_load(open(args.config, encoding="utf-8"))
    model = BussinForCausalLM(BussinConfig.from_dict(raw["model"]))
    load_checkpoint(Path(args.ckpt), model, strict_verify=False)
    model.eval()
    tok = Tokenizer.from_file(args.tokenizer)
    ann = RegisterAnnotator(Lexicon.load(args.lexicon))

    print(f"checkpoint {args.ckpt}   seed {args.seed}   temperature {args.temperature}   "
          f"top_k {args.top_k}   top_p {args.top_p}   {args.tokens} new tokens\n")

    summary = []
    for name, reg in CONDITIONS.items():
        torch.manual_seed(args.seed)
        texts = sample(model, tok, reg, args.n, args.tokens,
                       args.temperature, args.top_k, args.top_p)
        print("=" * 78)
        print(f"REQUESTED  {name}" + (f"   [{short(reg)}]" if reg else ""))
        print("=" * 78)
        dens, got = [], []
        for i, t in enumerate(texts, 1):
            clean = " ".join(t.split())
            feats = ann.features(t)
            got_reg = ann.annotate(t)
            dens.append(feats.slang_density)
            got.append(got_reg)
            print(f"[{i}] {clean[:420]}")
            print(f"     measured: {short(got_reg)}   (slang density {feats.slang_density:.1f}/100 tok)\n")
        summary.append((name, reg, sum(dens) / len(dens), got))

    print("=" * 78)
    print("SUMMARY: requested vs mean measured (n=%d per condition)" % args.n)
    print("=" * 78)
    for name, reg, d, got in summary:
        req = f"slang {reg.slang}" if reg else "none"
        m_slang = sum(g.slang for g in got) / len(got)
        m_emoji = sum(g.emoji for g in got) / len(got)
        m_form = sum(g.formal for g in got) / len(got)
        print(f"  {name[:48]:<48} req {req:<8} -> slang {m_slang:.2f}  emoji {m_emoji:.2f}  "
              f"formal {m_form:.2f}  density {d:.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
