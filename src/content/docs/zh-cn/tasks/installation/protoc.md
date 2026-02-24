---
title: 安装 protoc
description: 安装 Protocol Buffers 编译器及 Go gRPC 插件。
sidebar:
  order: 5

---

## 概述

<a href="https://protobuf.dev/" target="_blank">protoc</a> 是一个用于生成代码的工具，它可以根据 proto 文件生成C++、Java、Python、Go、PHP 等多重语言的代码，而 gRPC 的代码生成还依赖 <a href="https://github.com/golang/protobuf/tree/master/protoc-gen-go" target="_blank">protoc-gen-go</a>，<a href="https://pkg.go.dev/google.golang.org/grpc/cmd/protoc-gen-go-grpc" target="_blank">protoc-gen-go-grpc</a> 插件来配合生成 Go 语言的 gRPC 代码。

## 1. 一键安装(推荐)

通过 `goctl` 可以一键安装 `protoc`，`protoc-gen-go`，`protoc-gen-go-grpc` 相关组件，你可以执行如下命令：

```bash
$ goctl env check --install --verbose --force
```

关于 `goctl env` 指令详情可参考 <a href="/docs/tutorials/cli/env" target="_blank">goctl env</a>

## 2. 手动安装

### 2.1 下载

:::note 注意
这里以 `21.11` 版本为例子，并 **不推荐** 安装具体版本，开发者可根据需要自行选择，更多版本可前往 [前往 Github](https://github.com/protocolbuffers/protobuf/releases) 自行选择。
:::

<p>Windows Intel 64 位处理器</p>
    <a>protoc-21.11-win64.zip（2.17MB）</a>

<p>Windows Intel 32 位处理器</p>
    <a>protoc-21.11-win32.zip（2.2MB）</a>

<p>支持 macOS Apple 64 位处理器</p>
    <a>protoc-21.11-osx-aarch_64.zip（1.3MB）</a>

<p>支持 macOS 64 位处理器</p>
    <a>protoc-21.11-osx-x86_64.zip（1.42MB）</a>

<p>支持 Linux 64 位处理器</p>
    <a>protoc-21.11-linux-x86_64.zip（1.51MB）</a>

<p>支持 Linux 32 位处理器</p>
    <a>protoc-21.11-linux-x86_32.zip（1.61MB）</a>

其他版本及操作系统可 [前往 Github](https://github.com/protocolbuffers/protobuf/releases) 自行选择。

### 2.2 安装

解压下载的压缩包，并将其移动到 `$GOBIN` 目录，查看 `$GOBIN` 目录：

```bash
$ go env GOPATH
```

`GOBIN` 为 `$GOPATH/bin`，如果你的 `$GOPATH` 不在 `$PATH` 中，你需要将其添加到 `$PATH` 中。

## 3. 验证

安装完毕后，你可以执行如下指令来验证是否安装成功：

```bash
$ goctl env check --verbose
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is installed

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is installed

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is installed

[goctl-env]: congratulations! your goctl environment is ready!
```
