---
title: API DSL Reference
description: Reference for the go-zero .api DSL — parameters, types, route groups, middleware, JWT, and more.
sidebar:
  order: 5

---

## Overview

The `.api` DSL is go-zero's domain-specific language for describing HTTP APIs. This section covers every feature of the DSL.

## Contents

- [Route Rules](route-rule/) — Define URL patterns, methods, and handlers
- [Route Groups](route-group/) — Organize routes with shared settings
- [Route Prefix](route-prefix/) — Add a URL prefix to a group
- [Parameters](parameter/) — Request and response field types and tags
- [Types](type/) — Define shared request/response structs
- [JWT Authentication](jwt/) — Protect routes with JWT
- [Middleware](middleware/) — Apply pre/post-processing to routes
- [Request Signing](signature/) — HMAC signature verification
- [Import](import/) — Split `.api` files with imports
- [SSE Routes](route-sse/) — Server-Sent Events endpoints
- [FAQ](faq/) — Common questions and answers
