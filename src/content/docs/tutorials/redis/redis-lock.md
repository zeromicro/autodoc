---
title: Redis Distributed Lock
description: Implement distributed locks with Redis in go-zero.
sidebar:
  order: 4

---

## Overview

This section mainly describes the use of redis to create a distribution lock.

## Preparing

1. <a href="/docs/tasks" target="_blank">Complete golang installation</a>
2. Start redis service
3. <a href="/docs/tasks/redis/redis-conn" target="_blank">Redis created</a>

## Description

1. Random version number, prevent outdated releases.
2. Can reenter, automatic renewal.

## Methodological description

1. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/redislock.go#L46" target="_blank">NewRedisLock</a>

    ```go
    Function signature: 
        NewRedisLock func(store *Redis, key string) *RedisLock 
    description: 
        1. Deleting a single record will also clear the key cache
        Default expiration time of 1500 ms
    in participation:
        1. store: redis instance
        2. key: key
    return value:
        1. *RedLock: redis locker instance
    ```

2. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/redislock.go#L104" target="_blank">SetExpire</a>

    ```go
    Function signature: 
        SetExpire func(seconds int)
    description: 
        1. Set expiration time
    entry:
        1. seconds: expiration time, in seconds
    ```

3. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/redislock.go#L55" target="_blank">Acquire</a>

    ```go
    Function signature: 
        Acquire func() (bool, error)
    description: 
        1. Get lock
    return value:
        1. bool: get lock
        2. error: operator error
    ```

4. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/redislock.go#L60" target="_blank">AcquireCtx</a>

    ```go
    Function signature: 
    AcquireCtx func(ctx context.Context) (bool, error)
    description: 
        1. Get lock
    Input:
        1. ctx: context
    Return value:
        1. bool: Whether to get lock
        2. error: operator error
    ```

5. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/redislock.go#L83" target="_blank">Release</a>

    ```go
    Function signature: 
    Release func() (bool, error)
    description: 
        1. Get lock
    return value:
        1. bool: get lock
        2. error: operator error
    ```

6. <a href="https://github.com/zeromicro/go-zero/blob/master/core/stores/redis/redislock.go#L89" target="_blank">ReleaseCtx</a>

```go
Function signature: 
    ReleaseCtx function (ctx context.Context) (bool, error)
description: 
    1. Release Lock
Input:
    1. ctx: context
Return value:
    1. bool: Is locked released actively
    . error: operator
```

## Use demo

```go
{
    conf := RedisConf{
        Host: "127.0.0.1:55000",
        Type: "node",
        Pass: "123456",
        Tls:  false,
    }

    rds := MustNewRedis(conf)

    lock := NewRedisLock(rds, "test")

    lock.SetExpire(10)

    acquire, err := lock.Acquire()

    switch {
    case err != nil:
        // deal err
    case acquire:
        defer lock.Release() 
        // Add code here

    case !acquire:
        
    }
}
```
