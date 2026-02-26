---
title: HTTP Gateway
description: Proxy HTTP requests through the go-zero gateway.
sidebar:
  order: 2
---


**Author**: Kevin Wan  
**Date**: January 27, 2025

## Feature Overview

The HTTP-to-HTTP gateway feature allows you to:
- Route HTTP requests to HTTP backend services
- Configure URL path prefixes for backend services
- Set request timeouts per upstream

## Configuration

Here's how to configure an HTTP upstream in your gateway configuration:

```yaml
Upstreams:
  - Name: userservice  # optional, will use target if not specified
    Http:
      Target: localhost:8080
      Prefix: /api/v1  # optional
      Timeout: 3000    # in milliseconds, default 3000
    Mappings:
      - Method: GET
        Path: /users
      - Method: POST
        Path: /users/create
```

For comparison, here's a gRPC upstream configuration:

```yaml
Upstreams:
  - Name: orderservice
    Grpc:
      Target: localhost:9000
      Timeout: 3000
    ProtoSets:
      - order.pb
    Mappings:
      - Method: GET
        Path: /orders
        RpcPath: order.OrderService/GetOrders
```

## Example Usage

Let's look at a complete example that demonstrates how to set up HTTP-to-HTTP routing:

```go
package main

import (
    "github.com/zeromicro/go-zero/gateway"
    "github.com/zeromicro/go-zero/rest"
)

func main() {
    var c gateway.GatewayConf
    conf.MustLoad("gateway.yaml", &c)

    gw := gateway.MustNewServer(c)
    defer gw.Stop()
    
    gw.Start()
}
```

With the following `gateway.yaml`:

```yaml
Name: gateway
Host: 0.0.0.0
Port: 8888
Upstreams:
  - Name: userapi
    Http:
      Target: localhost:8080
      Prefix: /api
    Mappings:
      - Method: GET
        Path: /users
      - Method: POST
        Path: /users
      - Method: GET
        Path: /users/:id
```

## Key Features

1. **Flexible Routing**
    - Support for both HTTP and gRPC backends in the same gateway
    - Path-based routing with prefix support
    - Method-based routing (GET, POST, PUT, DELETE, etc.)

2. **Configuration Options**
    - Configurable timeouts per upstream
    - Optional URL prefix for path rewriting
    - Clear separation between HTTP and gRPC configurations

3. **Error Handling**
    - Proper propagation of HTTP status codes
    - Timeout handling for backend services

4. **Header Management**
    - Preservation of request/response headers
    - Automatic content type handling

## Implementation Details

The implementation maintains clean separation of concerns and integrates seamlessly with existing gateway functionality:

- HTTP upstreams are mutually exclusive with gRPC upstreams in configuration
- Request forwarding respects original HTTP methods and headers
- Response status codes and headers are preserved
- Timeout handling is consistent with go-zero's patterns

## Performance Considerations

The HTTP-to-HTTP gateway is designed with performance in mind:
- Efficient request forwarding
- Minimal overhead in the routing layer

## Best Practices

When using the HTTP-to-HTTP gateway feature:

1. Always set appropriate timeouts for your upstreams
2. Use meaningful names for your upstreams for better observability
3. Consider using URL prefixes to avoid path conflicts
4. Validate your configuration before deployment

## Conclusion

The addition of HTTP-to-HTTP support makes go-zero's gateway more versatile and suitable for a wider range of microservices architectures. Whether you're working with gRPC services, HTTP services, or both, you can now use a single gateway to manage all your routing needs.

For more information, check out:
- Full documentation: [go-zero docs](https://go-zero.dev)
- Source code: [GitHub PR #4605](https://github.com/zeromicro/go-zero/pull/4605)
- Examples: [go-zero examples](https://github.com/zeromicro/zero-examples)

We welcome feedback and contributions from the community to help improve this feature further.

---
Would you like me to expand on any particular aspect of the article or make any adjustments?