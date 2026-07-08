---
title: Queue Components
description: Message queue components for go-zero.
sidebar:
  order: 0
---

go-zero integrates with popular message brokers for asynchronous communication between services. Choose the queue that best fits your throughput, ordering, and delivery guarantee requirements.

## Contents

- [Kafka](kafka/) — High-throughput event streaming with the built-in `kq` consumer
- [RabbitMQ](rabbitmq/) — AMQP message queue with reliable delivery

For step-by-step integration tutorials, see [Queue Guide](../../guides/queue/) (also covers [Beanstalkd delay queues](../../guides/queue/beanstalkd/)).
