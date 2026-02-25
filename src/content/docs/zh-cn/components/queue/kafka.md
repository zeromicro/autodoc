---
title: Kafka
description: 在 go-zero 服务中生产和消费 Kafka 消息。
sidebar:
  order: 8
---

go-zero 的 `kq` 包提供了一个基于协程池的高吞吐 Kafka 消费者，以及一个使用 `go-zero/core/queue` 的轻量级生产者。

## 生产者

```go
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

## 使用 kq 消费

```yaml title="etc/app.yaml"
Kafka:
  Brokers:
    - localhost:9092
  Group: order-consumer
  Topic: order-events
  Offset: first     # "first" | "last"
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

## 错误处理

从 handler 返回错误会导致消息被**重试**。如需死信处理，可将失败消息写入单独的 topic：

```go
kq.WithHandle(func(k, v string) error {
    if err := process(v); err != nil {
        deadLetter.WriteMessages(ctx, kafka.Message{Value: []byte(v)})
        return nil // ack 以避免无限重试
    }
    return nil
})
```
