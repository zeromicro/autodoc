---
title: go-zero v1.10.3 release
source_type: release
source_url: https://github.com/zeromicro/go-zero/releases/tag/v1.10.3
captured_at: 2026-08-03
related_docs:
  - src/content/docs/reference/releases/v1.10.3.md
  - src/content/docs/zh-cn/reference/releases/v1.10.3.md
  - src/content/docs/ko/reference/releases/v1.10.3.md
status: ingested
---

## Key Facts

- Release: v1.10.3
- Published: 2026-08-01
- Previous tag: v1.10.2
- Compare: https://github.com/zeromicro/go-zero/compare/v1.10.2...v1.10.3

## Upstream Release Notes

## Highlights

**Core**
- `stringx.FirstN`: returns empty string for negative `n` (#5620)
- `stringx.Substr`: rejects `start > stop` to prevent slice panic (#5616)
- `mapping`: fixed unmarshaling of pointer-to-slice fields (#5662)
- `collection`: optimized queue growth strategy (#5704)

**Redis**
- Added `XGroupSetID`/`XGroupSetIDCtx` to update a consumer group's last-delivered ID (#5637)
- Fixed circuit breaker tripping under high concurrency / with incompatible servers (#5654), plus minor refactor (#5666)

**Docs**
- Added Korean translations (#5579)

**Dependencies**
- `go-redis/v9` 9.19.0 → 9.21.0
- `mongo-driver/v2` 2.6.0 → 2.8.0
- `pelletier/go-toml/v2` 2.3.1 → 2.4.3

## New Contributors
@Vierblatt, @sapirbaruch, @SAY-5, @jeonghyeon-net, @Meppo, @puneetdixit200, @lxffong, @014-code — thank you for your first contributions! 🎉

**Full Changelog**: https://github.com/zeromicro/go-zero/compare/v1.10.2...v1.10.3

## Changed Files

- modified: `.github/workflows/codeql-analysis.yml`
- modified: `.github/workflows/go.yml`
- modified: `.github/workflows/release.yaml`
- modified: `.github/workflows/reviewdog.yml`
- modified: `.github/workflows/version-check.yml`
- modified: `core/collection/fifo.go`
- modified: `core/collection/fifo_test.go`
- modified: `core/logx/readme-cn.md`
- added: `core/logx/readme-ko.md`
- modified: `core/logx/readme.md`
- modified: `core/mapping/jsonunmarshaler_test.go`
- modified: `core/mapping/unmarshaler.go`
- modified: `core/mr/readme-cn.md`
- added: `core/mr/readme-ko.md`
- modified: `core/mr/readme.md`
- modified: `core/stores/redis/breakerhook.go`
- modified: `core/stores/redis/breakerhook_test.go`
- modified: `core/stores/redis/conf.go`
- modified: `core/stores/redis/redis.go`
- modified: `core/stores/redis/redis_test.go`
- modified: `core/stores/redis/redisblockingnode.go`
- modified: `core/stores/redis/redisblockingnode_test.go`
- modified: `core/stores/redis/redisclientmanager.go`
- modified: `core/stores/redis/redisclustermanager.go`
- modified: `core/stores/redis/redisclustermanager_test.go`
- modified: `core/stringx/strings.go`
- modified: `core/stringx/strings_test.go`
- modified: `go.mod`
- modified: `go.sum`
- modified: `mcp/request_metadata_test.go`
- modified: `readme-cn.md`
- added: `readme-ko.md`
- modified: `readme.md`
- added: `tools/goctl/api/parser/inline_tag_test.go`
- modified: `tools/goctl/api/parser/parser.go`
- modified: `tools/goctl/api/spec/fn.go`
- added: `tools/goctl/api/spec/fn_test.go`
- modified: `tools/goctl/api/swagger/const.go`
- modified: `tools/goctl/api/swagger/example/example.api`
- modified: `tools/goctl/api/swagger/example/example.swagger.json`
- modified: `tools/goctl/api/swagger/example/example_cn.api`
- modified: `tools/goctl/api/swagger/example/example_cn.swagger.json`
- modified: `tools/goctl/api/swagger/response.go`
- added: `tools/goctl/api/swagger/response_test.go`
- modified: `tools/goctl/api/swagger/swagger.go`
- modified: `tools/goctl/api/swagger/swagger_test.go`
- modified: `tools/goctl/go.mod`
- modified: `tools/goctl/go.sum`
- modified: `tools/goctl/pkg/parser/api/parser/analyzer.go`
- added: `tools/goctl/pkg/parser/api/parser/inline_tag_test.go`
- modified: `tools/goctl/readme-cn.md`
- added: `tools/goctl/readme-ko.md`
- modified: `tools/goctl/readme.md`
- modified: `tools/goctl/rpc/CHANGELOG-cn.md`
- added: `tools/goctl/rpc/CHANGELOG-ko.md`
- modified: `tools/goctl/rpc/CHANGELOG.md`
- modified: `tools/goctl/rpc/README-cn.md`
- added: `tools/goctl/rpc/README-ko.md`
- modified: `tools/goctl/rpc/README.md`
- modified: `tools/goctl/rpc/example/01-basic/README-cn.md`
- added: `tools/goctl/rpc/example/01-basic/README-ko.md`
- modified: `tools/goctl/rpc/example/01-basic/README.md`
- modified: `tools/goctl/rpc/example/02-import-sibling/README-cn.md`
- added: `tools/goctl/rpc/example/02-import-sibling/README-ko.md`
- modified: `tools/goctl/rpc/example/02-import-sibling/README.md`
- modified: `tools/goctl/rpc/example/03-import-subdir/README-cn.md`
- added: `tools/goctl/rpc/example/03-import-subdir/README-ko.md`
- modified: `tools/goctl/rpc/example/03-import-subdir/README.md`
- modified: `tools/goctl/rpc/example/04-transitive-import/README-cn.md`
- added: `tools/goctl/rpc/example/04-transitive-import/README-ko.md`
- modified: `tools/goctl/rpc/example/04-transitive-import/README.md`
- modified: `tools/goctl/rpc/example/05-multiple-services/README-cn.md`
- added: `tools/goctl/rpc/example/05-multiple-services/README-ko.md`
- modified: `tools/goctl/rpc/example/05-multiple-services/README.md`
- modified: `tools/goctl/rpc/example/06-wellknown-types/README-cn.md`
- added: `tools/goctl/rpc/example/06-wellknown-types/README-ko.md`
- modified: `tools/goctl/rpc/example/06-wellknown-types/README.md`
- modified: `tools/goctl/rpc/example/07-external-proto-same-pkg/README-cn.md`
- added: `tools/goctl/rpc/example/07-external-proto-same-pkg/README-ko.md`
- modified: `tools/goctl/rpc/example/07-external-proto-same-pkg/README.md`
- modified: `tools/goctl/rpc/example/08-external-proto-diff-pkg/README-cn.md`
- added: `tools/goctl/rpc/example/08-external-proto-diff-pkg/README-ko.md`
- modified: `tools/goctl/rpc/example/08-external-proto-diff-pkg/README.md`
- modified: `tools/goctl/rpc/example/09-google-types-as-rpc/README-cn.md`
- added: `tools/goctl/rpc/example/09-google-types-as-rpc/README-ko.md`
- modified: `tools/goctl/rpc/example/09-google-types-as-rpc/README.md`
- modified: `tools/goctl/rpc/example/10-streaming/README-cn.md`
- added: `tools/goctl/rpc/example/10-streaming/README-ko.md`
- modified: `tools/goctl/rpc/example/10-streaming/README.md`
- added: `tools/goctl/rpc/example/README-cn.md`
- added: `tools/goctl/rpc/example/README-ko.md`
- modified: `tools/goctl/rpc/example/README.md`
- modified: `tools/goctl/rpc/generator/gencall.go`
- modified: `tools/goctl/rpc/generator/gencall_test.go`

## Documentation Impact

Review these changed upstream files and update related guides, components, reference pages, and FAQs when needed.

- `.github/workflows/codeql-analysis.yml`
- `.github/workflows/go.yml`
- `.github/workflows/release.yaml`
- `.github/workflows/reviewdog.yml`
- `.github/workflows/version-check.yml`
- `core/collection/fifo.go`
- `core/collection/fifo_test.go`
- `core/logx/readme-cn.md`
- `core/logx/readme-ko.md`
- `core/logx/readme.md`
- `core/mapping/jsonunmarshaler_test.go`
- `core/mapping/unmarshaler.go`
- `core/mr/readme-cn.md`
- `core/mr/readme-ko.md`
- `core/mr/readme.md`
- `core/stores/redis/breakerhook.go`
- `core/stores/redis/breakerhook_test.go`
- `core/stores/redis/conf.go`
- `core/stores/redis/redis.go`
- `core/stores/redis/redis_test.go`
- `core/stores/redis/redisblockingnode.go`
- `core/stores/redis/redisblockingnode_test.go`
- `core/stores/redis/redisclientmanager.go`
- `core/stores/redis/redisclustermanager.go`
- `core/stores/redis/redisclustermanager_test.go`
