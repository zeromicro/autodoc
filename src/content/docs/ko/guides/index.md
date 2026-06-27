---
title: 가이드
description: 주제별 단계별 가이드를 통해 go-zero 사용법을 익힙니다.
sidebar:
  order: 1

---


go-zero를 실제로 사용하는 방법을 주제별 단계별 가이드로 학습합니다.

## HTTP 서비스

- [기본 HTTP 서비스](./http/basic/) — 첫 REST API 만들기
- [미들웨어](./http/server/middleware/) — 요청/응답 인터셉터
- [JWT 인증](./http/jwt-auth/) — 토큰으로 엔드포인트 보호
- [파일 업로드](./http/file-upload/) — multipart form 데이터 처리

## gRPC 서비스

- [gRPC 서버](./grpc/server/) — protobuf 서비스 정의와 제공
- [gRPC 클라이언트](./grpc/client/) — Go에서 gRPC 서비스 호출
- [인터셉터](./grpc/interceptor/) — gRPC용 미들웨어

## 데이터베이스

- [MySQL](./database/mysql/) — goctl model을 사용하여 ORM 없는 데이터 접근
- [Redis](./database/redis/) — 캐싱과 분산 데이터
- [MongoDB](./database/mongodb/) — 문서 저장소 통합

## 마이크로서비스

- [서비스 디스커버리](./microservice/service-discovery/) — 서비스 등록과 조회
- [부하 분산](./microservice/load-balancing) — RPC 트래픽 분산
- [분산 추적](./microservice/distributed-tracing/) — 서비스 전반의 요청 추적

## 배포

- [Docker](./deployment/docker/) — go-zero 서비스 컨테이너화
- [Kubernetes](./deployment/kubernetes/) — K8s 클러스터에 배포
