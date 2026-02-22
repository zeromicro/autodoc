---
title: Getting Started
description: Prepare your environment and launch your first go-zero service in under 5 minutes.
sidebar:
  order: 1
---

# Getting Started

This section walks you from a blank machine to a running go-zero service. By the end you will have Go, goctl, and (optionally) protoc installed, and you will have run your first HTTP API and RPC service.

**Estimated time:** ~15 minutes for the full path, or ~5 minutes for Hello World only.

## Prerequisites

| Requirement | Minimum version | Notes |
|---|---|---|
| Go | 1.21 | [Download](https://go.dev/dl/) |
| goctl | latest | go-zero's code-generation CLI |
| protoc | 3.x | Required for RPC services only |

## Recommended Learning Path

Follow the steps in order the first time:

```
1. Install Go         →  installation/golang
2. Install goctl      →  installation/goctl
3. Install protoc     →  installation/protoc     (RPC only)
4. Configure IDE      →  installation/ide-plugins
5. Understand API DSL →  dsl/api-syntax
6. Hello World        →  quickstart/hello-world   ← start here if impatient
7. Full API service   →  quickstart/api-service
8. Full RPC service   →  quickstart/rpc-service
```

## 60-Second Quick Start

Already have Go ≥ 1.21? Run this:

```bash
# Install goctl
go install github.com/zeromicro/go-zero/tools/goctl@latest

# Scaffold and run a Hello World API
goctl api new greet
cd greet
go mod tidy
go run greet.go
```

Then in another terminal:

```bash
curl http://localhost:8888/from/you
# {"message":"Hello you"}
```

That's it — you have a running API service. Continue to the [full API quickstart](./quickstart/api-service) to learn how to add handlers, middleware, and database access.

## What goctl Generates

Running `goctl api new greet` produces a complete, production-ready layout:

```
greet/
├── etc/
│   └── greet-api.yaml      # configuration file
├── internal/
│   ├── config/             # config struct
│   ├── handler/            # HTTP handlers (auto-registered)
│   ├── logic/              # business logic (edit this)
│   ├── middleware/         # custom middleware hooks
│   ├── svc/                # service context (shared dependencies)
│   └── types/              # request/response types
├── greet.go                # entrypoint
└── greet.api               # DSL source
```

Edit only the files in `internal/logic/`. Everything else is regenerated from the `.api` file whenever you run `goctl api go`.

## Next Steps

- [Install Go →](./installation/golang)
- [Install goctl →](./installation/goctl)
- [Hello World →](./quickstart/hello-world)
