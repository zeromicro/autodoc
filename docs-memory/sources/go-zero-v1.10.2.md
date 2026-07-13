---
title: go-zero v1.10.2 release
source_type: release
source_url: https://github.com/zeromicro/go-zero/releases/tag/v1.10.2
captured_at: 2026-07-13
related_docs:
  - src/content/docs/reference/releases/v1.10.2.md
  - src/content/docs/zh-cn/reference/releases/v1.10.2.md
  - src/content/docs/ko/reference/releases/v1.10.2.md
status: ingested
---

## Key Facts

- Release: v1.10.2
- Published: 2026-05-31
- Previous tag: v1.10.1
- Compare: https://github.com/zeromicro/go-zero/compare/v1.10.1...v1.10.2

## Upstream Release Notes

### New Features

#### mcp — Opt-in HTTP request metadata bridge for tool handlers ([#5550](https://github.com/zeromicro/go-zero/pull/5550))

Added `WithRequestMetadataExtractor` option to the MCP server. When set, HTTP request metadata (headers, query parameters, path variables) is captured and injected into each handler's `context.Context`. Handlers retrieve it via the provided context helpers:

```go
server := mcp.NewMcpServer(conf, mcp.WithRequestMetadataExtractor(mcp.DefaultRequestMetadataExtractor))

server.AddTool(tool, func(ctx context.Context, req *mcp.ServerRequest) (*mcp.ToolResult, error) {
    tenantID, _ := mcp.HeaderFromContext(ctx, "X-Tenant-ID")
    userID, _   := mcp.QueryFromContext(ctx, "user_id")
    // ...
})
```

Available helpers: `RequestMetadataFromContext`, `HeaderFromContext`, `QueryFromContext`, `PathFromContext`. Fully backward-compatible — existing `NewMcpServer(c)` calls are unaffected.

### Bug Fixes

#### `discov` — Go 1.26 etcd URI compatibility ([#5548](https://github.com/zeromicro/go-zero/pull/5548))

Go 1.26 enforces strict RFC 3986 URI parsing and rejects comma-separated hosts in the URI authority component. `BuildDiscovTarget` was producing URIs in the form `etcd://host1:2379,host2:2379/key`, which broke all gRPC services using etcd service discovery with multiple endpoints on Go 1.26+.

The etcd target URL format has been updated to place hosts in the path and the etcd key in a query parameter:

```
# Before (breaks Go 1.26):
etcd://host1:2379,host2:2379/my-service-key

# After (RFC 3986 compliant, works on all Go versions):
etcd:///host1:2379,host2:2379?key=my-service-key
```

#### `discov` — Unbounded memory growth on duplicate etcd PUT events ([#5580](https://github.com/zeromicro/go-zero/pull/5580))

Fixed two related bugs in discov that caused memory to grow without bound in long-running zRPC services:

- **Redundant `OnAdd` calls**: `handleWatchEvents` called `OnAdd` on every etcd `PUT` event regardless of whether the value changed (e.g. lease refreshes, watch reconnects). Duplicate PUTs are now skipped; value changes fire `OnDelete(old)` followed by `OnAdd(new)` to keep listeners consistent.
- **Unbounded slice growth in `addKv`**: Keys were appended to the internal `container.values` slice unconditionally, causing a single etcd key to accumulate thousands of duplicates over time. `addKv` now returns early for exact duplicates, and cleans up stale entries when a key moves to a new server address.

### New Contributors

- [@caltechustc](https://github.com/caltechustc) made their first contribution in [#5596](https://github.com/zeromicro/go-zero/pull/5596)

**Full Changelog**: https://github.com/zeromicro/go-zero/compare/v1.10.1...v1.10.2

## Changed Files

- modified: `.github/workflows/go.yml`
- modified: `core/discov/internal/registry.go`
- modified: `core/discov/internal/registry_test.go`
- modified: `core/discov/subscriber.go`
- modified: `core/discov/subscriber_test.go`
- modified: `core/stores/monc/cachedmodel_test.go`
- modified: `go.mod`
- modified: `go.sum`
- added: `mcp/options.go`
- modified: `mcp/readme.md`
- added: `mcp/request_metadata.go`
- added: `mcp/request_metadata_test.go`
- modified: `mcp/server.go`
- modified: `mcp/server_test.go`
- modified: `tools/goctl/go.mod`
- modified: `tools/goctl/go.sum`
- modified: `tools/goctl/internal/version/version.go`
- modified: `zrpc/resolver/internal/discovbuilder.go`
- modified: `zrpc/resolver/internal/discovbuilder_test.go`
- modified: `zrpc/resolver/internal/targets/endpoints.go`
- modified: `zrpc/resolver/internal/targets/endpoints_test.go`
- modified: `zrpc/resolver/target.go`
- modified: `zrpc/resolver/target_test.go`

## Documentation Impact

Review these changed upstream files and update related guides, components, reference pages, and FAQs when needed.

- `.github/workflows/go.yml`
- `core/discov/internal/registry.go`
- `core/discov/internal/registry_test.go`
- `core/discov/subscriber.go`
- `core/discov/subscriber_test.go`
- `core/stores/monc/cachedmodel_test.go`
- `go.mod`
- `go.sum`
- `mcp/options.go`
- `mcp/readme.md`
- `mcp/request_metadata.go`
- `mcp/request_metadata_test.go`
- `mcp/server.go`
- `mcp/server_test.go`
- `tools/goctl/go.mod`
- `tools/goctl/go.sum`
- `tools/goctl/internal/version/version.go`
- `zrpc/resolver/internal/discovbuilder.go`
- `zrpc/resolver/internal/discovbuilder_test.go`
- `zrpc/resolver/internal/targets/endpoints.go`
- `zrpc/resolver/internal/targets/endpoints_test.go`
- `zrpc/resolver/target.go`
- `zrpc/resolver/target_test.go`
