#!/usr/bin/env python3
"""Render 1200x630 social cards for every case study and post.

The cards use the site's own woff2 fonts, so a card looks like the page it links to.
Output goes to static/images/og/<slug>.png; layouts/partials/head.html picks the file
up automatically when it exists (og:image), otherwise the site-wide og-default.png is used.

    python3 scripts/make-og-cards.py            # every page
    python3 scripts/make-og-cards.py --check    # list what would be rendered
    python3 scripts/make-og-cards.py record-plus

Needs Chrome, Chromium, or Edge on PATH (headless screenshot). No Python packages.
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUT_DIR = ROOT / "static" / "images" / "og"
FONTS = ROOT / "static" / "fonts"

CARD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<style>
  @font-face {{ font-family: "Newsreader"; font-weight: 500 600; font-display: block;
    src: url("file://{fonts}/newsreader-latin.woff2") format("woff2"); }}
  @font-face {{ font-family: "DM Mono"; font-weight: 400; font-display: block;
    src: url("file://{fonts}/dm-mono-400.woff2") format("woff2"); }}
  @font-face {{ font-family: "DM Mono"; font-weight: 500; font-display: block;
    src: url("file://{fonts}/dm-mono-500.woff2") format("woff2"); }}
  * {{ box-sizing: border-box; margin: 0; }}
  html, body {{ width: 1200px; height: 630px; }}
  body {{
    background: #f4f1e9; color: #17201f;
    font-family: "DM Mono", monospace;
    display: grid; grid-template-rows: auto 1fr auto;
    padding: 64px 72px;
  }}
  .top {{ display: flex; justify-content: space-between; align-items: baseline; }}
  .eyebrow {{ font: 500 19px "DM Mono", monospace; letter-spacing: .12em; text-transform: uppercase; color: #63706e; }}
  .mark {{ font: 600 30px "DM Mono", monospace; letter-spacing: -.14em; color: #17201f; }}
  .mark span {{ color: #5c7800; }}
  .title {{ align-self: center; font: 500 84px/0.98 "Newsreader", Georgia, serif; letter-spacing: -.045em; max-width: 1010px; }}
  .title em {{ font-style: normal; color: #667d15; }}
  .foot {{ display: flex; justify-content: space-between; align-items: baseline; border-top: 1px solid rgba(23,32,31,.25); padding-top: 22px; }}
  .url {{ font: 500 18px "DM Mono", monospace; letter-spacing: .06em; }}
  .meta {{ font: 400 17px "DM Mono", monospace; letter-spacing: .05em; color: #63706e; }}
  .bar {{ width: 54px; height: 5px; background: #d4ff40; margin-bottom: 18px; }}
</style>
</head>
<body>
  <div class="top">
    <p class="eyebrow">{eyebrow}</p>
    <p class="mark">CD<span>.</span></p>
  </div>
  <h1 class="title">{title}</h1>
  <div>
    <div class="bar"></div>
    <div class="foot">
      <p class="url">clintdavis.us</p>
      <p class="meta">{meta}</p>
    </div>
  </div>
</body>
</html>
"""


def front_matter(md: Path) -> dict:
    """Minimal YAML front matter reader: scalars plus `- item` lists."""
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data: dict = {}
    key = None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and key:
            value = item.group(1).strip().strip("'\"")
            if not isinstance(data.get(key), list):
                data[key] = []
            data[key].append(value)
            continue
        kv = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", line)
        if kv:
            key = kv.group(1)
            value = kv.group(2).strip()
            if value.startswith("[") and value.endswith("]"):
                data[key] = [v.strip().strip("'\"") for v in value[1:-1].split(",") if v.strip()]
            elif value:
                data[key] = value.strip("'\"")
            else:
                data[key] = ""
    return data


def cards():
    """Yield (slug, eyebrow, title_html, meta) for every work page and post."""
    work = sorted(CONTENT.glob("work/*/index.md"), key=lambda p: front_matter(p).get("weight") or 999)
    for md in work:
        fm = front_matter(md)
        if fm.get("draft") in (True, "true"):
            continue
        meta_bits = [b for b in fm.get("meta", [])[1:]] if isinstance(fm.get("meta"), list) else []
        yield (
            md.parent.name,
            fm.get("eyebrow") or "Case study",
            fm.get("heading") or html.escape(fm.get("title", md.parent.name)),
            " · ".join(meta_bits) or "Case study",
        )

    for md in sorted(CONTENT.glob("blog/*.md")):
        if md.stem.startswith("_"):
            continue
        fm = front_matter(md)
        if fm.get("draft") in (True, "true"):
            continue
        tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
        bits = [fm.get("date", ""), " · ".join(tags)] if tags else [fm.get("date", "")]
        yield (
            md.stem,
            fm.get("kicker") or "Writing",
            html.escape(fm.get("title", md.stem)),
            " · ".join([b for b in bits if b]) or "Writing",
        )


def find_chrome() -> str | None:
    for name in (
        "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome",
        "microsoft-edge", "msedge", "chrome.exe", "msedge.exe",
    ):
        found = shutil.which(name)
        if found:
            return found
    for candidate in (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ):
        if Path(candidate).exists():
            return candidate
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("slugs", nargs="*", help="only render these slugs")
    ap.add_argument("--check", action="store_true", help="list cards without rendering")
    args = ap.parse_args()

    wanted = [c for c in cards() if not args.slugs or c[0] in args.slugs]
    if not wanted:
        print("No published case studies or posts found.", file=sys.stderr)
        return 1

    chrome = find_chrome()
    if args.check:
        for slug, eyebrow, title, meta in wanted:
            clean = re.sub(r"<[^>]+>", "", title)
            print(f"{slug:28} {eyebrow:18} {clean[:60]}")
        if not chrome:
            print("\n(no Chrome found on PATH: --check works, rendering will not)", file=sys.stderr)
        return 0

    if not chrome:
        print("Chrome/Chromium/Edge not found. Install one, or run this on the laptop.", file=sys.stderr)
        return 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="og-cards-"))
    for slug, eyebrow, title, meta in wanted:
        page = tmp / f"{slug}.html"
        page.write_text(
            CARD.format(
                fonts=FONTS.as_posix(),
                eyebrow=html.escape(eyebrow),
                title=title,
                meta=html.escape(meta),
            ),
            encoding="utf-8",
        )
        target = OUT_DIR / f"{slug}.png"
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                "--window-size=1200,630",
                f"--user-data-dir={tmp / 'profile'}",
                f"--screenshot={target}",
                page.as_uri(),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"{target.relative_to(ROOT)}  {target.stat().st_size // 1024} KB")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
