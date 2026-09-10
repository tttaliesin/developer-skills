# 개발자 스킬

Codex에서 디버깅, API 설계, 코드 리뷰와 문서 작성에 사용하는 개발 스킬 모음
필요한 작업에 맞는 스킬 하나만 설치하거나 전체 설치 가능

## 빠르게 시작

Git과 Node.js/npm 준비
현재 프로젝트의 README를 독자 관점에서 정리하는 `readme-authoring` 설치·사용 예시

1. 터미널에서 스킬 하나 설치

   ```bash
   npx skills add tttaliesin/developer-skills --skill readme-authoring --agent codex --global --yes
   ```

2. Codex 대화에 다음 요청 입력

   ```text
   $readme-authoring 이 프로젝트의 README를 정리해줘
   ```

3. 기대 결과 확인

   - 현재 프로젝트의 `README.md`를 독자 목적·첫 사용·결과 확인 중심으로 수정
   - 실제 수행한 검증과 남은 한계를 Codex 응답에 보고

## 스킬

| 스킬 | 하는 일 |
| --- | --- |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | 근거 수집으로 버그 원인을 찾고 수정 결과 검증 |
| [api-design-principles](skills/api-design-principles/SKILL.md) | HTTP API와 비동기 메시지의 호환성·검증·멱등성 설계 |
| [differential-review](skills/differential-review/SKILL.md) | PR·커밋·diff의 보안 위험, 변경 영향과 테스트 누락 검토 |
| [webapp-testing](skills/webapp-testing/SKILL.md) | 로컬 웹 UI의 실제 화면, 브라우저 오류와 사용자 흐름 검증 |
| [design-doc-mermaid](skills/design-doc-mermaid/SKILL.md) | 코드·요구사항을 구조·배포·순서·상태 Mermaid 다이어그램으로 작성·검증 |
| [parallel-worktree-development](skills/parallel-worktree-development/SKILL.md) | 독립 구현 작업을 여러 Git worktree에 나누고 로컬 결과 통합 |
| [dual-session](skills/dual-session/SKILL.md) | 지속되는 두 Codex 대화에 설계·검토와 구현·실행 역할 분리 |
| [multi-github-account-operate](skills/multi-github-account-operate/SKILL.md) | 한 저장소를 지정 GitHub 계정에 연결하고 전역 로그인 변경 없이 인증 분리 |
| [markdown-authoring](skills/markdown-authoring/SKILL.md) | Markdown 문서의 구조·표·링크·코드·접근성 작성·편집·검토 |
| [readme-authoring](skills/readme-authoring/SKILL.md) | 저장소 README를 독자 목적·첫 사용·결과 확인 중심으로 작성·개편·검토 |
| [github-operations](skills/github-operations/SKILL.md) | Issue·브랜치·PR·merge·release의 권한, 납품과 실제 상태 검증 |

## 설치

Codex에 전체 스킬 설치

```bash
npx skills add tttaliesin/developer-skills --skill '*' --agent codex --global
```

## 업데이트

설치한 스킬 이름을 지정해 업데이트

```bash
npx skills update readme-authoring --global
```

## 라이선스

외부 스킬의 라이선스와 출처는 각 스킬 폴더의 `LICENSE.txt`와 `NOTICE.md` 참고
