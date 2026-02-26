---
title: Continuous Profiling
description: Real-time CPU and memory profiling in production using go-zero's Pyroscope integration
sidebar:
  order: 4
---

import { Aside } from '@astrojs/starlight/components';


As microservice architectures grow more complex and traffic increases, performance issues become harder to diagnose. Traditional `pprof` profiling requires manual triggering, file downloads, and manual analysis — none of which work well in production.

go-zero supports native **Continuous Profiling** via [Pyroscope](https://grafana.com/docs/pyroscope/), letting you collect performance data in real time without touching business code.

**What you get:**
- Locate CPU bottlenecks
- Track abnormal CPU/memory/goroutine behavior
- Analyze hot functions in production
- Reduce on-call operational cost

<Aside type="tip">
Requires **go-zero ≥ v1.8.4**
</Aside>

## Why Continuous Profiling?

| Traditional `pprof` | Continuous Profiling |
|---------------------|---------------------|
| Manual trigger | Automatic, always-on |
| Download & analyze offline | Real-time flame graphs in browser |
| Intrusive (code changes) | Transparent to business code |
| Point-in-time snapshot | Trend analysis over time |

**Use cases:**
- CPU suddenly spikes — can't reproduce locally
- Memory leak — can't identify the code path
- Want to know where the bottleneck is at higher QPS
- Collaborative analysis between ops and development

## 1. Start Pyroscope Locally

```bash
docker pull grafana/pyroscope
docker run -it -p 4040:4040 grafana/pyroscope
```

Open `http://localhost:4040` to view flame graphs and visualization data.

See the [Pyroscope Getting Started guide](https://grafana.com/docs/pyroscope/latest/get-started/) for production deployment options.

## 2. Create a Sample Service

```bash
goctl quickstart -t mono
cd greet/api
```

## 3. Enable Profiling in Config

Add the `Profiling` section to `etc/greet.yaml`:

```yaml
Name: ping
Host: localhost
Port: 8888
Log:
  Level: error
Profiling:
  ServerAddr: http://localhost:4040   # required: Pyroscope server address
  CpuThreshold: 0                     # 0 = continuous collection (good for demos)
```

### Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `CpuThreshold` | `700` | Trigger threshold (700 = 70% CPU). Set to `0` for continuous collection. |
| `UploadDuration` | `15s` | How often to push profiles |
| `ProfilingDuration` | `2m` | Duration of each collection window |
| `ProfileType` | see below | What to collect |

```go
ProfileType struct {
    CPU        bool `json:",default=true"`
    Memory     bool `json:",default=true"`
    Goroutines bool `json:",default=true"`
    Mutex      bool `json:",default=false"` // disabled by default, affects performance
    Block      bool `json:",default=false"` // disabled by default, affects performance
}
```

## 4. Simulate CPU Load (Optional)

To see profiling in action, add a CPU-intensive operation in `internal/logic/pinglogic.go`:

```go
func (l *PingLogic) Ping() (resp *types.Resp, err error) {
    simulateCPULoad()
    return &types.Resp{Msg: "pong"}, nil
}

func simulateCPULoad() {
    for i := 0; i < 1000000; i++ {
        _ = i * i * i
    }
}
```

## 5. Run and Generate Load

```bash
# Start the service
go run greet.go -f etc/greet.yaml

# In another terminal — generate load
hey -c 100 -z 60m "http://localhost:8888/ping"
```

With `CpuThreshold: 0`, the service starts uploading profiles to Pyroscope immediately. Open `http://localhost:4040` to watch the flame graph update in real time.

The flame graph will clearly show `simulateCPULoad` consuming the majority of CPU time, letting you pinpoint the exact hot function.

## 6. Verify the Fix

Remove the artificial load, restart, and re-run the load test. The flame graph will confirm that CPU usage has dropped and the bottleneck is gone.

## Production Recommendations

- Use `CpuThreshold: 700` (70%) in production to avoid continuous upload overhead
- Enable `Mutex` and `Block` profiling only when diagnosing specific concurrency issues
- Deploy Pyroscope with persistent storage for historical comparison
- Integrate with Grafana dashboards for combined metrics + profiles view

## Related

- [Metrics](./metrics/)
- [Tracing](./tracing/)
- [Logging](../log/)
