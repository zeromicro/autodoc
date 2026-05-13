---
title: 예제
description: 간단한 API부터 완전한 마이크로서비스 시스템까지 go-zero로 만든 실제 예제입니다.
sidebar:
  order: 1
---


이 섹션은 go-zero 패턴을 실제 문제에 적용할 수 있도록 실행 가능한 실용 예제를 모았습니다.

## 포함된 예제

| 예제 | 난이도 | 설명 |
|---------|------------|-------------|
| [Hello World](./hello-world/) | 입문 | 최소 API 서비스 |
| [JWT를 사용하는 REST API](./rest-api-jwt/) | 중급 | 인증이 적용된 HTTP 엔드포인트 |
| [Bookstore](./bookstore/) | 중급 | API + RPC 서비스 전체 구성 |
| [마이크로서비스 시스템](./microservice-system/) | 고급 | 서비스 디스커버리를 포함한 다중 서비스 |

## 예제 실행

모든 예제는 Go 1.21 이상과 goctl 설치가 필요합니다.

```bash
go install github.com/zeromicro/go-zero/tools/goctl@latest
```

공식 예제 저장소를 복제합니다.

```bash
git clone https://github.com/zeromicro/go-zero.git
cd go-zero/example
```
