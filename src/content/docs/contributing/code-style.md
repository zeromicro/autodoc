---
title: Code Style
description: Coding conventions and style guide for go-zero contributors.
sidebar:
  order: 2
---

# Code Style

go-zero follows standard Go conventions with a few additional guidelines.

## Formatting

All code must be formatted with `gofmt` / `goimports`:

```bash
goimports -w ./...
```

CI will reject PRs with formatting issues.

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Package | short, lowercase, no underscores | `logx`, `httpx` |
| Interface | descriptive noun or `-er` suffix | `UserModel`, `Breaker` |
| Constructor | `NewXxx` or `MustNewXxx` | `NewCache`, `MustNewServer` |
| Error vars | `ErrXxx` | `ErrNotFound`, `ErrTimeout` |
| Config structs | embed standard base | `RestConf`, `RpcServerConf` |

## Error Handling

- Never ignore errors silently.
- Wrap errors with context: `fmt.Errorf("createUser: %w", err)`.
- Use sentinel errors defined at package level for type assertions.

## Testing

- Unit tests alongside source: `foo_test.go` in the same package.
- Table-driven tests preferred.
- Mocks generated via `mockgen` or hand-written minimal stubs.
- Minimum coverage target: **80%** for new packages.

```bash
go test -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

## Comments

- All exported symbols must have a doc comment.
- Comments complete sentences, starting with the symbol name.
- Non-obvious logic gets an inline comment explaining *why*.
