---
title: Pull Request Process
description: How to open and get a pull request merged into go-zero.
sidebar:
  order: 3

---


## Before Opening a PR

1. Search existing issues and PRs to avoid duplicates.
2. For significant changes, open an issue first to discuss the approach.
3. Ensure all tests pass: `go test ./...`
4. Run `golangci-lint run` and fix any findings.
5. Run `goimports -w ./...` to format code.

## PR Title

Follow Conventional Commits:

```text
fix: prevent goroutine leak in http server shutdown
feat: add Redis cluster support to cache package
docs: update quickstart guide for v1.7
refactor: simplify breaker state machine
```

## PR Description

Use the template:

```markdown
## Summary
Brief description of the change.

## Changes
- List of files/packages changed and why

## Testing
How you tested the change.

## Breaking Change?
Yes / No. If yes, describe what breaks and migration path.
```

## Review Process

1. At least **one maintainer review** required.
2. CI must be green (tests + lint + build).
3. Once approved, maintainers merge using **squash merge**.

## After Merge

- The PR author is credited in the release notes.
- Close any issues fixed by the PR using `Fixes #<issue>` in the PR description.
