---
title: Design Principles
description: Core engineering principles behind go-zero project design and scalability.
sidebar:
  order: 4
---

# Design Principles

## Convention Over Configuration

goctl scaffolding and standard folders reduce team-level divergence and improve collaboration efficiency.

## Stability by Default

Resilience mechanisms are built in as framework capabilities, not optional add-ons.

## Clear Responsibility Boundaries

Handlers, logic modules, service context, and models are intentionally separated to reduce coupling.

## Observability-first Execution

Production-grade systems need logs, metrics, and traces from day one, not after incidents happen.

![resilience design](../../../assets/resilience.svg)
