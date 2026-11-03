"""Poster: the build line (six stages, one measured number each). Writes poster-linkedin-2.svg.
Run: python scripts/posters/build_line.py [output_dir]   (then render with scripts/posters/render.py)"""
import sys, textwrap
from html import escape
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # scripts/ (make_figures)
from make_figures import icon, GRAD

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "assets" / "posters"
OUT.mkdir(parents=True, exist_ok=True)
PAPER, INK, SLATE = "#EDF0F6", "#0F1A35", "#56617F"
VIOLET, MAGENTA, MIST, MIST2 = "#5B43F5", "#E8397D", "#AEB7D0", "#7F8BB0"
SANS = "Bahnschrift, 'Segoe UI', Arial, sans-serif"
W, H, M = 1080, 1350, 84


def t(x, y, s, size, fill=INK, weight=400, anchor="start", stretch=None, spacing=None):
    st = f' font-stretch="{stretch}"' if stretch else ""
    ls = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{st}{ls}>{escape(s)}</text>')


# each stage: title, one plain sentence, hard number, caption. Every figure is a measured or counted fact.
STAGES = [
    ("Measure", "A dated slang lexicon and a rule-based annotator score each document on five dials. No human labels.",
     "55,499", "terms in the lexicon"),
    ("Train", "A 125.9M-parameter decoder trained on two free Kaggle GPUs, with a schedule built for an unknown quota.",
     "7.8B", "training tokens"),
    ("Relay", "A lease, claimed by compare-and-swap on a commit hash, hands training between sessions without forking.",
     "0.0", "divergence when a run resumes"),
    ("Verify", "Six behavioural test suites, including one that checks what the model actually learned.",
     "6", "test suites"),
    ("Evaluate", "A shuffled baseline and single-dial sweeps show whether each dial really steers the output.",
     "2.88", "measured when slang 3 is requested"),
    ("Ship", "Exported to Llama format and checked against the original, so it loads in three lines of transformers.",
     "3.6e-5", "largest logit difference"),
]

b = [GRAD, f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']

# ---- header block (ink): the inverse of poster 1, so the two read as a pair
HEAD = 368
b.append(f'<rect width="{W}" height="{HEAD}" fill="{INK}"/>')
b.append(icon(M, 64, 60))
b.append(t(M + 80, 105, "bussin-125m", 30, "#FFFFFF", 600, stretch="semi-condensed"))
b.append(t(M - 4, 262, "Built end to end.", 112, "#FFFFFF", 700, stretch="semi-condensed", spacing="-2"))
b.append(t(M, 316, "From a slang dictionary to a model anyone can load.", 28, MIST, 400))

# ---- the build line
X = M + 32          # track x
TX = M + 96         # text column x
FIG_R = W - M       # figures are right-aligned here
Y0, STEP = 458, 138
b.append(f'<line x1="{X}" y1="{Y0}" x2="{X}" y2="{Y0 + 5 * STEP}" stroke="{VIOLET}" stroke-width="3" stroke-linecap="round"/>')
for i, (title, body, fig, cap) in enumerate(STAGES):
    y = Y0 + i * STEP
    last = i == len(STAGES) - 1
    col = MAGENTA if last else VIOLET
    b.append(f'<circle cx="{X}" cy="{y}" r="19" fill="{col}"/>')
    b.append(t(X, y + 7, str(i + 1), 21, "#FFFFFF", 700, anchor="middle"))
    b.append(t(TX, y + 9, title, 33, INK, 700, stretch="semi-condensed"))
    for j, ln in enumerate(textwrap.wrap(body, 55, break_on_hyphens=False)[:3]):
        b.append(t(TX, y + 42 + j * 30, ln, 22, SLATE, 400))
    b.append(t(FIG_R, y + 12, fig, 50, MAGENTA if last else INK, 700, anchor="end", stretch="semi-condensed", spacing="-1"))
    for j, ln in enumerate(textwrap.wrap(cap, 22)[:2]):
        b.append(t(FIG_R, y + 40 + j * 22, ln, 18, SLATE, 400, anchor="end"))

# ---- footer
FY = 1272
b.append(f'<line x1="{M}" y1="{FY - 26}" x2="{W - M}" y2="{FY - 26}" stroke="#C9D0E0" stroke-width="2"/>')
b.append(t(M, FY + 10, "huggingface.co/Ravikishan/bussin-125m", 23, INK, 700))
b.append(t(M, FY + 40, "github.com/Ravikisha/Bussin", 20, SLATE, 400))
b.append(t(W - M, FY + 10, "Ravi Kishan", 23, INK, 700, anchor="end"))
b.append(t(W - M, FY + 40, "ravikishan.me/blog", 20, SLATE, 400, anchor="end"))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-labelledby="t d"><title id="t">Built end to end: bussin-125m</title>'
       f'<desc id="d">Six stages from a slang lexicon to a released model, each with one measured number</desc>'
       + "".join(b) + "</svg>")
(OUT / "poster-linkedin-2.svg").write_text(svg, encoding="utf-8")
print("ok")
