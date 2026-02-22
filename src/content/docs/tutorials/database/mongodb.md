---
title: MongoDB
description: Integrate MongoDB into go-zero services using the official Go driver.
sidebar:
  order: 3
---

# MongoDB

go-zero wraps the official `mongo-driver` with connection management and instrumentation.

## Configuration

```yaml
Mongo:
  Uri: "mongodb://127.0.0.1:27017"
  Database: myapp
```

## Initialize

```go title="internal/svc/servicecontext.go"
import "github.com/zeromicro/go-zero/core/stores/mongo"

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:     c,
        ArticleMod: mongo.MustNewModel(c.Mongo.Uri, c.Mongo.Database, "articles"),
    }
}
```

## Insert

```go
article := &Article{Title: "Hello go-zero", Content: "..."}
result, err := l.svcCtx.ArticleMod.InsertOne(l.ctx, article)
```

## Query

```go
var articles []Article
err := l.svcCtx.ArticleMod.FindAll(l.ctx, bson.M{"published": true}, &articles)
```

## Update

```go
filter := bson.M{"_id": id}
update := bson.M{"$set": bson.M{"title": "Updated"}}
err := l.svcCtx.ArticleMod.UpdateOne(l.ctx, filter, update)
```
