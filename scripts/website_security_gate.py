"""Small dependency-free security gate for this static website."""

from __future__ import annotations

import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".woff", ".woff2", ".ttf"}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "Stripe live key": re.compile(r"\bsk_live_[A-Za-z0-9]{20,}\b"),
    "Supabase secret key": re.compile(r"\bsb_secret_[A-Za-z0-9_-]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
}
SECRET_ASSIGNMENT = re.compile(
    r"(?im)^\s*(?:SUPABASE_SECRET_KEY|SUPABASE_SERVICE_ROLE_KEY|DATABASE_URL|VERCEL_TOKEN)\s*=\s*(\S+)"
)


class PublicEmbedChecker(HTMLParser):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.path = path
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in {"script", "iframe"}:
            return
        source = dict(attrs).get("src") or ""
        if source.startswith(("http://", "//")):
            self.errors.append(f"{self.path}: {tag} uses an insecure or protocol-relative source")


def main() -> int:
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\0")
    errors: list[str] = []
    checked = 0
    for raw_path in paths:
        if not raw_path:
            continue
        relative = raw_path.decode("utf-8")
        path = ROOT / relative
        if path.suffix.lower() in BINARY_EXTENSIONS or relative == "scripts/website_security_gate.py":
            continue
        data = path.read_bytes()
        if b"\0" in data:
            continue
        text = data.decode("utf-8", errors="replace")
        checked += 1
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{relative}: possible {label}")
        for match in SECRET_ASSIGNMENT.finditer(text):
            value = match.group(1)
            if not value.startswith(("example", "placeholder", "your_", "<")):
                errors.append(f"{relative}: committed non-empty secret assignment")
        if relative.startswith("public/"):
            if "SUPABASE_SECRET_KEY" in text or "SUPABASE_SERVICE_ROLE_KEY" in text:
                errors.append(f"{relative}: server credential reference in public output")
            if path.suffix == ".html":
                checker = PublicEmbedChecker(relative)
                checker.feed(text)
                errors.extend(checker.errors)
    for error in errors:
        print(error)
    print(f"Checked {checked} text files; security issues: {len(errors)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
