---
title: Config Center
description: Manage dynamic configuration with go-zero's built-in config center backed by etcd.
sidebar:
  order: 5
---

go-zero provides a built-in config center (`core/configcenter`) that supports dynamic configuration backed by etcd or any custom subscriber. Configuration changes are automatically reflected without restarting the service.

## Basic Usage

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
	// Create an etcd subscriber
	ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
		Hosts: []string{"localhost:2379"},
		Key:   "app-config",
	})

	// Create a config center with typed config
	cc := configcenter.MustNewConfigCenter[AppConfig](configcenter.Config{
		Type: "json", // supported: json, yaml, toml
	}, ss)

	// GetConfig always returns the latest config snapshot
	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}
	println(v.Name)

	// Listen for config changes
	cc.AddListener(func() {
		v, err := cc.GetConfig()
		if err != nil {
			panic(err)
		}
		println("config changed:", v.Name)
	})

	select {} // block forever
}
```

## Using String Type

The config center supports two template types: `struct` and `string`. Use `string` when you need complex types like `[]struct`, `map`, or `[]map`, and parse them yourself:

```go
func main() {
	ss := subscriber.MustNewEtcdSubscriber(subscriber.EtcdConf{
		Hosts: []string{"localhost:2379"},
		Key:   "app-config",
	})

	// Use string type for custom parsing
	cc := configcenter.MustNewConfigCenter[string](configcenter.Config{
		Type: "json",
	}, ss)

	v, err := cc.GetConfig()
	if err != nil {
		panic(err)
	}

	// Parse v with your own logic
	_ = v
}
```

## Struct Validation

When using `struct` as the template type, the config center applies the same validation rules as static configuration. You can use standard go-zero config tags:

```go
type AppConfig struct {
	Name string `json:",optional"`
	Age  int    `json:",default=20"`
}
```

See [Parameter Rules](../../reference/api-dsl/parameter.md) for the full list of supported tags.

## Custom Subscriber

go-zero ships with an etcd subscriber by default. You can implement the `Subscriber` interface to integrate with your own config backend (e.g., Consul, Nacos, Apollo):

```go
package main

import (
	"sync"

	"github.com/zeromicro/go-zero/core/configcenter"
)

type AppConfig struct {
	Name string `json:"name"`
}

// CustomSubscriber implements the configcenter.Subscriber interface
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
	// Return the current config value from your backend
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

## Key Features

| Feature | Description |
|---|---|
| Built-in snapshot | High-performance reads from in-memory snapshot, no remote call on every `GetConfig()` |
| Pluggable subscriber | Default etcd support; implement `Subscriber` interface for custom backends |
| Automatic validation | Struct configs are validated using the same rules as static config |
| Change notification | Register listeners to react to config changes in real time |
| Type-safe generics | Uses Go generics (`ConfigCenter[T]`) for compile-time type safety |
