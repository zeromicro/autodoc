---
title: Architecture
description: Understand the layered architecture and service governance model of go-zero.
sidebar:
  order: 3
---

# Architecture

## Overview

go-zero uses a layered design that separates traffic entry, service governance, domain logic, and infrastructure dependencies.

## Architecture Diagram

![go-zero architecture](../../../assets/architecture.svg)

## Core Layers

### Entry Layer

- API gateway and protocol endpoints
- Request validation and authentication hooks

### Governance Layer

- Service discovery and load balancing
- Timeout, rate limiting, circuit breaking, and load shedding

### Business Layer

- Domain-specific logic orchestration
- Data access and external dependency coordination

### Infrastructure Layer

- Databases, cache, MQ, and registry
- Logging, metrics, and distributed tracing systems

## Next Step

Continue with [Design Principles](./design-principles.md) to understand how these layers are enforced in real projects.
