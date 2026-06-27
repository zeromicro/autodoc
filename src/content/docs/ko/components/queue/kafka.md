---
title: Kafka
description: go-zero의 Kafka에 대해 설명합니다.
sidebar:
  order: 1
---


## Producer

```go
import "github.com/zeromicro/go-zero/core/stores/redis"
import "github.com/zeromicro/go-zero/core/queue"
// 단순하게 사용하려면 Segment kafka writer를 직접 사용할 수도 있습니다:
import "github.com/segmentio/kafka-go"

writer := &kafka.Writer{
    Addr:     kafka.TCP("localhost:9092"),
    Topic:    "order-events",
    Balancer: &kafka.LeastBytes{},
}
defer writer.Close()

err := writer.WriteMessages(ctx,
    kafka.Message{Key: []byte("order-123"), Value: orderJSON},
)
```

## Consumer 사용하여 kq

```yaml title="etc/app.yaml"
Kafka:
  Brokers:
    - localhost:9092
  Group: order-consumer
  Topic: order-events
  Offset: first     # "first" 또는 "last"
  Processors: 8
```

```go
import "github.com/zeromicro/go-zero/core/queue/kq"

q := kq.MustNewQueue(c.Kafka, kq.WithHandle(func(k, v string) error {
    var event OrderEvent
    if err := json.Unmarshal([]byte(v), &event); err != nil {
        return err
    }
    return processOrder(event)
}))
defer q.Stop()
q.Start()
```

:::tip
go-zero 프로젝트에서 producer/consumer를 설정하는 전체 단계별 튜토리얼은 [Kafka 큐 가이드]를 참고하세요(../../guides/queue/kafka/).
:::

## 오류 처리


```go
kq.WithHandle(func(k, v string) error {
    if err := process(v); err != nil {
        deadLetter.WriteMessages(ctx, kafka.Message{Value: []byte(v)})
        return nil // 무한 재시도를 피하기 위해 ack를 보냅니다
    }
    return nil
})
```
