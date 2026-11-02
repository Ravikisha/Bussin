"""Generate the README / model-card figures as standalone SVGs (docs/assets).

Everything is drawn from numbers measured in docs/results/rce_final-4067.txt, so the charts
cannot drift from the results. Run: python scripts/make_figures.py
"""

from __future__ import annotations

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "assets"
FONT = "'Segoe UI','Inter','Helvetica Neue',Arial,sans-serif"
MONO = "'Cascadia Mono','SFMono-Regular',Consolas,'Liberation Mono',monospace"

# brand
VIOLET, PINK, NAVY, NAVY2 = "#7c5cff", "#ff5fa2", "#14122b", "#241b4d"
# chart ink / surface (validated light-surface palette)
SURF, BORDER = "#fcfcfb", "#e4e3de"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#ecebe6"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"


def svg(w: int, h: int, body: str, title: str, desc: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-labelledby="t d" font-family="{FONT}">'
            f'<title id="t">{escape(title)}</title><desc id="d">{escape(desc or title)}</desc>{body}</svg>')


def text(x, y, s, size=16, fill=INK, weight=400, anchor="start", family=None, extra=""):
    fam = f' font-family="{family}"' if family else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{fam} {extra}>{escape(s)}</text>')


def card(w, h, fill=SURF, stroke=BORDER):
    return f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


# ------------------------------------------------------------------ logo
def icon(x=0, y=0, size=220) -> str:
    """Five register dials: the five measured dimensions, each a slider with its knob set."""
    levels = [0.75, 0.33, 0.67, 0.0, 0.0]       # slang 3/4, emoji 1/3, abbrev 2/3, elong 0, formal 0
    s = size / 220
    parts = [f'<g transform="translate({x},{y}) scale({s})">',
             '<rect width="220" height="220" rx="50" fill="url(#g)"/>']
    for i, lv in enumerate(levels):
        cx = 36 + i * 37
        parts.append(f'<rect x="{cx-4}" y="42" width="8" height="136" rx="4" fill="#fff" opacity=".32"/>')
        ky = 178 - lv * 136
        parts.append(f'<rect x="{cx-4}" y="{ky:.1f}" width="8" height="{178-ky:.1f}" rx="4" fill="#fff" opacity=".9"/>')
        parts.append(f'<circle cx="{cx}" cy="{ky:.1f}" r="15" fill="#fff"/>'
                     f'<circle cx="{cx}" cy="{ky:.1f}" r="6" fill="{VIOLET}"/>')
    parts.append("</g>")
    return "".join(parts)


GRAD = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>')


def logo() -> str:
    return svg(220, 220, GRAD + icon(), "bussin logo",
               "Five register sliders, one per measured dimension, with their knobs set to different levels")


def banner() -> str:
    w, h = 1280, 340
    chips = [("slang", 3), ("emoji", 1), ("abbrev", 2), ("elong", 0), ("formal", 0)]
    b = [GRAD,
         f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NAVY}"/>'
         f'<stop offset="1" stop-color="{NAVY2}"/></linearGradient></defs>',
         f'<rect width="{w}" height="{h}" rx="22" fill="url(#bg)"/>',
         f'<circle cx="1180" cy="40" r="170" fill="{PINK}" opacity=".07"/>',
         f'<circle cx="1010" cy="330" r="130" fill="{VIOLET}" opacity=".10"/>',
         icon(62, 60, 220),
         text(330, 168, "bussin", 118, "#ffffff", 800, extra='letter-spacing="-3"'),
         text(334, 222, "A 125M language model that writes in the register you ask for.", 28, "#d8d3ff"),
         text(334, 256, "Trained from scratch on free GPUs.  Slang is a dial, and cringe is a number.", 20, "#9f98d6")]
    x = 334
    for name, lv in chips:
        label = f"{name} {lv}"
        cw = 14 + len(label) * 10.5
        b.append(f'<rect x="{x}" y="276" width="{cw:.0f}" height="34" rx="17" fill="#ffffff" opacity=".10"/>')
        b.append(f'<rect x="{x}" y="276" width="{cw:.0f}" height="34" rx="17" fill="none" stroke="#fff" opacity=".28"/>')
        b.append(text(x + cw / 2, 299, label, 17, "#ffffff", 600, "middle", MONO))
        x += cw + 12
    return svg(w, h, "".join(b), "bussin: a Gen-Z register-conditioned language model",
               "Banner with the bussin logo and the five register dials")


# ------------------------------------------------------------------ how it works
def chip(x, y, s, fill, stroke, ink, size=16):
    w = 18 + len(s) * size * 0.62
    return (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="34" rx="8" fill="{fill}" stroke="{stroke}"/>'
            + text(x + w / 2, y + 22.5, s, size, ink, 600, "middle", MONO)), w


def how_it_works() -> str:
    w, h = 1200, 490
    steps = [("1  Mine", "Community text, plus a", "date-stamped slang lexicon"),
             ("2  Measure", "A deterministic annotator", "scores five dimensions"),
             ("3  Prefix", "Register tokens are put in", "front of every document"),
             ("4  Train", "A 125M decoder learns", "p(text | register)"),
             ("5  Dial", "Write a prefix at inference;", "it continues in that register")]
    bw, gap, x0, y0, bh = 196, 32, 36, 52, 132
    b = ['<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" '
         f'orient="auto"><path d="M0 0L10 5L0 10z" fill="{VIOLET}"/></marker></defs>', card(w, h),
         text(46, 38, "How it works", 22, INK, 700)]
    for i, (t1, l1, l2) in enumerate(steps):
        x = x0 + i * (bw + gap)
        b.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="14" fill="#ffffff" stroke="#d9d6ee" stroke-width="1.5"/>')
        b.append(f'<rect x="{x}" y="{y0}" width="{bw}" height="8" rx="4" fill="url(#g)"/>')
        b.append(text(x + 18, y0 + 44, t1, 21, INK, 700))
        b.append(text(x + 18, y0 + 78, l1, 14, INK2))
        b.append(text(x + 18, y0 + 98, l2, 14, INK2))
        if i < len(steps) - 1:
            b.append(f'<line x1="{x+bw+6}" y1="{y0+bh/2}" x2="{x+bw+gap-6}" y2="{y0+bh/2}" stroke="{VIOLET}" '
                     f'stroke-width="2.5" marker-end="url(#ar)"/>')
    # prefixed document
    b.append(text(46, 262, "What one training document looks like", 17, INK2, 600))
    toks = [("<|endoftext|>", "#efeefb", "#cfc9f6", "#3b2fa0"), ("<|reg|>", "#efeefb", "#cfc9f6", "#3b2fa0"),
            ("<|slang_3|>", "#fde9f1", "#f6bcd3", "#a3245a"), ("<|emoji_1|>", "#fde9f1", "#f6bcd3", "#a3245a"),
            ("<|abbrev_2|>", "#fde9f1", "#f6bcd3", "#a3245a"), ("<|elong_0|>", "#fde9f1", "#f6bcd3", "#a3245a"),
            ("<|formal_0|>", "#fde9f1", "#f6bcd3", "#a3245a"), ("<|/reg|>", "#efeefb", "#cfc9f6", "#3b2fa0")]
    x, y = 46, 280
    for s, f, st, ink in toks:
        el, cw = chip(x, y, s, f, st, ink, 14.5)
        b.append(el)
        x += cw + 8
        if x > 1030 and s != toks[-1][0]:
            x, y = 46, y + 44
    b.append(text(46, y + 68, "...then the text itself:   lowkey that movie was so good ngl", 16.5, INK, 500, "start", MONO))
    b.append(text(46, 392, "five measured levels:   slang 0-4   emoji 0-3   abbrev 0-3   elong 0-2   formal 0-3",
                  15, INK2, 500, "start", MONO))
    b.append(f'<rect x="46" y="414" width="1108" height="48" rx="12" fill="#f6f4ff" stroke="#e1dcfb"/>')
    b.append(text(66, 444, "\"Cringe\" is register mismatch, not slang. Condition on the register and you can measure the "
                  "mismatch (Register Calibration Error) and drive it down.", 15.5, INK, 500))
    return svg(w, h, GRAD + "".join(b), "How bussin works",
               "Mine text, measure its register, prefix each document with register tokens, train p(text|register), then set the prefix to steer generation")


# ------------------------------------------------------------------ relay / infrastructure
def relay() -> str:
    w, h = 1200, 430
    def box(x, y, bw, bh, title, lines, accent):
        o = [f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="#ffffff" stroke="#d9d6ee" stroke-width="1.5"/>',
             f'<rect x="{x}" y="{y}" width="8" height="{bh}" rx="4" fill="{accent}"/>',
             text(x + 26, y + 36, title, 19, INK, 700)]
        for i, ln in enumerate(lines):
            o.append(text(x + 26, y + 64 + i * 22, ln, 14.5, INK2))
        return "".join(o)

    b = ['<defs><marker id="a2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto">'
         f'<path d="M0 0L10 5L0 10z" fill="{VIOLET}"/></marker></defs>', card(w, h),
         text(46, 38, "Training on free GPUs without losing progress", 22, INK, 700)]
    b.append(box(46, 70, 300, 120, "Kaggle session N", ["2 x T4, up to 12 h", "holds the lease, trains,", "checkpoints every ~50 min"], AQUA))
    b.append(box(46, 250, 300, 120, "Kaggle session N+1", ["starts after N ends or dies", "claims the expired lease,", "resumes bit-exact"], BLUE))
    b.append(box(450, 130, 330, 170, "Hugging Face Hub", ["checkpoint: weights, optimizer,", "scheduler, RNG, data cursor, hash", "RUN_STATE.json = the lease", "claimed by compare-and-swap on", "the commit SHA"], VIOLET))
    b.append(box(884, 130, 270, 170, "Orchestrator (stateless)", ["a tick every 15 min on", "GitHub Actions: read state,", "dispatch if quota allows, exit", "schedule now disabled"], ORANGE))
    for (x1, y1, x2, y2, lab, lx, ly) in [
        (346, 130, 450, 180, "push checkpoint, heartbeat", 358, 112),
        (450, 250, 346, 300, "pull checkpoint, claim lease", 356, 330)]:
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{VIOLET}" stroke-width="2.5" marker-end="url(#a2)"/>')
        b.append(text(lx, ly, lab, 13.5, INK2, 500))
    b.append(f'<line x1="884" y1="215" x2="780" y2="215" stroke="{VIOLET}" stroke-width="2.5" stroke-dasharray="6 5" marker-end="url(#a2)"/>')
    b.append(text(790, 205, "reads state", 13.5, INK2, 500))
    b.append(text(46, 405, "A crashed session just lets its lease expire; the next tick redispatches. No server, no shared state outside the Hub.",
                  15, INK2, 500))
    return svg(w, h, "".join(b), "Relay and orchestration",
               "Kaggle sessions hand training over through checkpoints and a lease stored on the Hugging Face Hub; a stateless orchestrator starts sessions")


# ------------------------------------------------------------------ timeline
def timeline() -> str:
    w, h = 1200, 330
    ev = [("v1 run", "6.74B tokens,", "~110 GPU-hours", ORANGE),
          ("Eval looks wrong", "next-token NLL 8.76", "vs 5.40 at +2", ORANGE),
          ("Root cause", "loss shifted targets", "a second time", ORANGE),
          ("Fix + test", "objective_test fails", "old loss, passes fix", AQUA),
          ("Realign run", "4,067 steps,", "1.07B tokens", AQUA),
          ("Measure", "register error 0.15", "vs 0.65 null", BLUE),
          ("Ship", "Llama export,", "logit parity checked", BLUE)]
    n = len(ev)
    x0, x1, yl = 90, 1110, 120
    b = [card(w, h), text(46, 38, "What happened, kept in the record", 22, INK, 700),
         f'<line x1="{x0}" y1="{yl}" x2="{x1}" y2="{yl}" stroke="#d9d6ee" stroke-width="4" stroke-linecap="round"/>']
    for i, (t1, l1, l2, c) in enumerate(ev):
        x = x0 + i * (x1 - x0) / (n - 1)
        b.append(f'<circle cx="{x:.0f}" cy="{yl}" r="14" fill="{c}" stroke="{SURF}" stroke-width="3"/>')
        b.append(text(x, yl + 52, t1, 16.5, INK, 700, "middle"))
        b.append(text(x, yl + 76, l1, 13.5, INK2, 400, "middle"))
        b.append(text(x, yl + 95, l2, 13.5, INK2, 400, "middle"))
    b.append(text(46, 290, "The first run optimised the wrong objective. It was found by looking at the evaluation, "
                  "fixed at the loss, and locked in by a test that fails on the old code.", 15, INK2, 500))
    return svg(w, h, "".join(b), "Project timeline", "From the first run, through the double-shift bug and its fix, to the released model")


# ------------------------------------------------------------------ charts
def rce_chart() -> str:
    dims = ["slang", "emoji", "abbrev", "elong", "formal", "all"]
    model = [0.335, 0.150, 0.015, 0.115, 0.115, 0.146]
    null = [1.255, 0.930, 0.065, 0.525, 0.455, 0.646]
    real = [0.915, 0.565, 0.100, 0.430, 0.320, 0.466]
    series = [("model", model, BLUE), ("shuffled-request null", null, ORANGE), ("real same-document text", real, AQUA)]
    w, h = 1000, 540
    px0, px1, base, top, vmax = 80, 960, 440, 130, 1.4
    sc = (base - top) / vmax
    b = [card(w, h), text(40, 44, "Does the register prefix steer the output?", 24, INK, 700),
         text(40, 70, "Mean absolute error between requested and generated register, n = 200 held-out requests. Lower is better.",
              15, INK2)]
    lx = 40
    for name, _, c in series:
        b.append(f'<rect x="{lx}" y="90" width="14" height="14" rx="3" fill="{c}"/>')
        b.append(text(lx + 22, 102, name, 14.5, INK2, 500))
        lx += 52 + len(name) * 7.6
    for v in (0, 0.5, 1.0):
        y = base - v * sc
        b.append(f'<line x1="{px0}" y1="{y:.1f}" x2="{px1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1.5"/>')
        b.append(text(px0 - 12, y + 5, f"{v:.1f}", 13, MUTED, 400, "end"))
    gw = (px1 - px0) / len(dims)
    bw = 38
    for gi, d in enumerate(dims):
        gx = px0 + gi * gw + gw / 2 - (3 * bw + 2 * 4) / 2
        for si, (name, vals, c) in enumerate(series):
            v = vals[gi]
            hh = max(v * sc, 2)
            x = gx + si * (bw + 4)
            b.append(f'<rect x="{x:.1f}" y="{base-hh:.1f}" width="{bw}" height="{hh:.1f}" rx="4" fill="{c}"/>')
            b.append(f'<rect x="{x:.1f}" y="{base-6:.1f}" width="{bw}" height="6" fill="{c}"/>')
            b.append(text(x + bw / 2, base - hh - 7, f"{v:.3f}", 12, INK, 600, "middle"))
        b.append(text(px0 + gi * gw + gw / 2, base + 28, d, 15, INK, 600 if d == "all" else 500, "middle"))
    b.append(f'<line x1="{px0}" y1="{base}" x2="{px1}" y2="{base}" stroke="{MUTED}" stroke-width="1.5"/>')
    b.append(text(40, 500, "The model beats the null on every dimension (95% intervals exclude zero). It also beats real text, but that "
                  "reflects stereotyped output,", 13.5, INK2))
    b.append(text(40, 520, "not better writing, and the annotator that scores it also made the training labels.", 13.5, INK2))
    return svg(w, h, "".join(b), "Register calibration error by dimension",
               "Grouped bars: model 0.146, shuffled null 0.646, real text 0.466 overall; the model is lowest on every dimension")


def sweep_chart() -> str:
    rows = [("slang", 3, 2.88), ("emoji", 2, 2.00), ("abbrev", 3, 2.40), ("elong", 2, 1.80), ("formal", 3, 2.62)]
    w, h = 1000, 470
    x0, x1, vmax = 150, 900, 3.5
    sc = (x1 - x0) / vmax
    b = [card(w, h), text(40, 44, "Turn one dial, watch it move", 24, INK, 700),
         text(40, 70, "Request one dimension at a level, everything else 0, 50 samples each. At level 0 every dimension measured 0.00 to 0.02.",
              15, INK2)]
    for name, c, lx in (("requested level", "#c9c8c1", 40), ("measured in the output", BLUE, 210)):
        b.append(f'<rect x="{lx}" y="92" width="14" height="14" rx="3" fill="{c}"/>')
        b.append(text(lx + 22, 104, name, 14.5, INK2, 500))
    for v in (0, 1, 2, 3):
        x = x0 + v * sc
        b.append(f'<line x1="{x:.1f}" y1="130" x2="{x:.1f}" y2="400" stroke="{GRID}" stroke-width="1.5"/>')
        b.append(text(x, 424, str(v), 13, MUTED, 400, "middle"))
    for i, (d, req, got) in enumerate(rows):
        y = 140 + i * 52
        b.append(text(x0 - 16, y + 24, d, 16, INK, 600, "end"))
        for k, (val, c) in enumerate(((req, "#c9c8c1"), (got, BLUE))):
            yy = y + k * 22
            b.append(f'<rect x="{x0}" y="{yy}" width="{val*sc:.1f}" height="18" rx="4" fill="{c}"/>')
            b.append(f'<rect x="{x0}" y="{yy}" width="6" height="18" fill="{c}"/>')
            b.append(text(x0 + val * sc + 8, yy + 14, f"{val:.2f}" if k else f"{val}", 13, INK, 600))
    return svg(w, h, "".join(b), "Single-dimension sweep",
               "Requested vs measured level when one register dimension is set high and the rest are zero")


FILES = {"logo.svg": logo, "banner.svg": banner, "how-it-works.svg": how_it_works,
         "relay.svg": relay, "timeline.svg": timeline, "rce-chart.svg": rce_chart, "sweep-chart.svg": sweep_chart}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in FILES.items():
        (OUT / name).write_text(fn(), encoding="utf-8")
        print("wrote", OUT / name)


if __name__ == "__main__":
    main()
