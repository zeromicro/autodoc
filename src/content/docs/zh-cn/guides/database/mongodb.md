---
title: MongoDB
description: 在 go-zero 项目中使用 MongoDB。
sidebar:
  order: 10
---


go-zero 封装了官方 `mongo-driver`，提供连接管理与可观测性支持。

## 配置

```yaml title="etc/app.yaml"
Mongo:
  Uri: "mongodb://127.0.0.1:27017"
  Database: myapp
```

在 Config 结构体中声明：

```go title="internal/config/config.go"
type Config struct {
    rest.RestConf
    Mongo struct {
        Uri      string
        Database string
    }
}
```

## 初始化

```go title="internal/svc/servicecontext.go"
import "github.com/zeromicro/go-zero/core/stores/mongo"

func NewServiceContext(c config.Config) *ServiceContext {
    return &ServiceContext{
        Config:     c,
        ArticleMod: mongo.MustNewModel(c.Mongo.Uri, c.Mongo.Database, "articles"),
    }
}
```

## 插入

```go
article := &Article{Title: "Hello go-zero", Content: "...", Published: false}
result, err := l.svcCtx.ArticleMod.InsertOne(l.ctx, article)
if err != nil {
    return nil, err
}
// result.InsertedID 为新文档的 _id
```

## 查询单条

```go
var article Article
err := l.svcCtx.ArticleMod.FindOne(l.ctx, bson.M{"_id": id}, &article)
if errors.Is(err, mongo.ErrNotFound) {
    return nil, errorx.ErrNotFound
}
```

## 查询多条

```go
var articles []Article
err := l.svcCtx.ArticleMod.FindAll(l.ctx, bson.M{"published": true}, &articles)
```

限制条数与排序：

```go
opts := options.Find().SetLimit(20).SetSort(bson.D{{Key: "createdAt", Value: -1}})
err := l.svcCtx.ArticleMod.FindAllWithOptions(l.ctx, bson.M{}, &articles, opts)
```

## 更新

使用 `$set` 更新指定字段：

```go
filter := bson.M{"_id": id}
update := bson.M{"$set": bson.M{"title": "已更新", "updatedAt": time.Now()}}
result, err := l.svcCtx.ArticleMod.UpdateOne(l.ctx, filter, update)
// result.MatchedCount / result.ModifiedCount
```

Upsert（不存在则插入）：

```go
opts := options.Update().SetUpsert(true)
_, err = l.svcCtx.ArticleMod.UpdateOneWithOptions(l.ctx, filter, update, opts)
```

## 删除

```go
// 删除单条
result, err := l.svcCtx.ArticleMod.DeleteOne(l.ctx, bson.M{"_id": id})

// 删除多条
result, err := l.svcCtx.ArticleMod.DeleteMany(l.ctx, bson.M{"published": false})
// result.DeletedCount
```

## 计数

```go
count, err := l.svcCtx.ArticleMod.CountDocuments(l.ctx, bson.M{"published": true})
```

## 聚合

```go
pipeline := mongo.Pipeline{
    {{Key: "$match", Value: bson.M{"published": true}}},
    {{Key: "$group", Value: bson.M{
        "_id":   "$authorId",
        "total": bson.M{"$sum": 1},
    }}},
    {{Key: "$sort", Value: bson.M{"total": -1}}},
    {{Key: "$limit", Value: 10}},
}

var results []bson.M
err := l.svcCtx.ArticleMod.Aggregate(l.ctx, pipeline, &results)
```

## 仓储模式

将 model 封装为带类型的仓储，使 logic 代码更清晰：

```go title="internal/model/articlemodel.go"
type ArticleModel interface {
    Insert(ctx context.Context, article *Article) error
    FindById(ctx context.Context, id primitive.ObjectID) (*Article, error)
    ListPublished(ctx context.Context, limit int64) ([]Article, error)
    Delete(ctx context.Context, id primitive.ObjectID) error
}

type defaultArticleModel struct {
    mod *mongo.Model
}

func NewArticleModel(uri, db string) ArticleModel {
    return &defaultArticleModel{mod: mongo.MustNewModel(uri, db, "articles")}
}

func (m *defaultArticleModel) FindById(ctx context.Context, id primitive.ObjectID) (*Article, error) {
    var a Article
    if err := m.mod.FindOne(ctx, bson.M{"_id": id}, &a); err != nil {
        return nil, err
    }
    return &a, nil
}
```
