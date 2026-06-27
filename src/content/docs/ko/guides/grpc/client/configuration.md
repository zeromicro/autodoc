---
title: gRPC 클라이언트 설정
description: go-zero의 gRPC 클라이언트 설정에 대해 설명합니다.
sidebar:
  order: 2

---


## 개요

이 가이드는 사용하는 방법을 설명합니다: go-zero framework 위한 gRPC 클라이언트 개발.

## 설정

```go
type RpcClientConf struct {
    Etcd          discov.EtcdConf `json:",optional,inherit"`
    Endpoints     []string        `json:",optional"`
    Target        string          `json:",optional"`
    App           string          `json:",optional"`
    Token         string          `json:",optional"`
    NonBlock      bool            `json:",optional"`
    Timeout       int64           `json:",default=2000"`
    KeepaliveTime time.Duration   `json:",default=20s"`
    Middlewares   ClientMiddlewaresConf
}

type EtcdConf struct {
    Hosts              []string
    Key                string
    ID                 int64  `json:",optional"`
    User               string `json:",optional"`
    Pass               string `json:",optional"`
    CertFile           string `json:",optional"`
    CertKeyFile        string `json:",optional=CertFile"`
    CACertFile         string `json:",optional=CertFile"`
    InsecureSkipVerify bool   `json:",optional"`
}

type ServerMiddlewaresConf struct {
    Trace      bool `json:",default=true"`
    Recover    bool `json:",default=true"`
    Stat       bool `json:",default=true"`
    Prometheus bool `json:",default=true"`
    Breaker    bool `json:",default=true"`
}
```

### RpcClientConf

| Name          | DataType              | Meaning                                                                                          | 기본값 value | 필수? |
| ------------- | --------------------- | ------------------------------------------------------------------------------------------------ | ------------- | --------- |
| Etcd          | EtcdConf              | Service finds 설정, 때 사용하여 etcd 위한 서비스 디스커버리                               | None          | 없음        |
| 엔드포인트     | String 타입 Array     |해당 항목의 동작과 사용법을 설명합니다. | None          | 없음        |
| Target        | string                | Domain URL solved, please refer 로 https://github.com/grpc/grpc/blob/master/doc/naming.md        | None          | 없음        |
| App           | string                | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.                   | None          | 없음        |
| 토큰         | string                | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.                      | None          | 없음        |
| NonBlock      | bool                  |해당 항목의 동작과 사용법을 설명합니다.                                        | false         | 없음        |
| 타임아웃       | int64                 | 타임아웃 time                                                                                     | 2000ms        | 없음        |
| KeepaliveTime | Time.Duration         | Keepalive Time                                                                                   | 20s           | 없음        |
| Middlewares   | ClientMiddlewaresConf | 활성화 미들웨어                                                                                | None          | 없음        |

### EtcdConf

EtcdConf 설정 서비스 디스커버리 때 사용하여 etcd 위한 서비스 디스커버리.

| Name               | DataType          | Meaning                                         | 기본값 value | 필수? |
| ------------------ | ----------------- | ----------------------------------------------- | ------------- | --------- |
| Hosts              | String 타입 Array | etcd cluster address                            | None          | YES       |
| Key                | string            | 서비스 디스커버리 key                           | None          | YES       |
| ID                 | int64             | etcd tenant id                                  | None          | 없음        |
| User               | string            | etcd username                                   | None          | 없음        |
| Pass               | string            | etcd password                                   | None          | 없음        |
| CertFile           | string            | etcd certificate 파일                           | CertFile      | 없음        |
| CertKeyFile        | string            | etcd certificate 비공개 key 파일               | None          | 없음        |
| CACertFile         | string            | etcd certificate 파일                           | CertFile      | 없음        |
| InsecureSkipVerify | bool              | Whether 또는 아님 로 skip certificate verification | None          | 없음        |

### ServerMiddlewaresConf

ServerMidlewaresConf is configured 로서 intermediary, 때 control은 required입니다.

| Name       | DataType | Meaning                                 | 기본값 value | 필수? |
| ---------- | -------- | --------------------------------------- | ------------- | --------- |
| 추적      | bool     | 활성화 link tracking                    | true          | 없음        |
| Recover    | bool     | Whether 로 활성화 exception recovery | true          | 없음        |
| Stat       | bool     | 활성화 stats                            | true          | 없음        |
| Prometheus | bool     | Whether prometheus are 활성화됨          | true          | 없음        |
| 브레이커    | bool     | Whether 로 turn 에서 smelting             | true          | 없음        |
