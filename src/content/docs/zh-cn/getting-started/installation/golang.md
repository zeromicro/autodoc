---
title: 安装 Go
description: 在 macOS、Linux 或 Windows 上安装 Go 并配置环境变量。
sidebar:
  order: 2
---

# 安装 Go

go-zero 需要 Go **1.19 或更高版本**。

## macOS

```bash
# 使用 Homebrew
brew install go

# 或手动下载
# 访问 https://go.dev/dl/ 下载 .pkg 安装包，双击安装
```

## Linux

```bash
# 下载并解压（以 1.22.0 为例）
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
```

## Windows

从 [go.dev/dl](https://go.dev/dl/) 下载 `.msi` 安装包，按向导安装，PATH 会自动配置。

## 配置 PATH

```bash
# 添加到 ~/.zshrc 或 ~/.bash_profile
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin   # 使 goctl 等工具命令可用
```

重新加载配置：

```bash
source ~/.zshrc
```

## 验证

```bash
go version
# 输出：go version go1.22.0 darwin/arm64

go env GOPATH
# 输出：/Users/you/go
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|---|---|---|
| `command not found: go` | PATH 未配置 | 添加 `/usr/local/go/bin` 到 PATH |
| `command not found: goctl` | GOPATH/bin 不在 PATH | 添加 `$GOPATH/bin` 到 PATH |
| `GOPROXY` 超时 | 国内网络限制 | 设置 `GOPROXY=https://goproxy.cn,direct` |

## 下一步

[安装 goctl →](./goctl)
