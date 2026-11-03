"""Poster: the idea (three fader consoles, three voices). Writes poster-idea.svg.
Run: python scripts/posters/idea.py [output_dir]   (then render with scripts/posters/render.py)"""
import sys, textwrap
from html import escape
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # scripts/ (make_figures)
from make_figures import icon, GRAD

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "assets" / "posters"
OUT.mkdir(parents=True, exist_ok=True)
PAPER, INK, SLATE = "#EDF0F6", "#0F1A35", "#56617F"
VIOLET, MAGENTA, LILAC, PINK, TRACK = "#5B43F5", "#E8397D", "#DCD6FF", "#FFD3E3", "#2B3859"
SANS = "Bahnschrift, 'Segoe UI', Arial, sans-serif"
SERIF = "Georgia, Cambria, 'Times New Roman', serif"
SERIF_E = SERIF + ", 'Segoe UI Emoji'"
W, H, M = 1080, 1350, 84


def t(x, y, s, size, fill=INK, weight=400, family=SANS, anchor="start", stretch=None, spacing=None, style=None):
    st = f' font-stretch="{stretch}"' if stretch else ""
    ls = f' letter-spacing="{spacing}"' if spacing is not None else ""
    fs = f' font-style="{style}"' if style else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{st}{ls}{fs}>{escape(s)}</text>')


def console(x, y, title, levels):
    """Five faders: slang 0-4, emoji 0-3, abbrev 0-3, elong 0-2, formal 0-3. Panel 300 x 150."""
    mx = (4, 3, 3, 2, 3)
    names = ("slang", "emoji", "abbrev", "elong", "formal")
    o = [f'<rect x="{x}" y="{y}" width="300" height="150" rx="22" fill="{INK}"/>',
         t(x + 24, y + 34, title, 18, "#FFFFFF", 600, stretch="semi-condensed")]
    top, bot = y + 54, y + 114
    for i, (n, lv, m) in enumerate(zip(names, levels, mx)):
        cx = x + 48 + i * 51
        ky = bot - (bot - top) * lv / m
        o.append(f'<rect x="{cx - 3}" y="{top}" width="6" height="{bot - top}" rx="3" fill="{TRACK}"/>')
        if lv:
            o.append(f'<rect x="{cx - 3}" y="{ky:.1f}" width="6" height="{bot - ky:.1f}" rx="3" fill="{VIOLET}"/>')
        o.append(f'<circle cx="{cx}" cy="{ky:.1f}" r="10" fill="#FFFFFF"/><circle cx="{cx}" cy="{ky:.1f}" r="4" fill="{VIOLET}"/>')
        o.append(t(cx, y + 139, n, 15, "#C3CAE0", 400, anchor="middle"))
    return "".join(o)


def burst(x, y, w, h, step=24, depth=9):
    """Spiky speech-burst outline around a rectangle."""
    pts = []
    def edge(x0, y0, x1, y1, nx, ny):
        n = max(int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 // step), 2)
        for k in range(n):
            f = k / n
            d = depth if k % 2 else -depth * 0.2
            pts.append((x0 + (x1 - x0) * f + nx * d, y0 + (y1 - y0) * f + ny * d))
    edge(x, y, x + w, y, 0, -1); edge(x + w, y, x + w, y + h, 1, 0)
    edge(x + w, y + h, x, y + h, 0, 1); edge(x, y + h, x, y, -1, 0)
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)


def bubble(kind, x, cy, text_lines, w=520, h=150):
    y = cy - h / 2
    o = []
    if kind == "formal":
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>')
        o.append(f'<polygon points="{x + 3},{cy - 9} {x - 15},{cy + 6} {x + 3},{cy + 21}" fill="#FFFFFF"/>')
        o.append(f'<polyline points="{x + 1},{cy - 9} {x - 15},{cy + 6} {x + 1},{cy + 21}" fill="none" stroke="{INK}" stroke-width="2.5" stroke-linejoin="miter"/>')
    elif kind == "casual":
        o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="38" fill="{LILAC}"/>')
        o.append(f'<polygon points="{x + 8},{cy - 13} {x - 22},{cy + 4} {x + 8},{cy + 22}" fill="{LILAC}"/>')
    else:
        o.append(f'<polygon points="{burst(x, y, w, h)}" fill="{PINK}" stroke="{MAGENTA}" stroke-width="3" stroke-linejoin="round"/>')
        o.append(f'<polygon points="{x + 7},{cy - 13} {x - 24},{cy + 4} {x + 7},{cy + 22}" fill="{PINK}"/>')
        o.append(f'<polyline points="{x + 4},{cy - 13} {x - 24},{cy + 4} {x + 4},{cy + 22}" fill="none" stroke="{MAGENTA}" stroke-width="3" stroke-linejoin="round"/>')
    n = len(text_lines)
    y0 = cy - (n - 1) * 16 + 8
    for i, ln in enumerate(text_lines):
        o.append(t(x + 34, y0 + i * 32, ln, 25, INK, 400, family=SERIF_E))
    return "".join(o)


b = [GRAD, f'<rect width="{W}" height="{H}" fill="{PAPER}"/>']
# masthead
b.append(icon(M, 64, 60))
b.append(t(M + 80, 105, "bussin-125m", 30, INK, 600, stretch="semi-condensed"))
# headline
b.append(t(M - 5, 270, "Same words.", 112, INK, 700, stretch="semi-condensed", spacing="-2"))
b.append(t(M - 5, 392, "Different register.", 112, INK, 700, stretch="semi-condensed", spacing="-2"))
sub = "Most language models write in one average voice. This one lets you set the voice before it writes."
for i, ln in enumerate(textwrap.wrap(sub, 62)):
    b.append(t(M, 454 + i * 36, ln, 27, SLATE, 400))

# three channels: a console on the left, the voice it produced on the right
ROWS = [
    ("formal", "the boardroom", (0, 0, 0, 0, 3), ["I've been meaning to ask if you're okay", "with this particular pizza..."]),
    ("casual", "the group chat", (3, 1, 2, 0, 0), ["for me pineapple is literally the best", "pizza because its easy to get in and", "out of ..."]),
    ("hype", "the livestream", (4, 2, 3, 1, 0), ["...i'm not actually gonna say pineapple", "on pizza is bad so yeah, i love", "pineapple on pizza bro \U0001F62D\U0001F62D\U0001F62D"]),
]
CY0, GAP = 668, 196
BX = 496
for i, (kind, scene, lv, lines) in enumerate(ROWS):
    cy = CY0 + i * GAP
    b.append(console(M, cy - 75, scene, lv))
    # patch cable from the console jack to the bubble
    jack_x, jack_y = M + 300, cy
    b.append(f'<path d="M{jack_x} {jack_y} C{jack_x + 40} {jack_y} {BX - 54} {jack_y} {BX - 24} {jack_y}" fill="none" stroke="{VIOLET}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'<circle cx="{jack_x}" cy="{jack_y}" r="7" fill="{VIOLET}"/><circle cx="{jack_x}" cy="{jack_y}" r="3" fill="{PAPER}"/>')
    b.append(bubble(kind, BX, cy, lines, w=W - M - BX))

# the idea, said once
b.append(t(M, 1226, "Cringe is not slang.", 40, INK, 400, family=SERIF, style="italic"))
b.append(t(M, 1274, "It is the wrong register in the wrong room.", 40, INK, 400, family=SERIF, style="italic"))
b.append(f'<line x1="{M}" y1="1298" x2="{W - M}" y2="1298" stroke="#C9D0E0" stroke-width="2"/>')
b.append(t(M, 1330, "Ravi Kishan", 21, INK, 700, stretch="semi-condensed"))
b.append(t(W - M, 1330, "huggingface.co/Ravikishan/bussin-125m", 19, SLATE, 400, anchor="end"))

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
       f'aria-labelledby="t d"><title id="t">Same words, different register: bussin-125m</title>'
       f"<desc id=\"d\">Three fader consoles, each connected to a speech bubble whose shape matches its register: formal, casual and hype</desc>"
       + "".join(b) + "</svg>")
(OUT / "poster-idea.svg").write_text(svg, encoding="utf-8")
print("ok")
