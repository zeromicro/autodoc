---
title: 微服务系统
description: 多服务示例，演示服务发现、RPC 调用链与可观测性。
sidebar:
  order: 5
---

# 微服务系统

高级示例，展示多个 go-zero 服务通过 etcd 协同工作的完整流程。

## 服务拓扑

```text
order-api  ──→  order-rpc  ──→  MySQL
               ↓
          inventory-rpc  ──→  Redis
               ↓
          payment-rpc    ──→  MySQL
```

## 前提条件

- etcd 运行在 `localhost:2379`
- MySQL 和 Redis 已就绪

## 服务注册配置

每个服务向 etcd 注册自身：

```yaml title="etc/order-rpc.yaml"
Name: order.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: order.rpc
```

## RPC 客户端配置

```yaml title="etc/order-api.yaml"
OrderRpc:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: order.rpc
```

## 可观测性

启用 Prometheus 指标采集与 Jaeger 链路追踪：

```yaml
Telemetry:
  Name: order-api
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```

## 核心知识点

- 基于 etcd 的服务注册与发现
- 多跳 RPC 调用链路
- 跨服务分布式追踪
- 熔断器与限流器实战
