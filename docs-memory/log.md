# Documentation Memory Log

Append entries in reverse chronological order.

## [2026-07-21] lint | go-zero upstream drift v1.10.2...master

- Generated `docs-memory/reports/v1.10.2...master.md`.
- Matched 6 documentation ownership area(s).
- Review the report before editing public docs.

## [2026-07-19] remediation | go-zero issue #5672

- Ingested the issue report and mapped every screenshot to the affected documentation.
- Corrected malformed asset paths, added legacy CLI route redirects, moved guide indexes before their child pages, and replaced the deprecated Swagger plugin listing.
- Added the v1.10.2 release notes and synchronized release indexes and changelogs in all locales.

## [2026-07-13] ingest | go-zero v1.10.2 release

- Captured upstream release notes and changed files for v1.10.2.
- Generated English, Simplified Chinese, and Korean release pages.
- Added a source packet for future cross-page documentation maintenance.

## [2026-06-27] setup | upstream drift reporting

- Added deterministic mapping from upstream `zeromicro/go-zero` source paths to documentation areas.
- Added scheduled drift report generation under `docs-memory/reports/`.
- Drift reports are advisory review queues; they do not edit public docs automatically.

## [2026-06-27] lint | documentation validation gates

- Replaced the regex-only internal link checker with a Markdown-aware checker that skips fenced code and understands Starlight route resolution.
- Added documentation structure validation for frontmatter, locale parity, and supported code fence languages.
- Normalized unsupported code fence labels so Astro builds without highlighter warnings for those pages.
- Wired `npm run validate` into deploy and documentation sync workflows.

## [2026-06-27] setup | LLM-wiki workflow scaffold

- Added the documentation memory workbench.
- Established `docs-memory/sources/` as the raw source intake location.
- Mapped the public Starlight docs as the wiki layer.
- Noted initial maintenance themes: three-locale alignment, release updates beyond changelog, link/build validation, and source-backed reference checks.
