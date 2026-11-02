"""Register Calibration Error (RCE): does the model write the register it is asked for?

Requests come from real text. For each held-out document, the first 48 tokens are
measured by the annotator; that measured register is the REQUEST. The model gets
only the register prefix and writes 48 tokens; the annotator measures those too.

Three numbers per dimension, all mean absolute error on the 0..k scale:
  model   |measured(generated) - request|
  null    the same generations scored against another document's request (shuffled);
          this is what "ignores the prefix" looks like
  floor   |measured(doc tokens 48..96) - request|; the next real 48 tokens of the
          SAME document, so it is the error a perfect writer would still show
          because the annotator is noisy on short text

Model beats null  -> the prefix steers output. Model near floor -> it does so about
as well as real text of that register. Also a single-dimension sweep (all else 0).

The annotator is deterministic code, not human judgement (B1 rho = 0.48), so this
measures agreement with the annotator, the same instrument the prefixes were made
with. Samples use distinct seeds per batch.

Run:
  python scripts/rce_test.py --ckpt eval_run/final-4067 --n 200
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import torch
import yaml
from tokenizers import Tokenizer

from bussin.data.lexicon import Lexicon
from bussin.data.register import Register, RegisterAnnotator
from bussin.model.bussin_model import BussinForCausalLM
from bussin.model.config import BussinConfig
from bussin.relay.checkpoint import load_checkpoint

EOS = 0
DIMS = ["slang", "emoji", "abbrev", "elong", "formal"]
SNIP = 48
# Finished batches are appended here, so a run killed for memory resumes where it
# stopped instead of regenerating everything. Keyed by everything that shapes a batch.
CACHE: dict[str, list[str]] = {}
CACHE_PATH: Path | None = None
CACHE_TAG = ""


def cache_load(path: Path) -> None:
    global CACHE_PATH
    CACHE_PATH = path
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
            except json.JSONDecodeError:      # last line cut off by a kill
                continue
            CACHE[row["key"]] = row["texts"]
        print(f"resumed {len(CACHE)} cached batches from {path}", flush=True)


def load_docs(val_dir: Path, per_file: int, rng: random.Random) -> list[str]:
    docs: list[str] = []
    for name in ("corpus_genz-part-00.jsonl.gz", "corpus-part-00.jsonl.gz"):
        rows = [json.loads(l)["text"] for l in gzip.open(val_dir / name, "rt", encoding="utf-8")]
        rng.shuffle(rows)
        docs += rows[:per_file]
    return docs


@torch.inference_mode()
def generate(model, tok, regs: list[Register], batch: int, seed: int,
             temperature: float, top_k: int, top_p: float) -> list[str]:
    out_texts: list[str] = []
    for b in range(0, len(regs), batch):
        chunk = regs[b:b + batch]
        key = hashlib.sha1(("|".join([CACHE_TAG, str(seed + b), str(temperature), str(top_k),
                                      str(top_p)] + [r.to_tokens() for r in chunk])
                            ).encode("utf-8")).hexdigest()
        if key in CACHE:
            out_texts += CACHE[key]
            print(f"  cached {min(b + batch, len(regs))}/{len(regs)}", flush=True)
            continue
        torch.manual_seed(seed + b)
        prompt = torch.tensor([[EOS] + tok.encode(r.to_tokens()).ids for r in chunk])
        out = model.generate(prompt, max_new_tokens=SNIP, temperature=temperature,
                             top_k=top_k, top_p=top_p, eos_token_id=None)
        got = []
        for row in out[:, prompt.size(1):].tolist():
            if EOS in row:
                row = row[: row.index(EOS)]
            got.append(tok.decode(row, skip_special_tokens=False))
        out_texts += got
        CACHE[key] = got
        if CACHE_PATH is not None:
            with open(CACHE_PATH, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"key": key, "texts": got}) + "\n")
        print(f"  generated {min(b + batch, len(regs))}/{len(regs)}", flush=True)
    return out_texts


def vec(r: Register) -> np.ndarray:
    return np.array([getattr(r, d) for d in DIMS], dtype=float)


def ranks(x: np.ndarray) -> np.ndarray:
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    r[order] = np.arange(len(x))
    for v in np.unique(x):                      # average ranks over ties
        m = x == v
        r[m] = r[m].mean()
    return r


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    if a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(ranks(a), ranks(b))[0, 1])


def boot(fn, n: int, reps: int, rng: np.random.Generator) -> tuple[float, float]:
    vals = [fn(rng.integers(0, n, n)) for _ in range(reps)]
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--config", default="configs/125m-realign.yaml")
    ap.add_argument("--tokenizer", default="tokenizer/tokenizer.json")
    ap.add_argument("--lexicon", default="data/lexicon/lexicon.jsonl")
    ap.add_argument("--val-dir", default="eval_run/val")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--sweep-n", type=int, default=100)
    ap.add_argument("--batch", type=int, default=50)
    ap.add_argument("--temperature", type=float, default=0.8)
    ap.add_argument("--top-k", type=int, default=50)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--out", default="")
    ap.add_argument("--cache", default="eval_run/rce_cache.jsonl")
    args = ap.parse_args()

    rng = random.Random(0)
    nprng = np.random.default_rng(0)
    raw = yaml.safe_load(open(args.config, encoding="utf-8"))
    model = BussinForCausalLM(BussinConfig.from_dict(raw["model"]))
    load_checkpoint(Path(args.ckpt), model, strict_verify=False)
    model.eval()
    tok = Tokenizer.from_file(args.tokenizer)
    ann = RegisterAnnotator(Lexicon.load(args.lexicon))
    global CACHE_TAG
    CACHE_TAG = f"{args.ckpt}|{args.batch}"
    cache_load(Path(args.cache))

    # documents with two full snippets: one to request from, one for the noise floor
    cand = load_docs(Path(args.val_dir), 5000, rng)
    reqs, floors = [], []
    for t in cand:
        ids = tok.encode(t).ids
        if len(ids) < 2 * SNIP:
            continue
        reqs.append(ann.annotate(tok.decode(ids[:SNIP], skip_special_tokens=False)))
        floors.append(ann.annotate(tok.decode(ids[SNIP:2 * SNIP], skip_special_tokens=False)))
    # Random docs are almost all slang 0 / formal 2, which cannot test calibration.
    # Round-robin over (slang, has-emoji) buckets so every level is requested.
    buckets: dict[tuple[int, bool], list[int]] = {}
    for i, r in enumerate(reqs):
        buckets.setdefault((int(r.slang), r.emoji > 0), []).append(i)
    for b in buckets.values():
        rng.shuffle(b)
    idx = []
    while len(idx) < args.n and any(buckets.values()):
        for key in sorted(buckets):
            if buckets[key] and len(idx) < args.n:
                idx.append(buckets[key].pop())
    print("bucket sizes available (slang, emoji>0):",
          {k: len(v) + sum(1 for i in idx if (int(reqs[i].slang), reqs[i].emoji > 0) == k)
           for k, v in sorted(buckets.items())}, flush=True)
    reqs = [reqs[i] for i in idx]
    floors = [floors[i] for i in idx]
    n = len(reqs)
    R = np.stack([vec(r) for r in reqs])
    F = np.stack([vec(r) for r in floors])
    print(f"checkpoint {args.ckpt}; {n} requests from held-out docs; temp {args.temperature} "
          f"top_k {args.top_k} top_p {args.top_p}; {SNIP} new tokens", flush=True)
    print("request level counts per dim:",
          {d: dict(zip(*np.unique(R[:, j], return_counts=True))) for j, d in enumerate(DIMS)}, flush=True)

    texts = generate(model, tok, reqs, args.batch, args.seed,
                     args.temperature, args.top_k, args.top_p)
    G = np.stack([vec(ann.annotate(t)) for t in texts])

    perm = np.roll(np.arange(n), n // 2)        # fixed derangement: request of another doc
    lines: list[str] = []

    def emit(s: str = "") -> None:
        print(s, flush=True)
        lines.append(s)

    emit("")
    emit(f"RCE: mean abs error vs request, n={n} (95% bootstrap CI on model-minus-null)")
    emit(f"{'dim':<8}{'model':>8}{'null':>8}{'floor':>8}{'model-null':>24}{'spearman':>10}{'floor_rho':>10}")
    for j, d in enumerate(DIMS):
        m = np.abs(G[:, j] - R[:, j])
        z = np.abs(G[:, j] - R[perm, j])
        f = np.abs(F[:, j] - R[:, j])
        lo, hi = boot(lambda i: (m[i] - z[i]).mean(), n, 2000, nprng)
        emit(f"{d:<8}{m.mean():>8.3f}{z.mean():>8.3f}{f.mean():>8.3f}"
             f"{m.mean() - z.mean():>+12.3f} [{lo:+.3f},{hi:+.3f}]"
             f"{spearman(G[:, j], R[:, j]):>10.3f}{spearman(F[:, j], R[:, j]):>10.3f}")
    allm = np.abs(G - R).mean()
    allz = np.abs(G - R[perm]).mean()
    allf = np.abs(F - R).mean()
    emit(f"{'ALL':<8}{allm:>8.3f}{allz:>8.3f}{allf:>8.3f}{allm - allz:>+12.3f}")
    emit("(model-null < 0 means the prefix steers output; floor = real same-doc text)")

    # single-dimension sweep: base all-zero except formal, vary one dimension
    emit("")
    emit(f"SWEEP: request low vs high on one dimension, others 0 (n={args.sweep_n} each)")
    emit(f"{'dim':<8}{'low->high':>10}{'meas low':>10}{'meas high':>10}{'diff':>20}")
    sweeps = [("slang", 0, 3), ("emoji", 0, 2), ("abbrev", 0, 3), ("elong", 0, 2), ("formal", 0, 3)]
    for d, lo_v, hi_v in sweeps:
        got = {}
        for k, v in enumerate((lo_v, hi_v)):
            r = Register(**{**{x: 0 for x in DIMS}, d: v})
            tx = generate(model, tok, [r] * args.sweep_n, args.batch,
                          args.seed + 7919 * (k + 1) + 101 * DIMS.index(d), args.temperature,
                          args.top_k, args.top_p)
            got[v] = np.array([getattr(ann.annotate(t), d) for t in tx], dtype=float)
        a, b = got[lo_v], got[hi_v]
        bs = [(b[nprng.integers(0, len(b), len(b))].mean() - a[nprng.integers(0, len(a), len(a))].mean())
              for _ in range(2000)]
        emit(f"{d:<8}{f'{lo_v}->{hi_v}':>10}{a.mean():>10.2f}{b.mean():>10.2f}"
             f"{b.mean() - a.mean():>+10.2f} [{np.percentile(bs, 2.5):+.2f},{np.percentile(bs, 97.5):+.2f}]")

    if args.out:
        Path(args.out).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
