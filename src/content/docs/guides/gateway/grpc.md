---
title: gRPC Gateway
description: Expose gRPC services over HTTP using go-zero's gateway.
sidebar:
  order: 3
---

## Overview

As microservice architectures become more common, gRPC is widely adopted as a high-performance, cross-language RPC framework. However, gRPC is not suitable for every scenario — for example, when clients do not support gRPC, or when you need to expose gRPC services to web applications via a RESTful API. In these cases, a gRPC gateway bridges the gap.

## How go-zero's gRPC Gateway Works

The gRPC gateway in go-zero is an HTTP server that translates RESTful requests into gRPC calls and converts gRPC responses back to HTTP. The flow is:

1. Load the gRPC service definition from a proto file.
2. Load HTTP-to-gRPC mapping rules from the configuration file.
3. Generate HTTP handlers for each gRPC method.
4. Start the HTTP server and accept incoming requests.
5. Translate each HTTP request into a gRPC request.
6. Translate the gRPC response into an HTTP response.
7. Return the HTTP response to the caller.

For the full gateway source, see [go-zero/gateway](https://github.com/zeromicro/go-zero/tree/master/gateway).

## Configure Introduction

```go
type (
    GatewayConf struct {
        rest.RestConf
        Upstreams []Upstream
        Timeout   time.Duration `json:",default=5s"`
    }

    RouteMapping struct {
        Method string
        Path string
        RpcPath string
    }

    Upstream struct {
        Name string `json:",optional"`
        Grpc zrpc.RpcClientConf
        ProtoSets []string `json:",optional"`
        Mappings []RouteMapping `json:",optional"`
    }
)
```

### GatewayConf

| <img width={100} />Name | Note                       | DataType   | Required? | Sample                             |
| ---------------------------------------- | -------------------------- | ---------- | --------- | ---------------------------------- |
| RestConf                                 | rest Service Configuration | RestConf   | YES       | See [Basic Service Configuration](../../reference/configuration/service-config) |
| Upstreams                                | gRPC Service Configuration | []Upstream | YES       |                                    |
| Timeout                                  | Timeout time               | duration   | NO        | `5s`                               |

### Upstream

| <img width={100} />Name | Note                                                 | DataType       | Required? | Sample                             |
| ---------------------------------------- | ---------------------------------------------------- | -------------- | --------- | ---------------------------------- |
| Name                                     | Service Name                                         | string         | NO        | `demo1-gateway`                    |
| Grpc                                     | gRPC Service Configuration                           | RpcClientConf  | YES       | See [RPC configuration](../grpc/server/configuration) |
| ProtoSets                                | proto file list                                      | []string       | NO        | `["hello.pb"]`                     |
| Mappings                                 | Route mapping, do not fill by default all grpc paths | []RouteMapping | NO        |                                    |

### RouteMapping

| <img width={100} />Name | Note         | DataType | Required? | Sample             |
| ---------------------------------------- | ------------ | -------- | --------- | ------------------ |
| Method                                   | HTTP methods | string   | YES       | `get`              |
| Path                                     | HTTP Path    | string   | YES       | `/ping`            |
| RpcPath                                  | gRPC Path    | string   | YES       | `hello.Hello/Ping` |

## Examples

In go-zero, there are two ways to use gRPC gateways: protoDescriptor and grpcReflection.

**protoDescriptor**
protoDescriptor method requires proto to be a pb file via protoc and then reference the pb file to rest-grpc rule in gateway.

:::tip
go-zero sdk version v1.5.0 gateway configuration will cause configuration conflicts, please avoid this version, the current example is using v1.4.4 version
:::

1 We create a new project, demo1, and a new hello.proto file in demo1, as follows:

```protobuf
syntax = "proto3";

package hello;

option go_package = "./hello";

message Request {
}

message Response {
  string msg = 1;
}

service Hello {
  rpc Ping(Request) returns(Response);
}
```

2 Create the `gateway` directory in the `demo1` directory, and then execute the following command in the `demo1` directory to generate the protoDescriptor:

```bash
$ protoc --descriptor_set_out=gateway/hello.pb hello.proto
```

3 Generate the grpc service code by executing the following command in the `demo1` directory:

```bash
$ goctl rpc protoc hello.proto --go_out=server --go-grpc_out=server --zrpc_out=server
```

Populate the logic for the `Ping` method in `demo1/server/internal/logic/pinglogic.go` with the following code:

```go
func (l *PingLogic) Ping(in *hello.Request) (*hello.Response, error) {
    return &hello.Response{
        Msg: "pong",
    }, nil
}
```

4 Modify the configuration file `demo1/server/etc/hello.yaml` to read as follows:

```yaml
Name: hello.rpc
ListenOn: 0.0.0.0:8080
```

5 Go to the `demo1/gateway` directory, create the directory `etc`, and add the configuration file `gateway.yaml`, as follows:

```yaml
Name: demo1-gateway
Host: localhost
Port: 8888
Upstreams:
  - Grpc:
      Target: localhost:8080
    # protoset mode
    ProtoSets:
      - hello.pb
    # Mappings can also be written in proto options
    Mappings:
      - Method: get
        Path: /ping
        RpcPath: hello.Hello/Ping
```

6 Go to the `demo1/gateway` directory and create a new `gateway.go` file with the following contents:

```go
package main

import (
    "flag"

    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/gateway"
)

var configFile = flag.String("f", "etc/gateway.yaml", "config file")

func main() {
    flag.Parse()

    var c gateway.GatewayConf
    conf.MustLoad(*configFile, &c)
    gw := gateway.MustNewServer(c)
    defer gw.Stop()
    gw.Start()
}
```

7 Open two separate terminals to start the grpc server service and the gateway service, and then visit `http://localhost:8888/ping`:

```bash
# Go to the demo1/server directory and start the grpc service
$ go run hello.go
Starting rpc server at 0.0.0.0:8080...
```

```bash
# Go to the demo1/gateway directory and start the gateway service
$ go run gateway.go
```

```bash
# Open a new terminal and access the gateway service
$ curl http://localhost:8888/ping
{"msg":"pong"}%
```

**grpcReflection**
The grpcReflection method is similar to the protoDescriptor method. Unlike the grpcReflection method does not require proto to be produced as a pb file through protoc but takes proto from the grpc server directly and then quotes the proto file for rest-grpc rule in gateway.

1 We create a new project, demo2, and a new hello.proto file in demo2, as follows:

```protobuf
syntax = "proto3";

package hello;

option go_package = "./hello";

message Request {
}

message Response {
  string msg = 1;
}

service Hello {
  rpc Ping(Request) returns(Response);
}
```

2 Create a `gateway` directory under the `demo2` directory for backup

3 Generate the grpc service code by executing the following command in the `demo2` directory:

```bash
$ goctl rpc protoc hello.proto --go_out=server --go-grpc_out=server --zrpc_out=server
```

Populate the logic for the `Ping` method in `demo2/server/internal/logic/pinglogic.go` with the following code:

```go
func (l *PingLogic) Ping(in *hello.Request) (*hello.Response, error) {
    return &hello.Response{
        Msg: "pong",
    }, nil
}
```

Modify the configuration file `demo2/server/etc/hello.yaml` as follows:

```yaml {3}
Name: hello.rpc
ListenOn: 0.0.0.0:8080
Mode: dev
```

:::tip
Since the grpc reflection mode is currently only supported by the `dev` and `test` environments, you need to set `Mode` to `dev` or `test` here.
:::

4 Go to the `demo2/gateway` directory, create the directory `etc`, and add the configuration file `gateway.yaml`, as follows:

```yaml
Name: demo1-gateway
Host: localhost
Port: 8888
Upstreams:
  - Grpc:
      Target: localhost:8080
    # Mappings can also be written in proto options
    Mappings:
      - Method: get
        Path: /ping
        RpcPath: hello.Hello/Ping
```

5 Go to the `demo2/gateway` directory and create a new `gateway.go` file with the following contents:

```go
package main

import (
    "flag"

    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/gateway"
)

var configFile = flag.String("f", "etc/gateway.yaml", "config file")

func main() {
    flag.Parse()

    var c gateway.GatewayConf
    conf.MustLoad(*configFile, &c)
    gw := gateway.MustNewServer(c)
    defer gw.Stop()
    gw.Start()
}
```

6 Open two separate terminals to start the grpc server service and the gateway service, and then visit `http://localhost:8888/ping`:

```bash
# Go to the demo1/server directory and start the grpc service
$ go run hello.go
Starting rpc server at 0.0.0.0:8080...
```

```bash
# Go to the demo1/gateway directory and start the gateway service
$ go run gateway.go
```

```bash
# Open a new terminal and access the gateway service
$ curl http://localhost:8888/ping
{"msg":"pong"}%
```

## Custom gRPC Client with `WithDialer` (since v1.10.0)

By default, the gateway creates gRPC clients using standard options. Use `WithDialer` to override this — for example, to increase the max message size:

```go
package main

import (
    "flag"

    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/gateway"
    "github.com/zeromicro/go-zero/zrpc"
    "google.golang.org/grpc"
)

var configFile = flag.String("f", "etc/gateway.yaml", "config file")

func main() {
    flag.Parse()

    var c gateway.GatewayConf
    conf.MustLoad(*configFile, &c)

    gw := gateway.MustNewServer(c,
        gateway.WithDialer(func(conf zrpc.RpcClientConf) zrpc.Client {
            return zrpc.MustNewClient(conf,
                zrpc.WithDialOption(grpc.MaxCallRecvMsgSize(50*1024*1024)),
                zrpc.WithDialOption(grpc.MaxCallSendMsgSize(50*1024*1024)),
            )
        }),
    )
    defer gw.Stop()
    gw.Start()
}
```

| Use case | Dial option |
|----------|------------|
| Increase receive message size | `grpc.MaxCallRecvMsgSize(n)` |
| Increase send message size | `grpc.MaxCallSendMsgSize(n)` |
| Custom TLS | `grpc.WithTransportCredentials(creds)` |
| Keep-alive | `grpc.WithKeepaliveParams(params)` |

## References

- [go-zero • gateway](https://github.com/zeromicro/go-zero/tree/master/gateway)
- [Basic Service Configuration](../../reference/configuration/service-config)
- [gRPC Server Configuration](../grpc/server/configuration)
