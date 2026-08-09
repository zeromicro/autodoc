# Contributing to go-zero documentation

Thank you for improving go-zero's documentation.

## Set up the site

Use Node.js 20 or later:

```bash
npm ci
npm run dev
```

## Make documentation changes

- Edit public pages under `src/content/docs/`.
- Keep the English, Simplified Chinese, and Korean page structures aligned.
- Follow `.github/copilot-instructions.md` for frontmatter, headings, links, and code examples.
- For changes based on releases, source changes, issues, or reports, read `docs-memory/index.md` and follow the documentation memory workflow.
- Keep code samples complete and runnable whenever possible.

## Verify your contribution

Run every check before opening a pull request:

```bash
npm test
npm run validate
npm run build
```

The pull-request workflow runs the same commands. Include source links and explain how you verified behavior when changing technical guidance.
