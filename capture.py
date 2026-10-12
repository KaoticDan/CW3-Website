"""Capture the public CW3 Webflow site for a local, reviewable replica."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path

from lxml import html


ROOT = "https://cw3-v1.webflow.io"
OUT = Path(__file__).parent
SOURCE = OUT / "source"
ASSETS = OUT / "public" / "assets"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CW3 local capture/1.0)"}
ASSET_HOSTS = {"cdn.prod.website-files.com", "assets-global.website-files.com", "fonts.googleapis.com", "fonts.gstatic.com"}
URL_RE = re.compile(r"https?://[^\s\"'<>\\]+")
sys.stdout.reconfigure(encoding="utf-8")


def get(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.read()


def local_path(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    ext = Path(urllib.parse.unquote(parsed.path)).suffix.lower()
    if not ext or len(ext) > 7:
        ext = ".bin"
    digest = hashlib.sha256(url.encode()).hexdigest()[:16]
    return f"/assets/{digest}{ext}"


def download(url: str, inventory: dict[str, str]) -> None:
    if url in inventory:
        return
    local = local_path(url)
    path = ASSETS / local.removeprefix("/assets/")
    if path.exists() and not local.endswith(".css"):
        inventory[url] = local
        return
    try:
        data = get(url)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        inventory[url] = local
        print("asset", local, len(data), url)
    except Exception as exc:
        print("FAILED asset", url, repr(exc))


def extract_urls(text: str) -> set[str]:
    result = set()
    for found in URL_RE.findall(text):
        url = found.rstrip(",;]")
        parsed = urllib.parse.urlparse(url)
        if parsed.hostname in ASSET_HOSTS and parsed.path not in ("", "/"):
            result.add(url)
    return result


def route_file(route: str) -> Path:
    route = route.strip("/")
    return SOURCE / route / "index.html" if route else SOURCE / "index.html"


def main() -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    queue = deque(["/"])
    try:
        sitemap = ET.fromstring(get(ROOT + "/sitemap.xml"))
        for loc in sitemap.findall(".//{*}loc"):
            parsed = urllib.parse.urlparse((loc.text or "").strip())
            if parsed.netloc == "cw3-v1.webflow.io":
                route = parsed.path or "/"
                if route not in queue:
                    queue.append(route)
    except Exception as exc:
        print("FAILED sitemap", repr(exc))
    pages: dict[str, str] = {}
    assets: dict[str, str] = {}
    while queue and len(pages) < 80:
        route = queue.popleft()
        if route in pages:
            continue
        url = ROOT + route
        try:
            body = get(url).decode("utf-8")
        except Exception as exc:
            print("FAILED page", route, repr(exc))
            continue
        tree = html.fromstring(body)
        title = tree.xpath("string(//title)")
        pages[route] = title
        path = route_file(route)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        print("page", route, len(body), title)
        for href in tree.xpath("//a/@href"):
            absolute = urllib.parse.urljoin(url, href)
            parsed = urllib.parse.urlparse(absolute)
            if parsed.netloc == "cw3-v1.webflow.io" and not parsed.query:
                child = parsed.path or "/"
                if child not in pages and child not in queue:
                    queue.append(child)
        for asset in extract_urls(body):
            download(asset, assets)

    # CSS often refers to more images and font files than are present in HTML.
    for _ in range(3):
        before = len(assets)
        for local in list(assets.values()):
            if local.endswith(".css"):
                css = (OUT / "public" / local.removeprefix("/")).read_text(encoding="utf-8", errors="ignore")
                for value in re.findall(r"url\(([^)]+)\)", css):
                    value = value.strip(" \"'")
                    if value.startswith("//"):
                        value = "https:" + value
                    if value.startswith("http"):
                        download(value, assets)
        if len(assets) == before:
            break

    # Keep captured source separate from the runnable copy.
    for route in pages:
        original = route_file(route).read_text(encoding="utf-8")
        rewritten = original
        for url, local in sorted(assets.items(), key=lambda item: len(item[0]), reverse=True):
            rewritten = rewritten.replace(url, local)
            rewritten = rewritten.replace(url.replace("&", "&amp;"), local)
        target = OUT / "public" / route.strip("/") / "index.html" if route != "/" else OUT / "public" / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rewritten, encoding="utf-8")
    for url, local in assets.items():
        if local.endswith(".css"):
            path = OUT / "public" / local.removeprefix("/")
            css = path.read_text(encoding="utf-8", errors="ignore")
            for remote, replacement in sorted(assets.items(), key=lambda item: len(item[0]), reverse=True):
                css = css.replace(remote, replacement)
            path.write_text(css, encoding="utf-8")
    (OUT / "source" / "inventory.json").write_text(json.dumps({"pages": pages, "assets": assets}, indent=2), encoding="utf-8")
    print("captured", len(pages), "pages", len(assets), "assets")


if __name__ == "__main__":
    main()
