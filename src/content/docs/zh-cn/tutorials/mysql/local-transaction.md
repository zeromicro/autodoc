---
title: 本地事务
description: 在 go-zero sqlx 中使用本地事务。
sidebar:
  order: 6

---


## 概述

sqlx.SqlConn 提供了基础的事务机制，简单实例：

```go
    var conn sqlx.SqlConn
	err := conn.TransactCtx(context.Background(), func(ctx context.Context, session sqlx.Session) error {
		r, err := session.ExecCtx(ctx, "insert into user (id, name) values (?, ?)", 1, "test")
		if err != nil {
			return err
		}
		r ,err =session.ExecCtx(ctx, "insert into user (id, name) values (?, ?)", 2, "test")
		if err != nil {
			return err
		}
	})
```
