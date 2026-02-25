#!/usr/bin/env python3
"""Check for broken internal links in markdown docs."""
import os
import re

docs_root = "src/content/docs"
errors = []

for root, dirs, files in os.walk(docs_root):
    for f in files:
        if not f.endswith(".md") and not f.endswith(".mdx"):
            continue
        filepath = os.path.join(root, f)
        with open(filepath) as fh:
            content = fh.read()
        for m in re.finditer(r"\[([^\]]*)\]\(([^)]+)\)", content):
            text, link = m.group(1), m.group(2)
            if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                continue
            link_path = link.split("#")[0]
            if not link_path:
                continue
            if any(link_path.endswith(ext) for ext in [".png", ".jpg", ".svg", ".gif", ".webp"]):
                continue
            file_dir = os.path.dirname(filepath)
            resolved = os.path.normpath(os.path.join(file_dir, link_path))
            found = False
            candidates = [resolved]
            if resolved.endswith(".md") or resolved.endswith(".mdx"):
                base = resolved.rsplit(".", 1)[0]
                candidates.append(os.path.join(base, "index.md"))
            else:
                candidates.append(resolved + ".md")
                candidates.append(resolved + ".mdx")
                candidates.append(os.path.join(resolved, "index.md"))
                candidates.append(os.path.join(resolved, "index.mdx"))
            for c in candidates:
                if os.path.exists(c):
                    found = True
                    break
            if not found:
                rel_file = os.path.relpath(filepath, docs_root)
                errors.append((rel_file, link))

seen = set()
for e in sorted(errors):
    if e not in seen:
        seen.add(e)
        print(f"  {e[0]}  ->  {e[1]}")

print(f"\nTotal: {len(seen)} broken links")
