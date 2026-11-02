"""Same message, four registers: hold the message fixed and turn the register dials.

Loads the published model, then for each message generates one continuation under each of
four register prefixes (formal, chill, casual, hype) with identical sampling settings and a
per-message seed, so the only thing that changes is the prefix.

Requirements: pip install torch transformers
Run:  python scripts/dial_test.py [hf_repo_or_local_dir] [out.json]
Review the outputs before publishing them: this is a base model trained on raw community text.
"""
import json, sys, torch
from transformers import AutoModelForCausalLM, AutoTokenizer
REPO = sys.argv[1] if len(sys.argv) > 1 else "Ravikishan/bussin-125m"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dial_results.json"
REGS = {"formal": (0, 0, 0, 0, 3), "chill": (1, 0, 1, 0, 0), "casual": (3, 1, 2, 0, 0), "hype": (4, 2, 3, 1, 0)}
MSGS = ["is pineapple on pizza ok or nah", "thoughts on the new iphone", "how should i prepare for a job interview"]
tok = AutoTokenizer.from_pretrained(REPO); model = AutoModelForCausalLM.from_pretrained(REPO).eval()
out = []
for mi, msg in enumerate(MSGS):
    for name, (s, e, a, el, f) in REGS.items():
        pre = f"<|endoftext|><|reg|><|slang_{s}|><|emoji_{e}|><|abbrev_{a}|><|elong_{el}|><|formal_{f}|><|/reg|>"
        ids = tok(pre + f"{msg}\n\n", return_tensors="pt", add_special_tokens=False)
        torch.manual_seed(2000 + mi)
        with torch.inference_mode():
            g = model.generate(**ids, max_new_tokens=60, do_sample=True, temperature=0.8, top_k=50, top_p=0.95, pad_token_id=1, eos_token_id=0)
        text = tok.decode(g[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()
        out.append({"message": msg, "register": name, "levels": (s, e, a, el, f), "reply": text})
        print(f"[{len(out)}/12] {name}: {' '.join(text.split())[:90]}", flush=True)
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("DIAL_DONE", flush=True)
