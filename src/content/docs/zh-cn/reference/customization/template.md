---
title: 模板自定义
description: 自定义 goctl 代码生成模板。
---


## 概述

goctl 代码生成是基于 go 的模板去实现数据驱动的，虽然目前 goctl 的代码生成可以满足一部分代码生成功能，但是模板的自定义可以更加丰富代码生成。

模板指令可参考 <a href="/docs/reference/cli-guide/template" target="_blank">goctl template</a>

## 示例

## 场景

实现统一格式的 body 响应，格式如下：

```json
{
  "code": 0,
  "msg": "OK",
  "data": {}
  // ①
}
```

① 实际响应数据

:::tip
`go-zero`生成的代码没有对其进行处理
:::

### 准备工作

我们提前在 `module` 为 `greet` 的工程下的 `response` 包中写一个 `Response` 方法，目录树类似如下：

```text
greet
├── response
│   └── response.go
└── xxx...
```

代码如下

```go
package response

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
)

type Body struct {
	Code int         `json:"code"`
	Msg  string      `json:"msg"`
	Data interface{} `json:"data,omitempty"`
}

func Response(w http.ResponseWriter, resp interface{}, err error) {
    var body Body
    if err != nil {
        body.Code = -1
        body.Msg = err.Error()
    } else {
        body.Msg = "OK"
        body.Data = resp
    }
    httpx.OkJson(w, body)
}
```

### 修改 `handler` 模板

```shell
$ vim ~/.goctl/${goctl版本号}/api/handler.tpl
```

将模板替换为以下内容

```go
package handler

import (
	"net/http"
	"greet/response"// ①
	{{.ImportPackages}}
)

func {{.HandlerName}}(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		{{if .HasRequest}}var req types.{{.RequestType}}
		if err := httpx.Parse(r, &req); err != nil {
			httpx.Error(w, err)
			return
		}{{end}}

		l := {{.LogicName}}.New{{.LogicType}}(r.Context(), svcCtx)
		{{if .HasResp}}resp, {{end}}err := l.{{.Call}}({{if .HasRequest}}&req{{end}})
		{{if .HasResp}}response.Response(w, resp, err){{else}}response.Response(w, nil, err){{end}}//②

	}
}
```

① 替换为你真实的`response`包名，仅供参考

② 自定义模板内容

:::tip 1.如果本地没有`~/.goctl/${goctl版本号}/api/handler.tpl`文件，可以通过模板初始化命令`goctl template init`进行初始化
:::

### 修改模板前后对比

- 修改前

```go
func GreetHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.Request
		if err := httpx.Parse(r, &req); err != nil {
			httpx.Error(w, err)
			return
		}

		l := logic.NewGreetLogic(r.Context(), svcCtx)
		resp, err := l.Greet(&req)
		// 以下内容将被自定义模板替换
		if err != nil {
			httpx.Error(w, err)
		} else {
			httpx.OkJson(w, resp)
		}
	}
}
```

- 修改后

```go
func GreetHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.Request
		if err := httpx.Parse(r, &req); err != nil {
			httpx.Error(w, err)
			return
		}

		l := logic.NewGreetLogic(r.Context(), svcCtx)
		resp, err := l.Greet(&req)
		response.Response(w, resp, err)
	}
}
```

### 修改模板前后响应体对比

- 修改前

```json
{
  "message": "Hello go-zero!"
}
```

- 修改后

```json
{
  "code": 0,
  "msg": "OK",
  "data": {
    "message": "Hello go-zero!"
  }
}
```

## 模板自定义规则

1. 在 goctl 提供的有效数据范围内修改，即不支持外部变量
2. 不支持新增模板文件
3. 不支持变量修改

## 模板变量

### goctl api -o 代码生成模板

模板默认目录 `~/.goctl/${goctl-version}/newapi`

#### api.tpl

```go
syntax = "v1"

info (
	title: // TODO: add title
	desc: // TODO: add description
	author: "{{.gitUser}}"
	email: "{{.gitEmail}}"
)

type request {
	// TODO: add members here and delete this comment
}

type response {
	// TODO: add members here and delete this comment
}

service {{.serviceName}} {
	@handler GetUser // TODO: set handler name and delete this comment
	get /users/id/:userId(request) returns(response)

	@handler CreateUser // TODO: set handler name and delete this comment
	post /users/create(request)
}

```

对应指令 `goctl api -o`

模板注入对象为 `map[string]string`

```go
map[string]string{
    "gitUser":     getGitName(),
    "gitEmail":    getGitEmail(),
    "serviceName": baseName + "-api",
}
```

| pipeline变量   | 类型     | 说明     |
|--------------|--------|--------|
| .gitUser     | string | Git用户名 |
| .gitEmail    | string | Git邮箱  |
| .serviceName | string | 服务名称   |

### goctl api go 代码生成模板

对应指令 `goctl api go ...`

模板默认目录 `~/.goctl/${goctl-version}/api`

#### config.tpl

```go
package config

import {{.authImport}}

type Config struct {
	rest.RestConf
	{{.auth}}
	{{.jwtTrans}}
}

```

模板注入对象为 `map[string]string`

```go
map[string]string{
    "authImport": authImportStr,
    "auth":       strings.Join(auths, "\n"),
    "jwtTrans":   strings.Join(jwtTransList, "\n"),
}
```

| pipeline变量  | 类型     | 说明    |
|-------------|--------|-------|
| .authImport | string | 认证导入  |
| .auth       | string | 认证配置  |
| .jwtTrans   | string | JWT配置 |

#### etc.tpl

```go
Name: {{.serviceName}}
Host: {{.host}}
Port: {{.port}}
```

模板注入对象为 map[string]string

```go
map[string]string{
    "serviceName": service.Name,
    "host":        host,
    "port":        port,
}
```

| pipeline变量   | 类型     | 说明   |
|--------------|--------|------|
| .serviceName | string | 服务名称 |
| .host        | string | 主机地址 |
| .port        | string | 端口号  |

#### handler.tpl

```go
package {{.PkgName}}

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	{{.ImportPackages}}
)

{{if .HasDoc}}{{.Doc}}{{end}}
func {{.HandlerName}}(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		{{if .HasRequest}}var req types.{{.RequestType}}
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		{{end}}l := {{.LogicName}}.New{{.LogicType}}(r.Context(), svcCtx)
		{{if .HasResp}}resp, {{end}}err := l.{{.Call}}({{if .HasRequest}}&req{{end}})
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			{{if .HasResp}}httpx.OkJsonCtx(r.Context(), w, resp){{else}}httpx.Ok(w){{end}}
		}
	}
}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "PkgName":        pkgName,
    "ImportPackages": genHandlerImports(group, route, rootPkg),
    "HandlerName":    handler,
    "RequestType":    util.Title(route.RequestTypeName()),
    "LogicName":      logicName,
    "LogicType":      strings.Title(getLogicName(route)),
    "Call":           strings.Title(strings.TrimSuffix(handler, "Handler")),
    "HasResp":        len(route.ResponseTypeName()) > 0,
    "HasRequest":     len(route.RequestTypeName()) > 0,
    "HasDoc":         len(route.JoinedDoc()) > 0,
    "Doc":            getDoc(route.JoinedDoc()),
}
```

| pipeline变量      | 类型     | 说明                               |
|-----------------|--------|----------------------------------|
| .PkgName        | string | 包名                               |
| .ImportPackages | string | 导入包                              |
| .HasDoc         | bool   | 是否有文档注释                          |
| .Doc            | string | 文档注释                             |
| .HandlerName    | string | handler 名称                       |
| .HasRequest     | bool   | 是否有请求体                           |
| .RequestType    | string | 请求类型                             |
| .LogicName      | string | 逻辑包名称，默认为logic,如果有分组时为具体的group名称 |
| .LogicType      | string | 逻辑对象type名称                       |
| .Call           | string | logic 对象调用方法名称                   |
| .HasResp        | bool   | 是否有响应体                           |

#### logic.tpl

```go
package {{.pkgName}}

import (
	{{.imports}}
)

type {{.logic}} struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

{{if .hasDoc}}{{.doc}}{{end}}
func New{{.logic}}(ctx context.Context, svcCtx *svc.ServiceContext) *{{.logic}} {
	return &{{.logic}}{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *{{.logic}}) {{.function}}({{.request}}) {{.responseType}} {
	// todo: add your logic here and delete this line

	{{.returnString}}
}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "pkgName":      subDir[strings.LastIndex(subDir, "/")+1:],
    "imports":      imports,
    "logic":        strings.Title(logic),
    "function":     strings.Title(strings.TrimSuffix(logic, "Logic")),
    "responseType": responseString,
    "returnString": returnString,
    "request":      requestString,
    "hasDoc":       len(route.JoinedDoc()) > 0,
    "doc":          getDoc(route.JoinedDoc()),
}
```

| pipeline变量    | 类型     | 说明                   |
|---------------|--------|----------------------|
| .pkgName      | string | 包名                   |
| .imports      | string | 导入包                  |
| .logic        | string | 逻辑结构体名称              |
| .hasDoc       | bool   | 是否有文档注释              |
| .doc          | string | 文档注释                 |
| .function     | string | logic 函数名称           |
| .request      | string | 请求体表达式，包含参数名称，参数类型   |
| .responseType | string | 响应类型体表达式，包含参数名称，参数类型 |
| .returnString | string | 返回语句，返回的结构体          |

#### main.tpl

```go
package main

import (
	"flag"
	"fmt"

	{{.importPackages}}
)

var configFile = flag.String("f", "etc/{{.serviceName}}.yaml", "the config file")

func main() {
	flag.Parse()

	var c config.Config
	conf.MustLoad(*configFile, &c)

	server := rest.MustNewServer(c.RestConf)
	defer server.Stop()

	ctx := svc.NewServiceContext(c)
	handler.RegisterHandlers(server, ctx)

	fmt.Printf("Starting server at %s:%d...\n", c.Host, c.Port)
	server.Start()
}

```

模板注入对象为 `map[string]string`

```go
map[string]string{
    "importPackages": genMainImports(rootPkg),
    "serviceName":    configName,
}
```

| pipeline变量      | 类型     | 说明   |
|-----------------|--------|------|
| .importPackages | string | 导入包  |
| .serviceName    | string | 服务名称 |

#### middleware.tpl

```go
package middleware

import "net/http"

type {{.name}} struct {
}

func New{{.name}}() *{{.name}} {
	return &{{.name}}{}
}

func (m *{{.name}})Handle(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// TODO generate middleware implement function, delete after code implementation

		// Passthrough to next handler if need
		next(w, r)
	}
}

```

模板注入对象为 `map[string]string`

```go
map[string]string{
    "name": strings.Title(name),
}
```

| pipeline变量 | 类型     | 说明    |
|------------|--------|-------|
| .name      | string | 中间件名称 |

#### svc.tpl

```go
package svc

import (
	{{.configImport}}
)

type ServiceContext struct {
	Config {{.config}}
	{{.middleware}}
}

func NewServiceContext(c {{.config}}) *ServiceContext {
	return &ServiceContext{
		Config: c,
		{{.middlewareAssignment}}
	}
}

```

模板注入对象为 `map[string]string`

```go
map[string]string{
    "configImport":         configImport,
    "config":               "config.Config",
    "middleware":           middlewareStr,
    "middlewareAssignment": middlewareAssignment,
}
```

| pipeline变量            | 类型     | 说明      |
|-----------------------|--------|---------|
| .configImport         | string | pkg 导入  |
| .config               | string | 配置结构体名称 |
| .middleware           | string | 中间件字段   |
| .middlewareAssignment | string | 中间件赋值语句 |

#### type.tpl

```go
// Code generated by goctl. DO NOT EDIT.
package types{{if .containsTime}}
import (
	"time"
){{end}}
{{.types}}
```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "types":        val,
    "containsTime": false,
}
```

| pipeline变量    | 类型     | 说明     |
|---------------|--------|--------|
| .containsTime | bool   | 是否包含时间 |
| .types        | string | 类型     |

### goctl api new 代码生成模板

对应指令为 `goctl api new ...`

模板默认目录 `~/.goctl/${goctl-version}/newapi`

#### api.tpl

```go
syntax = "v1"

type Request {
  Name string `path:"name,options=you|me"`
}

type Response {
  Message string `json:"message"`
}

service {{.name}}-api {
  @handler {{.handler}}Handler
  get /from/:name(Request) returns (Response)
}

```

模板注入对象 `map[string]string`

```go
map[string]string{
    "name":    dirName,
    "handler": strings.Title(dirName),
}
```

| pipeline变量 | 类型     | 说明    |
|------------|--------|-------|
| .name      | string | 服务名称  |
| .handler   | string | 处理器名称 |

### mongo 代码生成模板

模板默认目录 `~/.goctl/${goctl-version}/mongo`

#### error.tpl

```go
package model

import (
	"errors"

	"github.com/zeromicro/go-zero/core/stores/mon"
)

var (
	ErrNotFound        = mon.ErrNotFound
	ErrInvalidObjectId = errors.New("invalid objectId")
)

```

#### model.tpl

```go
// Code generated by goctl. DO NOT EDIT.
package model

import (
    "context"
    "time"

    {{if .Cache}}"github.com/zeromicro/go-zero/core/stores/monc"{{else}}"github.com/zeromicro/go-zero/core/stores/mon"{{end}}
    "go.mongodb.org/mongo-driver/bson"
    "go.mongodb.org/mongo-driver/bson/primitive"
    "go.mongodb.org/mongo-driver/mongo"
)

{{if .Cache}}var prefix{{.Type}}CacheKey = "cache:{{.lowerType}}:"{{end}}

type {{.lowerType}}Model interface{
    Insert(ctx context.Context,data *{{.Type}}) error
    FindOne(ctx context.Context,id string) (*{{.Type}}, error)
    Update(ctx context.Context,data *{{.Type}}) (*mongo.UpdateResult, error)
    Delete(ctx context.Context,id string) (int64, error)
}

type default{{.Type}}Model struct {
    conn {{if .Cache}}*monc.Model{{else}}*mon.Model{{end}}
}

func newDefault{{.Type}}Model(conn {{if .Cache}}*monc.Model{{else}}*mon.Model{{end}}) *default{{.Type}}Model {
    return &default{{.Type}}Model{conn: conn}
}


func (m *default{{.Type}}Model) Insert(ctx context.Context, data *{{.Type}}) error {
    if data.ID.IsZero() {
        data.ID = primitive.NewObjectID()
        data.CreateAt = time.Now()
        data.UpdateAt = time.Now()
    }

    {{if .Cache}}key := prefix{{.Type}}CacheKey + data.ID.Hex(){{end}}
    _, err := m.conn.InsertOne(ctx, {{if .Cache}}key, {{end}} data)
    return err
}

func (m *default{{.Type}}Model) FindOne(ctx context.Context, id string) (*{{.Type}}, error) {
    oid, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return nil, ErrInvalidObjectId
    }

    var data {{.Type}}
    {{if .Cache}}key := prefix{{.Type}}CacheKey + id{{end}}
    err = m.conn.FindOne(ctx, {{if .Cache}}key, {{end}}&data, bson.M{"_id": oid})
    switch err {
    case nil:
        return &data, nil
    case {{if .Cache}}monc{{else}}mon{{end}}.ErrNotFound:
        return nil, ErrNotFound
    default:
        return nil, err
    }
}

func (m *default{{.Type}}Model) Update(ctx context.Context, data *{{.Type}}) (*mongo.UpdateResult, error) {
    data.UpdateAt = time.Now()
    {{if .Cache}}key := prefix{{.Type}}CacheKey + data.ID.Hex(){{end}}
    res, err := m.conn.UpdateOne(ctx, {{if .Cache}}key, {{end}}bson.M{"_id": data.ID}, bson.M{"$set": data})
    return res, err
}

func (m *default{{.Type}}Model) Delete(ctx context.Context, id string) (int64, error) {
    oid, err := primitive.ObjectIDFromHex(id)
    if err != nil {
        return 0, ErrInvalidObjectId
    }
	{{if .Cache}}key := prefix{{.Type}}CacheKey +id{{end}}
    res, err := m.conn.DeleteOne(ctx, {{if .Cache}}key, {{end}}bson.M{"_id": oid})
	return res, err
}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "Type":      stringx.From(t).Title(),
    "lowerType": stringx.From(t).Untitle(),
    "Cache":     ctx.Cache,
}
```

| pipeline变量 | 类型     | 说明       |
|------------|--------|----------|
| .Cache     | bool   | 是否启用缓存   |
| .Type      | string | 模型类型名称   |
| .lowerType | string | 小写模型类型名称 |

#### model_custom.tpl

```go
package model

{{if .Cache}}import (
    "github.com/zeromicro/go-zero/core/stores/cache"
    "github.com/zeromicro/go-zero/core/stores/monc"
){{else}}import "github.com/zeromicro/go-zero/core/stores/mon"{{end}}

{{if .Easy}}
const {{.Type}}CollectionName = "{{.snakeType}}"
{{end}}

var _ {{.Type}}Model = (*custom{{.Type}}Model)(nil)

type (
    // {{.Type}}Model is an interface to be customized, add more methods here,
    // and implement the added methods in custom{{.Type}}Model.
    {{.Type}}Model interface {
        {{.lowerType}}Model
    }

    custom{{.Type}}Model struct {
        *default{{.Type}}Model
    }
)


// New{{.Type}}Model returns a model for the mongo.
{{if .Easy}}func New{{.Type}}Model(url, db string{{if .Cache}}, c cache.CacheConf{{end}}) {{.Type}}Model {
    conn := {{if .Cache}}monc{{else}}mon{{end}}.MustNewModel(url, db, {{.Type}}CollectionName{{if .Cache}}, c{{end}})
    return &custom{{.Type}}Model{
        default{{.Type}}Model: newDefault{{.Type}}Model(conn),
    }
}{{else}}func New{{.Type}}Model(url, db, collection string{{if .Cache}}, c cache.CacheConf{{end}}) {{.Type}}Model {
    conn := {{if .Cache}}monc{{else}}mon{{end}}.MustNewModel(url, db, collection{{if .Cache}}, c{{end}})
    return &custom{{.Type}}Model{
        default{{.Type}}Model: newDefault{{.Type}}Model(conn),
    }
}{{end}}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "Type":      stringx.From(t).Title(),
    "lowerType": stringx.From(t).Untitle(),
    "snakeType": stringx.From(t).ToSnake(),
    "Cache":     ctx.Cache,
    "Easy":      ctx.Easy,
}
```

| pipeline变量 | 类型     | 说明       |
|------------|--------|----------|
| .Cache     | bool   | 是否启用缓存   |
| .Easy      | bool   | 是否简易模式   |
| .Type      | string | 模型类型名称   |
| .snakeType | string | 蛇形模型类型名称 |
| .lowerType | string | 小写模型类型名称 |

#### types.tpl

```go
package model

import (
	"time"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type {{.Type}} struct {
	ID primitive.ObjectID `bson:"_id,omitempty" json:"id,omitempty"`
	// TODO: Fill your own fields
	UpdateAt time.Time `bson:"updateAt,omitempty" json:"updateAt,omitempty"`
	CreateAt time.Time `bson:"createAt,omitempty" json:"createAt,omitempty"`
}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "Type": stringx.From(t).Title(),
}
```

| pipeline变量 | 类型     | 说明     |
|------------|--------|--------|
| .Type      | string | 模型类型名称 |

### mysql 代码生成模板

模板默认目录 `~/.goctl/${goctl-version}/model`

#### customized.tpl

空模板，方便自定义

```go

```

模板注入对象 `map[string]any`

```go
mmap[string]any{
    "withCache":                 withCache,
    "containsIndexCache":        table.ContainsUniqueCacheKey,
    "upperStartCamelObject":     camel,
    "lowerStartCamelObject":     stringx.From(camel).Untitle(),
    "lowerStartCamelPrimaryKey": util.EscapeGolangKeyword(stringx.From(table.PrimaryKey.Name.ToCamel()).Untitle()),
    "upperStartCamelPrimaryKey": table.PrimaryKey.Name.ToCamel(),
    "primaryKeyDataType":        table.PrimaryKey.DataType,
    "originalPrimaryKey":        wrapWithRawString(table.PrimaryKey.Name.Source(), postgreSql),
    "primaryCacheKey":           table.PrimaryCacheKey.DataKeyExpression,
    "primaryKeyVariable":        table.PrimaryCacheKey.KeyLeft,
    "keys":                      strings.Join(keys, "\n"),
    "keyValues":                 strings.Join(keyVars, ", "),
    "expression":                strings.Join(expressions, ", "),
    "expressionValues":          strings.Join(expressionValues, ", "),
    "postgreSql":                postgreSql,
    "fields":                    fields,
    "data":                      table,
}
```

#### delete.tpl

```go
func (m *default{{.upperStartCamelObject}}Model) Delete(ctx context.Context, {{.lowerStartCamelPrimaryKey}} {{.dataType}}) error {
	{{if .withCache}}{{if .containsIndexCache}}data, err:=m.FindOne(ctx, {{.lowerStartCamelPrimaryKey}})
	if err!=nil{
		return err
	}

{{end}}	{{.keys}}
    _, err {{if .containsIndexCache}}={{else}}:={{end}} m.ExecCtx(ctx, func(ctx context.Context, conn sqlx.SqlConn) (result sql.Result, err error) {
		query := fmt.Sprintf("delete from %s where {{.originalPrimaryKey}} = {{if .postgreSql}}$1{{else}}?{{end}}", m.table)
		return conn.ExecCtx(ctx, query, {{.lowerStartCamelPrimaryKey}})
	}, {{.keyValues}}){{else}}query := fmt.Sprintf("delete from %s where {{.originalPrimaryKey}} = {{if .postgreSql}}$1{{else}}?{{end}}", m.table)
		_,err:=m.conn.ExecCtx(ctx, query, {{.lowerStartCamelPrimaryKey}}){{end}}
	return err
}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "upperStartCamelObject":     camel,
    "withCache":                 withCache,
    "containsIndexCache":        table.ContainsUniqueCacheKey,
    "lowerStartCamelPrimaryKey": util.EscapeGolangKeyword(stringx.From(table.PrimaryKey.Name.ToCamel()).Untitle()),
    "dataType":                  table.PrimaryKey.DataType,
    "keys":                      strings.Join(keys, "\n"),
    "originalPrimaryKey":        wrapWithRawString(table.PrimaryKey.Name.Source(), postgreSql),
    "keyValues":                 strings.Join(keyVars, ", "),
    "postgreSql":                postgreSql,
    "data":                      table,
}
```

| pipeline变量                 | 类型     | 说明                 |
|----------------------------|--------|--------------------|
| .upperStartCamelObject     | string | 对象名称的首字母大写形式       |
| .lowerStartCamelPrimaryKey | string | 主键变量名的首字母小写形式      |
| .dataType                  | string | 主键数据类型             |
| .withCache                 | bool   | 是否启用缓存             |
| .containsIndexCache        | bool   | 是否包含索引缓存逻辑         |
| .keys                      | string | 在包含索引缓存时，用于查找数据的逻辑 |
| .keyValues                 | string | 在缓存中找到的键值对         |
| .postgreSql                | bool   | 是否使用 PostgreSQL    |
| .originalPrimaryKey        | string | 原始主键名称             |

#### err.tpl

```go
package {{.pkg}}

import "github.com/zeromicro/go-zero/core/stores/sqlx"

var ErrNotFound = sqlx.ErrNotFound

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "pkg": g.pkg,
}
```

| pipeline变量 | 类型     | 说明  |
|------------|--------|-----|
| .pkg       | string | 包名  |

#### field.tpl

```go
{{.name}} {{.type}} {{.tag}} {{if .hasComment}}// {{.comment}}{{end}}
```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "name":       util.SafeString(field.Name.ToCamel()),
    "type":       field.DataType,
    "tag":        tag,
    "hasComment": field.Comment != "",
    "comment":    field.Comment,
    "data":       table,
}
```

| pipeline变量  | 类型     | 说明        |
|-------------|--------|-----------|
| .name       | string | 名称        |
| .type       | string | 类型        |
| .tag        | string | 标签        |
| .hasComment | bool   | 是否有注释     |
| .comment    | string | 注释内容 (可选) |

#### find-one.tpl

```go
func (m *default{{.upperStartCamelObject}}Model) FindOne(ctx context.Context, {{.lowerStartCamelPrimaryKey}} {{.dataType}}) (*{{.upperStartCamelObject}}, error) {
	{{if .withCache}}{{.cacheKey}}
	var resp {{.upperStartCamelObject}}
	err := m.QueryRowCtx(ctx, &resp, {{.cacheKeyVariable}}, func(ctx context.Context, conn sqlx.SqlConn, v any) error {
		query :=  fmt.Sprintf("select %s from %s where {{.originalPrimaryKey}} = {{if .postgreSql}}$1{{else}}?{{end}} limit 1", {{.lowerStartCamelObject}}Rows, m.table)
		return conn.QueryRowCtx(ctx, v, query, {{.lowerStartCamelPrimaryKey}})
	})
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}{{else}}query := fmt.Sprintf("select %s from %s where {{.originalPrimaryKey}} = {{if .postgreSql}}$1{{else}}?{{end}} limit 1", {{.lowerStartCamelObject}}Rows, m.table)
	var resp {{.upperStartCamelObject}}
	err := m.conn.QueryRowCtx(ctx, &resp, query, {{.lowerStartCamelPrimaryKey}})
	switch err {
	case nil:
		return &resp, nil
	case sqlx.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}{{end}}
}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "withCache":                 withCache,
    "upperStartCamelObject":     camel,
    "lowerStartCamelObject":     stringx.From(camel).Untitle(),
    "originalPrimaryKey":        wrapWithRawString(table.PrimaryKey.Name.Source(), postgreSql),
    "lowerStartCamelPrimaryKey": util.EscapeGolangKeyword(stringx.From(table.PrimaryKey.Name.ToCamel()).Untitle()),
    "dataType":                  table.PrimaryKey.DataType,
    "cacheKey":                  table.PrimaryCacheKey.KeyExpression,
    "cacheKeyVariable":          table.PrimaryCacheKey.KeyLeft,
    "postgreSql":                postgreSql,
    "data":                      table,
}
```

| pipeline变量                 | 类型     | 说明              |
|----------------------------|--------|-----------------|
| .upperStartCamelObject     | string | 对象名称的首字母大写形式    |
| .lowerStartCamelPrimaryKey | string | 主键变量名的首字母小写形式   |
| .dataType                  | string | 主键数据类型          |
| .withCache                 | bool   | 是否启用缓存          |
| .cacheKey                  | string | 缓存键             |
| .cacheKeyVariable          | string | 缓存键变量           |
| .postgreSql                | bool   | 是否使用 PostgreSQL |
| .originalPrimaryKey        | string | 原始主键名称          |
| .lowerStartCamelObject     | string | 对象名称的首字母小写形式    |

#### find-one-by-field.tpl

```go
func (m *default{{.upperStartCamelObject}}Model) FindOneBy{{.upperField}}(ctx context.Context, {{.in}}) (*{{.upperStartCamelObject}}, error) {
	{{if .withCache}}{{.cacheKey}}
	var resp {{.upperStartCamelObject}}
	err := m.QueryRowIndexCtx(ctx, &resp, {{.cacheKeyVariable}}, m.formatPrimary, func(ctx context.Context, conn sqlx.SqlConn, v any) (i any, e error) {
		query := fmt.Sprintf("select %s from %s where {{.originalField}} limit 1", {{.lowerStartCamelObject}}Rows, m.table)
		if err := conn.QueryRowCtx(ctx, &resp, query, {{.lowerStartCamelField}}); err != nil {
			return nil, err
		}
		return resp.{{.upperStartCamelPrimaryKey}}, nil
	}, m.queryPrimary)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}{{else}}var resp {{.upperStartCamelObject}}
	query := fmt.Sprintf("select %s from %s where {{.originalField}} limit 1", {{.lowerStartCamelObject}}Rows, m.table )
	err := m.conn.QueryRowCtx(ctx, &resp, query, {{.lowerStartCamelField}})
	switch err {
	case nil:
		return &resp, nil
	case sqlx.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}{{end}}

```

模板注入对象为 `map[string]any`

```go
map[string]any{
    "upperStartCamelObject":     camelTableName,
    "upperField":                key.FieldNameJoin.Camel().With("").Source(),
    "in":                        in,
    "withCache":                 withCache,
    "cacheKey":                  key.KeyExpression,
    "cacheKeyVariable":          key.KeyLeft,
    "lowerStartCamelObject":     stringx.From(camelTableName).Untitle(),
    "lowerStartCamelField":      paramJoinString,
    "upperStartCamelPrimaryKey": table.PrimaryKey.Name.ToCamel(),
    "originalField":             originalFieldString,
    "postgreSql":                postgreSql,
    "data":                      table,
}
```

| 模板变量                       | 类型     | 描述           |
|----------------------------|--------|--------------|
| .upperStartCamelObject     | string | 对象名称的首字母大写形式 |
| .upperField                | string | 字段名称的首字母大写形式 |
| .in                        | string | 输入参数变量名      |
| .withCache                 | bool   | 是否启用缓存       |
| .cacheKey                  | string | 缓存键          |
| .cacheKeyVariable          | string | 缓存键变量名       |
| .formatPrimary             | string | 主键格式化字符串     |
| .lowerStartCamelObject     | string | 对象名称的首字母小写形式 |
| .originalField             | string | 原始字段名        |
| .lowerStartCamelObjectRows | string | 对象行数的首字母小写形式 |
| .table                     | string | 表名           |
| .queryPrimary              | string | 主要查询         |

#### find-one-by-field-extra-method.tpl

```go
func (m *default{{.upperStartCamelObject}}Model) formatPrimary(primary any) string {
	return fmt.Sprintf("%s%v", {{.primaryKeyLeft}}, primary)
}

func (m *default{{.upperStartCamelObject}}Model) queryPrimary(ctx context.Context, conn sqlx.SqlConn, v, primary any) error {
	query := fmt.Sprintf("select %s from %s where {{.originalPrimaryField}} = {{if .postgreSql}}$1{{else}}?{{end}} limit 1", {{.lowerStartCamelObject}}Rows, m.table )
	return conn.QueryRowCtx(ctx, v, query, primary)
}

```

模板注入对象为

```go
map[string]any{
    "upperStartCamelObject": camelTableName,
    "primaryKeyLeft":        table.PrimaryCacheKey.VarLeft,
    "lowerStartCamelObject": stringx.From(camelTableName).Untitle(),
    "originalPrimaryField":  wrapWithRawString(table.PrimaryKey.Name.Source(), postgreSql),
    "postgreSql":            postgreSql,
    "data":                  table,
}
```

| 模板变量                       | 类型     | 描述              |
|----------------------------|--------|-----------------|
| .upperStartCamelObject     | string | 对象名称的首字母大写形式    |
| .primaryKeyLeft            | string | 主键左部分字符串        |
| .lowerStartCamelObject     | string | 对象名称的首字母小写形式    |
| .originalPrimaryField      | string | 原始主键字段名         |
| .postgreSql                | bool   | 是否使用 PostgreSQL |
| .lowerStartCamelObjectRows | string | 对象行数的首字母小写形式    |

#### import.tpl

```go
import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	{{if .time}}"time"{{end}}

	{{if .containsPQ}}"github.com/lib/pq"{{end}}
	"github.com/zeromicro/go-zero/core/stores/builder"
	"github.com/zeromicro/go-zero/core/stores/cache"
	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
	"github.com/zeromicro/go-zero/core/stringx"

	{{.third}}
)

```

模板注入对象为

```go
map[string]any{
    "time":       timeImport,
    "containsPQ": table.ContainsPQ,
    "data":       table,
    "third":      strings.Join(thirdImports, "\n"),
}
```

| 模板变量        | 类型     | 描述                                        |
|-------------|--------|-------------------------------------------|
| .time       | bool   | 是否导入时间包 (`time`)                          |
| .containsPQ | bool   | 是否包含 PostgreSQL 的依赖 (`github.com/lib/pq`) |
| .third      | string | 其他第三方包的导入路径                               |

#### import.no-cache.tpl

```go
import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	{{if .time}}"time"{{end}}

    {{if .containsPQ}}"github.com/lib/pq"{{end}}
	"github.com/zeromicro/go-zero/core/stores/builder"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
	"github.com/zeromicro/go-zero/core/stringx"

	{{.third}}
)

```

模板注入对象为：

```go
map[string]any{
    "time":       timeImport,
    "containsPQ": table.ContainsPQ,
    "data":       table,
    "third":      strings.Join(thirdImports, "\n"),
}
```

| 模板变量        | 类型     | 描述                                        |
|-------------|--------|-------------------------------------------|
| .time       | bool   | 是否导入时间包 (`time`)                          |
| .containsPQ | bool   | 是否包含 PostgreSQL 的依赖 (`github.com/lib/pq`) |
| .third      | string | 其他第三方包的导入路径                               |

#### insert.tpl

```go
func (m *default{{.upperStartCamelObject}}Model) Insert(ctx context.Context, data *{{.upperStartCamelObject}}) (sql.Result,error) {
	{{if .withCache}}{{.keys}}
    ret, err := m.ExecCtx(ctx, func(ctx context.Context, conn sqlx.SqlConn) (result sql.Result, err error) {
		query := fmt.Sprintf("insert into %s (%s) values ({{.expression}})", m.table, {{.lowerStartCamelObject}}RowsExpectAutoSet)
		return conn.ExecCtx(ctx, query, {{.expressionValues}})
	}, {{.keyValues}}){{else}}query := fmt.Sprintf("insert into %s (%s) values ({{.expression}})", m.table, {{.lowerStartCamelObject}}RowsExpectAutoSet)
    ret,err:=m.conn.ExecCtx(ctx, query, {{.expressionValues}}){{end}}
	return ret,err
}

```

模板注入对象为

```go
map[string]any{
    "withCache":             withCache,
    "upperStartCamelObject": camel,
    "lowerStartCamelObject": stringx.From(camel).Untitle(),
    "expression":            strings.Join(expressions, ", "),
    "expressionValues":      strings.Join(expressionValues, ", "),
    "keys":                  strings.Join(keys, "\n"),
    "keyValues":             strings.Join(keyVars, ", "),
    "data":                  table,
})
```

| 模板变量                   | 类型     | 描述              |
|------------------------|--------|-----------------|
| .upperStartCamelObject | string | 对象名称的首字母大写形式    |
| .withCache             | bool   | 是否启用缓存          |
| .keys                  | string | 在启用缓存时，用于键的生成逻辑 |
| .lowerStartCamelObject | string | 对象名称的首字母小写形式    |
| .expression            | string | 表达式             |
| .expressionValues      | string | 表达式值            |

#### interface-delete.tpl

```go
Delete(ctx context.Context, {{.lowerStartCamelPrimaryKey}} {{.dataType}}) error
```

模板注入对象为

```go
map[string]any{
    "lowerStartCamelPrimaryKey": util.EscapeGolangKeyword(stringx.From(table.PrimaryKey.Name.ToCamel()).Untitle()),
    "dataType":                  table.PrimaryKey.DataType,
    "data":                      table,
}
```

| 模板变量                       | 类型     | 描述            |
|----------------------------|--------|---------------|
| .lowerStartCamelPrimaryKey | string | 主键变量名的首字母小写形式 |
| .dataType                  | string | 主键数据类型        |

#### interface-find-one.tpl

```go
FindOne(ctx context.Context, {{.lowerStartCamelPrimaryKey}} {{.dataType}}) (*{{.upperStartCamelObject}}, error)
```

模板注入对象为：

```go
map[string]any{
    "upperStartCamelObject":     camel,
    "lowerStartCamelPrimaryKey": util.EscapeGolangKeyword(stringx.From(table.PrimaryKey.Name.ToCamel()).Untitle()),
    "dataType":                  table.PrimaryKey.DataType,
    "data":                      table,
}
```

| 模板变量                       | 类型     | 描述            |
|----------------------------|--------|---------------|
| .lowerStartCamelPrimaryKey | string | 主键变量名的首字母小写形式 |
| .dataType                  | string | 主键数据类型        |
| .upperStartCamelObject     | string | 对象名称的首字母大写形式  |

#### interface-find-one-by-field.tpl

```go
FindOneBy{{.upperField}}(ctx context.Context, {{.in}}) (*{{.upperStartCamelObject}}, error)
```

模板注入对象为：

```go
string]any{
    "upperStartCamelObject": camelTableName,
    "upperField":            key.FieldNameJoin.Camel().With("").Source(),
    "in":                    in,
    "data":                  table,
}
```

| 模板变量                   | 类型     | 描述           |
|------------------------|--------|--------------|
| .upperField            | string | 字段名称的首字母大写形式 |
| .in                    | string | 输入参数变量名      |
| .upperStartCamelObject | string | 对象名称的首字母大写形式 |

#### interface-insert.tpl

```go
Insert(ctx context.Context, data *{{.upperStartCamelObject}}) (sql.Result,error)
```

注入对象为

```go
string]any{
    "upperStartCamelObject": camel,
    "data":                  table,
}
```

| 模板变量                   | 类型     | 描述           |
|------------------------|--------|--------------|
| .upperStartCamelObject | string | 对象名称的首字母大写形式 |

#### interface-update.tpl

```go
Update(ctx context.Context, {{if .containsIndexCache}}newData{{else}}data{{end}} *{{.upperStartCamelObject}}) error
```

模板注入对象为：

```go
map[string]any{
    "upperStartCamelObject": camelTableName,
    "data":                  table,
}
```

| 模板变量                   | 类型     | 描述           |
|------------------------|--------|--------------|
| .containsIndexCache    | bool   | 是否包含索引缓存     |
| .upperStartCamelObject | string | 对象名称的首字母大写形式 |

#### model.tpl

```go
package {{.pkg}}
{{if .withCache}}
import (
	"github.com/zeromicro/go-zero/core/stores/cache"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)
{{else}}

import "github.com/zeromicro/go-zero/core/stores/sqlx"
{{end}}
var _ {{.upperStartCamelObject}}Model = (*custom{{.upperStartCamelObject}}Model)(nil)

type (
	// {{.upperStartCamelObject}}Model is an interface to be customized, add more methods here,
	// and implement the added methods in custom{{.upperStartCamelObject}}Model.
	{{.upperStartCamelObject}}Model interface {
		{{.lowerStartCamelObject}}Model
		{{if not .withCache}}withSession(session sqlx.Session) {{.upperStartCamelObject}}Model{{end}}
	}

	custom{{.upperStartCamelObject}}Model struct {
		*default{{.upperStartCamelObject}}Model
	}
)

// New{{.upperStartCamelObject}}Model returns a model for the database table.
func New{{.upperStartCamelObject}}Model(conn sqlx.SqlConn{{if .withCache}}, c cache.CacheConf, opts ...cache.Option{{end}}) {{.upperStartCamelObject}}Model {
	return &custom{{.upperStartCamelObject}}Model{
		default{{.upperStartCamelObject}}Model: new{{.upperStartCamelObject}}Model(conn{{if .withCache}}, c, opts...{{end}}),
	}
}

{{if not .withCache}}
func (m *custom{{.upperStartCamelObject}}Model) withSession(session sqlx.Session) {{.upperStartCamelObject}}Model {
    return New{{.upperStartCamelObject}}Model(sqlx.NewSqlConnFromSession(session))
}
{{end}}


```

模板注入对象为：

```go
map[string]any{
    "pkg":                   g.pkg,
    "withCache":             withCache,
    "upperStartCamelObject": in.Name.ToCamel(),
    "lowerStartCamelObject": stringx.From(in.Name.ToCamel()).Untitle(),
}
```

| 模板变量                   | 类型     | 描述           |
|------------------------|--------|--------------|
| .pkg                   | string | 包名           |
| .withCache             | bool   | 是否启用缓存       |
| .upperStartCamelObject | string | 对象名称的首字母大写形式 |
| .lowerStartCamelObject | string | 对象名称的首字母小写形式 |

#### model-new.tpl

```go
func new{{.upperStartCamelObject}}Model(conn sqlx.SqlConn{{if .withCache}}, c cache.CacheConf, opts ...cache.Option{{end}}) *default{{.upperStartCamelObject}}Model {
	return &default{{.upperStartCamelObject}}Model{
		{{if .withCache}}CachedConn: sqlc.NewConn(conn, c, opts...){{else}}conn:conn{{end}},
		table:      {{.table}},
	}
}


```

模板注入对象为：

```go
map[string]any{
    "table":                 t,
    "withCache":             withCache,
    "upperStartCamelObject": table.Name.ToCamel(),
    "data":                  table,
}
```

| 模板变量                   | 类型     | 描述           |
|------------------------|--------|--------------|
| .upperStartCamelObject | string | 对象名称的首字母大写形式 |
| .withCache             | bool   | 是否启用缓存       |
| .table                 | string | 数据库表名        |

#### table-name.tpl

```go
func (m *default{{.upperStartCamelObject}}Model) tableName() string {
	return m.table
}

```

模板注入对象为：

```go
map[string]any{
    "tableName":             table.Name.Source(),
    "upperStartCamelObject": table.Name.ToCamel(),
}
```

| 模板变量                   | 类型     | 描述           |
|------------------------|--------|--------------|
| .upperStartCamelObject | string | 对象名称的首字母大写形式 |

#### tag.tpl

```go
`db:"{{.field}}"`
```

模板注入对象为：

```go
map[string]any{
    "field": in,
    "data":  table,
}
```

| 模板变量   | 类型     | 描述        |
|--------|--------|-----------|
| .field | string | db tag 名称 |

#### types.tpl

```go
type (
	{{.lowerStartCamelObject}}Model interface{
		{{.method}}
	}

	default{{.upperStartCamelObject}}Model struct {
		{{if .withCache}}sqlc.CachedConn{{else}}conn sqlx.SqlConn{{end}}
		table string
	}

	{{.upperStartCamelObject}} struct {
		{{.fields}}
	}
)

```

模板注入对象为：

```go
map[string]any{
    "withCache":             withCache,
    "method":                methods,
    "upperStartCamelObject": table.Name.ToCamel(),
    "lowerStartCamelObject": stringx.From(table.Name.ToCamel()).Untitle(),
    "fields":                fieldsString,
    "data":                  table,
}
```

| 模板变量                   | 类型     | 描述           |
|------------------------|--------|--------------|
| .lowerStartCamelObject | string | 对象名称的首字母小写形式 |
| .method                | string | 接口方法定义       |
| .upperStartCamelObject | string | 对象名称的首字母大写形式 |
| .withCache             | bool   | 是否启用缓存       |
| .fields                | string | 结构体字段定义      |

#### update.tpl

```go
func (m *default{{.upperStartCamelObject}}Model) Update(ctx context.Context, {{if .containsIndexCache}}newData{{else}}data{{end}} *{{.upperStartCamelObject}}) error {
	{{if .withCache}}{{if .containsIndexCache}}data, err:=m.FindOne(ctx, newData.{{.upperStartCamelPrimaryKey}})
	if err!=nil{
		return err
	}

{{end}}	{{.keys}}
    _, {{if .containsIndexCache}}err{{else}}err:{{end}}= m.ExecCtx(ctx, func(ctx context.Context, conn sqlx.SqlConn) (result sql.Result, err error) {
		query := fmt.Sprintf("update %s set %s where {{.originalPrimaryKey}} = {{if .postgreSql}}$1{{else}}?{{end}}", m.table, {{.lowerStartCamelObject}}RowsWithPlaceHolder)
		return conn.ExecCtx(ctx, query, {{.expressionValues}})
	}, {{.keyValues}}){{else}}query := fmt.Sprintf("update %s set %s where {{.originalPrimaryKey}} = {{if .postgreSql}}$1{{else}}?{{end}}", m.table, {{.lowerStartCamelObject}}RowsWithPlaceHolder)
    _,err:=m.conn.ExecCtx(ctx, query, {{.expressionValues}}){{end}}
	return err
}

```

模板注入对象为：

```go
map[string]any{
    "withCache":             withCache,
    "containsIndexCache":    table.ContainsUniqueCacheKey,
    "upperStartCamelObject": camelTableName,
    "keys":                  strings.Join(keys, "\n"),
    "keyValues":             strings.Join(keyVars, ", "),
    "primaryCacheKey":       table.PrimaryCacheKey.DataKeyExpression,
    "primaryKeyVariable":    table.PrimaryCacheKey.KeyLeft,
    "lowerStartCamelObject": stringx.From(camelTableName).Untitle(),
    "upperStartCamelPrimaryKey": util.EscapeGolangKeyword(
        stringx.From(table.PrimaryKey.Name.ToCamel()).Title(),
    ),
    "originalPrimaryKey": wrapWithRawString(
        table.PrimaryKey.Name.Source(), postgreSql,
    ),
    "expressionValues": strings.Join(
        expressionValues, ", ",
    ),
    "postgreSql": postgreSql,
    "data":       table,
}
```

| 模板变量                       | 类型     | 描述                 |
|----------------------------|--------|--------------------|
| .upperStartCamelObject     | string | 对象名称的首字母大写形式       |
| .containsIndexCache        | bool   | 是否包含索引缓存           |
| .withCache                 | bool   | 是否启用缓存             |
| .upperStartCamelPrimaryKey | string | 主键字段名称的首字母大写形式     |
| .lowerStartCamelObject     | string | 对象名称的首字母小写形式       |
| .lowerStartCamelPrimaryKey | string | 主键字段名称的首字母小写形式     |
| .postgreSql                | bool   | 是否为 PostgreSQL 数据库 |
| .keys                      | string | 键值                 |
| .expressionValues          | string | 表达值                |

#### var.tpl

```go
var (
{{.lowerStartCamelObject}}FieldNames = builder.RawFieldNames(&{{.upperStartCamelObject}}{}{{if .postgreSql}}, true{{end}})
{{.lowerStartCamelObject}}Rows = strings.Join({{.lowerStartCamelObject}}FieldNames, ",")
{{.lowerStartCamelObject}}RowsExpectAutoSet = {{if .postgreSql}}strings.Join(stringx.Remove({{.lowerStartCamelObject}}FieldNames, {{if .autoIncrement}}"{{.originalPrimaryKey}}", {{end}} {{.ignoreColumns}}), ","){{else}}strings.Join(stringx.Remove({{.lowerStartCamelObject}}FieldNames, {{if .autoIncrement}}"{{.originalPrimaryKey}}", {{end}} {{.ignoreColumns}}), ","){{end}}
{{.lowerStartCamelObject}}RowsWithPlaceHolder = {{if .postgreSql}}builder.PostgreSqlJoin(stringx.Remove({{.lowerStartCamelObject}}FieldNames, "{{.originalPrimaryKey}}", {{.ignoreColumns}})){{else}}strings.Join(stringx.Remove({{.lowerStartCamelObject}}FieldNames, "{{.originalPrimaryKey}}", {{.ignoreColumns}}), "=?,") + "=?"{{end}}

{{if .withCache}}{{.cacheKeys}}{{end}}
)

```

模板注入对象为：

```go
map[string]any{
    "lowerStartCamelObject": stringx.From(camel).Untitle(),
    "upperStartCamelObject": camel,
    "cacheKeys":             strings.Join(keys, "\n"),
    "autoIncrement":         table.PrimaryKey.AutoIncrement,
    "originalPrimaryKey":    wrapWithRawString(table.PrimaryKey.Name.Source(), postgreSql),
    "withCache":             withCache,
    "postgreSql":            postgreSql,
    "data":                  table,
    "ignoreColumns": func() string {
        var set = collection.NewSet()
        for _, c := range table.ignoreColumns {
            if postgreSql {
                set.AddStr(fmt.Sprintf(`"%s"`, c))
            } else {
                set.AddStr(fmt.Sprintf("\"`%s`\"", c))
            }
        }
        list := set.KeysStr()
        sort.Strings(list)
        return strings.Join(list, ", ")
    }(),
}
```

| 模板变量                   | 类型     | 描述                 |
|------------------------|--------|--------------------|
| .lowerStartCamelObject | string | 对象名称的首字母小写形式       |
| .upperStartCamelObject | string | 对象名称的首字母大写形式       |
| .postgreSql            | bool   | 是否为 PostgreSQL 数据库 |
| .autoIncrement         | string | 自动增量标识符            |
| .originalPrimaryKey    | string | 原始主键字段名            |
| .ignoreColumns         | string | 忽略的列名列表            |
| .withCache             | bool   | 是否启用缓存             |
| .cacheKeys             | string | 缓存键列表              |

### goctl kube 代码生成模板

模板默认目录 `~/.goctl/${goctl-version}/kube`

#### deployment.tpl

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{.Name}}
  namespace: {{.Namespace}}
  labels:
    app: {{.Name}}
spec:
  replicas: {{.Replicas}}
  revisionHistoryLimit: {{.Revisions}}
  selector:
    matchLabels:
      app: {{.Name}}
  template:
    metadata:
      labels:
        app: {{.Name}}
    spec:{{if .ServiceAccount}}
    serviceAccountName: {{.ServiceAccount}}{{end}}
    containers:
      - name: {{.Name}}
        image: {{.Image}}
        {{if .ImagePullPolicy}}imagePullPolicy: {{.ImagePullPolicy}}
        {{end}}ports:
        - containerPort: {{.Port}}
        readinessProbe:
          tcpSocket:
            port: {{.Port}}
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          tcpSocket:
            port: {{.Port}}
          initialDelaySeconds: 15
          periodSeconds: 20
        resources:
          requests:
            cpu: {{.RequestCpu}}m
            memory: {{.RequestMem}}Mi
          limits:
            cpu: {{.LimitCpu}}m
            memory: {{.LimitMem}}Mi
        volumeMounts:
          - name: timezone
            mountPath: /etc/localtime
    {{if .Secret}}imagePullSecrets:
    - name: {{.Secret}}
    {{end}}volumes:
    - name: timezone
      hostPath:
        path: /usr/share/zoneinfo/Asia/Shanghai

---

apiVersion: v1
kind: Service
metadata:
  name: {{.Name}}-svc
  namespace: {{.Namespace}}
spec:
  ports:
  {{if .UseNodePort}}- nodePort: {{.NodePort}}
  port: {{.Port}}
  protocol: TCP
  targetPort: {{.TargetPort}}
  type:
    NodePort{{else}}- port: {{.Port}}
      targetPort: {{.TargetPort}}{{end}}
  selector:
    app: {{.Name}}

---

apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: {{.Name}}-hpa-c
  namespace: {{.Namespace}}
  labels:
    app: {{.Name}}-hpa-c
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{.Name}}
  minReplicas: {{.MinReplicas}}
  maxReplicas: {{.MaxReplicas}}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 80

---

apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: {{.Name}}-hpa-m
  namespace: {{.Namespace}}
  labels:
    app: {{.Name}}-hpa-m
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{.Name}}
  minReplicas: {{.MinReplicas}}
  maxReplicas: {{.MaxReplicas}}
  metrics:
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

```

模板注入对象为 `Deployment`

```go
Deployment{
    Name:            varStringName,
    Namespace:       varStringNamespace,
    Image:           varStringImage,
    Secret:          varStringSecret,
    Replicas:        varIntReplicas,
    Revisions:       varIntRevisions,
    Port:            varIntPort,
    TargetPort:      varIntTargetPort,
    NodePort:        nodePort,
    UseNodePort:     nodePort > 0,
    RequestCpu:      varIntRequestCpu,
    RequestMem:      varIntRequestMem,
    LimitCpu:        varIntLimitCpu,
    LimitMem:        varIntLimitMem,
    MinReplicas:     varIntMinReplicas,
    MaxReplicas:     varIntMaxReplicas,
    ServiceAccount:  varStringServiceAccount,
    ImagePullPolicy: varStringImagePullPolicy,
}
```

| pipeline变量       | 类型     | 说明                                   |
|------------------|--------|--------------------------------------|
| .Name            | string | 名称                                   |
| .Namespace       | string | 命名空间                                 |
| .Replicas        | int    | 副本数量                                 |
| .Revisions       | int    | 修订历史限制                               |
| .ServiceAccount  | string | 服务账户名称 (可选)                          |
| .Image           | string | 容器镜像                                 |
| .ImagePullPolicy | string | 镜像拉取策略 (可选)                          |
| .Port            | int    | 容器端口                                 |
| .RequestCpu      | int    | CPU 请求 (单位: millicores)              |
| .RequestMem      | int    | 内存请求 (单位: MiB)                       |
| .LimitCpu        | int    | CPU 限制 (单位: millicores)              |
| .LimitMem        | int    | 内存限制 (单位: MiB)                       |
| .Secret          | string | 镜像拉取密钥 (可选)                          |
| .UseNodePort     | bool   | 使用 NodePort (布尔值)                    |
| .NodePort        | int    | NodePort 端口 (当 UseNodePort 为 true 时) |
| .TargetPort      | int    | 目标端口                                 |
| .MinReplicas     | int    | 最小副本数                                |
| .MaxReplicas     | int    | 最大副本数                                |

### goctl docker 生成模板

模板默认目录 `~/.goctl/${goctl-version}/docker`

#### docker.tpl

```shell
FROM golang:{{.Version}}alpine AS builder

LABEL stage=gobuilder

ENV CGO_ENABLED 0
{{if .Chinese}}ENV GOPROXY https://goproxy.cn,direct
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
{{end}}{{if .HasTimezone}}
RUN apk update --no-cache && apk add --no-cache tzdata
{{end}}
WORKDIR /build

ADD go.mod .
ADD go.sum .
RUN go mod download
COPY . .
{{if .Argument}}COPY {{.GoRelPath}}/etc /app/etc
{{end}}RUN go build -ldflags="-s -w" -o /app/{{.ExeFile}} {{.GoMainFrom}}


FROM {{.BaseImage}}

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt
{{if .HasTimezone}}COPY --from=builder /usr/share/zoneinfo/{{.Timezone}} /usr/share/zoneinfo/{{.Timezone}}
ENV TZ {{.Timezone}}
{{end}}
WORKDIR /app
COPY --from=builder /app/{{.ExeFile}} /app/{{.ExeFile}}{{if .Argument}}
COPY --from=builder /app/etc /app/etc{{end}}
{{if .HasPort}}
EXPOSE {{.Port}}
{{end}}
CMD ["./{{.ExeFile}}"{{.Argument}}]

```

模板注入对象为 `Docker`

```go
Docker{
    Chinese:     env.InChina(),
    GoMainFrom:  path.Join(projPath, goFile),
    GoRelPath:   projPath,
    GoFile:      goFile,
    ExeFile:     exeName,
    BaseImage:   base,
    HasPort:     port > 0,
    Port:        port,
    Argument:    builder.String(),
    Version:     version,
    HasTimezone: len(timezone) > 0,
    Timezone:    timezone,
}
```

| pipeline变量   | 类型     | 说明          |
|--------------|--------|-------------|
| .Version     | string | Golang 版本   |
| .Chinese     | bool   | 是否使用中国时区    |
| .HasTimezone | bool   | 是否需要时区设置    |
| .Argument    | string | 命令行参数 (可选)  |
| .GoRelPath   | string | Go 项目相对路径   |
| .ExeFile     | string | 可执行文件名称     |
| .GoMainFrom  | string | Go 主程序源文件路径 |
| .BaseImage   | string | 基础镜像        |
| .Timezone    | string | 时区          |
| .HasPort     | bool   | 是否需要暴露端口    |

### rpc 代码生成模板

模板默认目录 `~/.goctl/${goctl-version}/rpc`

#### call.tpl

```go
{{.head}}

package {{.filePackage}}

import (
	"context"

	{{.pbPackage}}
	{{if ne .pbPackage .protoGoPackage}}{{.protoGoPackage}}{{end}}

	"github.com/zeromicro/go-zero/zrpc"
	"google.golang.org/grpc"
)

type (
	{{.alias}}

	{{.serviceName}} interface {
		{{.interface}}
	}

	default{{.serviceName}} struct {
		cli zrpc.Client
	}
)

func New{{.serviceName}}(cli zrpc.Client) {{.serviceName}} {
	return &default{{.serviceName}}{
		cli: cli,
	}
}

{{.functions}}

```

模板注入对象 `map[string]any`

```go
map[string]any{
    "name":           callFilename,
    "alias":          strings.Join(aliasKeys, pathx.NL),
    "head":           head,
    "filePackage":    childDir,
    "pbPackage":      pbPackage,
    "protoGoPackage": protoGoPackage,
    "serviceName":    serviceName,
    "functions":      strings.Join(functions, pathx.NL),
    "interface":      strings.Join(iFunctions, pathx.NL),
}
```

| pipeline变量      | 类型     | 说明                             |
|-----------------|--------|--------------------------------|
| .head           | string | 头部信息                           |
| .filePackage    | string | 文件包名                           |
| .pbPackage      | string | Protocol Buffers 包导入路径         |
| .protoGoPackage | string | Protocol Buffers Go 包导入路径 (可选) |
| .alias          | string | 类型别名声明                         |
| .serviceName    | string | 服务名称                           |
| .interface      | string | 接口定义                           |
| .functions      | string | 函数实现                           |

#### config.tpl

```go
package config

import "github.com/zeromicro/go-zero/zrpc"

type Config struct {
	zrpc.RpcServerConf
}

```

无变量注入

#### etc.tpl

```yaml
Name: {{.serviceName}}.rpc
ListenOn: 0.0.0.0:8080
Etcd:
  Hosts:
    - 127.0.0.1:2379
  Key: {{.serviceName}}.rpc

```

模板注入对象为：

```go
map[string]any{
    "serviceName": strings.ToLower(stringx.From(ctx.GetServiceName().Source()).ToCamel()),
}
```

| pipeline变量   | 类型     | 描述      |
|--------------|--------|---------|
| .serviceName | string | 服务名称的变量 |

#### logic.tpl

```go
package {{.packageName}}

import (
	"context"

	{{.imports}}

	"github.com/zeromicro/go-zero/core/logx"
)

type {{.logicName}} struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func New{{.logicName}}(ctx context.Context,svcCtx *svc.ServiceContext) *{{.logicName}} {
	return &{{.logicName}}{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}
{{.functions}}

```

模板注入对象为：

- 不支持分组情况下

```go
map[string]any{
    "logicName":   fmt.Sprintf("%sLogic", stringx.From(rpc.Name).ToCamel()),
    "functions":   functions,
    "packageName": "logic",
    "imports":     strings.Join(imports.KeysStr(), pathx.NL),
}
```

- 支持分组情况下

```go
map[string]any{
    "logicName":   logicName,
    "functions":   functions,
    "packageName": packageName,
    "imports":     strings.Join(imports.KeysStr(), pathx.NL),
} 
```

| pipeline变量   | 类型     | 描述      |
|--------------|--------|---------|
| .packageName | string | 包名      |
| .imports     | string | 导入的包列表  |
| .logicName   | string | 逻辑结构体名称 |
| .functions   | string | 函数定义部分  |

#### main.tpl

```go
package main

import (
	"flag"
	"fmt"

	{{.imports}}

	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/service"
	"github.com/zeromicro/go-zero/zrpc"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

var configFile = flag.String("f", "etc/{{.serviceName}}.yaml", "the config file")

func main() {
	flag.Parse()

	var c config.Config
	conf.MustLoad(*configFile, &c)
	ctx := svc.NewServiceContext(c)

	s := zrpc.MustNewServer(c.RpcServerConf, func(grpcServer *grpc.Server) {
{{range .serviceNames}}       {{.Pkg}}.Register{{.GRPCService}}Server(grpcServer, {{.ServerPkg}}.New{{.Service}}Server(ctx))
{{end}}
		if c.Mode == service.DevMode || c.Mode == service.TestMode {
			reflection.Register(grpcServer)
		}
	})
	defer s.Stop()

	fmt.Printf("Starting rpc server at %s...\n", c.ListenOn)
	s.Start()
}

```

模板注入对象为：

```go
map[string]any{
    "serviceName":  etcFileName,
    "imports":      strings.Join(imports, pathx.NL),
    "pkg":          proto.PbPackage,
    "serviceNames": serviceNames,
}
```

| pipeline变量                | 类型     | 描述         |
|---------------------------|--------|------------|
| .imports                  | string | 导入的包列表     |
| .serviceName              | string | 服务名称       |
| .serviceNames             | 列表     | 包含以下子变量的列表 |
| .serviceNames.Pkg         | string | 服务包名       |
| .serviceNames.GRPCService | string | gRPC 服务名称  |
| .serviceNames.ServerPkg   | string | gRPC 服务包名  |
| .serviceNames.Service     | string | 服务名称       |

#### rpc.tpl

```go
{{.head}}

package server

import (
	{{if .notStream}}"context"{{end}}

	{{.imports}}
)

type {{.server}}Server struct {
	svcCtx *svc.ServiceContext
	{{.unimplementedServer}}
}

func New{{.server}}Server(svcCtx *svc.ServiceContext) *{{.server}}Server {
	return &{{.server}}Server{
		svcCtx: svcCtx,
	}
}

{{.funcs}}

```

模板注入对象为：

- 不支持分组情况

```go
map[string]any{
    "head": head,
    "unimplementedServer": fmt.Sprintf("%s.Unimplemented%sServer", proto.PbPackage,
        parser.CamelCase(service.Name)),
    "server":    stringx.From(service.Name).ToCamel(),
    "imports":   strings.Join(imports.KeysStr(), pathx.NL),
    "funcs":     strings.Join(funcList, pathx.NL),
    "notStream": notStream,
}
```

- 支持分组情况

```go
map[string]any{
    "head": head,
    "unimplementedServer": fmt.Sprintf("%s.Unimplemented%sServer", proto.PbPackage,
        parser.CamelCase(service.Name)),
    "server":    stringx.From(service.Name).ToCamel(),
    "imports":   strings.Join(imports.KeysStr(), pathx.NL),
    "funcs":     strings.Join(funcList, pathx.NL),
    "notStream": notStream,
}
```

| pipeline变量             | 类型  | 描述                     |
|------------------------|-----|------------------------|
| `.head`                | 文本  | 包级别注释或其他代码             |
| `.notStream`           | 布尔  | 根据条件是否引入 `context` 包   |
| `.imports`             | 文本  | 其他导入语句                 |
| `.server`              | 文本  | 定义服务名称的占位符             |
| `.unimplementedServer` | 文本  | 定义未实现服务器的占位符           |
| `.funcs`               | 文本  | 生成特定于服务器类型的其他函数/方法的占位符 |

#### svc.tpl

```go
package svc

import {{.imports}}

type ServiceContext struct {
	Config config.Config
}

func NewServiceContext(c config.Config) *ServiceContext {
	return &ServiceContext{
		Config:c,
	}
}

```

模板注入对象为：

```go
map[string]any{
    "imports": fmt.Sprintf(`"%v"`, ctx.GetConfig().Package),
}
```

| pipeline变量 | 类型  | 描述     |
|------------|-----|--------|
| `.imports` | 文本  | 其他导入语句 |

## 参考文献

- <a href="/docs/reference/cli-guide/template" target="_blank">《goctl template》</a>
- <a href="https://golang.org/pkg/text/template/" target="_blank">《text/template》</a>
