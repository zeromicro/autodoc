---
title: 创建项目（CLI）
description: 通过命令行脚手架创建新的 go-zero 项目。
sidebar:
  order: 2

---


## 概览

我们在完成 Golang 安装后，可以正式进入 golang 开发了，目前比较主流的两款编辑器是 Goland 和 VSCode，除此之外，我们还可以从终端创建 Golang 工程，本文将介绍如何使用命令行创建一个 golang 项目。

## 创建项目

```bash
# 创建 golang 工程
➜ ~  mkdir -p ~/workspace/helloworld/ && cd ~/workspace/helloworld
➜ helloworld  # 创建 go module
➜ helloworld  go mod init helloworld
go: creating new go.mod: module helloworld
➜ helloworld  # 创建 main.go 文件
➜ helloworld  touch main.go
➜ helloworld  # 添加代码
➜ helloworld  echo 'package main
>
> import "fmt"
>
> func main() {
>   fmt.Println("Hello World!")
> }
> ' > main.go
```

## 运行 main.go

```bash
➜ go run main.go
Hello World!
```
