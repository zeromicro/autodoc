---
title: API Route Groups
description: Group routes in an .api file.
sidebar:
  order: 3

---


## Overview

In go-zero, we declared HTTP service via api language, and then generated HTTP service code via goctl, after our systematic introduction to <a href="/docs/tutorials" target="_blank">API norm</a>.

In HTTP service development, as business develops, our services interfaces will grow, and the number of code files generated (handler, logic files, etc.) will grow, when some of the generated code files will need to be aggregated in order to facilitate development and maintenance.

## Service Group

Assume that we have a user service, we have multiple interfaces below：

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

Let's first look at api language prophylactic without grouping：

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

Code directory structure generated without a group below：

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

Since we do not group in groups, all the files in the generated code handler and the log directory are blown together. This directory structure is not well managed and read in the project, and we follow as `user`,`role`,`class` for grouping. In api language, we can group by using `server` group keywords in the `group` groups below：

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

Let's look again at the code-generation directory structure after grouping：

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

By clustering we can easily group different business logic into different directories so that different business logic can be managed easily.
