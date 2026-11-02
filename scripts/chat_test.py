"""Run 50 chat-style messages through bussin-125m and save the responses.

The model is a base language model with register control tokens, not an instruction-tuned
assistant, so a "chat" is a chat-log continuation. Two framings are run for every message:
  chat   "User: <msg>\nBot:"   the model continues the log (stopped at the next "User:")
  reply  "<msg>\n\n"           the model continues as the reply
Each message carries a register prefix (casual / chill / formal).

Requirements: pip install torch transformers
Run:  python scripts/chat_test.py [hf_repo_or_local_dir] [out.json]
The published results (docs/results/chat_samples_50.*) withhold the few outputs with self-harm or
insulting content; review raw outputs before publishing them, since this is a base model.
"""
import json
import sys
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

REPO = sys.argv[1] if len(sys.argv) > 1 else "Ravikishan/bussin-125m"
OUT = sys.argv[2] if len(sys.argv) > 2 else "chat_results.json"
EOS = 0

REG = {  # slang, emoji, abbrev, elong, formal
    "casual": (3, 1, 2, 0, 0),
    "chill": (1, 0, 1, 0, 0),
    "formal": (0, 0, 0, 0, 3),
}
MSGS = (
    [("casual", m) for m in [
        "yo whats up", "just failed my driving test lol", "what should i eat tonight",
        "this new album is actually fire", "my boss keeps texting me after work",
        "is pineapple on pizza ok or nah", "i have an exam tomorrow and havent studied",
        "my crush just left me on read", "can you recommend a good show to binge",
        "what does cooked mean", "bro thinks he's the main character", "i just got my first paycheck",
        "why is monday so bad", "my phone battery is at 2 percent", "thoughts on the new iphone",
        "i cant sleep help", "what's the best game right now", "my friend ghosted me for a week",
        "should i cut my own hair", "tell me something funny"]]
    + [("chill", m) for m in [
        "how do i learn python quickly", "what is a good workout routine for beginners",
        "can you explain what an llm is", "i want to start a youtube channel", "how do i ask for a raise",
        "any tips for a first date", "what should i name my dog", "how do i stop procrastinating",
        "is it worth learning to code in 2026", "how do i get better at chess",
        "what is the meaning of life", "can you help me write a text to my ex", "how do i cook rice properly",
        "best way to save money as a student", "what do you think about ai taking jobs"]]
    + [("formal", m) for m in [
        "Could you summarize the main causes of inflation?", "Please write a short introduction for a cover letter.",
        "What are the benefits of regular exercise?", "Explain how photosynthesis works.",
        "How should I prepare for a job interview?", "What is the capital of France?",
        "Describe the history of the internet.", "Why is sleep important for health?",
        "How does a neural network learn?", "Write a polite email declining a meeting.",
        "What are good habits for studying effectively?", "Explain the difference between weather and climate.",
        "How do vaccines work?", "What should I consider when buying a laptop?",
        "Give me advice on managing stress."]]
)
assert len(MSGS) == 50, len(MSGS)


def prefix(kind):
    s, e, a, el, f = REG[kind]
    return f"<|endoftext|><|reg|><|slang_{s}|><|emoji_{e}|><|abbrev_{a}|><|elong_{el}|><|formal_{f}|><|/reg|>"


tok = AutoTokenizer.from_pretrained(REPO)
model = AutoModelForCausalLM.from_pretrained(REPO).eval()
dev = "cuda" if torch.cuda.is_available() else "cpu"
model.to(dev)
print("device", dev, flush=True)

results = []
for i, (kind, msg) in enumerate(MSGS):
    row = {"i": i + 1, "register": kind, "levels": REG[kind], "message": msg}
    for mode, body in (("chat", f"User: {msg}\nBot:"), ("reply", f"{msg}\n\n")):
        ids = tok(prefix(kind) + body, return_tensors="pt", add_special_tokens=False).to(dev)
        torch.manual_seed(1000 + i)
        with torch.inference_mode():
            out = model.generate(**ids, max_new_tokens=70, do_sample=True, temperature=0.8, top_k=50, top_p=0.95,
                                 pad_token_id=1, eos_token_id=EOS)
        text = tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)
        if mode == "chat":
            text = text.split("\nUser:")[0]
        row[mode] = text.strip()
    results.append(row)
    print(f"[{i+1}/50] {msg!r} -> {row['chat'][:70]!r}", flush=True)
json.dump(results, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("WROTE", OUT, flush=True)
