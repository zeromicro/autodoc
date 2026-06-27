---
title: gRPC 서버 설정
description: go-zero의 gRPC 서버 설정에 대해 설명합니다.
sidebar:
  order: 2

---


## 개요

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

### 설정

zRPC 서버 설정 Structure 상태 below：

```go
type RpcServerConf struct {
    service.ServiceConf
    ListenOn      string
    Etcd          discov.EtcdConf    `json:",optional,inherit"`
    Auth          bool               `json:",optional"`
    Redis         redis.RedisKeyConf `json:",optional"`
    StrictControl bool               `json:",optional"`
    // 0으로 설정하면 타임아웃이 없다는 뜻입니다
    Timeout      int64 `json:",default=2000"`
    CpuThreshold int64 `json:",default=900,range=[0:1000]"`
    // gRPC 헬스 체크 스위치
    Health      bool `json:",default=true"`
    Middlewares ServerMiddlewaresConf
}
```

#### RpcServerConf

| Name          | DataType              | Meaning                                                                                      | 기본값 value | 필수? |
| ------------- | --------------------- | -------------------------------------------------------------------------------------------- | ------------- | --------- |
| ServiceConf   | ServiceConf           | 기본 서비스 설정                                                                  | None          | YES       |
| ListenOn      | string                | Listening address                                                                            | None          | YES       |
| Etcd          | EtcdConf              | etcd 설정 Item                                                                      | None          | 없음        |
| 인증          | bool                  | 인증 활성화됨                                                                                 | None          | 없음        |
| Redis         | RedisKeyConf          | rpc 인증, 만 경우 인증 is true                                                     | None          | 없음        |
| StrictControl | bool                  | _Whether Strict Mode, 경우 오류 is 인증 failed, otherwise it can be considered successful_ | None          | 없음        |
| 타임아웃       | int64                 | 타임아웃                                                                                      | 2000ms        | 없음        |
| CpuThreshold  | int64                 | Downloading 임계값,기본값 900(90%),Allow range 0 로 1000                                 | 900           | 없음        |
| 헬스        | bool                  | 활성화 헬스 체크                                                                          | true          | 없음        |
| Middlewares   | ServerMiddlewaresConf | 활성화 미들웨어                                                                            | None          | 없음        |

위한 ServiceConfig general 설정, see [기본 서비스 설정](../../../reference/configuration/service-config.md).

#### EtcdConf

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```go
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
```

| Name        | DataType          | Meaning                                                                               | 기본값 value | 필수? |
| ----------- | ----------------- | ------------------------------------------------------------------------------------- | ------------- | --------- |
| Hosts       | String 타입 Array | etcd cluster address                                                                  | None          | YES       |
| Key         | string            | Defines unique expression 의 서비스, 사용됨 위한 서비스 registration 디스커버리 | None          | YES       |
| User        | string            | etcd username                                                                         | None          | 없음        |
| Pass        | string            | etcd password                                                                         | None          | 없음        |
| CertFile    | tring             | Certificate 파일                                                                      | None          | 없음        |
| CertKeyFile | string            | 비공개 key 파일                                                                      | None          | 없음        |
| CACertFile  | String            | CA Certificate 파일                                                                   | None          | 없음        |

#### RedisKeyConf


```go
type (
    // A, RedisConf 예시입니다
    RedisConf struct {
        Host string
        Type string `json:",default=node,options=node|cluster"`
        Pass string `json:",optional"`
        Tls  bool   `json:",optional"`
    }

    // RedisKeyConf는 key를 포함한 redis 설정입니다.
    RedisKeyConf struct {
        RedisConf
        Key string
    }
)
```

| Name | DataType | Meaning                  | 기본값 value | 필수? |
| ---- | -------- | ------------------------ | ------------- | --------- |
| 호스트 | string   | Redis address, 호스트+포트 | None          | YES       |
| 타입 | string   | Redis 타입               | node          | 없음        |
| Pass | string   | Redis password           | None          | 없음        |
| Tls  | bool     | 활성화 tls               | false         | 없음        |
| Key  | string   | Redis key                | None          | YES       |

ServerMiddlewaresConf 설정：

```go
ServerMiddlewaresConf struct {
    Trace      bool `json:",default=true"`
    Recover    bool `json:",default=true"`
    Stat       bool `json:",default=true"`
    Prometheus bool `json:",default=true"`
    Breaker    bool `json:",default=true"`
}
```

| Name       | DataType | Meaning                                                  | 기본값 value | 필수? |
| ---------- | -------- | -------------------------------------------------------- | ------------- | --------- |
| 추적      | bool     | 활성화 link tracking                                     | true          | 없음        |
| Recover    | bool     | Whether 또는 아님 로 활성화 abnormal capture intermediation | true          | 없음        |
| Stat       | bool     | Whether 로 turn 에서 stats intermediate                    | true          | 없음        |
| Prometheus | bool     | 활성화 Prometheus 미들웨어                             | true          | 없음        |
| 브레이커    | bool     | 활성화 브레이커 intermediate                              | true          | 없음        |
