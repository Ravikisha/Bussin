import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # scripts/ (make_figures)
import make_figures as mf
from make_figures import (svg, text, card, icon, GRAD, NAVY, NAVY2, VIOLET, PINK, INK, INK2, MONO, AQUA, BLUE, ORANGE)
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

def cover():
    w, h = 1200, 630
    b = [GRAD,
         f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient></defs>',
         f'<rect width="{w}" height="{h}" fill="url(#bg)"/>',
         f'<circle cx="1090" cy="80" r="260" fill="{PINK}" opacity=".08"/><circle cx="930" cy="610" r="210" fill="{VIOLET}" opacity=".12"/>',
         icon(70, 64, 120), text(214, 112, "bussin-125m", 30, "#d8d3ff", 700, extra='letter-spacing="1"'),
         text(70, 262, "Slang is a dial.", 84, "#ffffff", 800, extra='letter-spacing="-2"'),
         text(70, 352, "A language model built from scratch,", 40, "#ffffff", 600),
         text(70, 404, "end to end, on free GPUs.", 40, "#ffffff", 600),
         text(70, 466, "Data pipeline, model, training systems, evaluation and release.", 26, "#b8b1f0")]
    x = 70
    for name, lv in [("slang", 3), ("emoji", 1), ("abbrev", 2), ("elong", 0), ("formal", 0)]:
        label = f"{name} {lv}"; cw = 18 + len(label) * 12.6
        b.append(f'<rect x="{x}" y="520" width="{cw:.0f}" height="46" rx="23" fill="#fff" opacity=".10"/><rect x="{x}" y="520" width="{cw:.0f}" height="46" rx="23" fill="none" stroke="#fff" opacity=".3"/>')
        b.append(text(x + cw / 2, 551, label, 22, "#ffffff", 600, "middle", MONO)); x += cw + 14
    return svg(w, h, "".join(b), "Slang is a dial: bussin-125m cover", "Cover image with the bussin logo and register dials")

def milestones():
    w, h = 1200, 380
    ev = [("Spec", "17-section research", "and design document"), ("Lexicon", "dated slang dictionary", "+ register annotator"),
          ("Data", "mining, cleaning, PII", "49,152-token BPE"), ("Model", "Llama-style 125.9M,", "verified by tests"),
          ("Relay", "lease-based training", "on free GPUs"), ("Pretrain", "6.74B tokens,", "~110 GPU-hours"),
          ("Anneal", "1.07B tokens of the", "register curriculum"), ("Evaluate", "register error 0.146", "vs 0.646 baseline"),
          ("Ship", "Llama export, logit", "parity, Hugging Face")]
    n = len(ev); x0, x1, yl = 84, 1116, 130
    cols = [VIOLET, VIOLET, VIOLET, PINK, PINK, AQUA, AQUA, BLUE, BLUE]
    b = [card(w, h), text(46, 40, "From idea to release, built end to end", 24, INK, 700),
         f'<line x1="{x0}" y1="{yl}" x2="{x1}" y2="{yl}" stroke="#d9d6ee" stroke-width="4" stroke-linecap="round"/>']
    for i, (t1, l1, l2) in enumerate(ev):
        x = x0 + i * (x1 - x0) / (n - 1)
        b.append(f'<circle cx="{x:.0f}" cy="{yl}" r="14" fill="{cols[i]}" stroke="#fcfcfb" stroke-width="3"/>')
        b.append(text(x, yl + 50, t1, 17, INK, 700, "middle"))
        b.append(text(x, yl + 74, l1, 13, INK2, 400, "middle")); b.append(text(x, yl + 93, l2, 13, INK2, 400, "middle"))
    b.append(text(46, 318, "Research, data engineering, model engineering, distributed training systems, evaluation and release: every layer", 15.5, INK2, 500))
    b.append(text(46, 342, "is code in one repository, with tests.", 15.5, INK2, 500))
    return svg(w, h, "".join(b), "From idea to release", "Nine milestones from the specification to the released model")

(OUT / "cover2.svg").write_text(cover(), encoding="utf-8")
(OUT / "milestones.svg").write_text(milestones(), encoding="utf-8")
s = mf.rce_chart()
s2 = re.sub(r'<text x="40" y="500"[^>]*>.*?</text><text x="40" y="520"[^>]*>.*?</text>',
            '<text x="40" y="506" font-size="14.5" fill="#52514e" font-weight="400" text-anchor="start">About 4x lower register error than a shuffled-request baseline, on every dimension (95% intervals exclude zero).</text>',
            s, flags=re.S)
assert s2 != s, "footer not replaced"
(OUT / "rce-chart2.svg").write_text(s2, encoding="utf-8")
print("ok")
