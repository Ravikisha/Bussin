"""Poster: the slang ruler (one message placed at its slang level). Writes poster-linkedin.svg.
Run: python scripts/posters/ruler.py [output_dir]   (then render with scripts/posters/render.py)"""
import sys, textwrap
from html import escape
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # scripts/ (make_figures)
from make_figures import icon, GRAD

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "assets" / "posters"
OUT.mkdir(parents=True, exist_ok=True)
PAPER, INK, SLATE, RULE = "#EDF0F6", "#0F1A35", "#56617F", "#C9D0E0"
VIOLET, MAGENTA = "#5B43F5", "#E8397D"
SANS = "Bahnschrift, 'Segoe UI', Arial, sans-serif"
SERIF = "Georgia, Cambria, 'Times New Roman', serif"
EMOJI = "'Segoe UI Emoji'"
W, H = 1080, 1350
M = 84  # outer margin


def t(x, y, s, size, fill=INK, weight=400, family=SANS, anchor="start", stretch=None, spacing=None, extra=""):
    st = f' font-stretch="{stretch}"' if stretch else ""
    ls = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{st}{ls} {extra}>{escape(s)}</text>')


# the four real outputs for "thoughts on the new iphone" (verbatim excerpts; "..." marks a cut)
PRAY = chr(0x1F64F)
ROWS = [
    (0, "slang 0, formal 3", "...I was thinking of buying the new one, however I'm not quite sure how to connect to the new phone."),
    (1, "slang 1, abbrev 1", "also if you know anyone who uses airpods, pls share them"),
    (3, "slang 3, emoji 1, abbrev 2", "i don't know what the phone is worth rn but it's a nice looking phone that i wanna use for a couple of hours ..."),
    (4, "slang 4, emoji 2, abbrev 3, elong 1", "...lmk i wanna get a new iPhone idk if i should get the iphone 12 or the 12 pro i wanna keep my 16 pro btw " + PRAY),
]

b = [GRAD, f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']

# ---- masthead
b.append(icon(M, 64, 60))
b.append(t(M + 80, 105, "bussin-125m", 30, INK, 600, stretch="semi-condensed"))

# ---- headline (leading is generous so the g in "Slang" never touches the l in "dial")
b.append(t(M - 6, 272, "Slang is", 140, INK, 700, stretch="semi-condensed", spacing="-3"))
b.append(t(M - 6, 408, "a dial.", 140, INK, 700, stretch="semi-condensed", spacing="-3"))
sub = "A 125M-parameter language model, trained on free GPUs, that writes in the register you ask for."
for i, ln in enumerate(textwrap.wrap(sub, 58)):
    b.append(t(M, 468 + i * 36, ln, 27, SLATE, 400))

# ---- the ruler: position on the axis is the slang level
msg_y = 566
b.append(f'<text x="{M}" y="{msg_y}" font-family="{SANS}" font-size="23" fill="{SLATE}">One message, four registers: '
         f'<tspan font-family="{SERIF}" font-style="italic" font-weight="700" fill="{INK}" font-size="24">'
         f'{escape(chr(0x201C) + "thoughts on the new iphone" + chr(0x201D))}</tspan></text>')
X_AXIS = M + 46
Q_X = M + 112
Y0, STEP = 640, 96
top, bot = Y0 - 18, Y0 + 4 * STEP + 18
b.append(f'<line x1="{X_AXIS}" y1="{top}" x2="{X_AXIS}" y2="{bot}" stroke="{VIOLET}" stroke-width="3" stroke-linecap="round"/>')
b.append(t(X_AXIS, top - 14, "slang", 18, SLATE, 400, anchor="middle"))
for lv in range(5):
    y = Y0 + lv * STEP
    b.append(t(X_AXIS - 22, y + 7, str(lv), 20, SLATE, 600, anchor="end"))
    b.append(f'<line x1="{X_AXIS - 10}" y1="{y}" x2="{X_AXIS + 10}" y2="{y}" stroke="{VIOLET}" stroke-width="3" stroke-linecap="round"/>')
for lv, dials, quote in ROWS:
    y = Y0 + lv * STEP
    live = lv == 4
    if live:  # the single hot element: the knob that is live on the heaviest register
        b.append(f'<circle cx="{X_AXIS}" cy="{y}" r="17" fill="{MAGENTA}"/><circle cx="{X_AXIS}" cy="{y}" r="6.5" fill="{PAPER}"/>')
    else:
        b.append(f'<circle cx="{X_AXIS}" cy="{y}" r="9" fill="{INK}"/>')
    b.append(t(Q_X, y - 6, dials, 19, MAGENTA if live else SLATE, 600 if live else 400))
    for i, ln in enumerate(textwrap.wrap(quote, 62)[:3]):
        b.append(t(Q_X, y + 24 + i * 33, ln, 27, INK, 400, family=SERIF + "," + EMOJI))

# ---- proof band
BAND = 1124
b.append(f'<rect x="0" y="{BAND}" width="{W}" height="{H - BAND}" fill="{INK}"/>')
b.append(t(M - 4, BAND + 86, "0.146", 78, "#FFFFFF", 700, stretch="semi-condensed", spacing="-1"))
b.append(t(M + 196, BAND + 86, "vs 0.646", 78, "#7F8BB0", 700, stretch="semi-condensed", spacing="-1"))
b.append(t(M, BAND + 118, "register error: the model against a shuffled-request baseline, 200 held-out requests", 20, "#AEB7D0", 400))
b.append(t(W - M, BAND + 46, "7.8B tokens", 28, "#FFFFFF", 600, anchor="end", stretch="semi-condensed"))
b.append(t(W - M, BAND + 78, "on free Kaggle GPUs", 20, "#AEB7D0", 400, anchor="end"))
b.append(t(W - M, BAND + 116, "$0 spent", 28, "#FFFFFF", 600, anchor="end", stretch="semi-condensed"))
b.append(f'<line x1="{M}" y1="{BAND + 140}" x2="{W - M}" y2="{BAND + 140}" stroke="#2B3859" stroke-width="2"/>')
b.append(t(M, BAND + 178, "huggingface.co/Ravikishan/bussin-125m", 23, "#FFFFFF", 600))
b.append(t(M, BAND + 206, "github.com/Ravikisha/Bussin", 20, "#AEB7D0", 400))
b.append(t(W - M, BAND + 178, "Ravi Kishan", 23, "#FFFFFF", 600, anchor="end"))
b.append(t(W - M, BAND + 206, "ravikishan.me/blog", 20, "#AEB7D0", 400, anchor="end"))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-labelledby="t d"><title id="t">Slang is a dial: bussin-125m</title>'
       f"<desc id=\"d\">One message placed on a slang scale from 0 to 4, with the model's real outputs and the headline results</desc>"
       + "".join(b) + "</svg>")
(OUT / "poster-linkedin.svg").write_text(svg, encoding="utf-8")
print("ok")
