# Documentation Memory Index

This is the compact navigation map for agent-assisted documentation work. Keep it short enough to read before a documentation edit.

## Public Documentation Map

| Area | English path | Localized mirrors | Purpose |
| --- | --- | --- | --- |
| Concepts | `src/content/docs/concepts/` | `zh-cn/concepts/`, `ko/concepts/` | Architecture, design principles, project structure, glossary |
| Getting Started | `src/content/docs/getting-started/` | `zh-cn/getting-started/`, `ko/getting-started/` | Installation and first successful use |
| Guides | `src/content/docs/guides/` | `zh-cn/guides/`, `ko/guides/` | Task-oriented HTTP, gRPC, database, deployment, queue, gateway, cron, MCP, and microservice guides |
| Components | `src/content/docs/components/` | `zh-cn/components/`, `ko/components/` | go-zero package behavior and usage examples |
| Reference | `src/content/docs/reference/` | `zh-cn/reference/`, `ko/reference/` | DSLs, CLI, configuration, customization, releases, changelog |
| Community | `src/content/docs/community/` | `zh-cn/community/`, `ko/community/` | FAQ, contribution docs, code style, contributors |
| Examples | `src/content/docs/examples/` | `zh-cn/examples/`, `ko/examples/` | End-to-end examples and scenario walkthroughs |

## Source Packets

No source packets have been ingested yet.

- [Latest upstream drift report](reports/v1.10.2...master.md) - mapped go-zero source changes to documentation areas.

## Known Maintenance Themes

- Keep README and AI writing instructions aligned with the actual three-locale site: English, Simplified Chinese, and Korean.
- Release-note automation currently updates the changelog only; source-driven release work should also update affected guide, component, reference, and FAQ pages.
- `npm run validate` checks documentation structure and internal links; run it before publishing large doc changes.
- The Go crawler in `tools/linkcheck/` checks the deployed site; use it separately for production URL health.
- `check-go-zero-drift.yml` generates upstream drift reports under `docs-memory/reports/`; use them as review queues for source-code changes that may stale public docs.

## Open Gaps To Investigate

- Whether every locale has the same page set and sidebar coverage.
- Whether examples compile against the latest go-zero release.
- Whether configuration and CLI reference pages are generated from or checked against current go-zero source.
- Whether generated Korean release pages need a translation-quality pass before publication.
