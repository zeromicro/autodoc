---
title: Kafka 큐
description: go-zero에서 Kafka를 메시지 큐로 사용하는 방법입니다.
sidebar:
  order: 2

---


## go-queue의 kq(Kafka)

메시지 큐는 대규모 마이크로서비스 시스템에서 필수적인 구성 요소입니다. 주로 트래픽 피크를 흡수하고, 서비스 간 결합도를 낮추며, 비동기 처리 기능을 제공하는 데 사용됩니다.

[go-queue](https://github.com/zeromicro/go-queue)는 `segmentio/kafka-go` 패키지 위에 go-zero 스타일의 상위 추상화를 제공해 개발자가 Kafka 연동보다 비즈니스 로직에 더 집중할 수 있게 합니다.

### 1.1 설정

```go
type KqConf struct {
   service.ServiceConf
   Brokers    []string
   Group      string
   Topic      string
   Offset     string `json:",options=first|last,default=last"`
   Conns      int    `json:",default=1"`
   Consumers  int    `json:",default=8"`
   Processors int    `json:",default=8"`
   MinBytes   int    `json:",default=10240"`    // 10K
   MaxBytes   int    `json:",default=10485760"` // 10M
   Username   string `json:",optional"`
   Password   string `json:",optional"`
}
```

- `Brokers`: 여러 Kafka broker node입니다.
- `Group`: consumer group입니다.
- `Topic`: 구독할 topic입니다.
- `Offset`: 새 topic에 offset 정보가 없거나 현재 offset이 유효하지 않을 때(예: 과거 데이터 삭제) 처음부터 소비할지(`first`), 끝부터 소비할지(`last`) 지정합니다.
- `Conns`: Kafka queue 연결 수입니다. 하나의 Kafka queue에 여러 consumer가 대응할 수 있으며, 기본값은 1입니다.
- `Consumers`: go-queue 내부 channel로 Kafka 메시지를 가져오는 goroutine 수를 제어합니다. 실제 비즈니스 소비 로직의 동시 처리 수와는 다릅니다.
- `Processors`: `Consumers`가 channel로 가져온 메시지를 실제 소비 로직에 전달할 때 사용할 goroutine 수를 제어합니다.
- `MinBytes`: 한 번에 반환받을 최소 byte 수입니다.
- `MaxBytes`: 한 번에 반환받을 최대 byte 수입니다. 첫 메시지가 이 값을 초과하더라도 consumer가 계속 동작하도록 해당 메시지는 가져옵니다. 따라서 절대적인 제한은 아니며, broker의 `message.max.bytes`와 topic의 `max.message.bytes`도 함께 고려해야 합니다.
- `Username`: Kafka 계정입니다.
- `Password`: Kafka 비밀번호입니다.

### 1.2 go-zero에서 go-queue producer pusher 사용하기

먼저 프로젝트에 go-queue 의존성을 추가합니다.

```shell
$ go get github.com/zeromicro/go-queue@latest
```

현재 Kafka 설정 정보를 `etc/xxx.yaml` 설정 파일에 추가합니다.

```yaml
Name: mq
Host: 0.0.0.0
Port: 8888

......

KqPusherConf:
  Brokers:
    - 127.0.0.1:9092
  Topic: payment-success
```

`internal/config/config.go`에서 Go 설정 매핑을 정의합니다.

```go
type Config struct {
    ......
    KqPusherConf struct {
        Brokers []string
        Topic   string
    }
}
```

`svc/serviceContext.go`에서 kq client를 초기화합니다.

```go
type ServiceContext struct {
    Config         config.Config
  .....
    KqPusherClient *kq.Pusher
}

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:         c,
    .....
        KqPusherClient: kq.NewPusher(c.KqPusherConf.Brokers, c.KqPusherConf.Topic),
    }
}
```

로직 계층에서 go-queue의 kq client를 사용해 Kafka로 메시지를 보냅니다.

```go
.......
func (l *PusherLogic) Pusher() error {

  //......비즈니스 로직....

    data := "zhangSan"
    if err := l.svcCtx.KqPusherClient.Push(data); err != nil {
        logx.Errorf("KqPusherClient Push Error , err :%v", err)
    }

    return nil
}
```

`svc/serviceContext.go`에서 kq client를 초기화할 때 선택 매개변수를 전달할 수도 있습니다. `kq.NewPusher`는 세 번째 인자로 옵션을 받습니다.

- `chunkSize`: 효율을 위해 kq client는 메시지를 batch로 제출합니다. 누적 메시지 수가 이 크기에 도달하면 Kafka로 제출합니다.
- `flushInterval`: flush 주기입니다. `chunkSize`에 도달하지 않아도 이 주기가 지나면 Kafka로 제출합니다.

### 1.3 go-zero에서 go-queue consumer 사용하기

먼저 프로젝트에 go-queue 의존성을 추가합니다.

```shell
$ go get github.com/zeromicro/go-queue@latest
```

현재 Kafka 설정 정보를 `etc/xxx.yaml` 설정 파일에 추가합니다.

```yaml
Name: mq
Host: 0.0.0.0
Port: 8888

#kq
KqConsumerConf:
  Name: kqConsumer
  Brokers:
    - 127.0.1:9092
  Group: kqConsumer
  Topic: payment-success
  Offset: first
  Consumers: 8
  Processors: 8
```

`internal/config/config.go`에서 Go 설정 매핑을 정의합니다.

```go
package config

import (
    "github.com/zeromicro/go-queue/kq"
    "github.com/zeromicro/go-zero/rest"
)

type Config struct {
    rest.RestConf
    .......
    KqConsumerConf kq.KqConf
}
```

`internal` 아래에 `mqs` 폴더를 만듭니다.

`mqs` 폴더 아래에 `paymentSuccess.go`를 만들고 `PaymentSuccess` consumer를 정의합니다.

```go
package mqs

import (
    "context"
    "github.com/zeromicro/go-zero/core/logx"
    "zerodocgo/internal/svc"
)

type PaymentSuccess struct {
    ctx    context.Context
    svcCtx *svc.ServiceContext
}

func NewPaymentSuccess(ctx context.Context, svcCtx *svc.ServiceContext) *PaymentSuccess {
    return &PaymentSuccess{
        ctx:    ctx,
        svcCtx: svcCtx,
    }
}

func (l *PaymentSuccess) Consume(key, val string) error {
    logx.Infof("PaymentSuccess key :%s , val :%s", key, val)
    return nil
}
```

여러 consumer를 등록하기 위해 `mqs` 폴더 아래에 `mqs.go` 파일을 만듭니다.

```go
package mqs

import (
    "context"
    "zerodocgo/internal/config"
    "zerodocgo/internal/svc"

    "github.com/zeromicro/go-queue/kq"
    "github.com/zeromicro/go-zero/core/service"
)

func Consumers(c config.Config, ctx context.Context, svcContext *svc.ServiceContext) []service.Service {

    return []service.Service{
        // 소비 흐름 상태 변화를 수신합니다
        kq.MustNewQueue(c.KqConsumerConf, NewPaymentSuccess(ctx, svcContext)),
        //.....
    }

}
```

`main.go`에서 consumer를 시작하고 메시지 소비를 기다립니다.

```go
package main

import (
    "context"
    "flag"
    "github.com/zeromicro/go-zero/core/service"
    "zerodocgo/internal/mqs"
    "zerodocgo/internal/svc"

    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/rest"
    "zerodocgo/internal/config"
)

var configFile = flag.String("f", "etc/mq.yaml", "the config file")

func main() {
    flag.Parse()

    var c config.Config
    conf.MustLoad(*configFile, &c)

    server := rest.MustNewServer(c.RestConf)
    defer server.Stop()

    svcCtx := svc.NewServiceContext(c)
    ctx := context.Background()
    serviceGroup := service.NewServiceGroup()
    defer serviceGroup.Stop()

    for _, mq := range mqs.Consumers(ctx, svcCtx) {
        serviceGroup.Add(mq)
    }

    serviceGroup.Start()
}
```

물론 `mqs.go`에서 `kq.MustNewQueue`를 초기화할 때 consumer 관련 선택 매개변수를 전달할 수 있습니다.

- `commitInterval`: Kafka broker에 commit하는 주기이며 기본값은 1초입니다.
- `queueCapacity`: Kafka 내부 queue 길이입니다.
- `maxWait`: Kafka에서 batch로 데이터를 가져올 때 새 데이터를 기다리는 최대 시간입니다.
- `metrics`: 메시지별 소비 시간을 보고합니다. 기본적으로 내부에서 초기화되므로 보통 직접 지정할 필요는 없습니다.
