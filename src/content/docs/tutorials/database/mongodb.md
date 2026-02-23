---
title: MongoDB
description: Integrate MongoDB into go-zero services using the official Go driver.
sidebar:
  order: 3
---

# MongoDB

go-zero wraps the official `mongo-driver` with connection management and instrumentation.

## Configuration

```yaml title="etc/app.yaml"
Mongo:
  Uri: "mongodb://127.0.0.1:27017"
  Database: myapp
```

Add the struct to your config:

```go title="internal/config/config.go"
type Config struct {
    rest.RestConf
    Mongo struct {
        Uri      string
        Database string
    }
}
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
article := &Article{Title: "Hello go-zero", Content: "...", Published: false}
result, err := l.svcCtx.ArticleMod.InsertOne(l.ctx, article)
if err != nil {
    return nil, err
}
// result.InsertedID contains the new document's _id
```

## Find One

```go
var article Article
err := l.svcCtx.ArticleMod.FindOne(l.ctx, bson.M{"_id": id}, &article)
if errors.Is(err, mongo.ErrNotFound) {
    return nil, errorx.ErrNotFound
}
```

## Find Many

```go
var articles []Article
err := l.svcCtx.ArticleMod.FindAll(l.ctx, bson.M{"published": true}, &articles)
```

Limit and sort:

```go
opts := options.Find().SetLimit(20).SetSort(bson.D{{Key: "createdAt", Value: -1}})
err := l.svcCtx.ArticleMod.FindAllWithOptions(l.ctx, bson.M{}, &articles, opts)
```

## Update

Replace specific fields with `$set`:

```go
filter := bson.M{"_id": id}
update := bson.M{"$set": bson.M{"title": "Updated", "updatedAt": time.Now()}}
result, err := l.svcCtx.ArticleMod.UpdateOne(l.ctx, filter, update)
// result.MatchedCount / result.ModifiedCount
```

Upsert (insert if not found):

```go
opts := options.Update().SetUpsert(true)
_, err = l.svcCtx.ArticleMod.UpdateOneWithOptions(l.ctx, filter, update, opts)
```

## Delete

```go
// Delete one document
result, err := l.svcCtx.ArticleMod.DeleteOne(l.ctx, bson.M{"_id": id})

// Delete multiple documents
result, err := l.svcCtx.ArticleMod.DeleteMany(l.ctx, bson.M{"published": false})
// result.DeletedCount
```

## Count

```go
count, err := l.svcCtx.ArticleMod.CountDocuments(l.ctx, bson.M{"published": true})
```

## Aggregation

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

## Repository Pattern

Wrap the model in a typed repository for cleaner logic code:

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
