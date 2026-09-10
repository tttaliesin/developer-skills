# 개발자 스킬

개발 작업용 스킬 여덟 개를 보관하는 저장소
수정할 때는 `skills/` 안의 파일을 직접 편집하고, 변경 이력과 되돌리기는 Git으로 관리한다.

## 어떤 스킬이 있나

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

## 파일은 무슨 역할인가

각 스킬 폴더가 하나의 설치 단위다.

| 파일·폴더 | 역할 |
| --- | --- |
| `SKILL.md` | 스킬을 언제 쓰고 어떻게 작업할지 알려주는 지침 |
| `references/`와 보조 `.md` 파일 | 작업 중 필요할 때 읽는 상세 설명 |
| `assets/` | 문서·코드의 시작 틀과 이미지 자료 |
| `examples/` | 적용 방법을 보여주는 예제 |
| `agents/openai.yaml` | 스킬 이름 등 앱 표시 정보 |
| Mermaid의 `scripts/` | 다이어그램 추출·검증·이미지 변환에 쓰는 실행 도구 |
| Mermaid의 `runtime/` | 이미지 변환에 사용하는 Mermaid CLI의 의존성 정의 |
| `LICENSE.txt`, `NOTICE.md` | 외부 저작물의 사용 조건과 원작자·수정 출처 |

Mermaid 실행 도구를 쓸 때만 [실행 환경 안내](skills/design-doc-mermaid/references/runtime-setup.md)를 참고한다.
[외부 스킬 개인 수정 메모](docs/local-skill-customizations.md)는 이 저장소 밖에서 관리되는 스킬에 적용했던 수정 의도를 설명한다.
`.gitignore`는 실행 중 생기는 캐시와 설치한 의존성이 Git에 들어가지 않게 한다.

## 수정과 설치

개발용 정본은 이 저장소의 `skills/` 디렉터리이며, 배포 원본은 GitHub의 `tttaliesin/developer-skills`
필요 조건은 Git, Node.js와 npm이 제공하는 `npx`, [Skills CLI](https://github.com/vercel-labs/skills) 실행 환경
공개 저장소 조회와 설치에는 읽기 접근만 필요하며, GitHub push에는 해당 저장소 쓰기 권한을 가진 계정 인증 필요

수정부터 설치본 갱신까지의 기본 흐름은 다음 순서

1. `skills/` 아래 지침과 자료를 정본에서 수정
2. 변경 범위에 맞는 링크, Markdown 구조, 스크립트 또는 실제 동작 검증
3. diff와 검증 결과를 검토한 뒤 Git commit 생성
4. 검증된 commit을 GitHub `main`에 push
5. 설치본과 정본을 비교하고 설치본에만 있는 변경을 별도로 보존
6. GitHub 소스를 사용하는 Skills CLI로 필요한 전역 설치본 갱신

별도의 원본 복사본, patch, 파일 해시 기록이나 상시 테스트 체계는 유지하지 않음
저장소 수정이나 push만으로 기존 설치본까지 자동 갱신되지는 않음

Skills CLI는 GitHub 저장소의 `skills/<name>/SKILL.md`를 검색 대상으로 사용
설치 전에 발견되는 스킬 목록 확인

```bash
npx skills add tttaliesin/developer-skills --list
```

`dual-session`만 Codex 전역 스킬로 설치

```bash
npx skills add tttaliesin/developer-skills --skill dual-session --agent codex --global
```

저장소의 여덟 스킬을 모두 Codex 전역 스킬로 설치

```bash
npx skills add tttaliesin/developer-skills --skill '*' --agent codex --global
```

이미 설치된 스킬은 설치본의 별도 변경을 보존한 뒤 대상 이름으로 갱신
현재 Skills CLI 문법의 `dual-session` 전역 갱신 예시

```bash
npx skills update dual-session --global
```

다른 스킬 갱신 시 `dual-session`을 대상 스킬 이름으로 교체
실행 전에 설치된 Skills CLI 버전이 대상 이름과 `--global`을 받는 update 문법을 지원하는지 확인

외부 스킬의 라이선스와 출처 고지는 유지한다.
`parallel-worktree-development`는 workspace-rules에서 이관한 자체 스킬이며 별도 라이선스를 부여하지 않는다.
