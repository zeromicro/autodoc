---
title: 队列组件
description: go-zero 消息队列组件。
sidebar:
  order: 8

---

go-zero 集成了主流消息中间件，用于服务之间的异步通信。根据吞吐量、消息顺序和投递保证需求选择合适的队列。

## 内容

- [Kafka](kafka.md) — 基于内置 `kq` 消费者的高吞吐事件流
- [RabbitMQ](rabbitmq.md) — 支持可靠投递的 AMQP 消息队列
