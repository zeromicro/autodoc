---
title: goctl 플러그인
description: go-zero의 goctl 플러그인에 대해 설명합니다.
sidebar:
  order: 4

---


## 개요

`goctl api plugin` 명령으로 API 기능을 확장할 수 있습니다. 내장 기능으로 부족하거나 코드를 생성하는 과정을 맞춤화해야 할 때 커뮤니티 플러그인을 사용할 수 있습니다. 자세한 내용은 [goctl api plugin](./cli-guide/api.md#plugin)을 참고하세요.

## 플러그인 리소스

- [goctl-go-compact](https://github.com/zeromicro/goctl-go-compact) 라우트별 파일을 하나의 파일로 합칩니다.
- [goctl api swagger](./cli-guide/swagger.md) API 파일에서 Swagger/OpenAPI 문서를 생성합니다.
- [goctl-php](https://github.com/zeromicro/goctl-php) PHP client와 HTTP server 요청 코드를 생성하는 goctl 플러그인입니다.
- [goctl-helper](https://plugins.jetbrains.com/plugin/25693-goctl-helper) Goland에서 간단한 API와 protobuf 파일을 생성하는 플러그인입니다.
- [goctl-proto](https://github.com/liferod/goctl-proto) API 파일에서 protobuf 파일을 만들고 RPC 코드를 생성합니다. [goctl rpc protoc](./cli-guide/rpc.md#goctl-rpc-protoc)도 참고하세요.
- [goctl-validate](https://github.com/linabellbiu/goctl-validate) go-playground/validator를 사용해 go-zero API에 요청 검증을 추가합니다.
