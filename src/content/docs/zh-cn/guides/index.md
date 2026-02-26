---
title: 指南
description: 按业务场景学习 go-zero 的开发、治理与部署。
sidebar:
  order: 1

---

通过实践性的分步指南学习 go-zero，按主题组织。

## HTTP 服务

- [HTTP 基础开发](./http/basic/) — 创建你的第一个 REST API
- [中间件](./http/server/middleware/) — 请求/响应拦截器
- [JWT 认证](./http/jwt-auth/) — 使用令牌保护接口
- [文件上传](./http/file-upload/) — 处理 multipart 表单数据

## gRPC 服务

- [gRPC 服务端](./grpc/server/) — 定义并启动 protobuf 服务
- [gRPC 客户端](./grpc/client/) — 在 Go 中调用 gRPC 服务
- [拦截器](./grpc/interceptor/) — gRPC 中间件

## 数据库

- [MySQL](./database/mysql/) — 使用 goctl model 进行无 ORM 数据访问
- [Redis](./database/redis/) — 缓存与分布式数据
- [MongoDB](./database/mongodb/) — 文档存储集成

## 微服务

- [服务发现](./microservice/service-discovery/) — 注册与解析服务
- [负载均衡](./microservice/load-balancing) — 分配 RPC 流量
- [分布式追踪](./microservice/distributed-tracing/) — 跨服务请求追踪

## 部署

- [Docker](./deployment/docker/) — 将 go-zero 服务容器化
- [Kubernetes](./deployment/kubernetes/) — 部署到 K8s 集群
