---
title: goctl 命令参考
description: goctl 全量命令与参数说明，涵盖 api、rpc、model、docker、kube 等所有子命令。
sidebar:
  order: 2

---

`goctl` 是 go-zero 的代码生成 CLI。它可以从 `.api` 或 `.proto` 文件生成完整的服务脚手架，也可以生成数据库模型、Docker 镜像、Kubernetes 清单等。

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
goctl --version
```

---

## `goctl api`

从 `.api` 定义文件生成 HTTP 服务脚手架。

### `goctl api new`

从零开始创建新 API 项目：

```bash
goctl api new <serviceName>
```

```bash
goctl api new order
cd order && go mod tidy && go run order.go -f etc/order-api.yaml
```

### `goctl api go`

从已有的 `.api` 文件生成 Go 代码：

```bash
goctl api go [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-api` | — | `.api` 文件路径（必填） |
| `-dir` | `.` | 输出根目录 |
| `-style` | `gozero` | 文件命名风格：`gozero` \| `go_zero` \| `goZero` |
| `-home` | `~/.goctl` | 自定义模板目录 |
| `-remote` | — | 远程 Git 模板 URL |
| `-branch` | — | 远程模板分支 |

```bash
# 基本用法
goctl api go -api user.api -dir .

# 自定义命名风格
goctl api go -api user.api -dir . -style go_zero

# 使用自定义模板
goctl api go -api user.api -dir . -home ./custom-templates
```

### `goctl api validate`

检查 `.api` 文件语法是否正确，不生成代码：

```bash
goctl api validate -api user.api
```

### `goctl api format`

就地格式化 `.api` 文件：

```bash
goctl api format -dir .
```

### `goctl api doc`

从 `.api` 文件生成 Markdown 文档：

```bash
goctl api doc -dir . -o ./docs
```

---

## `goctl rpc`

从 `.proto` 文件生成 gRPC 服务脚手架。

### `goctl rpc new`

从零开始创建新 RPC 项目：

```bash
goctl rpc new <serviceName>
```

### `goctl rpc protoc`

从已有的 `.proto` 文件生成：

```bash
goctl rpc protoc <proto-file> [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--go_out` | — | `.pb.go` 文件输出目录（必填） |
| `--go-grpc_out` | — | `_grpc.pb.go` 文件输出目录（必填） |
| `--zrpc_out` | — | zRPC 服务代码输出目录（必填） |
| `-m` | `false` | 允许一个 proto 文件中定义多个服务 |
| `--style` | `gozero` | 文件命名风格 |
| `--home` | `~/.goctl` | 自定义模板目录 |
| `--remote` | — | 远程 Git 模板 URL |
| `--branch` | — | 远程模板分支 |

```bash
# 标准单服务生成
goctl rpc protoc user.proto \
  --go_out=./pb \
  --go-grpc_out=./pb \
  --zrpc_out=.

# 单文件多服务
goctl rpc protoc multi.proto \
  --go_out=./pb \
  --go-grpc_out=./pb \
  --zrpc_out=. \
  -m
```

---

## `goctl model`

生成类型安全、零反射的数据访问代码。

### `goctl model mysql ddl`

从 SQL DDL 文件生成：

```bash
goctl model mysql ddl [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-src` | — | `.sql` DDL 文件路径（必填） |
| `-dir` | — | 输出目录（必填） |
| `-cache` | `false` | 生成 Redis 缓存层 |
| `-idea` | `false` | 抑制进度输出（IDE 集成用） |
| `-style` | `gozero` | 文件命名风格 |
| `-home` | `~/.goctl` | 自定义模板目录 |

```bash
goctl model mysql ddl -src schema.sql -dir ./internal/model
goctl model mysql ddl -src schema.sql -dir ./internal/model -cache
```

### `goctl model mysql datasource`

从 MySQL 连接生成：

```bash
goctl model mysql datasource [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-url` | — | MySQL DSN（必填） |
| `-table` | — | 逗号分隔的表名，`"*"` 表示全部 |
| `-dir` | — | 输出目录（必填） |
| `-cache` | `false` | 添加 Redis 缓存层 |
| `-style` | `gozero` | 文件命名风格 |

```bash
goctl model mysql datasource \
  -url "root:password@tcp(127.0.0.1:3306)/mydb" \
  -table "user,order,product" \
  -dir ./internal/model \
  -cache
```

### `goctl model pg datasource`

从 PostgreSQL 连接生成：

```bash
goctl model pg datasource [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-url` | — | PostgreSQL DSN（必填） |
| `-table` | — | 表名 |
| `-schema` | `public` | PostgreSQL schema |
| `-dir` | — | 输出目录（必填） |
| `-cache` | `false` | 添加 Redis 缓存层 |
| `-style` | `gozero` | 文件命名风格 |

```bash
goctl model pg datasource \
  -url "postgres://root:password@localhost:5432/mydb?sslmode=disable" \
  -table "users" \
  -dir ./internal/model
```

### `goctl model mongo`

生成 MongoDB 模型代码：

```bash
goctl model mongo [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-type` | — | 集合文档的 Go 类型名 |
| `-dir` | — | 输出目录 |
| `-cache` | `false` | 添加 Redis 缓存层 |
| `-easy` | `false` | 生成更简单的模型接口 |
| `-style` | `gozero` | 文件命名风格 |

```bash
goctl model mongo -type Article -dir ./internal/model -cache
```

---

## `goctl docker`

生成优化的多阶段 `Dockerfile`：

```bash
goctl docker [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-go` | — | `main.go` 入口路径（必填） |
| `-port` | `8888` | 容器暴露端口 |
| `-version` | `1.22-alpine` | Go 基础镜像版本 |
| `-home` | `~/.goctl` | 自定义模板目录 |
| `-namespace` | — | Kubernetes 命名空间（用于生成标签） |

```bash
goctl docker -go main.go
goctl docker -go main.go -port 8080 -version 1.22-alpine
```

---

## `goctl kube`

生成 Kubernetes Deployment + Service + HPA 清单：

```bash
goctl kube deploy [flags]
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `-name` | — | 服务名（必填） |
| `-namespace` | — | Kubernetes 命名空间（必填） |
| `-image` | — | 容器镜像（必填） |
| `-port` | — | 服务端口（必填） |
| `-o` | — | 输出 YAML 文件路径 |
| `-minreplicas` | `3` | HPA 最小副本数 |
| `-maxreplicas` | `10` | HPA 最大副本数 |
| `-requestCpu` | `500m` | CPU request |
| `-requestMem` | `512Mi` | 内存 request |
| `-limitCpu` | `1000m` | CPU limit |
| `-limitMem` | `1024Mi` | 内存 limit |

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

管理 goctl 的代码生成模板。

| 子命令 | 说明 |
|---|---|
| `goctl template init` | 将默认模板复制到 `~/.goctl/` |
| `goctl template clean` | 清除缓存模板 |
| `goctl template update` | 强制更新模板至当前 goctl 版本 |
| `goctl template revert` | 恢复单个模板为默认值 |

```bash
goctl template init
ls ~/.goctl/api/         # api 模板
ls ~/.goctl/rpc/         # rpc 模板
ls ~/.goctl/model/       # model 模板
```

---

## `goctl env`

检查并自动安装所需工具。

```bash
goctl env check [flags]
```

| 参数 | 说明 |
|---|---|
| `--install` | 自动安装缺失工具 |
| `--verbose` | 显示详细输出 |

```bash
goctl env check --install --verbose
```

输出示例：

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

升级 goctl 至最新版本：

```bash
goctl upgrade
```

---

## 文件命名风格

| 风格值 | 输出示例 |
|---|---|
| `gozero` | `getuserhandler.go` |
| `go_zero` | `get_user_handler.go` |
| `goZero` | `getUserHandler.go` |
