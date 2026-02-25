---
title: RabbitMQ
description: AMQP message queue integration in go-zero services.
sidebar:
  order: 2
---


go-zero works with RabbitMQ through the official `amqp091-go` library. The community provides a `rabbitmq` plugin under `zeromicro/zero-contrib`.

## Install

```bash
go get github.com/zeromicro/zero-contrib/zrpc/rabbitmq
```

## Producer

```go
import amqp "github.com/rabbitmq/amqp091-go"

conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
ch, err := conn.Channel()

err = ch.Publish(
    "orders",   // exchange
    "created",  // routing key
    false,      // mandatory
    false,      // immediate
    amqp.Publishing{
        ContentType: "application/json",
        Body:        orderJSON,
    },
)
```

## Consumer

```go
msgs, err := ch.Consume(
    "order-queue", // queue
    "",            // consumer tag
    false,         // auto-ack
    false,         // exclusive
    false,         // no-local
    false,         // no-wait
    nil,
)

for msg := range msgs {
    if err := processOrder(msg.Body); err != nil {
        msg.Nack(false, true) // re-queue
    } else {
        msg.Ack(false)
    }
}
```

## Connection Resilience

Wrap the connection in a reconnect loop:

```go
for {
    conn, err := amqp.Dial(url)
    if err != nil {
        time.Sleep(5 * time.Second)
        continue
    }
    runConsumer(conn)
    // conn closed — reconnect
}
```
