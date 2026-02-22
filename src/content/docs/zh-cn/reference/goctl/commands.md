---
title: goctl 命令参考
description: goctl 全量命令与参数说明，涵盖 api、rpc、model、docker、kube 等所有子命令。
sidebar:
  order: 1
---

# goctl 命令参考

`goctl` 是 go-zero 的代码生成 CLI。本文列出所有命令及其参数。

## goctl api

```bash
goctl api new <service-name>        # 创建新 API 项目脚手架
goctl api go   --api <file> --dir <dir>  # 从 .api 文件生成 Go 代码
goctl api validate --api <file>     # 语法校验
goctl api format --dir <dir>        # 格式化 .api 文件
goctl api doc --dir <dir>           # 生成 Markdown 文档
```

### goctl api go

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--api` | — | .api 文件路径（必填） |
| `--dir` | `.` | 输出目录 |
| `--style` | `goZero` | 文件命名风格 |
| `--home` | `~/.goctl` | 自定义模板目录 |
| `--remote` | — | 指定远程模板仓库 |
| `--branch` | — | 远程模板分支 |
| `--idea` | `false` | 机器可读输出（IDE 集成用） |

## goctl rpc

```bash
goctl rpc new <service-name>        # 创建新 RPC 项目脚手架
goctl rpc protoc <proto-file> ...   # 从 .proto 生成 Go 代码
```

### goctl rpc protoc

```bash
goctl rpc protoc user.proto \
  --go_out=./pb \
  --go-grpc_out=./pb \
  --zrpc_out=. \
  --style goZero
```

| 参数 | 说明 |
|---|---|
| `--go_out` | protoc-gen-go 输出目录 |
| `--go-grpc_out` | protoc-gen-go-grpc 输出目录 |
| `--zrpc_out` | go-zero RPC 骨架输出目录 |
| `--style` | 文件命名风格 |
| `--home` | 自定义模板目录 |
| `--idea` | 机器可读输出 |

## goctl model

```bash
goctl model mysql ddl        --src <file>  --dir <dir>  [--cache]
goctl model mysql datasource --url <dsn>   --table <t>  --dir <dir>  [--cache]
goctl model pg    datasource --url <dsn>   --table <t>  --dir <dir>  [--cache]
goctl model mongo            --type <T>    --dir <dir>  [--easy]
```

参数说明见 [goctl model 参考](./model)。

## goctl docker

从 go-zero 项目生成多阶段 Dockerfile：

```bash
goctl docker --go main.go --port 8888
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--go` | — | main.go 入口文件路径 |
| `--port` | `8080` | 暴露端口 |
| `--version` | — | 基础 Go 镜像版本 |
| `--home` | `~/.goctl` | 自定义模板目录 |
| `--tz` | `Asia/Shanghai` | 容器时区 |
| `--base` | `scratch` | 运行时基础镜像 |

## goctl kube

```bash
goctl kube deploy \
  --name user-api \
  --namespace default \
  --image myregistry/user-api:v1.0.0 \
  --port 8888 \
  -o user-api.yaml
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--name` | — | Deployment 名称 |
| `--namespace` | `default` | Kubernetes 命名空间 |
| `--image` | — | 容器镜像引用 |
| `--replicas` | `3` | Deployment 副本数 |
| `--port` | — | 容器监听端口 |
| `--minReplicas` | `3` | HPA 最小实例数 |
| `--maxReplicas` | `10` | HPA 最大实例数 |
| `--requestCpu` | `500` | CPU request（m） |
| `--requestMem` | `512` | 内存 request（Mi） |
| `--limitCpu` | `1000` | CPU limit（m） |
| `--limitMem` | `1024` | 内存 limit（Mi） |
| `--imagePullPolicy` | `IfNotPresent` | 镜像拉取策略 |
| `-o` | — | 输出文件路径 |
| `--home` | `~/.goctl` | 自定义模板目录 |

## goctl template

```bash
goctl template init              # 初始化默认模板到 ~/.goctl/
goctl template clean             # 清空本地模板缓存
goctl template update            # 更新模板到最新版本
goctl template revert --category api   # 还原指定类别模板
```

## goctl env

```bash
goctl env check     # 检查所有依赖工具
goctl env install   # 自动安装缺失工具
```

`goctl env check` 会验证以下依赖：protoc、protoc-gen-go、protoc-gen-go-grpc、goctl-gen-go-rpc。

## goctl upgrade

```bash
goctl upgrade   # 升级 goctl 至最新版本
```

## 文件命名风格

| 风格 | 示例 |
|---|---|
| `goZero`（默认） | `userhandler.go` |
| `go_zero` | `user_handler.go` |
| `GoZero` | `UserHandler.go` |

## 全局参数

所有 goctl 子命令均支持以下全局参数：

| 参数 | 说明 |
|---|---|
| `--home` | 自定义模板目录，覆盖 `~/.goctl` |
| `--remote` | Git 仓库 URL，用于远程模板 |
| `--branch` | 远程模板的 Git 分支 |
| `--style` | 生成文件的命名风格 |
