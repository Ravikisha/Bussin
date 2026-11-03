"""Poster: the cover (the logo's faders, enlarged). Writes poster-cover.svg.
Run: python scripts/posters/cover.py [output_dir]   (then render with scripts/posters/render.py)"""
import sys
from html import escape
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # scripts/ (make_figures)
from make_figures import icon, GRAD

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "assets" / "posters"
OUT.mkdir(parents=True, exist_ok=True)
VIOLET, PAPER, LILAC, TRACK, TICK = "#5B43F5", "#EDF0F6", "#D3CCFF", "#7C69FA", "#9A8BFC"
MAGENTA, INK = "#E8397D", "#0F1A35"
SANS = "Bahnschrift, 'Segoe UI', Arial, sans-serif"
W, H, M = 1080, 1350, 84


def t(x, y, s, size, fill=PAPER, weight=400, anchor="start", stretch=None, spacing=None):
    st = f' font-stretch="{stretch}"' if stretch else ""
    ls = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{st}{ls}>{escape(s)}</text>')


b = [GRAD, f'<rect width="{W}" height="{H}" fill="{VIOLET}"/>']

# masthead: the logo on violet needs a paper tile so it stays legible
b.append(f'<rect x="{M}" y="64" width="60" height="60" rx="14" fill="{PAPER}"/>')
for i, lv in enumerate((0.75, 0.33, 0.67, 0.0, 0.0)):
    cx = M + 12 + i * 9
    ky = 112 - lv * 40
    b.append(f'<rect x="{cx - 1.5}" y="76" width="3" height="36" rx="1.5" fill="{TRACK}"/>')
    b.append(f'<rect x="{cx - 1.5}" y="{ky:.1f}" width="3" height="{112 - ky:.1f}" rx="1.5" fill="{VIOLET}"/>')
    b.append(f'<circle cx="{cx}" cy="{ky:.1f}" r="4.4" fill="{VIOLET}"/><circle cx="{cx}" cy="{ky:.1f}" r="1.7" fill="{PAPER}"/>')
b.append(t(M + 80, 105, "bussin-125m", 30, PAPER, 600, stretch="semi-condensed"))

# the title
for i, ln in enumerate(("I built a", "language model", "from scratch.")):
    b.append(t(M - 6, 296 + i * 122, ln, 126, PAPER, 700, stretch="semi-condensed", spacing="-3"))
b.append(t(M, 626, "Slang is a dial. Swipe for the idea, the build and the proof.", 27, LILAC, 400))

# the hero: five giant faders (the logo, enlarged). Casual setting: slang 3, emoji 1, abbrev 2, elong 0, formal 0.
names = ("slang", "emoji", "abbrev", "elong", "formal")
lvls = (3, 1, 2, 0, 0)
mx = (4, 3, 3, 2, 3)
top, bot = 706, 1162
span = W - 2 * M
for i, (n, lv, m) in enumerate(zip(names, lvls, mx)):
    cx = M + span / 10 + i * span / 5
    ky = bot - (bot - top) * lv / m
    for k in range(m + 1):                                   # level ticks, so it reads as an instrument
        y = bot - (bot - top) * k / m
        b.append(f'<line x1="{cx - 40:.1f}" y1="{y:.1f}" x2="{cx - 26:.1f}" y2="{y:.1f}" stroke="{TICK}" stroke-width="3" stroke-linecap="round"/>')
    b.append(f'<rect x="{cx - 14:.1f}" y="{top}" width="28" height="{bot - top}" rx="14" fill="{TRACK}"/>')
    if lv:
        b.append(f'<rect x="{cx - 14:.1f}" y="{ky:.1f}" width="28" height="{bot - ky:.1f}" rx="14" fill="{PAPER}"/>')
    hot = i == 0
    b.append(f'<circle cx="{cx:.1f}" cy="{ky:.1f}" r="40" fill="{MAGENTA if hot else PAPER}"/>'
             f'<circle cx="{cx:.1f}" cy="{ky:.1f}" r="15" fill="{PAPER if hot else VIOLET}"/>')
    b.append(t(cx, 1252, n, 26, PAPER, 600, anchor="middle", stretch="semi-condensed"))

# footer: name left, swipe cue right (a drawn chevron, not an arrow glyph)
b.append(t(M, 1318, "Ravi Kishan", 22, PAPER, 700, stretch="semi-condensed"))
b.append(t(W - M - 36, 1318, "Swipe", 22, PAPER, 700, anchor="end", stretch="semi-condensed"))
b.append(f'<polyline points="{W - M - 22},1304 {W - M - 8},1312 {W - M - 22},1320" fill="none" stroke="{PAPER}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-labelledby="t d"><title id="t">I built a language model from scratch: bussin-125m</title>'
       f'<desc id="d">Cover with five large register faders on a violet field and the title I built a language model from scratch</desc>'
       + "".join(b) + "</svg>")
(OUT / "poster-cover.svg").write_text(svg, encoding="utf-8")
print("ok")
