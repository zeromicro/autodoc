---
title: go-zero v1.10.3 release
source_type: release
source_url: https://github.com/zeromicro/go-zero/releases/tag/v1.10.3
captured_at: 2026-08-09
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

### Core

- `stringx.FirstN`: returns empty string for negative `n` ([#5620](https://github.com/zeromicro/go-zero/pull/5620))
- `stringx.Substr`: rejects `start > stop` to prevent slice panic ([#5616](https://github.com/zeromicro/go-zero/pull/5616))
- `mapping`: fixed unmarshaling of pointer-to-slice fields ([#5662](https://github.com/zeromicro/go-zero/pull/5662))
- `collection`: optimized queue growth strategy ([#5704](https://github.com/zeromicro/go-zero/pull/5704))

### Redis

- Added `XGroupSetID`/`XGroupSetIDCtx` to update a consumer group's last-delivered ID ([#5637](https://github.com/zeromicro/go-zero/pull/5637))
- Fixed circuit breaker tripping under high concurrency / with incompatible servers ([#5654](https://github.com/zeromicro/go-zero/pull/5654)), plus minor refactor ([#5666](https://github.com/zeromicro/go-zero/pull/5666))

### Docs

- Added Korean translations ([#5579](https://github.com/zeromicro/go-zero/pull/5579)) — upstream repo docs, not this site.

### Dependencies

- `go-redis/v9` 9.19.0 → 9.21.0
- `mongo-driver/v2` 2.6.0 → 2.8.0
- `pelletier/go-toml/v2` 2.3.1 → 2.4.3

### New Contributors

@Vierblatt, @sapirbaruch, @SAY-5, @jeonghyeon-net, @Meppo, @puneetdixit200, @lxffong, @014-code

## Documentation Impact

- Added English, Simplified Chinese, and Korean release-notes pages under `reference/releases/v1.10.3.md`.
- Updated all three `reference/releases/index.md` files and all three `reference/changelog.md` files with the new entry.
- No component/guide pages required updates — all changes in this release are internal bug fixes, a performance optimization, and one additive Redis API method with no existing documented behavior contradicted.
- Gave `v1.10.3.md` `sidebar.order: 0` (rather than renumbering all 47 other release files) so it sorts first; pre-existing duplicate order values among older release files (e.g. v1.10.1 and v1.10.2 both previously used `order: 1`) were left as-is — out of scope for this ingest.
