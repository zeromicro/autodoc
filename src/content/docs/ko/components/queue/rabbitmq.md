---
title: RabbitMQ
description: go-zero의 RabbitMQ에 대해 설명합니다.
sidebar:
  order: 2
---


go-zero는 공식 `amqp091-go` 라이브러리를 통해 RabbitMQ와 연동합니다. 커뮤니티는 `zeromicro/zero-contrib` 아래에 `rabbitmq` 플러그인을 제공합니다.

## 설치

```bash
go get github.com/zeromicro/zero-contrib/zrpc/rabbitmq
```

## Producer

```go
import amqp "github.com/rabbitmq/amqp091-go"

conn, err := amqp.Dial("amqp:// 예시입니다
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

## 연결 탄력성

연결을 재연결 루프로 감쌉니다.

```go
for {
    conn, err := amqp.Dial(url)
    if err != nil {
        time.Sleep(5 * time.Second)
        continue
    }
    runConsumer(conn)
    // 연결이 닫히면 다시 연결합니다
}
```
