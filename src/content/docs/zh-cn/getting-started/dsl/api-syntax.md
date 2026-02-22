---
title: API DSL 语法
description: goctl API DSL 的基本语法结构。
sidebar:
  order: 6
---

# API DSL 语法

```txt
type Request {
  Name string `path:"name"`
}

type Response {
  Message string `json:"message"`
}

service greet-api {
  @handler Greet
  get /from/:name(Request) returns (Response)
}
```

常用元素包括：`type`、`service`、路由声明、handler 绑定与请求响应类型定义。
