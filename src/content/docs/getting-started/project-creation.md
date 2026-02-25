---
title: Project Creation Methods
description: All ways to bootstrap and scaffold go-zero projects with goctl.
sidebar:
  order: 4

---


goctl provides several ways to create projects depending on your starting point.

## From Scratch (interactive scaffold)

The fastest way to start a brand-new service:

```bash
# HTTP API service
goctl api new myservice
cd myservice && go mod tidy

# gRPC service
goctl rpc new myservice
cd myservice && go mod tidy
```

goctl creates a working project with a sample `.api` / `.proto` file, entrypoint, config, and a stub logic layer.

## From an Existing DSL File

When you already have a `.api` or `.proto` file (e.g. shared across teams):

```bash
# From .api file
mkdir myservice && cd myservice
go mod init myservice
goctl api go -api myservice.api -dir .
go mod tidy

# From .proto file
mkdir myservice && cd myservice
go mod init myservice
goctl rpc protoc myservice.proto \
    --go_out=./pb \
    --go-grpc_out=./pb \
    --zrpc_out=.
go mod tidy
```

Use this approach when the DSL is the source of truth checked into a separate repo.

## Regenerating an Existing Project

After editing the `.api` or `.proto` file, regenerate without overwriting your logic:

```bash
# API: re-runs generation, preserves internal/logic/
goctl api go -api myservice.api -dir .

# RPC: re-runs generation, preserves internal/logic/
goctl rpc protoc myservice.proto \
    --go_out=./pb \
    --go-grpc_out=./pb \
    --zrpc_out=.
```

goctl never writes to `internal/logic/`. Everything else (handlers, routes, types, config structs) is regenerated.

## From a Custom Template

For teams that want to enforce conventions (logging setup, error codes, CI config), goctl supports custom templates:

```bash
# Init the default template directory
goctl template init
# Templates saved to: ~/.goctl/

# Edit a template, e.g. the logic file template
vim ~/.goctl/api/logic.tpl

# Use the templates next time you generate
goctl api go -api myservice.api -dir .
```

The template directory mirrors the generated output structure. Common customizations:
- Add standard error code imports
- Inject team-specific logging calls
- Add OpenTelemetry span creation

## Generating Supporting Files

goctl can also generate non-Go artifacts:

```bash
# Dockerfile
goctl docker -go main.go

# Kubernetes deployment + service manifests
goctl kube deploy \
    -name myservice \
    -namespace prod \
    -image myregistry/myservice:v1.0.0 \
    -o deployment.yaml

# DB model layer from SQL DDL
goctl model mysql ddl \
    -src schema.sql \
    -dir internal/model

# Client SDKs
goctl api ts -api myservice.api -dir ./sdk/ts
goctl api dart -api myservice.api -dir ./sdk/dart
```

## Summary

| Method | When to use |
|---|---|
| `goctl api new` / `rpc new` | Starting a new service from zero |
| `goctl api go` / `rpc protoc` | DSL file already exists |
| Regeneration | After editing `.api` or `.proto` |
| Custom templates | Enforcing team-level conventions |
| `goctl docker` / `kube` | Generating deployment artifacts |
