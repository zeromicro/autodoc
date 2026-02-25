---
title: gRPC Client Connection
description: Create a gRPC client connection in go-zero.
sidebar:
  order: 3

---


## Overview

This paper describes how to use the gRPC framework for the development of GRPC Client.

## Sample

**Preparation**

We run `goctl rpc new greet` to generate a rpc server service.

```bash
# Create a demo directory, Enter the demo directory
$ mkdir demo && cd demo
# Generate a gret service
$ goctl rpc new greet
# Create a new main. o File to create a client for a greet service
$ touch main.go
```

:::tip
The following configuration details are referenced <a href="/docs/guides/grpc/client/configuration" target="_blank">service configuration</a>

goctl rpc usage reference <a href="/docs/reference/cli-guide/rpc" target="_blank"> goctl rpc</a>
:::

## Direct

There are two modes of continuous connectivity, one for a single service and one for a continual service cluster.

### Address resolve mode

In main.go file the following code

```go
func main() {
    clientConf:=zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf)
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

### Multi-node direct connection mode

In main.go file the following code

```go
func main() {
   clientConf:=zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf)
    clientConf.Endpoints = []string{"127.0.0.1:8080","127.0.0.2:8080"}
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

## etcd service discovery

In main.go file the following code

```go
func main() {
    clientConf:=zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf)// 填充默认值，比如 trace 透传等，参考服务配置说明
    clientConf.Etcd = discov.EtcdConf{// 通过 etcd 服务发现时，只需要给 Etcd 配置即可
        Hosts:              []string{"127.0.0.1:2379"},
        Key:                "greet.rpc",
        User:               "",// 当 etcd 开启 acl 时才填写，这里为了展示所以没有删除，实际使用如果没有开启 acl 可忽略
        Pass:               "",// 当 etcd 开启 acl 时才填写，这里为了展示所以没有删除，实际使用如果没有开启 acl 可忽略
        CertFile:           "",// 当 etcd 开启 acl 时才填写，这里为了展示所以没有删除，实际使用如果没有开启 acl 可忽略
        CertKeyFile:        "",// 当 etcd 开启 acl 时才填写，这里为了展示所以没有删除，实际使用如果没有开启 acl 可忽略
        CACertFile:         "",// 当 etcd 开启 acl 时才填写，这里为了展示所以没有删除，实际使用如果没有开启 acl 可忽略
        InsecureSkipVerify: false,// 当 etcd 开启 acl 时才填写，这里为了展示所以没有删除，实际使用如果没有开启 acl 可忽略
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

## Native Support

If you do not want to initialize using a go-zero repc client, zrpc also supports grpc.ClientConn, you can use grpc.ClientConn directly.

```go
func main() {
    conn,err:=grpc.Dial("127.0.0.1:8080",grpc.WithBlock(), grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err!=nil{
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

## Other Service Discoveries

In addition to a go-zero built-in ecd as a service, the community also provides support for the discovery of services such as nacos, consul, etc. More Services found components <a href="https://github.com/zeromicro/zero-contrib/tree/main/zrpc/registry" target="_blank">for details</a>
