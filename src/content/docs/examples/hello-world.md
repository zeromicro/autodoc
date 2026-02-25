---
title: Hello World
description: The simplest possible go-zero API service.
sidebar:
  order: 2

---

# Hello World

The canonical entry point for any new go-zero developer.

## Prerequisites

- Go 1.21+
- goctl installed

## Generate

```bash
goctl api new greet
cd greet
go mod tidy
```

## Project Layout

```text
greet/
├── etc/
│   └── greet-api.yaml
├── internal/
│   ├── config/
│   ├── handler/
│   ├── logic/
│   ├── svc/
│   └── types/
└── greet.go
```

## Run

```bash
go run greet.go
```

## Test

```bash
curl http://localhost:8888/from/you
# {"message":"Hello you"}
```

## What's Next

- Add [middleware](../guides/http/server/middleware.md) for logging
- Connect a [database](../guides/database/mysql.md)
