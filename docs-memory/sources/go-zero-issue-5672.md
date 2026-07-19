---
title: go-zero issue #5672 documentation report
source_type: issue
source_url: https://github.com/zeromicro/go-zero/issues/5672
captured_at: 2026-07-19
related_docs:
  - src/content/docs/guides/http/server/sse.md
  - src/content/docs/reference/cli-guide/
  - src/content/docs/reference/goctl-plugins.md
  - src/content/docs/reference/releases/
status: addressed
---

## Reported Problems

Issue [#5672](https://github.com/zeromicro/go-zero/issues/5672), "go-zero.dev文档存在问题或更新不够及时", reports five categories of documentation defects:

1. Missing images in the SSE and Swagger documentation.
2. A 404 at `/docs/tutorials/cli/overview`.
3. Guide overview pages appearing after the child pages in the sidebar.
4. A deprecated `goctl-swagger` repository remaining in the plugin resources.
5. The release index lagging behind the latest v1.10.2 release.

The original report includes ten screenshots:

- https://github.com/user-attachments/assets/7af43d98-8e1f-4a7d-93ae-879b45b78e77
- https://github.com/user-attachments/assets/4dd73faa-350e-43c3-936e-b7aadc53677d
- https://github.com/user-attachments/assets/5719cfed-664f-4607-876d-6c4be597638e
- https://github.com/user-attachments/assets/79bd9d8f-c293-456a-be50-7e3f4a41d47b
- https://github.com/user-attachments/assets/cbb46b92-3f20-4ded-a5a5-0c56bd07470d
- https://github.com/user-attachments/assets/63328a5f-0d41-4915-8c59-6bcfade3df19
- https://github.com/user-attachments/assets/14f41826-98e8-471d-9180-7b138867d1eb
- https://github.com/user-attachments/assets/196e13d8-5e91-4611-832e-01d52d3e0abf
- https://github.com/user-attachments/assets/8d99665a-2e63-413e-8cc3-c851d7f5f883

## Findings

- Malformed `resour../` image paths affected the English and Simplified Chinese CLI and SSE pages.
- The referenced image assets already exist under `public/resource/tutorials/`.
- The legacy CLI routes require static redirect pages for the GitHub Pages deployment.
- Gateway and deployment guide index pages had sidebar orders greater than their child pages.
- The public v1.10.2 release, published 2026-05-31, was not yet represented in the checked-out documentation.
