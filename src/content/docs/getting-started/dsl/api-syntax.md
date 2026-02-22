---
title: API DSL Syntax
description: Learn the core syntax of goctl API DSL.
sidebar:
  order: 6
---

# API DSL Syntax

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

Key elements include `type` definitions, `service` blocks, route declarations, and handler bindings.
