---
title: Install Go
description: Install and validate the Go runtime for go-zero development.
sidebar:
  order: 2
---

# Install Go

go-zero requires **Go 1.21 or later**. This page shows how to install Go on macOS, Linux, and Windows, and how to verify the setup.

## Check Existing Installation

```bash
go version
# go version go1.23.4 linux/amd64
```

If the version is ≥ 1.21, skip to [Validate Environment](#validate-environment). Otherwise install or upgrade below.

## Install

### macOS

```bash
# Using Homebrew (recommended)
brew install go

# Or download the .pkg installer from:
# https://go.dev/dl/
```

### Linux

```bash
# Download and extract (replace 1.23.4 with the latest)
wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
```

Add Go to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PATH=$PATH:/usr/local/go/bin
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOBIN
```

Reload:

```bash
source ~/.zshrc   # or ~/.bashrc
```

### Windows

Download and run the `.msi` installer from [go.dev/dl](https://go.dev/dl/). The installer updates `PATH` automatically.

## Validate Environment

```bash
go version
# go version go1.23.4 ...

go env GOPATH GOBIN GOMODCACHE
# /home/user/go
# /home/user/go/bin
# /home/user/go/pkg/mod
```

Make sure `GOBIN` is in your `PATH` — this is where `goctl` and other Go-installed binaries live.

## Troubleshooting

| Problem | Fix |
|---|---|
| `go: command not found` | Add `/usr/local/go/bin` to `PATH` and reload shell |
| `goctl: command not found` after install | Add `$GOBIN` to `PATH` |
| Module download errors | Run `go env -w GOPROXY=https://goproxy.cn,direct` (China) |

## Next Step

[Install goctl →](./goctl)
