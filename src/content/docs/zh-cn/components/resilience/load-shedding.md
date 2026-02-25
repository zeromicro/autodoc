---
title: 降载
description: 通过过载保护机制避免系统雪崩。
sidebar:
  order: 5

---


go-zero 基于 CPU 使用率和在途请求数实现**自适应降载**。当系统过载时，新请求会被拒绝（HTTP 503 / gRPC UNAVAILABLE），以保护正在处理的请求。

## 工作原理

降载器同时监测两个指标：

1. **CPU 使用率** — 每 250 ms 采样一次，超过阈值（默认 90%）时激活降载。
2. **通过率** — 滑动窗口内已完成请求与总尝试请求的比率。通过率低于阈值时拒绝新请求。

## HTTP 服务

降载对每个 `rest.Server` **默认开启**，在 YAML 中配置 CPU 阈值：

```yaml title="etc/app.yaml"
CpuThreshold: 900  # 90%，单位为毫核×10（0-1000）
```

请求被降载时返回 **HTTP 503**。自定义响应体：

```go
server := rest.MustNewServer(c.RestConf,
    rest.WithUnauthorizedCallback(func(w http.ResponseWriter, r *http.Request, err error) {
        httpx.WriteJson(w, http.StatusServiceUnavailable, map[string]string{
            "code": "OVERLOADED",
            "msg":  "服务暂时不可用",
        })
    }),
)
```

## gRPC 服务

`SheddingInterceptor` **自动注册**到每个 `zrpc.Server`。被降载的请求返回 `codes.ResourceExhausted`。

## 自定义降载器

用于非 HTTP 工作负载（如消息消费者）：

```go
import "github.com/zeromicro/go-zero/core/load"

shedder := load.NewAdaptiveShedder(
    load.WithCpuThreshold(800),        // 80% CPU 触发降载
    load.WithWindow(5*time.Second),    // 滑动窗口大小
    load.WithBuckets(50),              // 窗口桶数（精度）
)

func processMessage(msg Message) error {
    promise, err := shedder.Allow()
    if err != nil {
        metrics.Inc("messages.shed")
        return ErrOverloaded
    }

    procErr := handle(msg)

    // 必须调用 Pass 或 Fail
    if procErr != nil {
        promise.Fail()
    } else {
        promise.Pass()
    }
    return procErr
}
```

:::caution[必须关闭 promise]
每次 `Allow()` 成功后，**必须**调用一次 `promise.Pass()` 或 `promise.Fail()`。泄漏 promise 会导致通过率计算偏差，进而引发误降载或永久不降载。
:::

## 配置参数

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `WithCpuThreshold(n)` | `900` | CPU 阈值（0-1000，单位毫核×10）|
| `WithWindow(d)` | `5s` | 滑动窗口时长 |
| `WithBuckets(n)` | `50` | 窗口桶数量 |

## 指标

开启 Prometheus 后，降载器导出：

| 指标 | 类型 | 说明 |
|------|------|------|
| `shedding_drops_total` | Counter | 被降载请求总数 |
| `shedding_pass_total` | Counter | 通过请求总数 |
| `cpu_usage` | Gauge | 当前 CPU 用量（0-1000）|

## 最佳实践

- 无状态服务可设置较高阈值（900-950），CPU 密集型服务建议设为 700-800。
- 监控 `shedding_drops_total` 与错误率，下游慢依赖往往是 drops 飙升的根因。
- 与熔断器、限流器配合使用，构建多层防御体系。
