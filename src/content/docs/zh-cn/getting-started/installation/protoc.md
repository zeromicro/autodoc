---
title: 安装 protoc
description: 安装 protoc 编译器及生成 gRPC 服务所需的插件。
sidebar:
  order: 4
---

# 安装 protoc

构建 **gRPC 服务**需要以下工具：

| 工具 | 用途 |
|---|---|
| `protoc` | Protocol Buffer 编译器 |
| `protoc-gen-go` | 生成 Go 数据类型 |
| `protoc-gen-go-grpc` | 生成 gRPC 存根 |

只需 HTTP API 服务可跳过此步骤。

## macOS

```bash
brew install protobuf
```

## Linux

```bash
PB_VERSION=25.1
curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v${PB_VERSION}/protoc-${PB_VERSION}-linux-x86_64.zip
unzip protoc-${PB_VERSION}-linux-x86_64.zip -d $HOME/.local
export PATH="$PATH:$HOME/.local/bin"
```

## Windows

从 [GitHub Releases](https://github.com/protocolbuffers/protobuf/releases) 下载 `protoc-*-win64.zip`，解压并将 `bin/` 添加到系统 PATH。

## 安装 Go 插件

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

## 一键检查并补全（推荐）

```bash
goctl env check --install --verbose
```

此命令会检查所有依赖，并自动安装缺失的工具。

## 验证

```bash
protoc --version
# 输出：libprotoc 25.1

protoc-gen-go --version
# 输出：protoc-gen-go v1.33.0
```

## 下一步

[安装 IDE 插件 →](./ide-plugins)
