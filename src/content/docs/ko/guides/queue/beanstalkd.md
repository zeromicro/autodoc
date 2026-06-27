---
title: Beanstalkd 큐
description: go-zero에서 Beanstalkd를 지연 큐로 사용하는 방법입니다.
sidebar:
  order: 3

---


## 개요

지연 큐는 예약 작업에 유용합니다. 예를 들어 주문이 생성된 뒤 20분 동안 결제되지 않으면 자동으로 취소하는 작업을 처리할 수 있습니다.

[go-queue](https://github.com/zeromicro/go-queue)는 Kafka 메시지 큐 `kq` 외에도 [beanstalkd](https://beanstalkd.github.io/) 기반 지연 큐 `dq`를 제공합니다.

### 설정

```go
type (
    Beanstalk struct {
        Endpoint string
        Tube     string
    }

    DqConf struct {
        Beanstalks []Beanstalk
        Redis      redis.RedisConf
    }
)
```

- `Beanstalks`: 여러 Beanstalk 노드 설정입니다.
- `Redis`: Redis 설정입니다. 여기서는 주로 `SETNX`에 사용됩니다.

### go-zero에서 dq pusher 사용하기

먼저 프로젝트에 go-queue 의존성을 추가합니다.

```shell
$ go get github.com/zeromicro/go-queue@latest
```

현재 dq 설정 정보를 `etc/xxx.yaml` 설정 파일에 추가합니다.

```yaml
Name: dq
Host: 0.0.0.0
Port: 8888

......

DqConf:
  Beanstalks:
    - Endpoint: 127.0.0.1:7771
      Tube: tube1
    - Endpoint: 127.0.0.1:7772
      Tube: tube2
```

`internal/config/config.go`에서 Go 설정 매핑을 정의합니다.

```go
type Config struct {
    ......
    DqConf struct {
        Brokers []string
        Topic   string
    }
}
```

`svc/serviceContext.go`에서 dq producer client를 초기화합니다.

```go
type ServiceContext struct {
    Config         config.Config
  .....
    DqPusherClient dq.Producer
}

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:         c,
    .....
        DqPusherClient: dq.NewProducer(c.DqConf.Beanstalks),
    }
}
```

로직 계층에서 go-queue dq client를 사용해 beanstalkd로 메시지를 보냅니다.

```go
.......
func (l *PusherLogic) Pusher() error {

  msg := "data"

    // 1. 5초 뒤에 실행합니다
    deplayResp, err := l.svcCtx.DqPusherClient.Delay([]byte(msg), time.Second*5)
    if err != nil {
        logx.Errorf("error from DqPusherClient Delay err : %v", err)
    }
    logx.Infof("resp : %s", deplayResp) // fmt.Sprintf("%s/%s/%d", p.endpoint, p.tube, id)

    // 2. 지정한 시각에 실행합니다
    atResp, err := l.svcCtx.DqPusherClient.At([]byte(msg), time.Now())
    if err != nil {
        logx.Errorf("error from DqPusherClient Delay err : %v", err)
    }
    logx.Infof("resp : %s", atResp) // fmt.Sprintf("%s/%s/%d", p.endpoint, p.tube, id)

  return nil
}
```

### go-zero에서 dq consumer 사용하기

먼저 프로젝트에 go-queue 의존성을 추가합니다.

```shell
$ go get github.com/zeromicro/go-queue@latest
```

현재 dq 설정 정보를 `etc/xxx.yaml` 설정 파일에 추가합니다.

```yaml
Name: dq
Host: 0.0.0.0
Port: 8889

.....

#dq
DqConf:
  Beanstalks:
    - Endpoint: 127.0.0.1:7771
      Tube: tube1
    - Endpoint: 127.0.0.1:7772
      Tube: tube2
  Redis:
    Host: 127.0.0.1:6379
    Type: node
```

`internal/config/config.go`에서 Go 설정 매핑을 정의합니다.

```go
package config

import (
    "github.com/zeromicro/go-queue/dq"
    "github.com/zeromicro/go-zero/rest"
)

type Config struct {
    rest.RestConf
    .......
    DqConf dq.DqConf
}
```

`svc/serviceContext.go`에서 dq consumer client를 초기화합니다.

```go
type ServiceContext struct {
    Config         config.Config
  .....
    DqConsumer dq.Consumer
}

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:         c,
    .....
        DqConsumer: dq.NewConsumer(c.DqConf),
    }
}
```

로직에서 지연 메시지를 소비합니다.

```go
func (l *PusherLogic) Consumer() error {
  l.svcCtx.DqConsumer.Consume(func(body []byte) {
        logx.Infof("consumer job  %s \n", string(body))
    })
}
```

beanstalkd 자체는 Redis에 의존하지 않습니다. go-queue는 같은 메시지가 두 번 이상 소비되는 것을 막기 위해 Redis `SETNX`를 짧은 기간의 중복 제거 필터로 사용합니다.

## 참조

1. [Beanstalkd 소개와 설치](https://beanstalkd.github.io/)
