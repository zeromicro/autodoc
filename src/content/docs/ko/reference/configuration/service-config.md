---
title: 서비스 설정
description: go-zero의 서비스 설정에 대해 설명합니다.
sidebar:
  order: 5

---


## Service 개요


예제:

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


## Definition 의 매개변수

ServiceConf 설정 defined 다음과 같이:

```go
// A, ServiceConf 예시입니다
type ServiceConf struct {
    Name       string
    Log        logx.LogConf
    Mode       string `json:",default=pro,options=dev|test|rt|pre|pro"`
    MetricsUrl string `json:",optional"`
    // Deprecated, Dev서버 진입점
    Prometheus prometheus.Config `json:",optional"`
    Telemetry  trace.Config      `json:",optional"`
    DevServer  devserver.Config  `json:",optional"`
}
```

| Params     | DataType          | 기본값 value | 참고                                                                                              | Enum Values          |
| ---------- | ----------------- | ------------- | ------------------------------------------------------------------------------------------------- | -------------------- |
| Name       | string            | -             |해당 항목의 동작과 사용법을 설명합니다.                               |                      |
| 로그        | logx.LogConf      | -             | Refer 로 [로그 설정](https://github.com/zeromicro/go-zero/blob/master/core/service/serviceconf.go)                                                                |                      |
| Mode       | string            | pro           |해당 항목의 동작과 사용법을 설명합니다.       | dev,테스트,rt,pre, pro |
| 메트릭Url | string            | 空             |해당 항목의 동작과 사용법을 설명합니다. |                      |
| Prometheus | prometheus.설정 | -             | 참조 [Prometheus](log/)    |                      |
| Telemetry  | 추적.설정      | -             | 참조 [추적](../../../components/observability/metrics)                                         |                      |
| DevServer  | devserver.설정  | -             | go-Zero 버전 `v1.4.3`과 above                                                                |                      |
