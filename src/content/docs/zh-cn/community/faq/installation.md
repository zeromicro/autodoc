---
title: 安装问题
description: Go、goctl、protoc 安装相关的常见问题。
sidebar:
  order: 2

---

## 安装后提示 `goctl: command not found`

确保 `$GOPATH/bin` 已加入 `PATH`：

```bash
export PATH=$PATH:$(go env GOPATH)/bin
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.zshrc
```

## `go mod tidy` 时提示 `go: module ... not found`

确保使用 Go 1.18+ 并且 `go.mod` 有效：

```bash
go version          # 必须 >= 1.18
go env GOPROXY      # 应包含 https://goproxy.cn 或 https://proxy.golang.org
```

如果在企业防火墙内，设置代理：

```bash
go env -w GOPROXY=https://goproxy.cn,direct
```

## 运行 goctl rpc 时提示 `protoc-gen-go: program not found`

安装所需的 protoc 插件：

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

或者使用 goctl 内置的安装器：

```bash
goctl env check --install
```

## 生成的代码有 import 错误

在生成目录中运行 `go mod tidy`。同时检查 `.proto` 中的 `go_package` 是否与实际生成目录路径一致。

## IDE 在生成文件中显示错误

这通常是因为 IDE 的索引还未更新。尝试重新加载项目或运行 `go mod tidy` 后等待索引完成。
