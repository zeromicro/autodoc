# Documentation Memory

This directory adapts the LLM-wiki pattern for the go-zero documentation site.

## Layers

| Layer | Path | Ownership | Purpose |
| --- | --- | --- | --- |
| Raw sources | `docs-memory/sources/` | Human/automation curated, immutable after ingest | Release notes, issue summaries, PR notes, source-code findings, migration reports, community questions |
| Public wiki | `src/content/docs/` | Reviewed documentation content | Starlight pages published on `go-zero.dev` |
| Memory index | `docs-memory/index.md` | Agent-maintained | Compact map of important doc areas, source packets, and known gaps |
| Memory log | `docs-memory/log.md` | Append-only | Timeline of ingests, queries, lint passes, and cross-page maintenance |
| Drift reports | `docs-memory/reports/` | Automation-generated, human-reviewed | Maps upstream go-zero source changes to docs that may need updates |

## Operating Rules

- Treat raw source packets as evidence. Do not rewrite them after ingest; add a new packet if the source changes.
- Update public docs from source-backed understanding, not from a single generated answer.
- Prefer improving existing pages over creating duplicates.
- When adding or moving public pages, keep English, `zh-cn`, and `ko` paths aligned unless a task is locale-specific.
- Record every source-driven documentation change in `log.md`.
- Use `index.md` as the first stop before a broad documentation edit.
- Treat drift reports as review queues, not proof that the public docs are wrong.

## Source Packet Format

Create one Markdown file per source packet under `docs-memory/sources/`:

```markdown
---
title: Short source title
source_type: release | issue | pr | code | discussion | external
source_url: https://example.com
captured_at: YYYY-MM-DD
related_docs:
  - src/content/docs/path/to/page.md
status: new | ingested | superseded
---

## Key Facts

- Fact that should influence docs.

## Documentation Impact

- Page or topic that may need an update.

## Open Questions

- Anything that needs verification before publishing.
```

## Maintenance Loop

1. Ingest one source packet.
2. Identify affected pages from `index.md` and `src/content/docs/`.
3. Edit the public docs.
4. Run `npm run build` and relevant link checks.
5. Update `index.md` if the map changed.
6. Append a `log.md` entry.

## Drift Reports

`check-go-zero-drift.yml` periodically compares upstream `zeromicro/go-zero` refs and writes reports under `docs-memory/reports/`.

Use a report like this:

1. Review each matched documentation area.
2. Read the upstream files before editing public docs.
3. Update English docs first, then mirror the change into `zh-cn` and `ko`.
4. Run `npm run validate` and `npm run build`.
