---
title: goctl 빠른 시작
description: go-zero의 goctl 빠른 시작에 대해 설명합니다.
sidebar:
  order: 3

---

## 개요


## goctl 빠른 시작 directive

```bash
$ goctl quickstart --help
quickly start a project

Usage:
  goctl quickstart [flags]

Flags:
  -h, --help                  help for quickstart
  -t, --service-type string   specify the service type, supported values: [mono, micro] (default "mono")
```

| <img width={100} /> 매개변수 필드 | <img width={150} /> 매개변수 타입 | <img width={200} /> 필수? | <img width={200} /> 기본값 value | <img width={800} /> 매개변수 설명        |
| ---------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------- |
| service-type                                         | string                                              | 없음                                             | mono                                               | 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다. |

## 예제

**生成单体服务**
경우 `mono` type은 selected, goctl 생성합니다 minimized HTTP 서비스과 starts HTTP service입니다.

1 생성 code

```bash
# 예시입니다
$ cd ~

# mkdir
$ mkdir quickstart && cd quickstart

# 예시입니다
$ goctl quickstart --service-type mono
go: creating new go.mod: module greet
>> Generating quickstart api project...
Done.
>> go mod tidy
go: finding module for package github.com/zeromicro/go-zero/core/logx
go: finding module for package github.com/zeromicro/go-zero/rest
go: finding module for package github.com/zeromicro/go-zero/rest/httpx
go: finding module for package github.com/zeromicro/go-zero/core/conf
go: found github.com/zeromicro/go-zero/core/conf in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/rest in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/rest/httpx in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/core/logx in github.com/zeromicro/go-zero v1.4.3
>> Ready to start an API server...
>> Run 'curl http://127.0.0.1:8888/ping' after service startup...
Starting server at 127.0.0.1:8888...
```

2curl

새로운 terminal, execute curl 테스트

```bash
$ curl -i http://127.0.0.1:8888/ping
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Traceparent: 00-2102678b8c7c5906b792c618b054c9a1-60194e95cceff37f-00
Date: Fri, 06 Jan 2023 08:52:30 GMT
Content-Length: 14

{"msg":"pong"}%
```

**生成微服务**

1Generate 서비스

```bash
# 예시입니다
$ cd ~

# mkdir
$ mkdir quickstart && cd quickstart

# 예시입니다
$ goctl quickstart --service-type micro
Detected that the "/Users/keson/quickstart/greet" already exists, do you clean up? [y: YES, n: NO]: y
Clean workspace...
go: creating new go.mod: module greet
>> Generating quickstart zRPC project...
[goctl-env]: preparing to check env

[goctl-env]: looking up "protoc"
[goctl-env]: "protoc" is installed

[goctl-env]: looking up "protoc-gen-go"
[goctl-env]: "protoc-gen-go" is installed

[goctl-env]: looking up "protoc-gen-go-grpc"
[goctl-env]: "protoc-gen-go-grpc" is installed

[goctl-env]: congratulations! your goctl environment is ready!
[command]: protoc greet.proto --go_out . --go-grpc_out .
Done.
>> Generating quickstart api project...
Done.
>> go mod tidy
go: finding module for package github.com/zeromicro/go-zero/core/conf
go: finding module for package github.com/zeromicro/go-zero/core/logx
go: finding module for package github.com/zeromicro/go-zero/core/service
go: finding module for package google.golang.org/grpc/reflection
go: finding module for package github.com/zeromicro/go-zero/zrpc
go: finding module for package github.com/zeromicro/go-zero/rest
go: finding module for package github.com/zeromicro/go-zero/rest/httpx
go: finding module for package google.golang.org/grpc
go: finding module for package google.golang.org/grpc/codes
go: finding module for package google.golang.org/grpc/status
go: finding module for package google.golang.org/protobuf/reflect/protoreflect
go: finding module for package google.golang.org/protobuf/runtime/protoimpl
go: found github.com/zeromicro/go-zero/core/conf in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/rest in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/rest/httpx in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/core/logx in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/zrpc in github.com/zeromicro/go-zero v1.4.3
go: found github.com/zeromicro/go-zero/core/service in github.com/zeromicro/go-zero v1.4.3
go: found google.golang.org/grpc in google.golang.org/grpc v1.51.0
go: found google.golang.org/grpc/reflection in google.golang.org/grpc v1.51.0
go: found google.golang.org/grpc/codes in google.golang.org/grpc v1.51.0
go: found google.golang.org/grpc/status in google.golang.org/grpc v1.51.0
go: found google.golang.org/protobuf/reflect/protoreflect in google.golang.org/protobuf v1.28.1
go: found google.golang.org/protobuf/runtime/protoimpl in google.golang.org/protobuf v1.28.1
>> Ready to start a zRPC server...
>> Ready to start an API server...
>> Run 'curl http://127.0.0.1:8888/ping' after service startup...
Starting rpc server at 127.0.0.1:8080...
Starting server at 127.0.0.1:8888...
```

2curl

새로운 terminal과 execute curl 테스트

```bash
$ curl -i http://127.0.0.1:8888/ping
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Traceparent: 00-b7c7bd5b28a49ab97960ed83d2888f1a-4da22e03825041e7-00
Date: Fri, 06 Jan 2023 08:55:33 GMT
Content-Length: 14

{"msg":"pong"}
```
