---
title: Proto 语法
description: go-zero RPC 项目常用的 Proto 语法。
sidebar:
  order: 7
---

# Proto 语法

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
