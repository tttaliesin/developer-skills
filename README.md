# 개발자 스킬

디버깅, API 설계, 코드 리뷰와 개발 작업에 사용하는 코딩 에이전트 스킬 모음

## 스킬

| 스킬 | 하는 일 |
| --- | --- |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | 버그의 원인을 조사하고 수정 결과 확인 |
| [api-design-principles](skills/api-design-principles/SKILL.md) | HTTP API와 비동기 메시지 규칙 설계 |
| [differential-review](skills/differential-review/SKILL.md) | 코드 변경의 보안 위험 검토 |
| [webapp-testing](skills/webapp-testing/SKILL.md) | 웹 화면과 사용자 동작 확인 |
| [design-doc-mermaid](skills/design-doc-mermaid/SKILL.md) | 구조·흐름 다이어그램 작성과 이미지 변환 |
| [parallel-worktree-development](skills/parallel-worktree-development/SKILL.md) | 여러 에이전트의 개발 작업 분담과 결과 통합 |
| [dual-session](skills/dual-session/SKILL.md) | 지속되는 두 대화로 설계·검토와 구현·실행을 분담 |
| [multi-github-account-operate](skills/multi-github-account-operate/SKILL.md) | 전역 인증을 바꾸지 않는 저장소별 GitHub 계정 연결 |
| [markdown-authoring](skills/markdown-authoring/SKILL.md) | Markdown 문서 작성·편집·검토 |
| [readme-authoring](skills/readme-authoring/SKILL.md) | 독자 목적·첫 사용·검증 기준에 따른 README 작성·검토 |
| [github-operations](skills/github-operations/SKILL.md) | GitHub 작업의 권한·납품·검증 관리 |

## 설치

Git과 Node.js/npm 필요

Codex에 전체 스킬 설치

```bash
npx skills add tttaliesin/developer-skills --skill '*' --agent codex --global
```

특정 스킬만 설치하는 예시

```bash
npx skills add tttaliesin/developer-skills --skill dual-session --agent codex --global
```

## 업데이트

설치한 스킬 이름을 지정해 업데이트

```bash
npx skills update dual-session --global
```

## 라이선스

외부 스킬의 라이선스와 출처는 각 스킬 폴더의 `LICENSE.txt`와 `NOTICE.md` 참고
