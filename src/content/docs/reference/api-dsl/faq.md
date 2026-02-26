---
title: API FAQ
description: Frequently asked questions about the go-zero .api DSL.
sidebar:
  order: 12

---


## 1. How do I experience new API features?

API new features are currently in testing. To try them, install the latest goctl version and enable `GOCTL_EXPERIMENTAL`:

```bash
$ goctl env -w GOCTL_EXPERIMENTAL=on
```

New features are supported starting from version 1.5.1, including:

1. Data type supports array type
1. Support Tag Ignore
1. Pure numbers are supported by routes, e.g. `/abc/123/`
1. api resolver migrated from antlr4 to goparser

When enabling new features in 1.5.1, there are some breaking changes to be aware of:

1. syntax header is required

For data type usage examples, see <a href="/reference/api-dsl/type#示例" target="_blank">Type Declarations • Examples</a>.

## 2. goctl api generated error： multiple service names defined...

Declares multiple services are not supported in api syntax files such as writing below as unsupported：

```go {1,6}
service foo {
    @handler fooPing
    get /foo/ping
}

service bar {
    @handler barPing
    get /bar/ping
}
```

The highlighted sections `foo` and `bar` show an unsupported pattern; only a single service name is allowed:

```go {1,6}
service foo {
    @handler fooPing
    get /foo/ping
}

service foo {
    @handler barPing
    get /bar/ping
}
```

## 3. goctl api does not support `any` type

Generic and weak types are not supported in api syntax.
