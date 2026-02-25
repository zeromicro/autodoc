---
title: Install goctl
description: Install the official go-zero code generation tool.
sidebar:
  order: 3
---


`goctl` (pronounced "go control") is go-zero's code-generation CLI. It reads `.api` and `.proto` files and produces complete, production-ready Go services — eliminating boilerplate.

## Install

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

## Verify

```bash
goctl --version
# goctl version 1.7.3 darwin/arm64
```

If you see `command not found`, your `$GOBIN` is not in `PATH`. Fix it:

```bash
# Add to ~/.zshrc or ~/.bashrc
export GOBIN=$(go env GOPATH)/bin
export PATH=$PATH:$GOBIN
source ~/.zshrc
```

## Upgrade

Re-run the same install command to get the latest version:

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
goctl --version
```

## What goctl Can Generate

| Command | Output |
|---|---|
| `goctl api new <name>` | Complete HTTP API service skeleton |
| `goctl api go -api f.api -dir .` | Go code from an existing `.api` file |
| `goctl rpc new <name>` | Complete gRPC service skeleton |
| `goctl rpc protoc f.proto ...` | Go code from an existing `.proto` file |
| `goctl model mysql ddl -src f.sql -dir .` | DB model layer from SQL schema |
| `goctl docker -go main.go` | Dockerfile |
| `goctl kube deploy ...` | Kubernetes deployment manifest |

## Next Step

For RPC services: [Install protoc →](./protoc)

For HTTP-only services: [Hello World →](../../guides/quickstart/hello-world)
