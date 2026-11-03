# Posters and blog images

Generators for every share image and blog figure, so nothing depends on a one-off script.

| script | writes |
|---|---|
| `cover.py` | `poster-cover.svg`, the opener |
| `idea.py` | `poster-idea.svg`, "Same words. Different register." |
| `build_line.py` | `poster-linkedin-2.svg`, "Built end to end." |
| `ruler.py` | `poster-linkedin.svg`, the slang ruler |
| `blog_images.py` | `cover2.svg`, `milestones.svg`, `rce-chart2.svg` (blog) |
| `render.py` | renders the poster SVGs to 2x PNGs (headless Edge or Chrome) |

```bash
python scripts/posters/cover.py            # writes docs/assets/posters/poster-cover.svg
python scripts/posters/render.py           # SVG to 2160x2700 PNG
```

Posters are 1080x1350 (4:5). They use Bahnschrift and Georgia, so render on Windows. Every quote on them is real model
output from `docs/results/`, and every number comes from the measured results.
