---
title: 安装 goctl
description: 安装并配置 go-zero 代码生成工具 goctl。
sidebar:
  order: 3
---


`goctl`（读作"go control"）是 go-zero 的脚手架工具，可从 `.api` 或 `.proto` 文件一键生成完整的服务代码。

## 安装

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

安装完成后，`goctl` 二进制文件保存在 `$GOPATH/bin/`，确保该路径已在 PATH 中。

## 验证

```bash
goctl --version
# 输出：goctl version 1.7.x ...
```

## 升级

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

## 主要功能

| 命令 | 功能 |
|---|---|
| `goctl api new` | 从零创建 API 服务 |
| `goctl api go` | 从 .api 文件生成 Go 代码 |
| `goctl rpc new` | 从零创建 RPC 服务 |
| `goctl rpc protoc` | 从 .proto 文件生成代码 |
| `goctl model mysql` | 从 SQL 生成数据模型 |
| `goctl docker` | 生成 Dockerfile |
| `goctl kube` | 生成 Kubernetes 部署清单 |

## 常见问题

若安装后提示 `command not found: goctl`，请将以下内容添加到 shell 配置文件：

```bash
export PATH=$PATH:$HOME/go/bin
```

## 下一步

[安装 protoc →](./protoc)
