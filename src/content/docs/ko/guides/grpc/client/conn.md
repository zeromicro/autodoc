---
title: gRPC 클라이언트 연결
description: go-zero의 gRPC 클라이언트 연결에 대해 설명합니다.
sidebar:
  order: 3

---


## 개요

이 가이드는 사용하는 방법을 설명합니다: gRPC framework 위한 gRPC 클라이언트 개발.

## 예제

**준비**

다음을 실행해 `goctl rpc new greet` 로 생성 rpc 서버 서비스.

```bash
# 생성합니다
$ mkdir demo && cd demo
# Generate 예시입니다
$ goctl rpc new greet
# 생성합니다
$ touch main.go
```

:::tip
위한 설정 details, see [서비스 설정](../configuration).

:::

## Direct 연결

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

### Address resolve mode

추가 다음 code 로 `main.go`:

```go
func main() {
    clientConf := zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf) // 기본값을 채웁니다(예: 추적 전파)
    clientConf.Target = "dns:///127.0.0.1:8080"
    conn := zrpc.MustNewClient(clientConf)
    client := greet.NewGreetClient(conn.Conn())
    resp, err := client.Ping(context.Background(), &greet.Request{})
    if err != nil {
        log.Println(err)
        return
    }
    log.Println(resp)
}
```

### Multi-node direct 연결 mode

추가 다음 code 로 `main.go`:

```go
func main() {
    clientConf := zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf)
    // 클러스터에 직접 연결합니다 — Endpoints를 RPC 서버 주소 목록으로 설정합니다
    clientConf.Endpoints = []string{"127.0.0.1:8080", "127.0.0.2:8080"}
    conn := zrpc.MustNewClient(clientConf)
    client := greet.NewGreetClient(conn.Conn())
    resp, err := client.Ping(context.Background(), &greet.Request{})
    if err != nil {
        log.Println(err)
        return
    }
    log.Println(resp)
}
```

## etcd 서비스 디스커버리

추가 다음 code 로 `main.go`:

```go
func main() {
    clientConf := zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf)
    clientConf.Etcd = discov.EtcdConf{
        Hosts: []string{"127.0.0.1:2379"},
        Key:   "greet.rpc",
        // 다음 필드는 etcd ACL이 활성화된 경우에만 필요합니다.
        // ACL 예시입니다
        User:               "",
        Pass:               "",
        CertFile:           "",
        CertKeyFile:        "",
        CACertFile:         "",
        InsecureSkipVerify: false,
    }
    conn := zrpc.MustNewClient(clientConf)
    client := greet.NewGreetClient(conn.Conn())
    resp, err := client.Ping(context.Background(), &greet.Request{})
    if err != nil {
        log.Println(err)
        return
    }
    log.Println(resp)
}
```

## Native gRPC 지원


```go
func main() {
    conn, err := grpc.Dial("127.0.0.1:8080", grpc.WithBlock(), grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil {
        log.Println(err)
        return
    }
    client := greet.NewGreetClient(conn)
    resp, err := client.Ping(context.Background(), &greet.Request{})
    if err != nil {
        log.Println(err)
        return
    }
    log.Println(resp)
}
```

## Other Service Registries
