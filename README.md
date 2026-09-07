# 개발자 스킬

Codex와 Pi의 개발 지원 스킬과 유지보수·검증 도구를 관리하는 `tools/` 소유 저장소다.
공개 스킬의 승인된 수정과 자체 스킬을 구분하여 관리한다.
Workspace 공통 정책은 workspace-rules가, Vault 운영은 Second Brain이 담당한다.
다음 표는 관리하는 패키지와 주요 수정 내용을 보여준다.

| 우선순위 | 패키지 | 주요 수정 내용 |
| --- | --- | --- |
| 1 | [systematic-debugging](skills/systematic-debugging/SKILL.md) | 자격 증명을 노출하지 않는 증거 수집, 로컬 테스트 지침, 네 번째 수정 전 상의 요건 유지 |
| 2 | [api-design-principles](skills/api-design-principles/SKILL.md) | HTTP·비동기 생산자와 소비자 간 계약, 실행 결과, 호환성 검증용 데이터와 환경 |
| 3 | [differential-review](skills/differential-review/SKILL.md) | 증거에 근거한 심각도 판정, 작업 범위 안의 보고서 저장, 자체적으로 수행 가능한 분석 |
| 4 | [webapp-testing](skills/webapp-testing/SKILL.md) | 기존 브라우저·테스트 도구 사용, 제한 시간 내 준비 상태 관찰, 프로세스 소유권 확인 |

새로 적용한 [Mermaid 스킬과 검증 runtime](docs/mermaid-adoption.md)은 Markdown 다이어그램 작성·검증·이미지 변환을 지원한다.

이관한 [parallel-worktree-development](skills/parallel-worktree-development/SKILL.md)는 자체 개발 지원 스킬이다.
[외부 스킬 개인 수정 기록](docs/local-skill-customizations.md)과 [패키지·출처 도구 유지보수](docs/package-maintenance.md)는 upstream 수정 패키지와 구분한다.

## 원본과 수정 기록

[원본 고정 정보](upstream-lock.json)는 저장소, 리비전, 원본 디렉터리, 라이선스와 보존한 모든 원본 파일의 해시를 기록한다.
`upstream/`에는 수정하지 않은 참조용 스냅샷을 보존한다.
이 스냅샷은 근거 자료이며, 설치할 지시문이나 실행 권장 예제가 아니다.
각 설치 패키지에는 해당 라이선스와 출처 고지가 포함된다.
전체 패키지에 하나의 새 라이선스를 적용하지 않는다.
수정된 differential-review는 CC BY-SA 4.0을, 나머지 패키지는 각각의 MIT 또는 Apache-2.0 조건을 유지한다.
승인된 변경 범위, 유지한 승인 요건, 제외한 보조 도구는 [변경 기록](docs/changes.md)을 참고한다.
`patches/`의 검토 가능한 patch는 고정된 원본 스냅샷으로부터 로컬 패키지를 재구성한다.
자동 생성되는 설치 출처 기록(provenance)은 patch에서 제외한다.

## 검증과 갱신

아래 명령은 모두 이 저장소 루트에서 Bash로 실행한다.
로컬 patch 생성과 재구성 검증에는 Python 3과 Git이 필요하며, 외부 Python 패키지는 필요하지 않다.

```bash
python3 scripts/validate.py
```

이 명령은 원본 해시와 patch 재구성 결과가 바이트 단위로 일치하는지 검사한다.
설치 출처 기록을 검증하거나 에이전트의 실제 동작을 입증하지는 않는다.
일반적인 로컬 수정에서는 `skills/` 아래 패키지를 수정하고, 해당 patch만 재생성한 뒤 검증을 다시 실행한다.
다음은 systematic-debugging 패키지의 예다.

```bash
python3 scripts/update-patch.py systematic-debugging
python3 scripts/validate.py
```

Patch 생성 도구는 `upstream-lock.json`에 등록된 패키지 이름 하나를 인자로 받는다.
고정된 스냅샷을 확인하고 자동 생성된 출처 기록을 제외한 뒤, 임시 디렉터리에서 재구성을 검증하고 나서 `patches/<name>.patch`를 교체한다.
`<name>`은 선택한 패키지 이름이다.
원본 스냅샷, 고정 정보, 패키지 내용과 설치된 스킬은 변경하지 않는다.
패키지와 patch의 변경 내역을 함께 검토한다.

전체 유지보수 검증에는 외부에 설치된 Skill Creator와 Markdown Authoring 도구도 사용한다.
설치 출처 검증 도구는 이 저장소의 `scripts/skill-provenance.py`이며 별도 checkout이 필요하지 않다.
Skill Creator와 Markdown Authoring만 외부 도구로 사용한다.
아래 예시는 이 개인 workspace의 디렉터리 구성을 사용한다.
다른 환경에서는 경로를 바꾸고, 명시된 스크립트가 존재하는지 확인한 뒤 실행한다.

```bash
SKILL_CREATOR_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator"
MARKDOWN_AUTHORING_ROOT="$HOME/.agents/skills/markdown-authoring"

(
for package in systematic-debugging api-design-principles differential-review webapp-testing; do
  python3 "$SKILL_CREATOR_ROOT/scripts/quick_validate.py" "skills/$package" || exit 1
done
)

python3 "$MARKDOWN_AUTHORING_ROOT/scripts/check-markdown.py" \
  README.md docs/changes.md \
  skills/systematic-debugging/SKILL.md \
  skills/systematic-debugging/references/failing-test.md
```

Markdown 파일 목록은 해당 작업에서 변경한 문서에 맞게 조정한다.
외부 도구를 사용할 수 없으면 로컬 검증을 수행하고, 실행하지 못한 검사를 보고한다.
이 경우 전체 유지보수 검증이나 설치 검증이 완료되었다고 주장하지 않는다.
에이전트 동작 평가와 검증 한계는 [검증 기록](docs/validation.md)을 참고한다.

Upstream을 갱신할 때는 기존 고정 정보와 스냅샷을 보존하고, 스크립트·자산·참조 문서·라이선스·호출 정책을 포함한 새 패키지 전체의 변경 내역을 검토한다.
로컬 patch를 새 upstream 지시와 대조한 뒤 수정하며, 검토 없이 기존 patch를 새 지시에 덮어씌우지 않는다.
선택한 upstream 리비전으로 스냅샷과 고정 정보를 검토·갱신한 뒤, 해당 patch를 재생성하고 위 검증을 실행한다.

## 전역 설치

아래 설치·출처 기록 절차는 공개 수정 패키지와 자체 스킬에 적용하며, 앞서 설명한 외부 도구를 갖춘 개인 Codex/Pi workspace를 대상으로 한다.
`npx`를 포함한 Node.js/npm, Skills CLI에 대한 접근, 선택한 전역 스킬 경로의 쓰기 권한이 필요하다.
저장소 수정이나 commit만으로 전역 동기화까지 승인되는 것은 아니다.
승인된 설치를 수행하기 전에 기존 설치본과 정본을 비교하고, 설치본에서 별도로 수정한 파일을 보존한다.

### 현재 checkout의 출처 기록 준비

새 출처 기록에는 portable repository locator, 저장소 상대 package 경로, 기준 Git 리비전과 패키지 해시가 포함된다.
같은 논리적 저장소와 package 상대 경로라면 checkout 이동 후에도 검증할 수 있다.
기존 절대 경로 기록은 구형 검증을 유지하므로 위치가 달라지면 원본을 검토한 뒤 재생성한다.
`HEAD` commit이 있는 Git checkout을 사용한다.
명령의 상대 package 경로는 실행 cwd 기준이며 아래 예시는 저장소 루트에서 실행한다.

유지보수 중 내용을 갱신할 때는 최종 패키지와 patch를 먼저 commit한 뒤, 출처 기록을 생성해 별도로 commit한다.
새 로컬 checkout에서는 내용 변경이나 원격 게시 없이 해당 checkout의 출처 기록을 생성할 수 있다.
아래 명령은 로컬 `source-provenance.json` 파일에 기록하므로, 이 변경은 스킬 내용과 구분해서 검토한다.
미commit 작업은 그 상태로 기록되며, 깨끗하게 commit된 릴리스의 증거가 되지는 않는다.

```bash
(
for package in systematic-debugging api-design-principles differential-review webapp-testing; do
  python3 scripts/skill-provenance.py write "skills/$package" --repository urn:local-repository:developer-skills || exit 1
  python3 scripts/skill-provenance.py check "skills/$package" --repository urn:local-repository:developer-skills || exit 1
done
)
```

반복문의 패키지 목록은 설치할 대상으로만 제한하고, 정본 검사에 실패한 패키지는 원인을 해결한 뒤 설치한다.
출처 기록만 포함하는 commit에서 `base_revision`은 의도적으로 그 직전의 내용 스냅샷을 가리킨다.

### 선택한 패키지 설치와 검증

Upstream 스냅샷이 선택되지 않도록 Skills CLI에 각 패키지의 정확한 경로를 지정한다.
아래 명령 중 설치할 패키지에 해당하는 명령만 실행한다.

```bash
npx skills add ./skills/systematic-debugging --agent codex pi --global --yes
npx skills add ./skills/api-design-principles --agent codex pi --global --yes
npx skills add ./skills/differential-review --agent codex pi --global --yes
npx skills add ./skills/webapp-testing --agent codex pi --global --yes
npx skills add ./skills/parallel-worktree-development --agent codex pi --global --yes
```

설치 도구가 보고한 두 에이전트의 설치 경로를 각각 검증한다.
아래 경로는 이 개인 workspace에서 사용하는 위치다.
설치 도구가 다른 경로를 선택했다면 해당 값으로 바꾸고, 반복문의 패키지 목록도 실제 설치한 대상으로 제한한다.

```bash
CODEX_SKILLS_ROOT="$HOME/.agents/skills"
PI_SKILLS_ROOT="$HOME/.pi/agent/skills"

(
for package in systematic-debugging api-design-principles differential-review webapp-testing; do
  python3 scripts/skill-provenance.py check "skills/$package" --repository urn:local-repository:developer-skills \
    --installed "$CODEX_SKILLS_ROOT/$package" || exit 1
  python3 scripts/skill-provenance.py check "skills/$package" --repository urn:local-repository:developer-skills \
    --installed "$PI_SKILLS_ROOT/$package" || exit 1
done
)
```

불일치가 있으면 해당 설치는 미검증 상태로 남는다.
다시 동기화하기 전에 정본과 설치본 중 어떤 내용이 다른지 확인한다.
전역 복사본이나 symlink를 수동으로 유지보수하지 않는다.
스킬의 자동 선택은 도구 사용 권한이나 운영 환경의 작업 승인을 부여하지 않는다.
