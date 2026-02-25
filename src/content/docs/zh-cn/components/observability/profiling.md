---
title: 持续性能分析
description: 使用 go-zero 集成 Pyroscope 在生产环境实时进行 CPU 和内存分析
sidebar:
  order: 4
---

import { Aside } from '@astrojs/starlight/components';


在微服务架构日益复杂、业务流量不断攀升的背景下，系统的稳定性成为我们追求的核心目标。而性能问题的排查，往往需要结合指标监控、日志、tracing，还少不了最难搞的 CPU/内存 Profiling。

现在，go-zero 支持原生集成 Continuous Profiling（持续性能分析），通过集成 [Pyroscope](https://grafana.com/docs/pyroscope/)，你可以方便地在生产环境中实时采集性能数据，做到：

- ✅ 定位性能瓶颈
- ✅ 追踪 CPU/内存/协程异常
- ✅ 分析线上热点函数
- ✅ 降低系统维护成本

<Aside type="tip">
需要 **go-zero ≥ v1.8.4**
</Aside>

## 为什么使用持续 Profiling？

传统的 `pprof` 工具虽然强大，但使用成本高：手动触发、文件下载、手动分析，难以做到自动化、实时性、对用户透明。

| 传统 `pprof` | 持续 Profiling |
|-------------|--------------|
| 手动触发 | 自动、持续采集 |
| 下载文件，离线分析 | 浏览器实时查看火焰图 |
| 需要侵入业务代码 | 对开发者完全透明 |
| 单点快照 | 趋势分析 |

**推荐使用场景：**
- CPU 使用突然升高，无法本地复现？
- 有内存泄漏，定位不到是哪段逻辑？
- 想知道服务 QPS 提高后瓶颈在哪？
- 支持 Grafana 可视化集成，运维与研发协同分析

## 第一步：本地部署 Pyroscope

使用 Docker 一键启动：

```bash
docker pull grafana/pyroscope
docker run -it -p 4040:4040 grafana/pyroscope
```

访问 `http://localhost:4040` 即可查看火焰图等可视化分析数据。

详细参考：[Pyroscope 官方文档](https://grafana.com/docs/pyroscope/latest/get-started/)

## 第二步：快速创建示例项目

```bash
# 创建示例项目
goctl quickstart -t mono

# 进入项目目录
cd greet/api
```

## 第三步：配置文件启用 Profiling

在 `etc/greet.yaml` 配置文件中添加 Profiling 配置：

```yaml
Name: ping
Host: localhost
Port: 8888
Log:
  Level: error
# 添加 Profiling 配置
Profiling:
  ServerAddr: http://localhost:4040  # 必须项
  CpuThreshold: 0                    # 设置为 0 表示持续采集，便于演示
```

### 支持参数说明

| 参数名 | 默认值 | 含义 |
|--------|--------|------|
| `CpuThreshold` | `700` | 即 70%，超过触发采集；为 0 表示持续采集 |
| `UploadDuration` | `15s` | 上报间隔 |
| `ProfilingDuration` | `2m` | 每次采集时长 |
| `ProfileType` | 见下方 | 支持 CPU、内存、协程、互斥锁等类型 |

```go
ProfileType struct {
    CPU        bool `json:",default=true"`
    Memory     bool `json:",default=true"`
    Goroutines bool `json:",default=true"`
    Mutex      bool `json:",default=false"` // 会影响性能，默认关闭
    Block      bool `json:",default=false"` // 会影响性能，默认关闭
}
```

## 第四步：模拟 CPU 负载（可选）

为了更好地演示 Profiling 效果，在 `internal/logic/pinglogic.go` 中添加 CPU 密集型操作：

```go
func (l *PingLogic) Ping() (resp *types.Resp, err error) {
    // 模拟 CPU 密集型操作
    simulateCPULoad()
    return &types.Resp{Msg: "pong"}, nil
}

// 模拟 CPU 负载的函数
func simulateCPULoad() {
    for i := 0; i < 1000000; i++ {
        _ = i * i * i
    }
}
```

## 第五步：启动服务测试

```bash
# 启动服务
go run greet.go -f etc/greet.yaml

# 在另一个终端发送请求产生负载
hey -c 100 -z 60m "http://localhost:8888/ping"
```

由于设置了 `CpuThreshold: 0`，服务启动后会立即开始持续采集性能数据并上报到 Pyroscope。

访问 `http://localhost:4040`，火焰图中可以清楚地看到：

- `simulateCPULoad` 函数占用了大量 CPU 时间
- 可以精确定位到具体的代码热点
- 点击函数节点可展示调用链路

## 第六步：验证优化效果

移除模拟负载代码，重启服务后再次观察火焰图。可以看到 CPU 使用率显著降低，主要的性能消耗集中在 HTTP 处理和 JSON 序列化等正常操作上。

## 生产环境建议

- 生产环境使用 `CpuThreshold: 700`（70%），避免持续上报的开销
- 仅在排查特定并发问题时才开启 `Mutex` 和 `Block` 采集
- 为 Pyroscope 配置持久化存储，支持历史数据对比
- 结合 Grafana 仪表盘，将指标监控与性能分析整合

## 相关文档

- [指标监控](./metrics.md)
- [链路追踪](./tracing.md)
- [日志](../log/index.md)
