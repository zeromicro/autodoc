---
title: 설정 센터
description: go-zero의 설정 센터에 대해 설명합니다.
sidebar:
  order: 5
---


## 기본 Usage

```go
package main

import (
	"github.com/zeromicro/go-zero/core/configcenter"
	"github.com/zeromicro/go-zero/core/configcenter/subscriber"
)

type AppConfig struct {
	Name string `json:"name"`
}

func main() {
	// 생성합니다
	ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
		Hosts: []string{"localhost:2379"},
		Key:   "app-config",
	})

	// 생성합니다
	cc := configcenter.MustNewConfigCenter[AppConfig](configcenter.Config{
		Type: "json", // supported: json, yaml, toml
	}, ss)

	// 가져옵니다
	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}
	println(v.Name)

	// Listen 예시입니다
	cc.AddListener(func() {
		v, err := cc.GetConfig()
		if err != nil {
			panic(err)
		}
		println("config changed:", v.Name)
	})

	select {} // 예시입니다
}
```

## 사용하여 String 타입


```go
func main() {
	ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
		Hosts: []string{"localhost:2379"},
		Key:   "app-config",
	})

	// 사용합니다
	cc := configcenter.MustNewConfigCenter[string](configcenter.Config{
		Type: "json",
	}, ss)

	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}

	// Parse 예시입니다
	_ = v
}
```

## Struct 검증


```go
type AppConfig struct {
	Name string `json:",optional"`
	Age  int    `json:",default=20"`
}
```

참고: [매개변수 Rules](../../reference/api-dsl/parameter.md) 위한 전체 list 의 supported tags.

## Custom Subscriber


```go
package main

import (
	"sync"

	"github.com/zeromicro/go-zero/core/configcenter"
)

type AppConfig struct {
	Name string `json:"name"`
}

// CustomSubscriber, Subscriber 예시입니다
type CustomSubscriber struct {
	listeners []func()
	lock      sync.Mutex
}

func (s *CustomSubscriber) AddListener(listener func()) error {
	s.lock.Lock()
	s.listeners = append(s.listeners, listener)
	s.lock.Unlock()
	return nil
}

func (s *CustomSubscriber) Value() (string, error) {
	// 반환값을 설명합니다
	return `{"name": "my-app"}`, nil
}

func main() {
	sub := &CustomSubscriber{}

	cc := configcenter.MustNewConfigCenter[AppConfig](configcenter.Config{
		Type: "json",
	}, sub)

	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}
	println(v.Name)
}
```

## Key 기능

| Feature | 설명 |
|---|---|
| Built-in snapshot |해당 항목의 동작과 사용법을 설명합니다. |
| Pluggable subscriber |해당 항목의 동작과 사용법을 설명합니다. |
| 자동 검증 |해당 항목의 동작과 사용법을 설명합니다. |
| Change notification |해당 항목의 동작과 사용법을 설명합니다. |
| Type-safe generics | 사용합니다 Go generics (`ConfigCenter[T]`) 위한 compile-time 타입 safety |
