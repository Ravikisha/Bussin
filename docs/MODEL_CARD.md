---
license: other
license_name: research-only
language:
- en
library_name: transformers
pipeline_tag: text-generation
tags:
- llama
- register-conditioning
- gen-z
- slang
- from-scratch
---

# bussin-125m

A 125.9M-parameter language model **trained from scratch on free compute** (Kaggle T4s) to write in a
requested *register*: how slangy, emoji-heavy, abbreviated, drawn-out and formal the text is.

It is a research / portfolio model. It is **not** instruction-tuned, not safety-tuned, and it writes
rambling, often incoherent text. Read the limitations before using it.

Code, data pipeline, evaluation and the full write-up: <https://github.com/Ravikisha/GenZLLM>

## How it works

Every training document was prefixed with five measured register control tokens:

```
<|endoftext|><|reg|><|slang_3|><|emoji_1|><|abbrev_2|><|elong_0|><|formal_0|><|/reg|> ...text...
```

so the model learns `p(text | register)`. Levels: `slang_0..4`, `emoji_0..3`, `abbrev_0..3`,
`elong_0..2`, `formal_0..3`. The labels come from a deterministic annotator plus a dated slang lexicon,
not from human raters.

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

repo = "GodAsap/bussin-125m"
tok = AutoTokenizer.from_pretrained(repo)
model = AutoModelForCausalLM.from_pretrained(repo).eval()

prompt = ("<|endoftext|><|reg|><|slang_3|><|emoji_1|><|abbrev_2|>"
          "<|elong_0|><|formal_0|><|/reg|>")
ids = tok(prompt, return_tensors="pt", add_special_tokens=False)
out = model.generate(**ids, max_new_tokens=60, do_sample=True,
                     temperature=0.8, top_k=50, top_p=0.95, pad_token_id=1)
print(tok.decode(out[0][ids["input_ids"].shape[1]:]))
```

## Architecture

Llama-style decoder, loads as `LlamaForCausalLM`: 14 layers, d_model 768, 12 heads with 4 KV heads (GQA),
SwiGLU FFN 2048, RoPE (theta 10,000), RMSNorm, tied embeddings, vocabulary 49,152 (custom byte-level BPE),
context 1,024. The export was checked against the original implementation: max logit difference 3.6e-05,
100% argmax agreement.

## Training history (read this)

1. **Run v1:** 25,757 steps, 6.74B tokens, about 110 GPU-hours. A bug in the loss shifted the targets a
   second time, so the model was trained to predict the token **two** positions ahead instead of the next
   one. It was found when evaluation looked wrong (next-token NLL 8.76 vs 5.40 at +2).
2. **Run realign:** initialised from the v1 weights and trained 4,067 steps, 1.07B tokens, with the loss
   fixed, following the project's staged data curriculum (S2 then S3). This is the released checkpoint.

So these weights carry the history of a mis-specified first phase. Validation loss on a general
held-out shard is 3.741 at step 3,314 and 3.748 at step 4,067, i.e. no measurable change over the last
750 steps; that shard does not contain the Gen-Z stage data, so it would not show gains there.

## Evaluation

**Register calibration (RCE).** 200 requests taken from the measured registers of real held-out
documents (stratified by slang level and emoji presence); the model writes 48 tokens from the prefix alone
and the annotator measures the output. Mean absolute error against the request, with a shuffled-request null
(generations scored against another document's request) and the error of real text from the same document:

| dimension | model | shuffled null | real same-doc text |
|---|---|---|---|
| slang | 0.335 | 1.255 | 0.915 |
| emoji | 0.150 | 0.930 | 0.565 |
| abbrev | 0.015 | 0.065 | 0.100 |
| elong | 0.115 | 0.525 | 0.430 |
| formal | 0.115 | 0.455 | 0.320 |
| **all** | **0.146** | **0.646** | **0.466** |

Single-dimension sweep, other dimensions 0 (n=50 each): slang 0 to 3 measured 0.00 to 2.88; emoji 0 to 2
measured 0.00 to 2.00; abbrev 0 to 3 measured 0.00 to 2.40; elong 0 to 2 measured 0.00 to 1.80; formal 0 to 3
measured 0.02 to 2.62.

What this does and does not show:

- The register prefix clearly steers the output (error far below the null; all intervals exclude zero).
- Error below the real-text column does **not** mean better than human text. Generations are stereotyped,
  easy-to-score registers; real documents mix registers and the annotator is noisy on short text.
- The annotator scores its own training labels. This is agreement with that instrument, not human judgement;
  its agreement with a human rater (me, one person) was Spearman 0.48 against a 0.70 gate I set.
- Few high-slang requests (21 of 200 at slang 3-4) and almost no abbreviations in real requests (193 of 200 at 0).
- One checkpoint, one seed set, temperature 0.8.

Full output: `docs/results/rce_final-4067.txt` in the GitHub repo.

**Not measured:** toxicity, factuality, any downstream benchmark. My benchmark (BussBench) has data for 3 of 15
planned tasks and known label problems, so I do not report a score.

## Limitations and risks

- **Text quality is poor.** Samples ramble, repeat lines and contain word salad. 125M parameters and about
  1B tokens of the final phase do not make a fluent model.
- **It can produce toxic content.** I read samples in the "very slangy" condition containing a baseless
  accusation against a person and crude insults. Toxicity was never measured and there is no safety tuning.
- **Training-data artifacts.** The data filter missed some Reddit bot text, which the model reproduces.
- **Lexicon provenance.** Much slang originates in African American English. The lexicon is dated and
  contains terms that have drifted in meaning; the model reflects its sources.
- **English only**, with a small amount of Hinglish.

## Data and licence

Training text was mined from public internet sources, including Reddit-derived community text (source tiers
are listed in `docs/SPEC.md` section 1.12 of the GitHub repo). I do **not** republish the training text. Because source licences are mixed
and have not had legal review, the weights are released **for research and non-commercial use only**; the code
in the GitHub repository is MIT.

## Compute

About 110 GPU-hours for run v1 plus the realign run, all on free Kaggle T4 x2 sessions,
coordinated by a lease-based relay that checkpoints to the Hugging Face Hub.
