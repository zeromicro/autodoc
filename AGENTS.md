# go-zero Documentation Agent Guide

This repository is the source for `go-zero.dev`, built with Astro and Starlight.

For documentation writing rules, start with [.github/copilot-instructions.md](.github/copilot-instructions.md). For long-running or source-driven documentation improvements, also use the documentation memory in [docs-memory/](docs-memory/).

## Documentation Memory Workflow

Use the memory workflow when a task is based on release notes, source-code changes, issues, PRs, external articles, user reports, or repeated questions.

1. Put immutable source material under `docs-memory/sources/`.
2. Read `docs-memory/index.md` before editing public docs.
3. Update affected public pages under `src/content/docs/`.
4. Keep English, Simplified Chinese, and Korean pages structurally aligned unless the task explicitly targets one locale.
5. Update `docs-memory/index.md` when a new important topic, page family, or source packet is added.
6. Append a dated entry to `docs-memory/log.md` describing the ingest, query, or lint pass.

Public documentation remains under `src/content/docs/`; `docs-memory/` is an agent-maintained workbench for source tracking, synthesis, and maintenance history.
