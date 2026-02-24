---
title: Installation FAQ
description: Common installation and setup issues with go-zero.
sidebar:
  order: 2

---

# Installation FAQ

## `goctl: command not found` after installation

Ensure `$GOPATH/bin` is in your `PATH`:

```bash
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.zshrc
```

## `go: module ... not found` during `go mod tidy`

Make sure you're using Go 1.18+ and have a valid `go.mod`:

```bash
go version          # must be >= 1.18
go env GOPROXY      # should include https://goproxy.cn or https://proxy.golang.org
```

Set a proxy if behind a corporate firewall:

```bash
go env -w GOPROXY=https://goproxy.cn,direct
```

## `protoc-gen-go: program not found` when running goctl rpc

Install the required protoc plugins:

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

Or use goctl's built-in installer:

```bash
goctl env check --install
```

## Generated code has import errors

Run `go mod tidy` inside the generated directory. Also check that `go_package` in your `.proto` matches the actual generated directory path.

## IDE shows errors in generated files

Ensure your IDE's Go module root is set correctly. For VS Code, open the workspace at the project root containing `go.mod`.
