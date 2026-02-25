---
title: API 路由分组
description: 在 .api 文件中对路由进行分组。
sidebar:
  order: 3

---


## 概述

在 go-zero 中，我们通过 api 语言来声明 HTTP 服务，然后通过 goctl 生成 HTTP 服务代码，在之前我们系统性的介绍了 <a href="/docs/reference/api-dsl" target="_blank">API 规范</a>。

在 HTTP 服务开发中，随着业务的发展，我们的服务接口会越来越多，生成的代码文件(handler，logic，types 文件等)也会越来越多，这时候我们需要将一些生成的代码文件按照一定维度进行文件夹聚合，以便于开发和维护。

## 服务分组

假设我们有一个用户服务，我们有多个接口如下：

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

我们首先来看一下在不进行分组的情况下 api 语言的写法：

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

在不分组的情况下生成的代码目录结构如下：

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

由于我们没有进行分组，所以生成的代码中handler 和 logic 结构体目录下的文件是全部揉在一起的，这样的目录结构在项目中不太好管理和阅读，接下来我们按照 `user`，`role`，`class` 来进行分组，在 api 语言中，我们可以通过在 `@server` 语句块中使用 `group` 关键字来进行分组，分组的语法如下：

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

我们再来看一下分组后的代码生成目录结构：

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
│       ├── class.go
│       ├── role.go
│       └── user.go
└── user.go

14 directories, 36 files

```

通过分组，我们可以很方便的将不同的业务逻辑分组到不同的目录下，这样可以很方便的管理不同的业务逻辑。


:::note 注意
通过命令行参数 `--types-group` 可开启 types 分组，types 分组会按照 group 名称生成不同的文件，而不是按照目录分组，生成示例如下
```shell
goctl api go --api $api --dir $output --type-group
```
types 分组需要 goctl 大于等于 `1.8.3` 版本
该功能处于实验性阶段，如果兼容问题请执行命令 `goctl env -w GOCTL_EXPERIMENTAL=off` 关闭实验性功能即可
请注意，实验功能非稳定版本，有存在调整的可能。
:::
