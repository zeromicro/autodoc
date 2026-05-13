---
title: Proto FAQ
description: go-zero의 Proto FAQ에 대해 설명합니다.
sidebar:
  order: 4

---


## 1. proto 사용 때 goctl 생성합니다 gRPC code


```protobuf
syntax = "proto3";

package greet;

import "base.proto"

service demo{
  rpc (base.DemoReq) returns (base.DemoResp);
}
```

正确写法

```protobuf
syntax = "proto3";

package greet;

message DemoReq{}
message DemoResp{}

service demo{
  rpc (DemoReq) returns (DemoResp);
}
```

1. 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

## Why does 사용 패키지 proto과 서비스 때 goctl is 사용되어 생성 gRPC code?


2. 이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

## 3. goctl 생성 gRPC does 아님 지원 `google/protocol/empty.proto` 패키지 import

답변, 사용하여 1,2
