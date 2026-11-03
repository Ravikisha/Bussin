<p align="center">
  <img src="docs/assets/banner.svg" alt="bussin: a 125M language model that writes in the register you ask for" width="100%">
</p>

<p align="center">
  <a href="https://huggingface.co/Ravikishan/bussin-125m"><img alt="Model on Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20model-Ravikishan%2Fbussin--125m-7c5cff?style=flat-square"></a>
  <img alt="Parameters" src="https://img.shields.io/badge/parameters-125.9M-ff5fa2?style=flat-square">
  <img alt="Trained on free GPUs" src="https://img.shields.io/badge/compute-free%20Kaggle%20T4s-1baf7a?style=flat-square">
  <img alt="Code licence" src="https://img.shields.io/badge/code-MIT-2a78d6?style=flat-square">
  <img alt="Weights licence" src="https://img.shields.io/badge/weights-research%20only-eb6834?style=flat-square">
</p>

**Bussin** is a language model trained **from scratch** that writes in a register you choose: how slangy,
emoji-heavy, abbreviated, drawn-out and formal the text is. It is a research and portfolio project: small,
not instruction-tuned, and often incoherent. The parts worth reading are the method, the measurement, and the
infrastructure for training on free GPUs, including the mistakes.

| | |
|---|---|
| Model | [`Ravikishan/bussin-125m`](https://huggingface.co/Ravikishan/bussin-125m), a Llama-format checkpoint that loads with `transformers` |
| Architecture | 14 layers, d_model 768, 12 heads / 4 KV heads, SwiGLU, RoPE, tied embeddings, 49,152-token BPE, 1,024 context |
| Training | Run v1: 6.74B tokens (a loss bug, see below), then realign: 1.07B tokens with the corrected objective |
| Compute | About 110 GPU-hours on free Kaggle T4 x2 sessions, no paid compute |
| Headline result | Generated register error 0.146 vs 0.646 for a shuffled-request baseline, measured on 200 held-out requests |
| Write-up | [`docs/SPEC.md`](docs/SPEC.md) · [model card](docs/MODEL_CARD.md) · [results](docs/results/rce_final-4067.txt) |

## The idea

Nobody cringes at a teenager saying "that's so cooked" to a friend. They cringe when a bank's account says it.
So cringe is **register mismatch**, not slang. Bussin makes the register an explicit input: every training
document is prefixed with five measured register levels, and the model learns `p(text | register)`.

<p align="center"><img src="docs/assets/how-it-works.svg" alt="Mine, measure, prefix, train, dial" width="100%"></p>

There is no Gen-Z pretraining corpus to download, so the register is mined from community text using a
date-stamped slang lexicon and a deterministic annotator. Once register is a conditioning variable, "cringe"
becomes a measurable number: **Register Calibration Error (RCE)**, the distance between the register you asked
for and the register you got.

## Does it work?

Yes, measurably, with caveats. 200 requests were taken from the measured registers of real held-out documents.
The model wrote 48 tokens from the prefix alone, and the annotator measured what came out.

<p align="center"><img src="docs/assets/rce-chart.svg" alt="Register error by dimension: model vs shuffled null vs real text" width="100%"></p>

Setting a single dial, with everything else at zero, moves exactly that dimension:

<p align="center"><img src="docs/assets/sweep-chart.svg" alt="Requested versus measured level when one dimension is set high" width="100%"></p>

**Read these honestly.**

- The prefix steers the output: error is far below the shuffled baseline on every dimension, and all 95%
  intervals exclude zero.
- Beating the "real text" column does not mean writing better than people. The model produces stereotyped,
  easy-to-score registers, while real documents mix registers.
- The annotator that scores the output also produced the training labels. Its agreement with a human rater
  (one person) was Spearman 0.48, under the 0.70 gate I set.
- Only 21 of 200 requests were slang 3-4, and 193 of 200 had no abbreviations. One checkpoint, one seed set.

## Talking to it

bussin-125m is a **base language model**, not an assistant: it has no instruction tuning, so it continues text in the
register you ask for instead of answering. That makes the register prefix the whole interface, and the clearest demo is to
hold the message fixed and turn the dials. Same message, same sampling settings, four registers:

**"thoughts on the new iphone"**

| register | dials | the model continues |
|---|---|---|
| formal | `slang 0, emoji 0, abbrev 0, formal 3` | I don't know much about phones, so I've been wondering how to connect my phone to the phone with a SIM. I was thinking of buying the new one, however I'm not quite sure how to connect to the new phone. Do you think the SIM connection is the problem? |
| chill | `slang 1, abbrev 1` | also if you know anyone who uses airpods, pls share them |
| casual | `slang 3, emoji 1, abbrev 2` | i don't know what the phone is worth rn but it's a nice looking phone that i wanna use for a couple of hours, but i dont know if it's worth anything at all to have a phone that's mid to not worth \$100 also, i feel like i would prefer it |
| hype | `slang 4, emoji 2, abbrev 3, elong 1` | i don't know what the phone is worth rn but if u wanna get a new phone lmk i wanna get a new iPhone idk if i should get the iphone 12 or the 12 pro i wanna keep my 16 pro btw 🙏 |

`formal` gives capitalised, fully punctuated sentences. `casual` and `hype` give lowercase text with `rn`, `lmk`, `idk`
and, at the high setting, emoji. Only the prefix changed.

A few of the 50 everyday prompts (20 casual, 15 neutral, 15 formal, each with a matching register prefix):

| prompt | register | the model continues |
|---|---|---|
| i have an exam tomorrow and havent studied | casual | i dont wanna fail, i wanna get into clg (pls do tell me if it actually works) can u pls tell me how to study? i wanna study for 12 hrs everyday edit: how many days will be left? |
| what's the best game right now | casual | edit: actually the best one rn is smash bros but i'm gonna go with smash bros ultimate edit 2: i'm playing sonic 3 rn and i like the character so much that i'm kinda thinking of buying it, ... |
| Explain the difference between weather and climate. | formal | Climate is a term used in studies that look at the climate of a particular region or area, especially in relation to weather patterns and the overall climate of a particular region or area. |
| What are the benefits of regular exercise? | formal | What kind of exercise is recommended to lose weight? How long does it usually take for your body to adjust? Also, what are the risks associated with increasing your activity level? |

Across all 50, the model holds a register for a whole passage and stays near the topic for a sentence or two, behaving like
a forum or chat post on the subject rather than an answer to it; an instruction-tuning stage is the natural next layer.
Responses with self-harm or insulting content are withheld from the published files and marked as such. Full results:
[`docs/results/chat_samples_50.md`](docs/results/chat_samples_50.md) ·
[`docs/results/dial_comparison.md`](docs/results/dial_comparison.md).

## Try it

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

repo = "Ravikishan/bussin-125m"
tok = AutoTokenizer.from_pretrained(repo)
model = AutoModelForCausalLM.from_pretrained(repo).eval()

# levels: slang 0-4, emoji 0-3, abbrev 0-3, elong 0-2, formal 0-3
prompt = "<|endoftext|><|reg|><|slang_3|><|emoji_1|><|abbrev_2|><|elong_0|><|formal_0|><|/reg|>"
ids = tok(prompt, return_tensors="pt", add_special_tokens=False)
out = model.generate(**ids, max_new_tokens=60, do_sample=True, temperature=0.8,
                     top_k=50, top_p=0.95, pad_token_id=1)
print(tok.decode(out[0][ids["input_ids"].shape[1]:]))
```

## What went wrong

The first training run, 6.74B tokens and about 110 GPU-hours, **optimised the wrong objective**. The loss shifted
the targets a second time, so the model learned to predict the token two positions ahead. Nothing crashed. It
surfaced only because the evaluation looked wrong. The fix is one line; the lasting change is
`scripts/objective_test.py`, which fails on the old loss and passes on the fix.

<p align="center"><img src="docs/assets/timeline.svg" alt="Timeline from the first run through the bug and fix to release" width="100%"></p>

The same audit found and fixed several accounting problems: tokens double-counted across two GPUs, one GPU
idle, the curriculum order shuffled, checkpoint pruning that could delete archived weights, and local checkpoints
filling the disk. Each has a test that fails on the old code (`scripts/accounting_test.py`,
`scripts/relay_e2e_test.py`). The full account is in `docs/SPEC.md` section 5.9e.

**Not measured or not done:** toxicity (samples contained crude and baseless accusatory text), downstream
benchmarks (BussBench has data for 3 of 15 tasks and known label problems), human validation of the annotator,
the 400M and 1B models (configs exist, never trained), and TPU training (unvalidated).

## Training on free GPUs

Free sessions end, so training is a relay. Each session checkpoints to the Hugging Face Hub and claims a lease
by compare-and-swap on the Hub's commit SHA. A crashed session just lets its lease expire, and a stateless
orchestrator starts the next one. Resume is bit-exact (`scripts/resume_test.py`, 0.0 relative divergence). The
orchestrator's schedule is disabled now that training is finished.

<p align="center"><img src="docs/assets/relay.svg" alt="Kaggle sessions hand over through checkpoints and a lease on the Hugging Face Hub" width="100%"></p>

## Repository

```
docs/SPEC.md          specification and the audit of what held up
docs/MODEL_CARD.md    model card
docs/results/         measured results (register error, 50 chat prompts, four-register comparison)
docs/assets/          logo and figures (generated by scripts/make_figures.py)
docs/assets/posters/  share posters (generated by scripts/posters/)
docs/blog/            the blog post source (published on ravikishan.me)
configs/              training configs (125m-realign.yaml produced the released model)
bussin/model/         architecture (Llama-style)
bussin/data/          cleaning, dedup, lexicon, register annotation
bussin/train/         trainer, WSD schedule, precision
bussin/relay/         lease, checkpoint, watchdog, bootstrap
bussin/orchestrator/  platform adapters, ledger, dashboard
bussin/eval/          register metrics, BussBench (partial)
scripts/              tests, evaluation (rce_test.py, register_conditioning_test.py), HF export
scripts/posters/      poster and blog-image generators
pipelines/            lexicon, corpus mining, tokenizer, sharding
```

## Reproduce the checks

```bash
python scripts/model_sanity_test.py     # init loss, causality, document isolation, RoPE, GQA
python scripts/objective_test.py        # the model learns next-token, not skip-ahead
python scripts/accounting_test.py       # token accounting, curriculum order, prune scope
python scripts/lease_test.py            # lease compare-and-swap, two-worker race
python scripts/rce_test.py --ckpt <ckpt dir> --n 200      # register calibration (a GPU is much faster)
python scripts/export_hf.py --ckpt <ckpt dir> --out hf_export   # Llama export with a logit-parity check
python scripts/chat_test.py             # 50 chat-style prompts through the published model
python scripts/dial_test.py             # one message under four registers
```

## Data and licensing

Training text is **not** redistributed; only filter code and manifests are published. Source tiers are listed in
`docs/SPEC.md` section 1.12. Author columns are dropped at ingest and PII scrubbing runs over message bodies.
Much of the slang lexicon has African American English provenance, and the model card says so.

Code is MIT. The weights are for research and non-commercial use only, pending legal review of mixed source
licences.
