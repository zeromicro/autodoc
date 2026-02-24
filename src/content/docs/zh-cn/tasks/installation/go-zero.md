---
title: 安装 go-zero
description: 将 go-zero 框架作为依赖安装到您的 Go 模块中。
sidebar:
  order: 3

---


## 概述

在 Golang 中，我们推荐使用 `go module` 来管理。

在 Golang 安装时，建议设置了 `GOPROXY`，详情可参考 <a href="/docs/tasks" target="_blank">golang 安装</a>

## 安装

```bash
$ mkdir <project name> && cd <project name> # project name 为具体值
$ go mod init <module name> # module name 为具体值
$ go get -u github.com/zeromicro/go-zero@latest
```

## 常见问题

### 1. 设置了 GOPROXY 后，依赖还是拉不下来？

确保设置 `GOPROXY` 的方式是正确的，并通过 `go env GOPROXY` 命令确认设置成功，如下：

```shell
$ go env -w GOPROXY=https://goproxy.cn,direct
$ go env GOPROXY
https://goproxy.cn,direct
```
