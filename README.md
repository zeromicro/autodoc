# go-zero Documentation Site

> The source for **[go-zero.dev](https://go-zero.dev)** — the official documentation website for the [go-zero](https://github.com/zeromicro/go-zero) microservices framework.

[![Deploy to GitHub Pages](https://github.com/zeromicro/autodoc/actions/workflows/deploy.yml/badge.svg)](https://github.com/zeromicro/autodoc/actions/workflows/deploy.yml)

---

## Overview

This repository contains the full source of the go-zero documentation site, built with [Astro](https://astro.build/) and the [Starlight](https://starlight.astro.build/) documentation theme. It provides bilingual documentation (English + Simplified Chinese) covering concepts, tutorials, components, API reference, and more.

**Live site:** https://go-zero.dev

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| [Astro](https://astro.build/) | 5.6.x | Site framework |
| [Starlight](https://starlight.astro.build/) | 0.37.x | Documentation theme |
| GitHub Pages | — | Hosting |
| GitHub Actions | — | CI/CD |

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) v20+
- npm

### Local Development

```bash
# Clone the repo
git clone https://github.com/zeromicro/autodoc.git
cd autodoc

# Install dependencies
npm ci

# Start the dev server
npm run dev
```

The site will be available at `http://localhost:4321`.

### Build

```bash
npm run build
```

The static output is generated into the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

---

## Project Structure

```
autodoc/
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml            # Auto-deploy to GitHub Pages on push to main
│   │   └── sync-release.yml      # Auto-sync go-zero release notes (weekly)
│   └── SITE_IMPLEMENTATION_GUIDE.md
├── public/
│   ├── CNAME                     # Custom domain: go-zero.dev
│   └── favicon.svg
├── src/
│   ├── assets/                   # Images and SVG diagrams
│   └── content/
│       └── docs/                 # All documentation content
│           ├── index.mdx         # English homepage
│           ├── concepts/         # Core concepts & architecture
│           ├── getting-started/  # Installation & quickstart
│           ├── tutorials/        # Hands-on guides (HTTP, gRPC, DB, etc.)
│           ├── components/       # Built-in components (resilience, cache, etc.)
│           ├── reference/        # goctl CLI, configuration, changelog
│           ├── examples/         # Code examples
│           ├── faq/              # Frequently asked questions
│           ├── contributing/     # Contribution guidelines
│           └── zh-cn/            # Simplified Chinese translations (mirrors above)
├── astro.config.mjs              # Astro + Starlight configuration
├── package.json
└── tsconfig.json
```

---

## Documentation Structure

| Section | Description |
|---------|-------------|
| **Getting Started** | Environment setup, goctl installation, hello world |
| **Tutorials** | Step-by-step guides for HTTP, gRPC, databases, microservices, deployment |
| **Components** | Built-in components: rate limiter, circuit breaker, cache, queue, observability |
| **Concepts** | Architecture overview, design principles, project structure, glossary |
| **Reference** | goctl CLI reference, configuration options, changelog |
| **FAQ** | Common issues and solutions |
| **Contributing** | How to contribute to go-zero |

All sections are available in both **English** (`/`) and **Simplified Chinese** (`/zh-cn/`).

---

## Contributing

Contributions to improve the documentation are welcome! You can:

- Fix typos or clarify explanations
- Add missing content or examples
- Improve Chinese translations
- Report issues via [GitHub Issues](https://github.com/zeromicro/autodoc/issues)

### Making Changes

1. Fork this repository
2. Create a branch: `git checkout -b docs/your-improvement`
3. Edit files under `src/content/docs/`
4. Run `npm run dev` to preview locally
5. Open a pull request

---

## Automated Workflows

### Deploy (`deploy.yml`)

Every push to `main` automatically builds and deploys the site to GitHub Pages. The deploy typically takes 1–2 minutes.

### Release Notes Sync (`sync-release.yml`)

Every Monday, a workflow checks for new go-zero releases and opens a pull request with an AI-generated changelog entry. Can also be triggered manually with a specific version tag.

---

## License

Documentation content is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
