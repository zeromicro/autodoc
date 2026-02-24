---
title: Local Transactions
description: Use local transactions with go-zero sqlx.
sidebar:
  order: 6

---


## Overview

sqlx.SqlConn provides the basic service mechanism, simple instance：

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
