---
title: go-zero issue #5599 documentation report
source_type: issue
source_url: https://github.com/zeromicro/go-zero/issues/5599
captured_at: 2026-10-01
related_docs:
  - src/content/docs/guides/http/server/request-body.md
  - src/content/docs/zh-cn/guides/http/server/request-body.md
  - src/content/docs/ko/guides/http/server/request-body.md
status: addressed
---

## Reported Problems

Issue [#5599](https://github.com/zeromicro/go-zero/issues/5599), "doc: Inconsistency in the description of parameter enumeration value", reports two inconsistencies in the HTTP request-body documentation:

1. The English description says enumeration values are comma-separated and uses `options=18,19`, while the following code example uses `options=18|19`.
2. The Simplified Chinese description says enumeration values are comma-separated, while its example uses `options=18|19`.

## Findings

- The go-zero `master` branch separates unbracketed option values with `|`, as in `options=18|19`.
- It also supports the bracketed comma-separated form `options=[18,19]`.
- The unbracketed form `options=18,19` does not define both values because commas outside brackets delimit struct tag options.
- The existing [`TestParseOptions`](https://github.com/zeromicro/go-zero/blob/master/rest/httpx/requests_test.go#L580-L588) unit test exercises pipe-separated request parameter options.
- A focused local test confirmed the following behavior:

| Struct tag | `18` | `19` | Other values |
| --- | --- | --- | --- |
| `options=18|19` | accepted | accepted | rejected |
| `options=[18,19]` | accepted | accepted | rejected |
| `options=18,19` | accepted | rejected | rejected |
