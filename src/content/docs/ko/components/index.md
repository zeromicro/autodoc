---
title: 컴포넌트
description: 탄력성, 캐싱, 관측 가능성, 메시징을 위한 go-zero 내장 컴포넌트입니다.
sidebar:
  order: 1
---


go-zero는 프로덕션 마이크로서비스에 필요한 공통 컴포넌트를 기본으로 제공합니다.

## 탄력성

- [서킷 브레이커](./resilience/circuit-breaker/) — 연쇄 장애 방지
- [속도 제한기](./resilience/rate-limiter/) — 슬라이딩 윈도우 기반 속도 제한
- [기간 제한기](./resilience/period-limiter/) — Redis 기반 기간별 속도 제한
- [토큰 제한기](./resilience/token-limiter/) — 토큰 버킷 속도 제한
- [부하 차단](./resilience/load-shedding/) — 과부하 상황에서 초과 트래픽 차단
- [타임아웃](./resilience/timeout/) — 요청별 마감 시간 적용

## 동시성

- [fx](./concurrency/fx/) — 함수형 스트림 처리
- [MapReduce](./concurrency/mr/) — 병렬 map-reduce
- [Limit](./concurrency/limit/) — syncx 기반 동시성 제한

## 캐싱

- [메모리 캐시](./cache/memory-cache/) — 프로세스 내부 LRU/TTL 캐시
- [Redis 캐시](./cache/redis-cache/) — read-through 방식의 분산 캐시

## 로깅

- [logx](./log/logx/) — 핵심 구조화 로거
- [logc](./log/logc/) — 컨텍스트 인식 로깅
- [비식별화](./log/desensitization/) — 민감한 로그 필드 마스킹

## 관측 가능성

- [메트릭](./observability/metrics/) — Prometheus 통합
- [추적](./observability/tracing/) — OpenTelemetry 분산 추적
- [프로파일링](./observability/profiling/) — 런타임 프로파일링

## 메시징

- [Kafka](./queue/kafka/) — Kafka 메시지 생산과 소비
- [RabbitMQ](./queue/rabbitmq/) — AMQP 메시지 큐 통합
