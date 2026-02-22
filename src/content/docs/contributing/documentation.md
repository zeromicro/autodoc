---
title: Documentation
description: How to contribute to the go-zero documentation website.
sidebar:
  order: 4
---

# Documentation

The documentation site is built with [Astro Starlight](https://starlight.astro.build/) and lives in the `zeromicro/zerodoc` repository.

## Local Setup

```bash
git clone https://github.com/zeromicro/zerodoc.git
cd zerodoc
npm install
npm run dev
# open http://localhost:4321
```

## File Structure

```text
src/content/docs/          # English content (root locale)
src/content/docs/zh-cn/    # Chinese content
```

Each page is a Markdown or MDX file with YAML frontmatter:

```yaml
---
title: Page Title
description: Short description for SEO and the card grid.
sidebar:
  order: 3
---
```

## Writing Guidelines

- Use second-person ("you"), active voice.
- Code blocks must include a language tag: ```go, ```bash, ```yaml.
- Add `title` to code blocks for context: ```go title="main.go"`
- Keep sentences short; use tables for comparisons.
- Every page should include a practical code example.

## Adding a New Page

1. Create the file in the appropriate chapter directory.
2. Add YAML frontmatter with `title`, `description`, and `sidebar.order`.
3. Add a link to the chapter's `index.md`.
4. Create a matching Chinese translation under `zh-cn/`.

## Submitting

Open a PR against the `main` branch of `zeromicro/zerodoc`. The deploy preview will be posted as a PR comment automatically.
