---
title: Proto Syntax
description: Common protobuf syntax used in go-zero RPC services.
sidebar:
  order: 7
---

# Proto Syntax

```proto
syntax = "proto3";

package greet;

service Greet {
	rpc SayHello (HelloReq) returns (HelloResp);
}

message HelloReq {
	string name = 1;
}

message HelloResp {
	string message = 1;
}
```
