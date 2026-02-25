---
title: 名词术语表
description: 快速理解 go-zero 文档中的常用概念。
sidebar:
  order: 8

---


## API DSL

go-zero 用于定义 HTTP 服务的领域专用语言。`.api` 文件描述路由、请求/响应类型和中间件分组。`goctl api go` 将其编译为完整的 Go 项目骨架。

## RPC DSL / Proto

Protobuf `.proto` 文件，用于定义 gRPC 服务契约。`goctl rpc protoc` 将其编译为 gRPC 存根以及 go-zero 的服务端/客户端脚手架代码。

## goctl

go-zero 的命令行代码生成工具。读取 `.api` 或 `.proto` 文件，生成完整可运行的项目骨架——handler、logic 存根、配置结构体、路由注册和 Dockerfile。

## ServiceContext

服务的唯一依赖注入容器。在启动阶段于 `internal/svc/servicecontext.go` 中初始化一次，持有数据库连接池、Redis 客户端、下游 RPC 客户端等所有共享资源。每个 logic 方法都会收到它的指针。

## Logic 层

业务逻辑层——每个用例对应一个 Go 文件（如 `CreateOrderLogic`）。Logic 方法接收强类型请求结构体，调用 model/缓存/RPC 层，返回强类型响应。这是 goctl 永远不会重新生成的唯一层。

## Handler

goctl 生成的 HTTP 适配层。Handler 解码传入请求，调用恰好一个 logic 方法，编码响应，不包含任何业务逻辑。

## Middleware（中间件）

包裹 HTTP handler 以添加横切能力的函数：JWT 鉴权、限流、请求日志、panic 恢复、Trace 注入等。通过 `server.Use()` 全局注册或按路由组挂载。

## Interceptor（拦截器）

gRPC 版本的 HTTP 中间件。一元拦截器包裹单次 RPC 调用；流式拦截器包裹流式 RPC。go-zero 默认注册了熔断、Tracing 和 Prometheus 拦截器。

## zrpc

go-zero 的 gRPC 客户端/服务端包。`zrpc.Server` 封装 `grpc.Server` 并添加健康检查、Prometheus 指标和 OpenTelemetry 追踪。`zrpc.Client` 添加服务发现、P2C 负载均衡和熔断器。

## P2C（二选一）

go-zero 默认的客户端负载均衡算法。每次请求从服务注册表中随机选两个候选实例，转发给加权负载（在途请求数 × 延迟）更低的那个，避免轮询算法的慢节点热点问题。

## 熔断器（Circuit Breaker）

韧性模式：在滑动窗口内统计错误率；当错误率超过阈值时熔断器"打开"，后续请求立即失败（快速失败），不再请求下游。冷却期后允许一个探测请求通过——若成功则"关闭"熔断器。

## 限流（Rate Limiter）

控制服务每秒接受的请求数量。go-zero 使用**令牌桶**算法；突发流量消耗令牌，令牌耗尽后请求被拒绝（返回 `429`）。

## 降载（Load Shedding）

自适应过载保护。当 CPU 使用率或队列深度超过配置上限时，go-zero 丢弃优先级最低的请求，保持服务对其余请求的响应能力。区别于限流——降载对实际系统负载做出反应，而非固定 QPS 上限。

## Telemetry（可观测性配置）

`Telemetry` 配置块为服务接入 OpenTelemetry 追踪。go-zero 自动为每个 HTTP handler 和 RPC 方法创建 span，并跨服务边界传播 trace context。

## logx

go-zero 的结构化日志包。提供分级方法（`Info`、`Error`、`Slow`）、零分配 JSON 输出、context 感知字段注入（trace ID、span ID）以及高吞吐路径的日志采样。

## goctl 模板

存储在 `~/.goctl/` 中的可定制代码模板。运行 `goctl template init` 导出默认模板，按需修改后，后续所有 `goctl` 调用都将使用新模板。

## Etcd Key

用于服务发现的注册标识符。RPC 服务端将自身地址注册到此 Key；RPC 客户端通过 Watch 获取实时实例列表。约定格式：`<服务名>.rpc`（如 `user.rpc`）。

## Model 层

由 `goctl model` 生成的数据访问层，包含带可选双层缓存（进程内 LRU + Redis）的 CRUD 方法。生成代码位于 `*_gen.go` 文件；手写查询放在 goctl 永不覆盖的配套文件中。
