---
title: 문서화
description: go-zero 문서 웹사이트에 기여하는 방법입니다.
sidebar:
  order: 4

---


문서 사이트는 [Astro Starlight](https://starlight.astro.build/)로 만들어졌으며 `zeromicro/zerodoc` 저장소에서 관리됩니다.

## 로컬 설정

```bash
git clone https://github.com/zeromicro/zerodoc.git
cd zerodoc
npm install
npm run dev
# http://localhost:4321 열기
```

## 파일 구조

```text
src/content/docs/          # 영어 콘텐츠(root locale)
src/content/docs/zh-cn/    # 중국어 콘텐츠
```

각 페이지는 YAML frontmatter가 있는 Markdown 또는 MDX 파일입니다.

```yaml
---
title: Page Title
description: Short description for SEO and the card grid.
sidebar:
  order: 3
---
```

## 작성 가이드라인

- 2인칭 표현과 능동태를 사용합니다.
- 코드 블록에는 `go`, `bash`, `yaml` 같은 언어 태그를 반드시 붙입니다.
- 문맥이 필요한 코드 블록에는 `title`을 추가합니다. 예: ```go title="main.go"`
- 문장은 짧게 쓰고, 비교가 필요하면 표를 사용합니다.
- 모든 페이지에는 실제로 실행하거나 참고할 수 있는 코드 예제가 포함되어야 합니다.

## 새 페이지 추가

1. 적절한 챕터 디렉터리에 파일을 만듭니다.
2. `title`, `description`, `sidebar.order`가 포함된 YAML frontmatter를 추가합니다.
3. 해당 챕터의 `index.md`에 링크를 추가합니다.
4. `zh-cn/` 아래에 대응하는 중국어 번역 파일을 만듭니다.

## 제출

`zeromicro/zerodoc`의 `main` 브랜치를 대상으로 PR을 엽니다. 배포 미리보기 링크는 PR 댓글로 자동 게시됩니다.
