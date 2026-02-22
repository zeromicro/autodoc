#!/usr/bin/env python3
"""Write zh-cn counterparts for all EN files changed this session."""
import pathlib, textwrap

base = pathlib.Path("src/content/docs/zh-cn")

files = {}

# ─── tutorials/grpc/client.md ──────────────────────────────────────────────
files["tutorials/grpc/client.md"] = """\
---
title: gRPC 客户端
description: 通过 go-zero 调用 gRPC 服务，含服务发现、负载均衡、熔断与超时。
sidebar:
  order: 2
---

# gRPC 客户端

`zrpc.Client` 是 go-zero 的 gRPC 客户端封装，自动集成**服务发现**、**P2C 负载均衡**、**熔断器**和 **OpenTelemetry 链路追踪**。

## 方案 A：直连（开发 / 测试）

```go title="internal/svc/servicecontext.go"
import (
    "github.com/zeromicro/go-zero/zrpc"
    "myservice/greeter"  // 生成的 proto 包
)

func NewServiceContext(c config.Config) *ServiceContext {
    conn, err := zrpc.NewClient(zrpc.RpcClientConf{
        Endpoints: []string{"localhost:8080"},
    })
    if err != nil {
        log.Fatal(err)
    }
    return &ServiceContext{
        Config:        c,
        GreeterClient: greeter.NewGreeterClient(conn.Conn()),
    }
}
```

## 方案 B：通过 etcd 服务发现（生产环境）

```yaml title="etc/app.yaml"
GreeterRpc:
  Etcd:
    Hosts:
      - 127.0.0.1:2379
    Key: greeter.rpc
  Timeout: 2000       # 请求超时（毫秒）
  KeepaliveTime: 20000
```

```go title="internal/svc/servicecontext.go"
func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:        c,
        GreeterClient: greeter.NewGreeterClient(
            zrpc.MustNewClient(c.GreeterRpc).Conn(),
        ),
    }
}
```

`MustNewClient` 启动阶段出错时会 panic。如需自行处理错误，请使用 `NewClient`。

## 发起调用

```go title="internal/logic/hellologic.go"
func (l *HelloLogic) Hello(req *types.HelloReq) (*types.HelloResp, error) {
    resp, err := l.svcCtx.GreeterClient.SayHello(l.ctx, &greeter.SayHelloReq{
        Name: req.Name,
    })
    if err != nil {
        return nil, err
    }
    return &types.HelloResp{Message: resp.Message}, nil
}
```

`l.ctx` 携带 OpenTelemetry trace context，下游 RPC span 会自动关联到父级 HTTP span。

## 配置参考

```yaml
GreeterRpc:
  # 方案一：etcd 服务发现
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: greeter.rpc

  # 方案二：静态地址
  Endpoints:
    - 127.0.0.1:8080

  Timeout: 2000           # 客户端请求超时（毫秒），0 表示不限
  KeepaliveTime: 20000    # gRPC keepalive ping 间隔（毫秒）
```

## 错误处理

gRPC 错误携带状态码，go-zero 熔断器会统计这些状态：

```go
import "google.golang.org/grpc/status"

resp, err := l.svcCtx.GreeterClient.SayHello(l.ctx, req)
if err != nil {
    st, _ := status.FromError(err)
    switch st.Code() {
    case codes.NotFound:
        return nil, errorx.NewCodeError(404, "用户不存在")
    case codes.DeadlineExceeded:
        return nil, errorx.NewCodeError(504, "上游超时")
    default:
        return nil, err
    }
}
```

## 熔断器

熔断器默认开启。10 秒内错误率超过 50% 时自动打开：

```
正常：  请求 → RPC 调用 → 响应
断开：  请求 → 立即返回 503（不发 RPC）
半开：  允许单个探测请求通过以检查恢复情况
```

每个 `zrpc.Client` 自动生效，无需额外配置。

## 添加拦截器

向每次请求注入自定义元数据（如 API Token、用户 ID）：

```go
conn, err := zrpc.NewClient(c.GreeterRpc,
    zrpc.WithUnaryClientInterceptor(func(
        ctx context.Context, method string,
        req, reply any, cc *grpc.ClientConn,
        invoker grpc.UnaryInvoker, opts ...grpc.CallOption,
    ) error {
        ctx = metadata.AppendToOutgoingContext(ctx,
            "x-request-id", requestIDFromCtx(ctx),
        )
        return invoker(ctx, method, req, reply, cc, opts...)
    }),
)
```

## 延伸阅读

- [gRPC 拦截器](./interceptor) — 服务端与客户端拦截器详解
- [负载均衡](../microservice/load-balancing) — P2C 如何在多实例间路由
"""

# ─── tutorials/microservice/distributed-tracing.md ─────────────────────────
files["tutorials/microservice/distributed-tracing.md"] = """\
---
title: 分布式链路追踪
description: 使用 OpenTelemetry 与 Jaeger 追踪 go-zero 服务，添加自定义 span、多端导出与日志关联。
sidebar:
  order: 3
---

# 分布式链路追踪

go-zero 内置 OpenTelemetry SDK，开箱即支持分布式链路追踪、跨服务 span 传播和 Prometheus 指标采集——无需手动埋点。

## 第一步：启动 Jaeger

```bash
docker run -d --name jaeger \\
  -p 5775:5775/udp -p 6831:6831/udp -p 6832:6832/udp \\
  -p 5778:5778 -p 16686:16686 -p 14268:14268 \\
  jaegertracing/all-in-one:latest
```

Jaeger UI：http://localhost:16686

## 第二步：配置服务

```yaml title="etc/user-api.yaml"
Telemetry:
  Name: user-api
  Endpoint: http://localhost:14268/api/traces
  Sampler: 1.0      # 1.0 = 全量采样
  Batcher: jaeger   # 协议：jaeger | otlp
```

```yaml title="etc/user-rpc.yaml"
Telemetry:
  Name: user-rpc
  Endpoint: http://localhost:14268/api/traces
  Sampler: 1.0
  Batcher: jaeger
```

go-zero 在首次请求时自动注册追踪器，无需任何代码改动。

## 第三步：验证链路

发起 HTTP 请求后，打开 Jaeger UI 并查看 `user-api` 服务。一条完整的跨服务链路应如下所示：

```
user-api: POST /api/user/login  [12 ms]
  └─ user-rpc: UserService/Login  [8 ms]
       └─ MySQL: SELECT users  [3 ms]
```

## 第四步：添加自定义 Span

在 go-zero 服务中可以添加任意自定义 span：

```go
import (
    "go.opentelemetry.io/otel"
    "go.opentelemetry.io/otel/attribute"
)

func (l *LoginLogic) Login(req *types.LoginReq) (*types.LoginResp, error) {
    // 开始自定义 span
    tracer := otel.Tracer("user-api")
    ctx, span := tracer.Start(l.ctx, "validate-credentials")
    defer span.End()

    // 为 span 添加属性
    span.SetAttributes(
        attribute.String("user.email", req.Email),
        attribute.String("auth.method", "password"),
    )

    // 执行业务逻辑
    if err := l.validatePassword(ctx, req); err != nil {
        span.RecordError(err)
        return nil, err
    }
    // ...
}
```

## 第五步：使用 OTLP 导出至 Grafana Tempo

```yaml title="etc/app.yaml"
Telemetry:
  Name: user-api
  Endpoint: http://tempo:4318/v1/traces
  Sampler: 1.0
  Batcher: otlp    # OTLP HTTP 协议
```

使用 OpenTelemetry Collector 代理时，可同时输出到多个后端：

```yaml title="otel-collector.yaml"
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  otlp/tempo:
    endpoint: tempo:4317
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [jaeger, otlp/tempo]
```

## 第六步：日志关联 Trace ID

go-zero 自动将 `trace_id` 和 `span_id` 注入结构化日志输出：

```json
{
  "level": "info",
  "ts": "2024-01-15T10:30:45Z",
  "msg": "user login",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "user_id": 12345
}
```

在 Grafana 中可使用 trace_id 在 Tempo 与 Loki 日志之间一键跳转。

## 延伸阅读

- [负载均衡](./load-balancing) — 了解请求如何在多实例间分发
- [架构概览](../../concepts/architecture) — Observability 流水线全貌
"""

# ─── tutorials/microservice/load-balancing.md ───────────────────────────────
files["tutorials/microservice/load-balancing.md"] = """\
---
title: 负载均衡
description: go-zero 默认使用 P2C 负载均衡，结合延迟感知与健康检查，智能路由 RPC 请求。
sidebar:
  order: 2
---

# 负载均衡

go-zero 的 `zrpc` 客户端默认使用 **P2C（Pick of Two Choices，二选一）** 负载均衡，相较于传统轮询更能感知实例延迟。

## P2C 算法原理

<pre class="mermaid">
flowchart LR
    Client -->|随机选两个实例| A[实例 A<br/>延迟 12 ms]
    Client --> B[实例 B<br/>延迟 45 ms]
    A -->|✓ 延迟更低，被选中| Req[发送请求]
    B -->|✗ 跳过| Skip[未选中]
</pre>

每次发起请求时，P2C 会从候选实例中**随机选取两个**，然后将请求路由至负载（延迟 × 在途请求数）更低的那个。这个 O(1) 的算法解决了轮询面对"慢实例"时的热点问题。

## 默认行为

当使用 etcd 服务发现时，P2C 负载均衡**自动生效**，无需任何配置：

```yaml title="etc/app.yaml"
UserRpc:
  Etcd:
    Hosts: [127.0.0.1:2379]
    Key: user.rpc
```

etcd 中每个注册的实例都会自动纳入 P2C 的候选池。

## 静态端点（轮询）

使用静态地址列表时，go-zero 使用轮询策略：

```yaml
UserRpc:
  Endpoints:
    - 10.0.0.1:8080
    - 10.0.0.2:8080
    - 10.0.0.3:8080
```

## 直连（无负载均衡）

测试或调试时，可以直接指定单个实例：

```yaml
UserRpc:
  Endpoints:
    - 127.0.0.1:8080
```

## Kubernetes 集成

在 Kubernetes 中，通常将 go-zero 服务作为 Headless Service 部署，结合 Pod DNS 地址实现均衡：

```yaml title="k8s/service.yaml"
apiVersion: v1
kind: Service
metadata:
  name: user-rpc
spec:
  clusterIP: None   # Headless Service
  selector:
    app: user-rpc
  ports:
    - port: 8080
```

然后在 go-zero 配置中直接使用 DNS 地址：

```yaml
UserRpc:
  Target: dns:///user-rpc.default.svc.cluster.local:8080
```

## 可观测性

可通过 Prometheus 监控负载均衡效果：

| 指标名 | 说明 |
|---|---|
| `rpc_client_requests_total` | 各实例请求总数 |
| `rpc_client_duration_ms_bucket` | 各实例延迟直方图 |

在 Grafana 中用分位数折线图对比各 Pod 的 P99 延迟，可直观看到 P2C 是否有效均摊流量。

## 超时与 Keepalive

```yaml
UserRpc:
  Timeout: 2000           # 单次请求超时（毫秒）
  KeepaliveTime: 20000    # TCP keepalive ping 间隔（毫秒）
```

超时期间只要约束对应 ctx 即可；go-zero 不会自动重试（防止副作用），如需重试请在业务层实现幂等逻辑后自行封装。

## 延伸阅读

- [gRPC 客户端](../grpc/client) — 客户端完整配置参考
- [分布式链路追踪](./distributed-tracing) — 追踪请求在各实例间的路径
"""

# ─── reference/goctl/model.md ───────────────────────────────────────────────
files["reference/goctl/model.md"] = """\
---
title: goctl model
description: 使用 goctl model 从 DDL、数据源或 MongoDB 生成数据库访问层代码。
sidebar:
  order: 3
---

# goctl model

`goctl model` 从 MySQL DDL、在线数据源或 MongoDB 集合生成完整的 Go 数据访问层代码，内置两级缓存（内存 LRU + Redis）。

## MySQL DDL → 代码

```bash
goctl model mysql ddl \\
  --src ./deploy/sql/user.sql \\
  --dir ./internal/model \\
  --cache
```

| 参数 | 说明 |
|---|---|
| `--src` | SQL DDL 文件路径 |
| `--dir` | 输出目录 |
| `--cache` | 启用 Redis 缓存层（推荐） |
| `--style` | 文件命名风格，默认 `goZero` |
| `--home` | 自定义模板目录 |
| `--idea` | 以机器可读格式输出错误（IDE 集成用） |

生成的文件结构：

```
internal/model/
├── usermodel.go         ← CRUD 方法
├── usermodel_gen.go     ← 自动生成代码（请勿手动修改）
└── vars.go              ← 错误变量（ErrNotFound 等）
```

## MySQL 数据源（在线生成）

直接连接到现有数据库进行代码生成：

```bash
goctl model mysql datasource \\
  --url "root:password@tcp(localhost:3306)/mydb" \\
  --table "user,order" \\
  --dir ./internal/model \\
  --cache
```

| 参数 | 说明 |
|---|---|
| `--url` | DSN 连接字符串 |
| `--table` | 表名，逗号分隔；支持通配符 `*` |
| `--dir` | 输出目录 |
| `--cache` | 启用缓存层 |
| `--strict` | 将 null 列映射为 Go 指针类型 |

## PostgreSQL 数据源

```bash
goctl model pg datasource \\
  --url "postgres://user:pass@localhost:5432/mydb?sslmode=disable" \\
  --table "public.users" \\
  --dir ./internal/model \\
  --cache
```

| 参数 | 说明 |
|---|---|
| `--url` | PostgreSQL DSN |
| `--table` | `schema.table` 格式 |
| `--schema` | Schema 名称，默认 `public` |
| `--dir` | 输出目录 |
| `--cache` | 启用缓存层 |

## MongoDB

```bash
goctl model mongo \\
  --type User \\
  --dir ./internal/model \\
  --easy
```

| 参数 | 说明 |
|---|---|
| `--type` | Go 类型名称 |
| `--dir` | 输出目录 |
| `--easy` | 生成 `FindOne`/`Insert`/`Update`/`Delete` 简化方法 |
| `--home` | 自定义模板目录 |

## 缓存层说明

使用 `--cache` 生成的 model 包含两级缓存：

1. **内存 LRU**：进程级热数据缓存，减少 Redis 访问
2. **Redis**：跨实例分布式缓存，WriteThrough 策略

缓存管理遵循以下规则：
- 每次写操作（Create/Update/Delete）自动失效对应缓存 key
- 缓存 key 格式：`cache:<db>:<table>:<主键>:<值>`
- TTL 默认 7 天，可通过 `CacheConf` 覆盖

使用缓存时，config 需要添加 `CacheConf`：

```go
type Config struct {
    rest.RestConf
    DB struct {
        DataSource string
    }
    CacheRedis cache.CacheConf
}
```

## 自定义模板

导出默认模板并按需修改：

```bash
# 导出 model 模板到 ~/.goctl/
goctl template init --category model

# 修改模板后重新生成代码
goctl model mysql ddl \\
  --src user.sql \\
  --dir ./internal/model \\
  --home ~/.goctl
```

## 延伸阅读

- [goctl 命令参考](./commands) — 全部子命令与参数
- [MySQL 教程](../../tutorials/database/mysql) — 在 go-zero 服务中使用生成的 model
"""

# ─── reference/goctl/commands.md ────────────────────────────────────────────
files["reference/goctl/commands.md"] = """\
---
title: goctl 命令参考
description: goctl 全量命令与参数说明，涵盖 api、rpc、model、docker、kube 等所有子命令。
sidebar:
  order: 1
---

# goctl 命令参考

`goctl` 是 go-zero 的代码生成 CLI。本文列出所有命令及其参数。

## goctl api

```bash
goctl api new <service-name>        # 创建新 API 项目脚手架
goctl api go   --api <file> --dir <dir>  # 从 .api 文件生成 Go 代码
goctl api validate --api <file>     # 语法校验
goctl api format --dir <dir>        # 格式化 .api 文件
goctl api doc --dir <dir>           # 生成 Markdown 文档
```

### goctl api go

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--api` | — | .api 文件路径（必填） |
| `--dir` | `.` | 输出目录 |
| `--style` | `goZero` | 文件命名风格 |
| `--home` | `~/.goctl` | 自定义模板目录 |
| `--remote` | — | 指定远程模板仓库 |
| `--branch` | — | 远程模板分支 |
| `--idea` | `false` | 机器可读输出（IDE 集成用） |

## goctl rpc

```bash
goctl rpc new <service-name>        # 创建新 RPC 项目脚手架
goctl rpc protoc <proto-file> ...   # 从 .proto 生成 Go 代码
```

### goctl rpc protoc

```bash
goctl rpc protoc user.proto \\
  --go_out=./pb \\
  --go-grpc_out=./pb \\
  --zrpc_out=. \\
  --style goZero
```

| 参数 | 说明 |
|---|---|
| `--go_out` | protoc-gen-go 输出目录 |
| `--go-grpc_out` | protoc-gen-go-grpc 输出目录 |
| `--zrpc_out` | go-zero RPC 骨架输出目录 |
| `--style` | 文件命名风格 |
| `--home` | 自定义模板目录 |
| `--idea` | 机器可读输出 |

## goctl model

```bash
goctl model mysql ddl        --src <file>  --dir <dir>  [--cache]
goctl model mysql datasource --url <dsn>   --table <t>  --dir <dir>  [--cache]
goctl model pg    datasource --url <dsn>   --table <t>  --dir <dir>  [--cache]
goctl model mongo            --type <T>    --dir <dir>  [--easy]
```

参数说明见 [goctl model 参考](./model)。

## goctl docker

从 go-zero 项目生成多阶段 Dockerfile：

```bash
goctl docker --go main.go --port 8888
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--go` | — | main.go 入口文件路径 |
| `--port` | `8080` | 暴露端口 |
| `--version` | — | 基础 Go 镜像版本 |
| `--home` | `~/.goctl` | 自定义模板目录 |
| `--tz` | `Asia/Shanghai` | 容器时区 |
| `--base` | `scratch` | 运行时基础镜像 |

## goctl kube

```bash
goctl kube deploy \\
  --name user-api \\
  --namespace default \\
  --image myregistry/user-api:v1.0.0 \\
  --port 8888 \\
  -o user-api.yaml
```

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--name` | — | Deployment 名称 |
| `--namespace` | `default` | Kubernetes 命名空间 |
| `--image` | — | 容器镜像引用 |
| `--replicas` | `3` | Deployment 副本数 |
| `--port` | — | 容器监听端口 |
| `--minReplicas` | `3` | HPA 最小实例数 |
| `--maxReplicas` | `10` | HPA 最大实例数 |
| `--requestCpu` | `500` | CPU request（m） |
| `--requestMem` | `512` | 内存 request（Mi） |
| `--limitCpu` | `1000` | CPU limit（m） |
| `--limitMem` | `1024` | 内存 limit（Mi） |
| `--imagePullPolicy` | `IfNotPresent` | 镜像拉取策略 |
| `-o` | — | 输出文件路径 |
| `--home` | `~/.goctl` | 自定义模板目录 |

## goctl template

```bash
goctl template init              # 初始化默认模板到 ~/.goctl/
goctl template clean             # 清空本地模板缓存
goctl template update            # 更新模板到最新版本
goctl template revert --category api   # 还原指定类别模板
```

## goctl env

```bash
goctl env check     # 检查所有依赖工具
goctl env install   # 自动安装缺失工具
```

`goctl env check` 会验证以下依赖：protoc、protoc-gen-go、protoc-gen-go-grpc、goctl-gen-go-rpc。

## goctl upgrade

```bash
goctl upgrade   # 升级 goctl 至最新版本
```

## 文件命名风格

| 风格 | 示例 |
|---|---|
| `goZero`（默认） | `userhandler.go` |
| `go_zero` | `user_handler.go` |
| `GoZero` | `UserHandler.go` |

## 全局参数

所有 goctl 子命令均支持以下全局参数：

| 参数 | 说明 |
|---|---|
| `--home` | 自定义模板目录，覆盖 `~/.goctl` |
| `--remote` | Git 仓库 URL，用于远程模板 |
| `--branch` | 远程模板的 Git 分支 |
| `--style` | 生成文件的命名风格 |
"""

# ─── concepts/architecture.md ───────────────────────────────────────────────
files["concepts/architecture.md"] = """\
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
"""

# Write all files
for rel_path, content in files.items():
    p = base / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"✅ zh-cn/{rel_path} ({len(content.splitlines())} lines)")

print("\nAll zh-cn files written successfully.")
