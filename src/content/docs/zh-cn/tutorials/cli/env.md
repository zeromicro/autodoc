---
title: goctl 环境
description: 检查和配置 goctl 构建环境。
sidebar:
  order: 9

---

## 概述

goctl env 可以快速检测 goctl 的依赖环境，如果你的环境中缺少了 goctl 的依赖环境，goctl env 会给出相应的提示，当然，你可以可以通过 goctl env install 命令来安装缺失的依赖环境。

## goctl env 帮助指令

```bash
$ goctl env --help
Check or edit goctl environment

Usage:
  goctl env [flags]
  goctl env [command]

Available Commands:
  check       Detect goctl env and dependency tools
  install     Goctl env installation

Flags:
  -f, --force           Silent installation of non-existent dependencies
  -h, --help            help for env
  -v, --verbose         Enable log output
  -w, --write strings   Edit goctl environment

Use "goctl env [command] --help" for more information about a command.
```

### goctl env 指令

goctl env 可以快速查看当前关于 goctl 环境的一些变量，在用户反馈 bug 时可以将这些信息一并提供给维护人员。

```bash
$ goctl env
GOCTL_OS=darwin 
GOCTL_ARCH=arm64
GOCTL_HOME=/Users/sh00414ml/.goctl
GOCTL_DEBUG=False
GOCTL_CACHE=/Users/sh00414ml/.goctl/cache
GOCTL_EXPERIMENTAL=off
GOCTL_VERSION=1.6.5
PROTOC_VERSION=3.19.4
PROTOC_GEN_GO_VERSION=v1.28.0
PROTO_GEN_GO_GRPC_VERSION=1.2.0
```

| <img width={100}/> 字段 | <img width={200}/> 默认值 | <img width={800}/> 参数说明 |
| -- | --- | --- |
| GOCTL_OS | 空字符串 | 操作系统 |
| GOCTL_ARCH | 空字符串 | 系统架构 |
| GOCTL_HOME | 空字符串 | goctl 配置目录 |
| GOCTL_DEBUG | 空字符串 | 是否开启 debug 模式，维护者使用，枚举值 Ture、False |
| GOCTL_CACHE | 空字符串 | 缓存目录 |
| GOCTL_EXPERIMENTAL | off | 是否开启试验性功能，枚举值 on：开启，off: 关闭 |
| GOCTL_VERSION | 空字符串 | goctl 版本 |
| PROTOC_VERSION | 空字符串 | protoc 版本 |
| PROTOC_GEN_GO_VERSION | 空字符串 | protoc_gen_go 插件版本，没有安装则无 |
| PROTO_GEN_GO_GRPC_VERSION | 空字符串 | protoc_gen_go_grpc 插件版本，没有安装则无 |

### goctl env check 指令

goctl env check 指令用于快速检测 goctl 的依赖环境是否准备好，如果你的环境中缺少了 goctl 的依赖环境，goctl env check 会给出相应的提示。

```bash
$ goctl env check --help
Detect goctl env and dependency tools

Usage:
  goctl env check [flags]

Flags:
  -h, --help      help for check
  -i, --install   Install dependencies if not found

Global Flags:
  -f, --force     Silent installation of non-existent dependencies
  -v, --verbose   Enable log output
```

| <img width={100}/> 参数字段 | <img width={150}/> 参数类型 |<img width={200}/> 是否必填 | <img width={200}/> 默认值 | <img width={800}/> 参数说明 |
| --- | --- | --- | --- | --- |
| i | boolean | NO | false | 安装依赖组件 |
| force | boolean | NO | false | 静默安装组件，如果false，则安装每个组件前会弹出安装确认选项 |
| verbose | boolean | NO | false |  是否输出执行日志 |

**示例示例**：

示例 1： 检测 goctl 依赖环境

**goctl 环境依赖已经安装**
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

**goctl 环境依赖未安装**
```bash
$ goctl env check --verbose
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is not found in PATH

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is not found in PATH

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is not found in PATH

[goctl-env]: check env finish, some dependencies is not found in PATH, you can execute
command 'goctl env check --install' to install it, for details, please execute command
'goctl env check --help'
```

示例 2： 检测 goctl 依赖环境并安装缺失的依赖环境

**不静默安装**
```bash
$ goctl env check --verbose --install
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is not found in PATH
[goctl-env]: do you want to install "protoc" [y: YES, n: No]
y
[goctl-env]: preparing to install "protoc"
[goctl-env]: "protoc" is already installed in "/Users/keson/go/bin/protoc"

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is not found in PATH
[goctl-env]: do you want to install "protoc-gen-go" [y: YES, n: No]
y
[goctl-env]: preparing to install "protoc-gen-go"
"protoc-gen-go" installed from cache
[goctl-env]: "protoc-gen-go" is already installed in "/Users/keson/go/bin/protoc-gen-go"

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is not found in PATH
[goctl-env]: do you want to install "protoc-gen-go-grpc" [y: YES, n: No]
y
[goctl-env]: preparing to install "protoc-gen-go-grpc"
"protoc-gen-go-grpc" installed from cache
[goctl-env]: "protoc-gen-go-grpc" is already installed in "/Users/keson/go/bin/protoc-gen-go-grpc"

[goctl-env]: congratulations! your goctl environment is ready!
```

**静默安装**
```bash
$ goctl env check --verbose --install --force
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is not found in PATH
[goctl-env]: preparing to install "protoc"
"protoc" installed from cache
[goctl-env]: "protoc" is already installed in "/Users/keson/go/bin/protoc"

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is not found in PATH
[goctl-env]: preparing to install "protoc-gen-go"
"protoc-gen-go" installed from cache
[goctl-env]: "protoc-gen-go" is already installed in "/Users/keson/go/bin/protoc-gen-go"

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is not found in PATH
[goctl-env]: preparing to install "protoc-gen-go-grpc"
"protoc-gen-go-grpc" installed from cache
[goctl-env]: "protoc-gen-go-grpc" is already installed in "/Users/keson/go/bin/protoc-gen-go-grpc"

[goctl-env]: congratulations! your goctl environment is ready!
```

### goctl env install 指令

goctl env install 指令其实和 goctl env check --install 的功能是一样的。

```bash
$ goctl env install --help
Goctl env installation

Usage:
  goctl env install [flags]

Flags:
  -h, --help   help for install

Global Flags:
  -f, --force     Silent installation of non-existent dependencies
  -v, --verbose   Enable log output
```

| <img width={100}/> 参数字段 | <img width={150}/> 参数类型 |<img width={200}/> 是否必填 | <img width={200}/> 默认值 | <img width={800}/> 参数说明 |
| --- | --- | --- | --- | --- |
| force | boolean | NO | false | 静默安装组件，如果false，则安装每个组件前会弹出安装确认选项 |
| verbose | boolean | NO | false |  是否输出执行日志 |
