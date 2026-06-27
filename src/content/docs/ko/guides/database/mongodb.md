---
title: MongoDB
description: go-zero의 MongoDB에 대해 설명합니다.
sidebar:
  order: 3
---


## 설정

```yaml title="etc/app.yaml"
Mongo:
  Uri: "mongodb://127.0.0.1:27017"
  Database: myapp
```

추가 struct 로 your 설정:

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
// result.InsertedID에는 새 문서의 _id가 들어 있습니다
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

제한과 sort:

```go
opts := options.Find().SetLimit(20).SetSort(bson.D{{Key: "createdAt", Value: -1}})
err := l.svcCtx.ArticleMod.FindAllWithOptions(l.ctx, bson.M{}, &articles, opts)
```

## 업데이트

Replace 특정 필드 사용하여 `$set`:

```go
filter := bson.M{"_id": id}
update := bson.M{"$set": bson.M{"title": "Updated", "updatedAt": time.Now()}}
result, err := l.svcCtx.ArticleMod.UpdateOne(l.ctx, filter, update)
// result.MatchedCount / result.ModifiedCount 값을 확인합니다
```

Upsert (insert 경우 아님 found):

```go
opts := options.Update().SetUpsert(true)
_, err = l.svcCtx.ArticleMod.UpdateOneWithOptions(l.ctx, filter, update, opts)
```

## Delete

```go
// 삭제합니다
result, err := l.svcCtx.ArticleMod.DeleteOne(l.ctx, bson.M{"_id": id})

// 여러 문서를 삭제합니다
result, err := l.svcCtx.ArticleMod.DeleteMany(l.ctx, bson.M{"published": false})
// DeletedCount 예시입니다
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

Wrap 모델 에서 타입이 지정된 repository 위한 cleaner 로직 code:

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
