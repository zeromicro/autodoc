---
title: API DSL Reference
description: Reference for the go-zero .api DSL — parameters, types, route groups, middleware, JWT, and more.
sidebar:
  order: 5

---

## Overview

The `.api` DSL is go-zero's domain-specific language for describing HTTP APIs. This section covers every feature of the DSL.

## Contents

- [Route Rules](route-rule.md) — Define URL patterns, methods, and handlers
- [Route Groups](route-group.md) — Organize routes with shared settings
- [Route Prefix](route-prefix.md) — Add a URL prefix to a group
- [Parameters](parameter.md) — Request and response field types and tags
- [Types](type.md) — Define shared request/response structs
- [JWT Authentication](jwt.md) — Protect routes with JWT
- [Middleware](middleware.md) — Apply pre/post-processing to routes
- [Request Signing](signature.md) — HMAC signature verification
- [Import](import.md) — Split `.api` files with imports
- [SSE Routes](route-sse.md) — Server-Sent Events endpoints
- [FAQ](faq.md) — Common questions and answers
