---
title: Pull Request 절차
description: go-zero에 Pull Request를 열고 병합받는 절차입니다.
sidebar:
  order: 3

---


## PR을 열기 전에

1. 중복을 피하기 위해 기존 issue와 PR을 먼저 검색합니다.
2. 큰 변경이라면 먼저 issue를 열어 접근 방식을 논의합니다.
3. 모든 테스트가 통과하는지 확인합니다: `go test ./...`
4. `golangci-lint run`을 실행하고 발견된 문제를 수정합니다.
5. `goimports -w ./...`를 실행해 코드를 포맷합니다.

## PR 제목

Conventional Commits 형식을 따릅니다.

```text
fix: prevent goroutine leak in http server shutdown
feat: add Redis cluster support to cache package
docs: update quickstart guide for v1.7
refactor: simplify breaker state machine
```

## PR 설명

다음 템플릿을 사용합니다.

```markdown
## Summary
Brief description of the change.

## Changes
- List of files/packages changed and why

## Testing
How you tested the change.

## Breaking Change?
Yes / No. If yes, describe what breaks and migration path.
```

## 리뷰 절차

1. 최소 **한 명의 메인테이너 리뷰**가 필요합니다.
2. CI가 모두 통과해야 합니다(테스트 + lint + 빌드).
3. 승인되면 메인테이너가 **squash merge**로 병합합니다.

## 머지 후

- PR 작성자는 릴리스 노트에 기여자로 기록됩니다.
- PR이 해결한 issue는 PR 설명에 `Fixes #<issue>`를 넣어 닫습니다.
