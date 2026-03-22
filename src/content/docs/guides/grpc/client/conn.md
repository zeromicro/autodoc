---
title: gRPC Client Connection
description: Create a gRPC client connection in go-zero.
sidebar:
  order: 3

---


## Overview

This guide describes how to use the gRPC framework for gRPC client development.

## Example

**Preparation**

We run `goctl rpc new greet` to generate a rpc server service.

```bash
# Create a demo directory and enter it
$ mkdir demo && cd demo
# Generate a greet service
$ goctl rpc new greet
# Create a new main.go file for the greet client
$ touch main.go
```

:::tip
For configuration details, see [service configuration](../configuration).

For goctl rpc usage, see [goctl rpc](../../../reference/cli-guide/rpc).
:::

## Direct Connection

There are two direct connection modes: connecting to a single service, or connecting to a service cluster.

### Address resolve mode

Add the following code to `main.go`:

```go
func main() {
    clientConf := zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf) // fill defaults (e.g. trace propagation)
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

Add the following code to `main.go`:

```go
func main() {
    clientConf := zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf)
    // direct connect to a cluster — set Endpoints to the list of rpc server addresses
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

## etcd Service Discovery

Add the following code to `main.go`:

```go
func main() {
    clientConf := zrpc.RpcClientConf{}
    conf.FillDefault(&clientConf)
    clientConf.Etcd = discov.EtcdConf{
        Hosts: []string{"127.0.0.1:2379"},
        Key:   "greet.rpc",
        // The following fields are only needed when etcd ACL is enabled;
        // omit them if ACL is not in use.
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

## Native gRPC Support

If you prefer not to use the go-zero RPC client, zrpc also accepts a raw `grpc.ClientConn`:

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

Beyond the built-in etcd support, the community provides adapters for nacos, consul, and more. See [zero-contrib service registries](https://github.com/zeromicro/zero-contrib/tree/main/zrpc/registry) for details.
