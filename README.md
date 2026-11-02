# Bussin

**A 125M-parameter language model, trained from scratch on free compute, that writes in a requested
register: how slangy, emoji-heavy, abbreviated, drawn-out and formal the text is.**

Model: <https://huggingface.co/GodAsap/bussin-125m> (Llama format, loads with `transformers`)
Write-up and design rationale: [`docs/SPEC.md`](docs/SPEC.md) · Model card: [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md)

This is a portfolio / research project. The model is small, not instruction-tuned, and writes rambling
text. The interesting parts are the method, the measurement, and the infrastructure built to train on
free GPUs.

## The idea

Nobody cringes at a teenager saying "that's so cooked" to a friend; they cringe when a bank's account
says it. So "cringe" is modelled as **register mismatch**, not slang. Every pretraining document gets a
measured 5-dimensional register prefix,

```
<|endoftext|><|reg|><|slang_3|><|emoji_1|><|abbrev_2|><|elong_0|><|formal_0|><|/reg|> ...text...
```

and the model learns `p(text | register)`. Slang becomes a dial that can be set and measured.
There is no Gen-Z pretraining corpus to download, so the register is mined out of community text with a
date-stamped slang lexicon and a deterministic annotator.

## What was measured

Register calibration on the final checkpoint (200 requests taken from real held-out documents; the model
writes 48 tokens from the prefix alone; the annotator measures the output; mean absolute error against
the request):

| dimension | model | shuffled-request null | real same-doc text |
|---|---|---|---|
| slang | 0.335 | 1.255 | 0.915 |
| emoji | 0.150 | 0.930 | 0.565 |
| abbrev | 0.015 | 0.065 | 0.100 |
| elong | 0.115 | 0.525 | 0.430 |
| formal | 0.115 | 0.455 | 0.320 |
| **all** | **0.146** | **0.646** | **0.466** |

The prefix steers output (every interval excludes zero). Requesting slang 0 vs 3 gives measured slang
0.00 vs 2.88. Caveats are real: the annotator scores its own training labels, human agreement with it was
only Spearman 0.48 (one rater, below my 0.70 gate), and error below the real-text column reflects
stereotyped output, not text better than a human's. Details: [`docs/results/rce_final-4067.txt`](docs/results/rce_final-4067.txt).

## What went wrong (kept in the record on purpose)

- **The first training run (6.74B tokens, ~110 GPU-hours) optimised the wrong objective.** The loss shifted
  targets a second time, so the model learned to predict the token two positions ahead. It was found when
  evaluation looked wrong, fixed, and covered by `scripts/objective_test.py`, which fails on the old loss and
  passes on the fix. The released weights come from a second run initialised from v1 and trained 1.07B tokens
  with the corrected objective. See `docs/SPEC.md` §5.9e.
- **Training accounting was wrong in several ways** (tokens double-counted across two GPUs, one GPU used,
  curriculum order shuffled, checkpoint pruning that could delete archived weights, local checkpoint copies
  filling the disk). All fixed and covered by `scripts/accounting_test.py` and `scripts/relay_e2e_test.py`.
- **Not measured / not done:** toxicity (samples included crude and baseless accusatory text), downstream
  benchmarks (BussBench has data for 3 of 15 tasks and known label problems), human validation of the
  annotator, the 400M and 1B models (configs exist, never trained), and TPU training (unvalidated).

## Compute and infrastructure

Everything ran on free tiers (Kaggle T4 x2). A lease-based relay (`bussin/relay/`) checkpoints to the
Hugging Face Hub and hands training between sessions using compare-and-swap on a state file. A stateless
orchestrator (`bussin/orchestrator/`) decided when to start sessions; its schedule is disabled now that
training is finished. Resume is bit-exact (`scripts/resume_test.py`, 0.0 relative divergence).

## Repo layout

```
docs/SPEC.md          the specification and the audit of what held up
docs/MODEL_CARD.md    model card
docs/results/         measured results
configs/              training configs (125m-realign.yaml produced the released model)
bussin/model/         architecture (Llama-style)
bussin/data/          cleaning, dedup, lexicon, register annotation
bussin/train/         trainer, WSD schedule, precision
bussin/relay/         lease, checkpoint, watchdog, bootstrap
bussin/orchestrator/  platform adapters, ledger, dashboard
bussin/eval/          register metrics, BussBench (partial)
scripts/              tests, evaluation (rce_test.py, register_conditioning_test.py), HF export
pipelines/            lexicon, corpus mining, tokenizer, sharding
```

## Use the model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
repo = "GodAsap/bussin-125m"
tok = AutoTokenizer.from_pretrained(repo)
model = AutoModelForCausalLM.from_pretrained(repo).eval()
prompt = "<|endoftext|><|reg|><|slang_3|><|emoji_1|><|abbrev_2|><|elong_0|><|formal_0|><|/reg|>"
ids = tok(prompt, return_tensors="pt", add_special_tokens=False)
out = model.generate(**ids, max_new_tokens=60, do_sample=True, temperature=0.8,
                     top_k=50, top_p=0.95, pad_token_id=1)
print(tok.decode(out[0][ids["input_ids"].shape[1]:]))
```

## Reproduce the tests

```bash
python scripts/model_sanity_test.py     # init loss, causality, document isolation, RoPE, GQA
python scripts/objective_test.py        # the model learns next-token, not skip-ahead
python scripts/accounting_test.py       # token accounting, curriculum order, prune scope
python scripts/lease_test.py            # lease compare-and-swap, two-worker race
python scripts/export_hf.py --ckpt <ckpt dir> --out hf_export   # Llama export with logit parity check
```

## Data and licensing

Training text is **not** redistributed; only filter code and manifests are published. Source tiers are in
`docs/SPEC.md` §1.12. Author columns are dropped at ingest and PII scrubbing runs over message bodies.
Much of the slang lexicon has African American English provenance, and the model card says so.
Code is MIT. Model weights are research / non-commercial only, pending legal review of mixed source licences.
