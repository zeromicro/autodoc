---
title: 名词术语表
description: 快速理解 go-zero 文档中的常用概念。
sidebar:
  order: 2
---

# 名词术语表

## API DSL

用于定义 HTTP 接口的领域语言，可由 goctl 生成代码骨架。

## RPC DSL / Proto

用于定义服务间通信协议与接口的描述语言。

## ServiceContext

业务依赖收敛入口，集中管理数据库、缓存、客户端等共享资源。

## Logic

业务逻辑层，接收请求模型、完成业务处理并返回响应。

## Middleware

横切能力层，负责鉴权、限流、日志、Tracing 等通用逻辑。
