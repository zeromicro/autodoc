---
title: Kafka
description: Produce and consume Kafka messages in go-zero services.
sidebar:
  order: 1
---


go-zero's `kq` package provides a high-throughput Kafka consumer backed by a goroutine pool, and a lightweight producer using `go-zero/core/queue`.

## Producer

```go
import "github.com/zeromicro/go-zero/core/stores/redis"
import "github.com/zeromicro/go-zero/core/queue"
// Or use the Segment kafka writer directly for simplicity:
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

## Consumer with kq

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

## Error Handling

Returning an error from the handler causes the message to be **retried**. For dead-lettering, write failures to a separate topic:

```go
kq.WithHandle(func(k, v string) error {
    if err := process(v); err != nil {
        deadLetter.WriteMessages(ctx, kafka.Message{Value: []byte(v)})
        return nil // ack to avoid infinite retry
    }
    return nil
})
```
