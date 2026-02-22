---
title: goctl Commands
description: Complete reference for all goctl CLI subcommands.
sidebar:
  order: 1
---

# goctl Commands

`goctl` is the code-generation CLI for go-zero. Install:

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

## Top-Level Commands

```text
goctl [command]

Available Commands:
  api         Generate API service scaffolding
  rpc         Generate RPC (gRPC) service scaffolding
  model       Generate database model code
  docker      Generate Dockerfile
  kube        Generate Kubernetes manifests
  template    Manage goctl code templates
  upgrade     Upgrade goctl to the latest version
  env         Check and configure goctl environment
```

## api

```bash
goctl api go -api <file.api> -dir <output-dir> [flags]

Flags:
  --api string    Path to .api definition file
  --dir string    Output directory (default ".")
  --style string  File naming style: gozero|go_zero|goZero (default "gozero")
```

## rpc

```bash
goctl rpc protoc <file.proto> --go_out=<dir> --go-grpc_out=<dir> --zrpc_out=<dir>
```

## model

```bash
# From DDL file
goctl model mysql ddl -src <file.sql> -dir <output-dir>

# From connected database
goctl model mysql datasource -url "dsn" -table "*" -dir <output-dir>
```

## docker

```bash
goctl docker -go <main.go> -port <port>
```

## upgrade

```bash
goctl upgrade
```
