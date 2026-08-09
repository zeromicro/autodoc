#!/usr/bin/env python3
"""Check internal Markdown links in Starlight docs.

The checker intentionally ignores fenced code blocks. The previous regex-only
implementation reported Go generic signatures and code examples as broken links,
which made the check too noisy to enforce in CI.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


DOCS_ROOT = Path("src/content/docs")
PUBLIC_ROOT = Path("public")
DOC_EXTS = {".md", ".mdx"}
ASSET_EXTS = {
    ".avif",
    ".gif",
    ".jpeg",
    ".jpg",
    ".pdf",
    ".png",
    ".svg",
    ".webp",
    ".zip",
}

LINK_RE = re.compile(r"!?\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
REF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
HTML_LINK_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
FENCE_RE = re.compile(r"(^|\n)[ \t]*(`{3,}|~{3,})[^\n]*\n.*?(?:\n[ \t]*\2)(?=\n|$)", re.DOTALL)
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
EXPLICIT_ID_RE = re.compile(r"\bid=[\"']([^\"']+)[\"']")
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def strip_fenced_code(markdown: str) -> str:
    return FENCE_RE.sub("\n", markdown)


def slugify_heading(heading: str) -> str:
    value = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", heading)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("`", "").lower().strip()
    value = re.sub(r"[^\w\- ]", "", value, flags=re.UNICODE)
    return re.sub(r"[ \t]+", "-", value)


def heading_ids(markdown: str) -> set[str]:
    body = FRONTMATTER_RE.sub("", strip_fenced_code(markdown), count=1)
    ids = set(EXPLICIT_ID_RE.findall(body))
    seen: dict[str, int] = {}
    for heading in HEADING_RE.findall(body):
        base = slugify_heading(heading)
        if not base:
            continue
        occurrence = seen.get(base, 0)
        seen[base] = occurrence + 1
        ids.add(base if occurrence == 0 else f"{base}-{occurrence}")
    return ids


def iter_doc_files() -> list[Path]:
    return sorted(
        path
        for path in DOCS_ROOT.rglob("*")
        if path.is_file() and path.suffix in DOC_EXTS
    )


def is_external(link: str) -> bool:
    parsed = urlparse(link)
    return parsed.scheme in {"http", "https", "mailto", "tel"}


def is_asset(path: str) -> bool:
    return Path(path).suffix.lower() in ASSET_EXTS


def candidate_docs(path: Path) -> list[Path]:
    if path.suffix in DOC_EXTS:
        base = path.with_suffix("")
        return [path, base / "index.md", base / "index.mdx"]
    return [
        path,
        Path(f"{path}.md"),
        Path(f"{path}.mdx"),
        path / "index.md",
        path / "index.mdx",
    ]


def route_to_doc(path: str) -> Path:
    route = path.strip("/")
    if route in {"", "docs"}:
        return DOCS_ROOT / "index.mdx"
    return DOCS_ROOT / route


def resolve_links(source: Path, link: str) -> list[Path] | None:
    parsed = urlparse(link)
    target = unquote(parsed.path)

    if not target or target.startswith("#") or is_external(link):
        return None

    if target.startswith("/"):
        public_file = PUBLIC_ROOT / target.lstrip("/")
        if is_asset(target) or public_file.exists():
            return [public_file]
        return [route_to_doc(target)]

    if source.stem == "index":
        route_base = source.parent
    else:
        # Starlight renders a file page as a directory route:
        # reference/changelog.md -> /reference/changelog/.
        # Relative links are resolved by the browser from that route.
        route_base = source.with_suffix("")

    source_base = source.parent
    candidates = []
    for base in (source_base, route_base):
        resolved_absolute = (base / target).resolve()
        try:
            resolved = resolved_absolute.relative_to(Path.cwd())
        except ValueError:
            resolved = Path("__outside_repo__") / resolved_absolute.as_posix().lstrip("/")
        if resolved not in candidates:
            candidates.append(resolved)
    return candidates


def exists(source: Path, link: str) -> bool:
    resolved_paths = resolve_links(source, link)
    if resolved_paths is None:
        return True

    for resolved in resolved_paths:
        if is_asset(str(resolved)) and resolved.exists():
            return True

        if resolved.exists() and resolved.is_file():
            return True

        if any(candidate.exists() and candidate.is_file() for candidate in candidate_docs(resolved)):
            return True

    return False


def existing_doc(source: Path, link: str) -> Path | None:
    parsed = urlparse(link)
    if is_external(link):
        return None
    if not parsed.path:
        return source

    for resolved in resolve_links(source, link) or []:
        if resolved.exists() and resolved.is_file() and resolved.suffix in DOC_EXTS:
            return resolved
        for candidate in candidate_docs(resolved):
            if candidate.exists() and candidate.is_file() and candidate.suffix in DOC_EXTS:
                return candidate
    return None


def anchor_exists(source: Path, link: str) -> bool:
    fragment = unquote(urlparse(link).fragment)
    if not fragment or is_external(link):
        return True
    target = existing_doc(source, link)
    if target is None:
        return True  # The broken path is reported separately.
    return fragment in heading_ids(target.read_text(encoding="utf-8"))


def collect_links(markdown: str) -> list[str]:
    body = strip_fenced_code(markdown)
    links = [match.group(1) for match in LINK_RE.finditer(body)]
    links.extend(match.group(1) for match in REF_RE.finditer(body))
    links.extend(match.group(1) for match in HTML_LINK_RE.finditer(body))
    return links


def main() -> int:
    errors: list[tuple[str, str, str]] = []

    for path in iter_doc_files():
        markdown = path.read_text(encoding="utf-8")
        for link in collect_links(markdown):
            clean = link.strip("<>")
            if not exists(path, clean):
                errors.append((str(path.relative_to(DOCS_ROOT)), clean, "broken target"))
            elif not anchor_exists(path, clean):
                errors.append((str(path.relative_to(DOCS_ROOT)), clean, "missing anchor"))

    for rel_file, link, reason in sorted(set(errors)):
        print(f"  {rel_file} -> {link} ({reason})")

    print(f"\nTotal: {len(set(errors))} broken links")
    return 1 if errors else 0


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parents[1])
    sys.exit(main())
