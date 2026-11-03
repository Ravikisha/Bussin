"""Render the poster SVGs to 2x PNGs with headless Edge or Chrome.

Run: python scripts/posters/render.py [svg_dir]    (default: docs/assets/posters)
The posters use the Windows fonts Bahnschrift and Georgia, so render on Windows.
"""
import re
import subprocess
import sys
from pathlib import Path

SVG_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2] / "docs" / "assets" / "posters"
BROWSERS = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe"]
exe = next((b for b in BROWSERS if Path(b).exists()), None)
if exe is None:
    raise SystemExit("Edge or Chrome not found")
for svg in sorted(SVG_DIR.glob("poster-*.svg")):
    m = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg.read_text(encoding="utf-8"))
    w, h = int(m.group(1)), int(m.group(2))
    png = svg.with_suffix(".png")
    subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size={w},{h}", f"--screenshot={png}", svg.resolve().as_uri()],
                   check=True, capture_output=True, timeout=180)
    print("rendered", png.name)
