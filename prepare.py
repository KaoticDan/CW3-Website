"""Build static clean-URL pages from the immutable Webflow source capture."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
SOURCE = ROOT / "source"
inventory = json.loads((SOURCE / "inventory.json").read_text(encoding="utf-8"))

for route in inventory["pages"]:
    source = SOURCE / route.strip("/") / "index.html" if route != "/" else SOURCE / "index.html"
    content = source.read_text(encoding="utf-8")
    for remote, local in sorted(inventory["assets"].items(), key=lambda pair: len(pair[0]), reverse=True):
        content = content.replace(remote, local).replace(remote.replace("&", "&amp;"), local)

    # Webflow's runtime uses this flag to inject its "Made in Webflow" badge.
    content = content.replace(' data-wf-status="1"', '')

    # The header uses two identical images for a Webflow hover swap. The second
    # peeks below the first at desktop widths, so keep one stable linked logo.
    def single_header_logo(match: re.Match[str]) -> str:
        opening = re.sub(r' data-w-id="[^"]+"', '', match.group(1))
        return opening + match.group(2)

    content, logo_count = re.subn(
        r'(<a[^>]*class="brand-logo[^\"]*"[^>]*>)(<img[^>]*class="logo"[^>]*/>)<img[^>]*class="logo hide"[^>]*/>',
        single_header_logo,
        content,
        count=1,
    )

    # Preserve absolute Open Graph URLs until the deployment has its final domain.
    original = source.read_text(encoding="utf-8")
    for prop in ("og:image", "twitter:image"):
        match = re.search(rf'<meta content="([^"]+)" (?:property|name)="{prop}"', original)
        if match:
            content = re.sub(
                rf'(<meta content=")[^"]+(" (?:property|name)="{prop}")',
                lambda m: m.group(1) + match.group(1) + m.group(2),
                content,
                count=1,
            )

    content = content.replace("</head>", '<link href="/cw3-overrides.css" rel="stylesheet"/></head>', 1)
    content = content.replace("</body>", '<script src="/cw3-site.js" defer></script></body>', 1)
    # The Webflow footer points these two labels to a placeholder and the Work page.
    content = re.sub(r'(<a href=")#(" class="button-with-line _2 w-inline-block"><div class="button-text-wrapper"><div class="button-text">Hire</div>)', r'\1/hire\2', content)
    content = re.sub(r'(<a href=")/work("[^>]*><div class="button-text-wrapper"><div class="button-text">About</div>)', r'\1/about\2', content)
    # The footer's Author link is a placeholder and has no destination.
    content = re.sub(
        r'<a href="#" class="button-with-line _2 w-inline-block"><div class="button-text-wrapper"><div class="button-text">Author</div><div class="button-text">Author</div></div><div class="button-line-first"><div class="button-line-overlay"></div></div></a>',
        '',
        content,
        count=1,
    )

    target = PUBLIC / (route.strip("/") + ".html") if route != "/" else PUBLIC / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    old_directory_index = PUBLIC / route.strip("/") / "index.html" if route != "/" else None
    if old_directory_index and old_directory_index.exists():
        old_directory_index.unlink()

# Rewrite CSS references to the downloaded images and fonts.
for local in inventory["assets"].values():
    if local.endswith(".css"):
        path = PUBLIC / local.removeprefix("/")
        css = path.read_text(encoding="utf-8")
        for remote, replacement in sorted(inventory["assets"].items(), key=lambda pair: len(pair[0]), reverse=True):
            css = css.replace(remote, replacement)
        path.write_text(css, encoding="utf-8")

print(f"Prepared {len(inventory['pages'])} routes")
