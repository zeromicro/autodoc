---
title: Service Configuration
description: Full reference for go-zero HTTP service configuration.
sidebar:
  order: 3

---


## Service Overview

[ServiceConf](https://github.com/zeromicro/go-zero/blob/master/core/service/serviceconf.go) This configuration is used to represent a configuration of our independent service.He is quoted by our rest,zrpc and so on. Of course, we can simply define our services.

Example:

```go
package main

import (
    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/core/service"
    "github.com/zeromicro/go-zero/zrpc"
)

type JobConfig struct {
    service.ServiceConf
    UserRpc zrpc.RpcClientConf
}

func main() {
    var c JobConfig
    conf.MustLoad("config.yaml", &c)

    c.MustSetUp()
    // do your job
}

```

As above, we defined a JobConfig, and initially set **MustSetup** at startup, so that we can start a service service, which automatically integrates Metrics, Prometheus, Trace , DevServer, Log and other capabilities.

## Definition of parameters

ServiceConf configuration defined as follows:

```go
// A ServiceConf is a service config.
type ServiceConf struct {
    Name       string
    Log        logx.LogConf
    Mode       string `json:",default=pro,options=dev|test|rt|pre|pro"`
    MetricsUrl string `json:",optional"`
    // Deprecated: please use DevServer
    Prometheus prometheus.Config `json:",optional"`
    Telemetry  trace.Config      `json:",optional"`
    DevServer  devserver.Config  `json:",optional"`
}
```

| Params     | DataType          | Default value | Note                                                                                              | Enum Values          |
| ---------- | ----------------- | ------------- | ------------------------------------------------------------------------------------------------- | -------------------- |
| Name       | string            | -             | Define the name of the service, which will appear in log and tracer                               |                      |
| Log        | logx.LogConf      | -             | Refer to [log](./log)                                         |                      |
| Mode       | string            | pro           | Service environment. Dev is currently defined.In dev environment we will turn on reflection       | dev,test,rt,pre, pro |
| MetricsUrl | string            | 空             | Tap to report and we'll report some metrics to the corresponding address, if empty, not an orphan |                      |
| Prometheus | prometheus.Config | -             | References [Prometheus](../../../components/observability/metrics)    |                      |
| Telemetry  | trace.Config      | -             | References [Tracing](../../../components/observability/tracing)                                         |                      |
| DevServer  | devserver.Config  | -             | go-Zero version `v1.4.3` and above                                                                |                      |
