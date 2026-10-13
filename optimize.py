"""Optimize the prepared static pages without changing the Webflow source capture.

Run after prepare.py. Requires Pillow for image conversion.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"

# Keep the original assets for a repeatable prepare.py run and for comparison.
# WebP files are used only where they save enough bytes to justify another file.
optimized: dict[str, str] = {}
dimensions: dict[str, tuple[int, int]] = {}
original_bytes = optimized_bytes = 0

for source in ASSETS.iterdir():
    if source.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue
    with Image.open(source) as image:
        dimensions[source.name] = image.size
        if source.stat().st_size < 20_000:
            continue
        # Small logos, flat artwork and transparent controls remain PNG.
        if source.suffix.lower() == ".png" and (image.mode in {"RGBA", "P"} or source.stat().st_size < 100_000):
            continue
        image = image.convert("RGB")
        image.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
        target = source.with_suffix(".webp")
        image.save(target, "WEBP", quality=83, method=6)
    if target.stat().st_size >= source.stat().st_size * 0.85:
        target.unlink()
        continue
    optimized[source.name] = target.name
    dimensions[target.name] = image.size
    original_bytes += source.stat().st_size
    optimized_bytes += target.stat().st_size

for source in ASSETS.glob("*.svg"):
    markup = source.read_text(encoding="utf-8")
    root = re.search(r"<svg\b[^>]*>", markup)
    if not root:
        continue
    opening = root.group(0)
    viewbox = re.search(r'viewBox="([\d.\s-]+)"', opening)
    if viewbox:
        numbers = [float(value) for value in viewbox.group(1).split()]
        if len(numbers) == 4 and numbers[2] > 0 and numbers[3] > 0:
            dimensions[source.name] = (round(numbers[2]), round(numbers[3]))
    else:
        width = re.search(r'\bwidth="(\d+(?:\.\d+)?)"', opening)
        height = re.search(r'\bheight="(\d+(?:\.\d+)?)"', opening)
        if width and height:
            dimensions[source.name] = (round(float(width.group(1))), round(float(height.group(1))))


def image_tag(match: re.Match[str]) -> str:
    tag = match.group(0)
    source = re.search(r'\bsrc="/assets/([^"]+)"', tag)
    if not source or source.group(1) not in dimensions:
        return tag
    width, height = dimensions[source.group(1)]
    existing_width = re.search(r'\bwidth="(\d+(?:\.\d+)?)"', tag)
    existing_height = re.search(r'\bheight="(\d+(?:\.\d+)?)"', tag)
    if existing_width and not existing_height:
        scaled_height = round(float(existing_width.group(1)) * height / width)
        tag = tag[:-2] + f' height="{scaled_height}"/>' if tag.endswith('/>') else tag[:-1] + f' height="{scaled_height}">'
    elif existing_height and not existing_width:
        scaled_width = round(float(existing_height.group(1)) * width / height)
        tag = tag[:-2] + f' width="{scaled_width}"/>' if tag.endswith('/>') else tag[:-1] + f' width="{scaled_width}">'
    elif not existing_width and not existing_height:
        values = f' width="{width}" height="{height}"'
        tag = tag[:-2] + values + '/>' if tag.endswith('/>') else tag[:-1] + values + '>'
    return tag


for path in PUBLIC.rglob("*.html"):
    html = path.read_text(encoding="utf-8")
    # WebFont.js downloads unused weights and duplicates the local Inter faces.
    html = re.sub(r'<script src="https://ajax\.googleapis\.com/ajax/libs/webfont/[^\"]+"[^>]*></script>', "", html)
    html = re.sub(r'<script type="text/javascript">WebFont\.load\(.*?</script>', "", html, count=1, flags=re.DOTALL)
    html = html.replace('<link href="https://fonts.googleapis.com" rel="preconnect"/>', "")
    html = html.replace('<link href="https://fonts.gstatic.com" rel="preconnect" crossorigin="anonymous"/>', "")
    for old, new in optimized.items():
        html = html.replace(f"/assets/{old}", f"/assets/{new}")
    html = re.sub(r"<img\b[^>]*>", image_tag, html)
    path.write_text(html, encoding="utf-8")

for path in ASSETS.glob("*.css"):
    css = path.read_text(encoding="utf-8")
    for old, new in optimized.items():
        css = css.replace(f"/assets/{old}", f"/assets/{new}")
    path.write_text(css, encoding="utf-8")

print(f"WebP images: {len(optimized)}; converted assets: {original_bytes:,} -> {optimized_bytes:,} bytes")
