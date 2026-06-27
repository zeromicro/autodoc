---
title: API 라우트 그룹
description: go-zero의 API 라우트 그룹에 대해 설명합니다.
sidebar:
  order: 3

---


## 개요


## 서비스 그룹


```
https://example.com/v1/user/login
https://example.com/v1/user/info
https://example.com/v1/user/info/update
https://example.com/v1/user/list

https://example.com/v1/user/role/list
https://example.com/v1/user/role/update
https://example.com/v1/user/role/info
https://example.com/v1/user/role/add
https://example.com/v1/user/role/delete

https://example.com/v1/user/class/list
https://example.com/v1/user/class/update
https://example.com/v1/user/class/info
https://example.com/v1/user/class/add
https://example.com/v1/user/class/delete
```


```go
syntax = "v1"

type (
    UserLoginReq{}
    UserInfoReq{}
    UserLoginResp{}
    UserInfoResp{}
    UserInfoUpdateReq{}
    UserInfoUpdateResp{}
)

type (
    UserRoleReq{}
    UserRoleResp{}
    UserRoleUpdateReq{}
    UserRoleUpdateResp{}
    UserRoleAddReq{}
    UserRoleAddResp{}
    UserRoleDeleteReq{}
    UserRoleDeleteResp{}
)

type (
    UserClassReq{}
    UserClassResp{}
    UserClassUpdateReq{}
    UserClassUpdateResp{}
    UserClassAddReq{}
    UserClassAddResp{}
    UserClassDeleteReq{}
    UserClassDeleteResp{}
)
@server(
    prefix: /v1
)
service user-api {
    @handler UserLogin
    post /user/login (UserLoginReq) returns (UserLoginResp)

    @handler UserInfo
    post /user/info (UserInfoReq) returns (UserInfoResp)

    @handler UserInfoUpdate
    post /user/info/update (UserInfoUpdateReq) returns (UserInfoUpdateResp)

    @handler UserList
    get /user/list returns ([]UserInfoResp)

    @handler UserRoleList
    get /user/role/list returns ([]UserRoleResp)

    @handler UserRoleUpdate
    get /user/role/update (UserRoleUpdateReq) returns (UserRoleUpdateResp)

    @handler UserRoleInfo
    get /user/role/info (UserRoleReq) returns (UserRoleResp)

    @handler UserRoleAdd
    get /user/role/add (UserRoleAddReq) returns (UserRoleAddResp)

    @handler UserRoleDelete
    get /user/role/delete (UserRoleDeleteReq) returns (UserRoleDeleteResp)

    @handler UserClassList
    get /user/class/list returns ([]UserClassResp)

    @handler UserClassUpdate
    get /user/class/update (UserClassUpdateReq) returns (UserClassUpdateResp)

    @handler UserClassInfo
    get /user/class/info (UserClassReq) returns (UserClassResp)

    @handler UserClassAdd
    get /user/class/add (UserClassAddReq) returns (UserClassAddResp)

    @handler UserClassDelete
    get /user/class/delete (UserClassDeleteReq) returns (UserClassDeleteResp)
}
```

Code 디렉터리 structure 생성된 없이 group below：

```bash
.
├── etc
│   └── user-api.yaml
├── internal
│   ├── config
│   │   └── config.go
│   ├── handler
│   │   ├── routes.go
│   │   ├── userclassaddhandler.go
│   │   ├── userclassdeletehandler.go
│   │   ├── userclassinfohandler.go
│   │   ├── userclasslisthandler.go
│   │   ├── userclassupdatehandler.go
│   │   ├── userinfohandler.go
│   │   ├── userinfoupdatehandler.go
│   │   ├── userlisthandler.go
│   │   ├── userloginhandler.go
│   │   ├── userroleaddhandler.go
│   │   ├── userroledeletehandler.go
│   │   ├── userroleinfohandler.go
│   │   ├── userrolelisthandler.go
│   │   └── userroleupdatehandler.go
│   ├── logic
│   │   ├── userclassaddlogic.go
│   │   ├── userclassdeletelogic.go
│   │   ├── userclassinfologic.go
│   │   ├── serclasslistlogic.go
│   │   ├── userclassupdatelogic.go
│   │   ├── userinfologic.go
│   │   ├── userinfoupdatelogic.go
│   │   ├── userlistlogic.go
│   │   ├── userloginlogic.go
│   │   ├── userroleaddlogic.go
│   │   ├── userroledeletelogic.go
│   │   ├── userroleinfologic.go
│   │   ├── userrolelistlogic.go
│   │   └── userroleupdatelogic.go
│   ├── svc
│   │   └── servicecontext.go
│   └── types
│       └── types.go
├── user.api
└── user.go

7 directories, 35 files

```


```go {36,54,75}
syntax = "v1"

type (
    UserLoginReq  {}
    UserInfoReq  {}
    UserLoginResp  {}
    UserInfoResp  {}
    UserInfoUpdateReq  {}
    UserInfoUpdateResp  {}
)

type (
    UserRoleReq  {}
    UserRoleResp  {}
    UserRoleUpdateReq  {}
    UserRoleUpdateResp  {}
    UserRoleAddReq  {}
    UserRoleAddResp  {}
    UserRoleDeleteReq  {}
    UserRoleDeleteResp  {}
)

type (
    UserClassReq  {}
    UserClassResp  {}
    UserClassUpdateReq  {}
    UserClassUpdateResp  {}
    UserClassAddReq  {}
    UserClassAddResp  {}
    UserClassDeleteReq  {}
    UserClassDeleteResp  {}
)

@server (
    prefix: /v1
    group:  user
)
service user-api {
    @handler UserLogin
    post /user/login (UserLoginReq) returns (UserLoginResp)

    @handler UserInfo
    post /user/info (UserInfoReq) returns (UserInfoResp)

    @handler UserInfoUpdate
    post /user/info/update (UserInfoUpdateReq) returns (UserInfoUpdateResp)

    @handler UserList
    get /user/list returns ([]UserInfoResp)
}

@server (
    prefix: /v1
    group:  role
)
service user-api {
    @handler UserRoleList
    get /user/role/list returns ([]UserRoleResp)

    @handler UserRoleUpdate
    get /user/role/update (UserRoleUpdateReq) returns (UserRoleUpdateResp)

    @handler UserRoleInfo
    get /user/role/info (UserRoleReq) returns (UserRoleResp)

    @handler UserRoleAdd
    get /user/role/add (UserRoleAddReq) returns (UserRoleAddResp)

    @handler UserRoleDelete
    get /user/role/delete (UserRoleDeleteReq) returns (UserRoleDeleteResp)
}

@server (
    prefix: /v1
    group:  class
)
service user-api {
    @handler UserClassList
    get /user/class/list returns ([]UserClassResp)

    @handler UserClassUpdate
    get /user/class/update (UserClassUpdateReq) returns (UserClassUpdateResp)

    @handler UserClassInfo
    get /user/class/info (UserClassReq) returns (UserClassResp)

    @handler UserClassAdd
    get /user/class/add (UserClassAddReq) returns (UserClassAddResp)

    @handler UserClassDelete
    get /user/class/delete (UserClassDeleteReq) returns (UserClassDeleteResp)
}


```


```bash
.
├── etc
│   └── user-api.yaml
├── internal
│   ├── config
│   │   └── config.go
│   ├── handler
│   │   ├── class
│   │   │   ├── userclassaddhandler.go
│   │   │   ├── userclassdeletehandler.go
│   │   │   ├── userclassinfohandler.go
│   │   │   ├── userclasslisthandler.go
│   │   │   └── userclassupdatehandler.go
│   │   ├── role
│   │   │   ├── userroleaddhandler.go
│   │   │   ├── userroledeletehandler.go
│   │   │   ├── userroleinfohandler.go
│   │   │   ├── userrolelisthandler.go
│   │   │   └── userroleupdatehandler.go
│   │   ├── routes.go
│   │   └── user
│   │       ├── userinfohandler.go
│   │       ├── userinfoupdatehandler.go
│   │       ├── userlisthandler.go
│   │       └── userloginhandler.go
│   ├── logic
│   │   ├── class
│   │   │   ├── userclassaddlogic.go
│   │   │   ├── userclassdeletelogic.go
│   │   │   ├── userclassinfologic.go
│   │   │   ├── userclasslistlogic.go
│   │   │   └── userclassupdatelogic.go
│   │   ├── role
│   │   │   ├── userroleaddlogic.go
│   │   │   ├── userroledeletelogic.go
│   │   │   ├── userroleinfologic.go
│   │   │   ├── userrolelistlogic.go
│   │   │   └── userroleupdatelogic.go
│   │   └── user
│   │       ├── userinfologic.go
│   │       ├── userinfoupdatelogic.go
│   │       ├── userlistlogic.go
│   │       └── userloginlogic.go
│   ├── svc
│   │   └── servicecontext.go
│   └── types
│       ├── class
│       │   └── class.go
│       ├── role
│       │   └── role.go
│       └── user
│           └── user.go
└── user.go

17 directories, 36 files
```

이 항목은 해당 기능의 사용 방법, 설정, 주의 사항을 설명합니다.
