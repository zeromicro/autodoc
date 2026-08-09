---
title: 변경 로그
description: go-zero의 변경 로그에 대해 설명합니다.
sidebar:
  order: 6

---
## v1.10.3 – 2026-08-01

- `stringx.FirstN`/`Substr` edge case, `mapping`의 pointer-to-slice unmarshal 문제, 높은 동시성에서의 Redis circuit breaker 오동작을 수정했습니다.
- `collection.Queue` growth 전략을 최적화하고 Redis `XGroupSetID`/`XGroupSetIDCtx`를 추가했습니다.

## v1.10.2 – 2026-05-31

- MCP tool handler에서 HTTP 요청 메타데이터를 추출할 수 있습니다.
- Go 1.26용 etcd 서비스 탐색 대상 URL과 중복 watch event로 인한 메모리 증가를 수정했습니다.

## v1.10.1 – 2026-03-28

- JSON5 설정과 Redis 범용 명령 `Do`/`DoCtx` 지원을 추가했습니다.
- 프로젝트를 Go 1.24로 업그레이드하고 중요한 `core/codec` 보안 문제를 수정했습니다.

각 go-zero 버전의 자세한 변경 사항은 [릴리스 노트](../releases/)에서 확인할 수 있습니다.

전체 기록은 [GitHub 릴리스 페이지](https://github.com/zeromicro/go-zero/releases)에서 확인하세요.

## 최신 릴리스

| 버전 | 날짜 | 주요 변경 사항 |
|---------|------|------------|
| [v1.10.3](../releases/v1.10.3) | 2026-08-01 | stringx/mapping 수정, Redis 회로 차단기 수정, Queue 확장 최적화 |
| [v1.10.2](../releases/v1.10.2) | 2026-05-31 | MCP 요청 메타데이터, Go 1.26 etcd 서비스 탐색 수정 |
| [v1.10.1](../releases/v1.10.1) | 2026-03-28 | JSON5 설정, Redis `Do`/`DoCtx`, Go 1.24, 보안 fixes |
| [v1.10.0](../releases/v1.10.0) | 2026-02-15 | MCP 지원, gateway 개선 사항, SSE improvements |
| [v1.9.4](../releases/v1.9.4) | 2025-12-24 | K8s EndpointSlice, Redis GETEX, etcd retry cooldown |
| [v1.9.3](../releases/v1.9.3) | 2025-11-16 | Consistent hash balancer, gateway 추적 헤더 fix |
| [v1.9.2](../releases/v1.9.2) | 2025-10-11 | go-redis retracted 버전 fix |
| [v1.9.1](../releases/v1.9.1) | 2025-10-02 | 사용자 정의 로그 키, SSE 안정성, mapreduce panic 스택 추적 |
| [v1.9.0](../releases/v1.9.0) | 2025-08-17 | 로그 desensitization, SSE 지원, MCP 서버 |
| [v1.8.5](../releases/v1.8.5) | 2025-07-12 | 버그 수정과 stability improvements |
| [v1.8.0](../releases/v1.8.0) | 2025-01-28 | Major 1.8 릴리스 |
| [v1.7.0](../releases/v1.7.0) | 2024-07-27 | Go 1.21+ 필수, OpenTelemetry SDK v1.24 |
| [v1.6.0](../releases/v1.6.0) | 2023-10-28 | 엔드포인트 설정, Prometheus rename, 브레이커 refactor |
| [v1.5.0](../releases/v1.5.0) | 2023-03-04 | OpenTelemetry replaces OpenTracing/Jaeger |

[모든 48개 릴리스 보기 →](../releases/)
