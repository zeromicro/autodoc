---
title: 서비스 그룹화
description: go-zero의 서비스 그룹화에 대해 설명합니다.
sidebar:
  order: 3

---


## 개요


## 서비스 그룹


### 없음 group

Assume we have proto 파일, below：

```protobuf
syntax = "proto3";

package user;

option go_package = "github.com/example/user";

message LoginReq{}
message LoginResp{}
message UserInfoReq{}
message UserInfoResp{}
message UserInfoUpdateReq{}
message UserInfoUpdateResp{}
message UserListReq{}
message UserListResp{}

message UserRoleListReq{}
message UserRoleListResp{}
message UserRoleUpdateReq{}
message UserRoleUpdateResp{}
message UserRoleInfoReq{}
message UserRoleInfoResp{}
message UserRoleAddReq{}
message UserRoleAddResp{}
message UserRoleDeleteReq{}
message UserRoleDeleteResp{}


message UserClassListReq{}
message UserClassListResp{}
message UserClassUpdateReq{}
message UserClassUpdateResp{}
message UserClassInfoReq{}
message UserClassInfoResp{}
message UserClassAddReq{}
message UserClassAddResp{}
message UserClassDeleteReq{}
message UserClassDeleteResp{}

service UserService{
  rpc Login (LoginReq) returns (LoginResp);
  rpc UserInfo (UserInfoReq) returns (UserInfoResp);
  rpc UserInfoUpdate (UserInfoUpdateReq) returns (UserInfoUpdateResp);
  rpc UserList (UserListReq) returns (UserListResp);

  rpc UserRoleList (UserRoleListReq) returns (UserRoleListResp);
  rpc UserRoleUpdate (UserRoleUpdateReq) returns (UserRoleUpdateResp);
  rpc UserRoleInfo (UserRoleInfoReq) returns (UserRoleInfoResp);
  rpc UserRoleAdd (UserRoleAddReq) returns (UserRoleAddResp);
  rpc UserRoleDelete (UserRoleDeleteReq) returns (UserRoleDeleteResp);

  rpc UserClassList (UserClassListReq) returns (UserClassListResp);
  rpc UserClassUpdate (UserClassUpdateReq) returns (UserClassUpdateResp);
  rpc UserClassInfo (UserClassInfoReq) returns (UserClassInfoResp);
  rpc UserClassAdd (UserClassAddReq) returns (UserClassAddResp);
  rpc UserClassDelete (UserClassDeleteReq) returns (UserClassDeleteResp);
}
```


```bash
$ goctl rpc protoc user.proto --go_out=. --go-grpc_out=. --zrpc_out=.
$ tree
.
├── etc
│   └── user.yaml
├── github.com
│   └── example
│       └── user
│           ├── user.pb.go
│           └── user_grpc.pb.go
├── go.mod
├── internal
│   ├── config
│   │   └── config.go
│   ├── logic
│   │   ├── loginlogic.go
│   │   ├── userclassaddlogic.go
│   │   ├── userclassdeletelogic.go
│   │   ├── userclassinfologic.go
│   │   ├── userclasslistlogic.go
│   │   ├── userclassupdatelogic.go
│   │   ├── userinfologic.go
│   │   ├── userinfoupdatelogic.go
│   │   ├── userlistlogic.go
│   │   ├── userroleaddlogic.go
│   │   ├── userroledeletelogic.go
│   │   ├── userroleinfologic.go
│   │   ├── userrolelistlogic.go
│   │   └── userroleupdatelogic.go
│   ├── server
│   │   └── userserviceserver.go
│   └── svc
│       └── servicecontext.go
├── user.go
├── user.proto
└── userservice
    └── userservice.go

10 directories, 24 files
```

:::note reminding
이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
:::

### Group

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.

```protobuf
syntax = "proto3";

package user;

option go_package = "github.com/example/user";

message LoginReq{}
message LoginResp{}
message UserInfoReq{}
message UserInfoResp{}
message UserInfoUpdateReq{}
message UserInfoUpdateResp{}
message UserListReq{}
message UserListResp{}
service UserService{
  rpc Login (LoginReq) returns (LoginResp);
  rpc UserInfo (UserInfoReq) returns (UserInfoResp);
  rpc UserInfoUpdate (UserInfoUpdateReq) returns (UserInfoUpdateResp);
  rpc UserList (UserListReq) returns (UserListResp);
}

message UserRoleListReq{}
message UserRoleListResp{}
message UserRoleUpdateReq{}
message UserRoleUpdateResp{}
message UserRoleInfoReq{}
message UserRoleInfoResp{}
message UserRoleAddReq{}
message UserRoleAddResp{}
message UserRoleDeleteReq{}
message UserRoleDeleteResp{}
service UserRoleService{
  rpc UserRoleList (UserRoleListReq) returns (UserRoleListResp);
  rpc UserRoleUpdate (UserRoleUpdateReq) returns (UserRoleUpdateResp);
  rpc UserRoleInfo (UserRoleInfoReq) returns (UserRoleInfoResp);
  rpc UserRoleAdd (UserRoleAddReq) returns (UserRoleAddResp);
  rpc UserRoleDelete (UserRoleDeleteReq) returns (UserRoleDeleteResp);
}

message UserClassListReq{}
message UserClassListResp{}
message UserClassUpdateReq{}
message UserClassUpdateResp{}
message UserClassInfoReq{}
message UserClassInfoResp{}
message UserClassAddReq{}
message UserClassAddResp{}
message UserClassDeleteReq{}
message UserClassDeleteResp{}
service UserClassService{
  rpc UserClassList (UserClassListReq) returns (UserClassListResp);
  rpc UserClassUpdate (UserClassUpdateReq) returns (UserClassUpdateResp);
  rpc UserClassInfo (UserClassInfoReq) returns (UserClassInfoResp);
  rpc UserClassAdd (UserClassAddReq) returns (UserClassAddResp);
  rpc UserClassDelete (UserClassDeleteReq) returns (UserClassDeleteResp);
}
```


```bash
# 通过 -m 指定 goctl 生成分组的代码
$ goctl rpc protoc user.proto --go_out=. --go-grpc_out=. --zrpc_out=. -m
$ tree
.
├── client
│   ├── userclassservice
│   │   └── userclassservice.go
│   ├── userroleservice
│   │   └── userroleservice.go
│   └── userservice
│       └── userservice.go
├── etc
│   └── user.yaml
├── github.com
│   └── example
│       └── user
│           ├── user.pb.go
│           └── user_grpc.pb.go
├── go.mod
├── internal
│   ├── config
│   │   └── config.go
│   ├── logic
│   │   ├── userclassservice
│   │   │   ├── userclassaddlogic.go
│   │   │   ├── userclassdeletelogic.go
│   │   │   ├── userclassinfologic.go
│   │   │   ├── userclasslistlogic.go
│   │   │   └── userclassupdatelogic.go
│   │   ├── userroleservice
│   │   │   ├── userroleaddlogic.go
│   │   │   ├── userroledeletelogic.go
│   │   │   ├── userroleinfologic.go
│   │   │   ├── userrolelistlogic.go
│   │   │   └── userroleupdatelogic.go
│   │   └── userservice
│   │       ├── loginlogic.go
│   │       ├── userinfologic.go
│   │       ├── userinfoupdatelogic.go
│   │       └── userlistlogic.go
│   ├── server
│   │   ├── userclassservice
│   │   │   └── userclassserviceserver.go
│   │   ├── userroleservice
│   │   │   └── userroleserviceserver.go
│   │   └── userservice
│   │       └── userserviceserver.go
│   └── svc
│       └── servicecontext.go
├── user.go
└── user.proto

19 directories, 28 files
```
