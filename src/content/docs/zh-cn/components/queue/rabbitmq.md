---
title: RabbitMQ
description: 在 go-zero 服务中集成 AMQP 消息队列。
sidebar:
  order: 9
---

go-zero 通过官方 `amqp091-go` 库与 RabbitMQ 集成。社区在 `zeromicro/zero-contrib` 下提供了 `rabbitmq` 插件。

## 安装

```bash
go get github.com/zeromicro/zero-contrib/zrpc/rabbitmq
```

## 生产者

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

## 消费者

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
        msg.Nack(false, true) // 重新入队
    } else {
        msg.Ack(false)
    }
}
```

## 连接容错

将连接包裹在重连循环中：

```go
for {
    conn, err := amqp.Dial(url)
    if err != nil {
        time.Sleep(5 * time.Second)
        continue
    }
    runConsumer(conn)
    // conn 已关闭 — 重新连接
}
```
