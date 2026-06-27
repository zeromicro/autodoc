#!/usr/bin/env python3
"""Validate documentation structure that Astro does not fully enforce."""

from __future__ import annotations

import re
import sys
from pathlib import Path


DOCS_ROOT = Path("src/content/docs")
LOCALES = ("zh-cn", "ko")
DOC_EXTS = {".md", ".mdx"}
SUPPORTED_FENCES = {
    "",
    "bash",
    "css",
    "diff",
    "dockerfile",
    "go",
    "html",
    "http",
    "ini",
    "js",
    "json",
    "json5",
    "groovy",
    "lua",
    "makefile",
    "markdown",
    "md",
    "mermaid",
    "plaintext",
    "proto",
    "protobuf",
    "sh",
    "shell",
    "sql",
    "text",
    "toml",
    "ts",
    "txt",
    "xml",
    "yaml",
    "yml",
}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---", re.DOTALL)
FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})([^\s`]*)", re.MULTILINE)


def doc_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and path.suffix in DOC_EXTS)


def rel_public_path(path: Path) -> str:
    rel = path.relative_to(DOCS_ROOT)
    parts = rel.parts
    if parts[0] in LOCALES:
        return str(Path(*parts[1:]))
    return str(rel)


def root_doc_files() -> list[Path]:
    files = []
    for path in doc_files(DOCS_ROOT):
        if path.relative_to(DOCS_ROOT).parts[0] not in LOCALES:
            files.append(path)
    return files


def has_frontmatter_field(frontmatter: str, field: str) -> bool:
    return re.search(rf"^{re.escape(field)}\s*:", frontmatter, re.MULTILINE) is not None


def check_frontmatter(errors: list[str]) -> None:
    for path in doc_files(DOCS_ROOT):
        content = path.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(content)
        rel = path.relative_to(DOCS_ROOT)
        if not match:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue

        frontmatter = match.group(1)
        for field in ("title", "description"):
            if not has_frontmatter_field(frontmatter, field):
                errors.append(f"{rel}: missing frontmatter field '{field}'")

        if path.name == "index.mdx" and path.parent in {DOCS_ROOT, DOCS_ROOT / "zh-cn", DOCS_ROOT / "ko"}:
            continue

        if not re.search(r"^\s*order\s*:", frontmatter, re.MULTILINE):
            errors.append(f"{rel}: missing frontmatter field 'sidebar.order'")


def check_locale_parity(errors: list[str]) -> None:
    english = {rel_public_path(path) for path in root_doc_files()}
    for locale in LOCALES:
        localized_root = DOCS_ROOT / locale
        localized = {str(path.relative_to(localized_root)) for path in doc_files(localized_root)}
        for missing in sorted(english - localized):
            errors.append(f"{locale}: missing localized page for {missing}")
        for extra in sorted(localized - english):
            errors.append(f"{locale}: extra localized page without English source {extra}")


def check_fences(errors: list[str]) -> None:
    for path in doc_files(DOCS_ROOT):
        content = path.read_text(encoding="utf-8")
        for match in FENCE_RE.finditer(content):
            lang = match.group(2).strip().lower()
            if lang not in SUPPORTED_FENCES:
                line = content.count("\n", 0, match.start()) + 1
                rel = path.relative_to(DOCS_ROOT)
                errors.append(f"{rel}:{line}: unsupported code fence language '{match.group(2)}'")


def main() -> int:
    errors: list[str] = []
    check_frontmatter(errors)
    check_locale_parity(errors)
    check_fences(errors)

    if errors:
        for error in errors:
            print(f"  {error}")
        print(f"\nTotal: {len(errors)} documentation structure error(s)")
        return 1

    print("Documentation structure checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
