---
title: Glossary
description: Key terminology used in go-zero projects and documentation.
sidebar:
  order: 2
---

# Glossary

## API DSL

A domain-specific language used to define HTTP API contracts that can be compiled into project scaffolding by goctl.

## Proto / RPC DSL

The service contract definition for inter-service communication, typically generated into RPC handlers and clients.

## ServiceContext

The dependency container where shared resources are initialized and reused (database clients, caches, RPC clients, and more).

## Logic Layer

The business layer in go-zero that implements use-case behavior and returns typed response models.

## Middleware

Cross-cutting request handling logic such as authentication, rate limiting, logging, and tracing.
