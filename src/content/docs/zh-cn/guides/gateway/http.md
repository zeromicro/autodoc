---
title: HTTP 网关
description: 通过 go-zero 网关代理 HTTP 请求。
sidebar:
  order: 2
---



**作者**：Kevin Wan  
**日期**：2025-01-28

## 功能概述

HTTP-to-HTTP 网关功能允许你：
- 将 HTTP 请求路由到 HTTP 后端服务
- 为后端服务配置 URL 路径前缀
- 为每个上游服务设置请求超时
- 保留所有现有的 gRPC 网关功能

## 配置说明

以下是在网关配置中设置 HTTP 上游的方式：

```yaml
Upstreams:
  - Name: userservice  # 可选，如果未指定则使用 target
    Http:
      Target: localhost:8080
      Prefix: /api/v1  # 可选
      Timeout: 3000    # 单位为毫秒，默认值 3000
    Mappings:
      - Method: GET
        Path: /users
      - Method: POST
        Path: /users/create
```

作为对比，这是 gRPC 上游的配置方式：

```yaml
Upstreams:
  - Name: orderservice
    Grpc:
      Target: localhost:9000
      Timeout: 3000
    ProtoSets:
      - order.pb
    Mappings:
      - Method: GET
        Path: /orders
        RpcPath: order.OrderService/GetOrders
```

## 使用示例

让我们看一个完整的示例，演示如何设置 HTTP-to-HTTP 路由：

```go
package main

import (
    "github.com/zeromicro/go-zero/gateway"
    "github.com/zeromicro/go-zero/rest"
)

func main() {
    var c gateway.GatewayConf
    conf.MustLoad("gateway.yaml", &c)

    gw := gateway.MustNewServer(c)
    defer gw.Stop()
    
    gw.Start()
}
```

对应的 `gateway.yaml` 配置如下：

```yaml
Name: gateway
Host: 0.0.0.0
Port: 8888
Upstreams:
  - Name: userapi
    Http:
      Target: localhost:8080
      Prefix: /api
    Mappings:
      - Method: GET
        Path: /users
      - Method: POST
        Path: /users
      - Method: GET
        Path: /users/:id
```

## 核心特性

1. **灵活的路由**
    - 在同一网关中支持 HTTP 和 gRPC 后端
    - 基于路径的路由，支持前缀配置
    - 基于方法的路由（GET、POST、PUT、DELETE 等）

2. **配置选项**
    - 可配置的每个上游超时时间
    - 可选的 URL 前缀用于路径重写
    - HTTP 和 gRPC 配置的清晰分离

3. **错误处理**
    - 正确传递 HTTP 状态码
    - 配置问题的详细错误信息
    - 后端服务的超时处理

4. **请求头管理**
    - 保留请求/响应头信息
    - 自动处理内容类型

## 实现细节

该实现保持了关注点分离，并与现有网关功能无缝集成：

- 配置中 HTTP 上游和 gRPC 上游互斥
- 请求转发保持原始 HTTP 方法和头信息
- 保留响应状态码和头信息
- 超时处理符合 go-zero 的一贯模式

## 性能考虑

HTTP-to-HTTP 网关的设计充分考虑了性能因素：
- 高效的请求转发
- 路由层最小开销
- 合理的连接管理
- 内存高效的请求/响应处理

## 最佳实践

使用 HTTP-to-HTTP 网关功能时的建议：

1. 始终为上游服务设置适当的超时时间
2. 为上游服务使用有意义的名称以提高可观察性
3. 考虑使用 URL 前缀避免路径冲突
4. 部署前验证配置

## 结语

HTTP-to-HTTP 支持的加入使得 go-zero 的网关更加通用，适用于更广泛的微服务架构场景。无论你使用 gRPC 服务、HTTP 服务还是两者都有，现在都可以使用单个网关来管理所有路由需求。

更多信息请参考：
- 完整文档：[go-zero docs](https://go-zero.dev)
- 源代码：[GitHub PR #4605](https://github.com/zeromicro/go-zero/pull/4605)
- 示例：[go-zero examples](https://github.com/zeromicro/zero-examples)