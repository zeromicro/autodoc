---
title: Project Structure
description: Standard folder layout and responsibilities in a generated go-zero project.
sidebar:
  order: 5
---

# Project Structure

```text
greet/
├── etc/                 # Config files
├── internal/
│   ├── config/          # Typed config structures
│   ├── handler/         # Request binding and routing
│   ├── logic/           # Business logic implementation
│   ├── svc/             # Dependency injection context
│   └── types/           # Request/response models
└── greet.go             # Service entrypoint
```

## Recommended Practices

- Keep shared dependencies in `svc.ServiceContext`
- Keep handlers thin and move business flow into logic modules
- Keep config values explicit and deployment-friendly
