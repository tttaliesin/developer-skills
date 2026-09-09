# 개발자 스킬

개발 작업에서 사용하는 일곱 가지 스킬을 보관하는 저장소다.
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

스킬의 지침이나 자료를 직접 수정하고 바뀐 내용에 맞춰 링크 또는 실제 동작을 확인한다.
별도의 원본 복사본, patch, 파일 해시 기록이나 상시 테스트 체계는 유지하지 않는다.

설치할 때는 필요한 스킬 폴더 전체를 사용하는 스킬 설치 위치에 반영한다.
기존 설치본에 따로 수정한 내용이 있다면 먼저 비교해 보존한다.
저장소 편집만으로 별도 설치본까지 갱신되지는 않는다.

외부 스킬의 라이선스와 출처 고지는 유지한다.
`parallel-worktree-development`는 workspace-rules에서 이관한 자체 스킬이며 별도 라이선스를 부여하지 않는다.
