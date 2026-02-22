---
title: 架构概览
description: go-zero 微服务架构深度解析，含 Mermaid 图表、各层职责说明与 YAML 配置示例。
---

# 架构概览

go-zero 是一套完整的微服务框架，采用分层架构，为从 API 网关到底层基础设施的每个关注点提供专用组件。

## 系统结构图

<pre class="mermaid">
graph TB
    subgraph API层
        GW[API 网关<br/>rest.Server]
        MW[中间件链<br/>Auth · Rate Limit · Logging]
    end

    subgraph RPC层
        RS[RPC 服务<br/>zrpc.Server]
        LB[负载均衡<br/>P2C]
        CB[熔断器<br/>自适应限流]
    end

    subgraph 基础设施层
        ET[服务注册<br/>etcd / Consul]
        CA[缓存层<br/>Redis + 内存 LRU]
        DB[数据库<br/>MySQL / PostgreSQL / MongoDB]
        MQ[消息队列<br/>Kafka / RabbitMQ]
    end

    subgraph 可观测性层
        MT[指标采集<br/>Prometheus]
        TR[链路追踪<br/>OpenTelemetry / Jaeger]
        LG[结构化日志<br/>logx]
    end

    GW --> MW --> RS
    RS --> LB --> CB
    RS --> ET
    RS --> CA --> DB
    RS --> MQ
    GW --> MT
    GW --> TR
    GW --> LG
    RS --> MT
    RS --> TR
</pre>

## 各层职责

| 层级 | 组件 | 职责 |
|---|---|---|
| API 层 | `rest.Server` | HTTP/1.1、HTTP/2、WebSocket；JWT 认证；速率限制 |
| RPC 层 | `zrpc.Server/Client` | gRPC 通信；P2C 负载均衡；熔断器 |
| 服务发现 | etcd / Consul | 实例注册、健康检查、Watch 推送 |
| 缓存层 | Redis + LRU | 双层缓存；WriteThrough；7 天 TTL |
| 可观测性 | OTel + Prometheus | 统一 Traces / Metrics / Logs |

## HTTP 请求生命周期

<pre class="mermaid">
sequenceDiagram
    participant 客户端
    participant rest.Server
    participant 中间件
    participant Handler
    participant zrpc.Client
    participant RPC 服务

    客户端->>rest.Server: HTTP 请求
    rest.Server->>中间件: 执行中间件链
    中间件->>中间件: JWT 验证
    中间件->>中间件: 速率限制检查
    中间件->>中间件: 注入 Trace Context
    中间件->>Handler: 调用 Handler
    Handler->>zrpc.Client: RPC 调用（携带 ctx）
    zrpc.Client->>RPC 服务: gRPC 请求
    RPC 服务-->>zrpc.Client: 响应
    zrpc.Client-->>Handler: 反序列化结果
    Handler-->>客户端: JSON 响应
</pre>

## 中间件链

<pre class="mermaid">
flowchart LR
    Req[请求] --> Log[日志中间件<br/>记录耗时与状态码]
    Log --> Auth[认证中间件<br/>校验 JWT]
    Auth --> RL[速率限制<br/>令牌桶]
    RL --> Trace[追踪注入<br/>创建 OTel span]
    Trace --> H[业务 Handler]
</pre>

中间件通过 `server.Use(middleware)` 注册，支持全局或按路由挂载。

## API 网关与 RPC 服务联动

<pre class="mermaid">
flowchart TD
    API[API 服务] -->|zrpc.Client| SD[etcd 服务发现]
    SD -->|解析实例列表| LB[P2C 负载均衡]
    LB --> I1[RPC 实例 1]
    LB --> I2[RPC 实例 2]
    LB --> I3[RPC 实例 3]
    I1 & I2 & I3 -->|注册心跳| SD
</pre>

API 服务通过 etcd 动态感知 RPC 实例的上线与下线，无需任何人工干预。

## 韧性机制：速率限制与熔断

<pre class="mermaid">
flowchart TD
    R[请求到达] --> RL{速率限制器<br/>令牌足够？}
    RL -->|否| Rej[拒绝 429]
    RL -->|是| CB{熔断器<br/>处于关闭状态？}
    CB -->|断开| Fast[快速失败 503]
    CB -->|关闭| Proc[处理请求]
    Proc --> OK[成功响应]
    Proc --> Err[超时 / 错误]
    Err --> Update[更新熔断器状态]
</pre>

## 可观测性流水线

<pre class="mermaid">
flowchart LR
    SVC[go-zero 服务] -->|OTLP gRPC| OCA[OTel Collector]
    SVC -->|/metrics| PM[Prometheus]
    OCA --> JG[Jaeger / Tempo<br/>链路追踪]
    OCA --> GM[Grafana<br/>可视化]
    PM --> GM
    SVC -->|JSON 日志| LK[Loki / ELK<br/>日志聚合]
    LK --> GM
</pre>

## 配置层次结构

go-zero 配置可以内嵌组合：

```yaml
Name: user-api
Host: 0.0.0.0
Port: 8888

# 嵌入 REST 配置
MaxConns: 1000       # 最大并发连接数
Timeout: 5000        # 全局请求超时（毫秒）

# 下游 RPC 依赖
UserRpc:
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: user.rpc
  Timeout: 2000

# 缓存
CacheRedis:
  - Host: 127.0.0.1:6379
    Type: node

# 可观测性
Telemetry:
  Name: user-api
  Endpoint: http://jaeger:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```

## 延伸阅读

- [快速开始](../getting-started/quickstart) — 5 分钟运行第一个 go-zero 服务
- [gRPC 客户端](../tutorials/grpc/client) — zrpc.Client 完整配置参考
- [分布式链路追踪](../tutorials/microservice/distributed-tracing) — 端到端追踪配置
