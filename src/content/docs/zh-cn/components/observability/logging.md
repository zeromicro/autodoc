---
title: 日志
description: 统一日志规范与采集策略。
sidebar:
  order: 10
---

# 日志

go-zero 的 `logx` 包提供结构化、分级、零分配 JSON 日志，并自动关联 trace 信息。

## 基本用法

```go
import "github.com/zeromicro/go-zero/core/logx"

logx.Info("服务已启动")
logx.Infof("监听端口 %d", port)
logx.Infow("订单已创建",
    logx.Field("orderId", id),
    logx.Field("userId", userId),
    logx.Field("amount", amount),
)
logx.Errorw("数据库错误", logx.Field("err", err), logx.Field("query", sql))
```

## 日志级别

```go
logx.Debug("详细调试信息")     // 默认不输出，Level 设为 "debug" 时生效
logx.Info("正常运行信息")
logx.Slow("查询耗时 200ms")    // 用于慢操作阈值告警
logx.Error("发生错误")
logx.Severe("严重故障")       // 同时写入 stderr
```

级别由低到高：`debug < info < slow < error < severe`

## 配置

```yaml title="etc/app.yaml"
Log:
  ServiceName: order-api
  Mode: file              # "console" | "file" | "volume"
  Path: /var/log/order-api
  Level: info             # "debug" | "info" | "error"
  Encoding: json          # "json" | "plain"
  Compress: true          # 对已轮转的日志文件进行 gzip 压缩
  KeepDays: 7             # 删除 N 天之前的日志文件
  StackCooldownMillis: 100
```

### 输出模式说明

| 模式 | 行为 |
|------|------|
| `console` | 写入 stdout，适合容器和本地开发 |
| `file` | 写入 `<Path>/<ServiceName>.log`，按天轮转 |
| `volume` | 写入挂载卷（行为同 `file`） |

## 上下文日志

使用 `logx.WithContext` 自动附加当前的 trace ID 和 span ID：

```go
func (l *OrderLogic) CreateOrder(req *types.OrderReq) (*types.OrderResp, error) {
    // l.Logger 已预绑定到 l.ctx
    l.Logger.Infow("正在创建订单",
        logx.Field("userId", req.UserId),
        logx.Field("amount", req.Amount),
    )
    // 输出：{"level":"info","trace_id":"4bf92...","span_id":"00f06...","userId":42,"amount":100}
    return nil, nil
}
```

在 logic 结构体之外使用：

```go
logger := logx.WithContext(ctx)
logger.Infow("事件", logx.Field("key", value))
```

## 日志采样

高吞吐服务每秒产生大量日志。可通过代码控制采样：

```go
logx.SetLevel(logx.InfoLevel)
logx.DisableStat()   // 关闭周期性 CPU/内存统计日志
```

## 自定义写入器

将日志路由到任意 `io.Writer`——适合接入 Sentry、Loki 或日志聚合系统：

```go
logx.SetWriter(logx.NewWriter(myWriter))
```

多目标输出（扇出）：

```go
type teeWriter struct {
    a, b io.Writer
}
func (t *teeWriter) Write(p []byte) (int, error) {
    t.a.Write(p)
    return t.b.Write(p)
}
logx.SetWriter(logx.NewWriter(&teeWriter{os.Stdout, sentryWriter}))
```

## 测试时禁用日志

在单元测试中屏蔽所有日志输出：

```go
func TestMain(m *testing.M) {
    logx.Disable()
    os.Exit(m.Run())
}
```

## 结构化字段模式

| 场景 | 写法 |
|------|------|
| 错误（带堆栈） | `logx.Field("err", err)` |
| 耗时 | `logx.Field("latency", time.Since(start))` |
| 切片 | `logx.Field("ids", ids)` |
| 嵌套结构体 | `logx.Field("req", req)`（自动序列化为 JSON） |

## 慢日志阈值

超过 `Timeout` 的请求会被 go-zero 自动以 `slow` 级别记录——无需额外代码：

```yaml
Timeout: 3000   # 超过 3 秒的请求自动进入慢日志
```
