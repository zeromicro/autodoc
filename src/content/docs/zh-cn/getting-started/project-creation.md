---
title: 项目创建方式
description: 介绍 go-zero 常见项目创建路径。
sidebar:
  order: 11
---

# 项目创建方式

## 从零创建

- `goctl api new <name>`
- `goctl rpc new <name>`

## 从 DSL 生成

- `goctl api go -api <file>.api -dir .`
- `goctl rpc protoc <file>.proto --go_out=. --go-grpc_out=. --zrpc_out=.`

## 从模板扩展

可通过自定义模板把组织规范固化进生成代码。
