---
title: goctl Commands
description: Complete reference for all goctl CLI subcommands and flags.
sidebar:
  order: 2

---

# goctl Commands

`goctl` is the code-generation CLI for go-zero. It generates complete service scaffolding from `.api` or `.proto` files, and produces DB models, Docker images, Kubernetes manifests, and more.

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
goctl --version
```

---

## `goctl api`

Generate HTTP service scaffolding from a `.api` definition file.

### `goctl api new`

Scaffold a new API project from scratch:

```bash
goctl api new <serviceName>
```

```bash
goctl api new order
cd order && go mod tidy && go run order.go -f etc/order-api.yaml
```

### `goctl api go`

Generate Go code from an existing `.api` file:

```bash
goctl api go [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-api` | — | Path to the `.api` file (required) |
| `-dir` | `.` | Output root directory |
| `-style` | `gozero` | File naming style: `gozero` \| `go_zero` \| `goZero` |
| `-home` | `~/.goctl` | Custom template directory |
| `-remote` | — | Remote git template URL |
| `-branch` | — | Branch for remote template |

```bash
# Basic generation
goctl api go -api user.api -dir .

# With custom file naming style
goctl api go -api user.api -dir . -style go_zero

# Using custom templates
goctl api go -api user.api -dir . -home ./custom-templates
```

### `goctl api validate`

Check a `.api` file for syntax errors without generating code:

```bash
goctl api validate -api user.api
```

### `goctl api format`

Format an `.api` file in place:

```bash
goctl api format -dir .
```

### `goctl api doc`

Generate Markdown documentation from a `.api` file:

```bash
goctl api doc -dir . -o ./docs
```

---

## `goctl rpc`

Generate gRPC service scaffolding from a `.proto` file.

### `goctl rpc new`

Scaffold a new RPC project from scratch:

```bash
goctl rpc new <serviceName>
```

### `goctl rpc protoc`

Generate from an existing `.proto` file:

```bash
goctl rpc protoc <proto-file> [flags]
```

| Flag | Default | Description |
|---|---|---|
| `--go_out` | — | Output directory for `.pb.go` files (required) |
| `--go-grpc_out` | — | Output directory for `_grpc.pb.go` files (required) |
| `--zrpc_out` | — | Output directory for zRPC service code (required) |
| `-m` | `false` | Enable multiple services in one proto file |
| `--style` | `gozero` | File naming style |
| `--home` | `~/.goctl` | Custom template directory |
| `--remote` | — | Remote git template URL |
| `--branch` | — | Branch for remote template |

```bash
# Standard single-service generation
goctl rpc protoc user.proto \
  --go_out=./pb \
  --go-grpc_out=./pb \
  --zrpc_out=.

# Multiple services in one file
goctl rpc protoc multi.proto \
  --go_out=./pb \
  --go-grpc_out=./pb \
  --zrpc_out=. \
  -m
```

---

## `goctl model`

Generate type-safe, zero-reflection data access code.

### `goctl model mysql ddl`

Generate from a SQL DDL file:

```bash
goctl model mysql ddl [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-src` | — | Path to the `.sql` DDL file (required) |
| `-dir` | — | Output directory (required) |
| `-cache` | `false` | Wrap generated code with Redis cache layer |
| `-idea` | `false` | Suppress progress output (for IDE plugins) |
| `-style` | `gozero` | File naming style |
| `-home` | `~/.goctl` | Custom template directory |

```bash
goctl model mysql ddl -src schema.sql -dir ./internal/model
goctl model mysql ddl -src schema.sql -dir ./internal/model -cache
```

### `goctl model mysql datasource`

Generate from a live MySQL connection:

```bash
goctl model mysql datasource [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-url` | — | MySQL DSN (required) |
| `-table` | — | Comma-separated table names, `"*"` for all |
| `-dir` | — | Output directory (required) |
| `-cache` | `false` | Add Redis cache layer |
| `-style` | `gozero` | File naming style |

```bash
goctl model mysql datasource \
  -url "root:password@tcp(127.0.0.1:3306)/mydb" \
  -table "user,order,product" \
  -dir ./internal/model \
  -cache
```

### `goctl model pg datasource`

Generate from a live PostgreSQL connection:

```bash
goctl model pg datasource [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-url` | — | PostgreSQL DSN (required) |
| `-table` | — | Table name(s) |
| `-schema` | `public` | PostgreSQL schema |
| `-dir` | — | Output directory (required) |
| `-cache` | `false` | Add Redis cache layer |
| `-style` | `gozero` | File naming style |

```bash
goctl model pg datasource \
  -url "postgres://root:password@localhost:5432/mydb?sslmode=disable" \
  -table "users" \
  -dir ./internal/model
```

### `goctl model mongo`

Generate MongoDB model code:

```bash
goctl model mongo [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-type` | — | Go type name for the collection document |
| `-dir` | — | Output directory |
| `-cache` | `false` | Add Redis cache layer |
| `-easy` | `false` | Generate a simpler model interface |
| `-style` | `gozero` | File naming style |

```bash
goctl model mongo -type Article -dir ./internal/model -cache
```

---

## `goctl docker`

Generate an optimized multi-stage `Dockerfile`:

```bash
goctl docker [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-go` | — | Path to `main.go` (required) |
| `-port` | `8888` | Container exposed port |
| `-version` | `1.22-alpine` | Go base image version |
| `-home` | `~/.goctl` | Custom template directory |
| `-namespace` | — | Kubernetes namespace (for generated labels) |

```bash
goctl docker -go main.go
goctl docker -go main.go -port 8080 -version 1.22-alpine
```

---

## `goctl kube`

Generate Kubernetes Deployment + Service + HPA manifests:

```bash
goctl kube deploy [flags]
```

| Flag | Default | Description |
|---|---|---|
| `-name` | — | Service name (required) |
| `-namespace` | — | Kubernetes namespace (required) |
| `-image` | — | Container image (required) |
| `-port` | — | Service port (required) |
| `-o` | — | Output YAML file |
| `-minreplicas` | `3` | HPA min replicas |
| `-maxreplicas` | `10` | HPA max replicas |
| `-requestCpu` | `500m` | CPU request |
| `-requestMem` | `512Mi` | Memory request |
| `-limitCpu` | `1000m` | CPU limit |
| `-limitMem` | `1024Mi` | Memory limit |

```bash
goctl kube deploy \
  -name order-api \
  -namespace production \
  -image myregistry/order-api:v1.2.0 \
  -port 8888 \
  -o k8s/order-api.yaml
```

---

## `goctl template`

Manage goctl's code generation templates.

| Subcommand | Description |
|---|---|
| `goctl template init` | Copy default templates to `~/.goctl/` |
| `goctl template clean` | Remove cached templates |
| `goctl template update` | Force-update templates to match current goctl version |
| `goctl template revert` | Restore a single template to default |

```bash
goctl template init
ls ~/.goctl/api/         # api templates
ls ~/.goctl/rpc/         # rpc templates
ls ~/.goctl/model/       # model templates
```

---

## `goctl env`

Check and auto-install required tools.

```bash
goctl env check [flags]
```

| Flag | Description |
|---|---|
| `--install` | Install missing tools automatically |
| `--verbose` | Show detailed output |

```bash
goctl env check --install --verbose
```

Sample output:

```
goctl version: 1.7.x
go: 1.22.0
protoc: 25.1
protoc-gen-go: 1.33.0
protoc-gen-go-grpc: 1.3.0
goctl-intellij: OK
goctl-vscode: OK
```

---

## `goctl upgrade`

Upgrade goctl to the latest release:

```bash
goctl upgrade
```

---

## File Naming Styles

| Style value | Example output |
|---|---|
| `gozero` | `getuserhandler.go` |
| `go_zero` | `get_user_handler.go` |
| `goZero` | `getUserHandler.go` |
