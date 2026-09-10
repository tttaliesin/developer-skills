# 저장소별 GitHub 계정 운영

## 지원 범위

`github_account_router.py`는 GitHub.com HTTPS remote 하나와 계정 하나의 저장소 로컬 바인딩만 지원
GitHub Enterprise, SSH remote, 여러 계정 fallback과 로그인 자동화는 미지원
`extensions.worktreeConfig=true`는 main과 모든 linked worktree의 설정 파일에 Codex의 `codex.localEnvironmentConfigPath`만 존재할 때 지원
credential·alias·remote·include 등 다른 worktree 설정은 연결과 사용 시 거절

GitHub CLI 2.100.0의 `gh auth git-credential`은 credential 요청의 username으로 계정을 선택하지 않고 host의 `ActiveToken`과 `ActiveUser`만 조회
비활성 계정을 안전하게 선택하려면 [`gh auth token --hostname ... --user ...`](https://cli.github.com/manual/gh_auth_token)의 결과를 capture하는 별도 helper 필요
근거는 [GitHub CLI 2.100.0 credential helper 구현](https://github.com/cli/cli/blob/v2.100.0/pkg/cmd/auth/gitcredential/helper.go)

Git은 여러 credential helper가 있으면 자격 증명이 채워질 때까지 다음 helper를 실행
선택 계정 조회 실패 후 다른 계정이나 askpass로 넘어가지 않도록 [Git credential helper 규약](https://git-scm.com/docs/gitcredentials)의 `quit=true` 사용

## 바인딩 전 점검

1. 실제 저장소와 모든 linked worktree의 진행 중 변경 확인
2. `git remote get-url --all <REMOTE>`와 push URL이 선택한 GitHub.com HTTPS URL과 같은지 확인
3. 계정이 이미 GitHub CLI에 등록됐는지 비밀을 출력하지 않는 방식으로 확인
4. 실제 GitHub 작업의 owner·repository·권한·보호 규칙 확인
5. commit author가 필요하면 인증 계정과 별도로 검증

helper 자체는 로그인, 전역 계정 전환, remote 변경, repository 생성이나 게시를 수행하지 않음

## 명령

Python 3.10 이상 필요
아래 `<SKILL_ROOT>`는 설치된 스킬 디렉터리, `<REPOSITORY>`는 대상 Git worktree 경로
공백이나 한글이 있는 경로는 shell에 맞게 하나의 인자로 quoting

바인딩

```bash
python3 <SKILL_ROOT>/scripts/github_account_router.py bind \
  --repository <REPOSITORY> \
  --remote origin \
  --url https://github.com/<OWNER>/<REPOSITORY_NAME> \
  --account <ACCOUNT>
```

상태 검사

```bash
python3 <SKILL_ROOT>/scripts/github_account_router.py status --repository <REPOSITORY>
```

`bind`와 `status`는 remote·local config·상태 파일의 일치만 검사하며 계정 토큰의 유효성을 확인하지 않음
실제 선택 계정의 read-only 확인은 다음 출력이 `<ACCOUNT>`와 같은지 대조

```bash
git -C <REPOSITORY> gh api user --jq .login
```

선택 계정으로 GitHub CLI 전달

```bash
git -C <REPOSITORY> gh pr status
git -C <REPOSITORY> gh repo view
```

`git gh`는 바인딩 owner/repository를 `GH_REPO` 기본값으로 설정
명시적인 `--repo` 또는 `-R`은 같은 owner/repository만 허용하지만, API endpoint와 각 명령의 실제 영향은 호출자가 별도 확인
인증·alias·전역 config를 바꾸는 `gh auth`, `gh alias`, `gh config` 명령 전달은 차단

연결 해제

```bash
python3 <SKILL_ROOT>/scripts/github_account_router.py unbind --repository <REPOSITORY>
```

## 저장 상태

Git common directory의 `multi-github-account-operate.json`에 다음 비밀 없는 값만 저장

- schema version
- canonical GitHub URL·host·owner·repository
- 선택 계정 이름과 remote 이름
- Python·helper·GitHub CLI 실행 경로
- helper가 설치한 repo-local config의 정확한 key와 값
- 바인딩 전 해당 local key가 비어 있었다는 복구 기록

repo-local GitHub.com credential URL에는 빈 helper 항목을 먼저 넣어 상위 scope에서 상속한 helper 목록 초기화
이어 router helper·username·`useHttpPath=true` 설정
credential helper는 protocol, host, owner/repository path와 선택 username을 모두 대조한 뒤에만 토큰 조회
따라서 remote가 다른 GitHub repository로 바뀌거나 `.git` suffix가 달라도 전역 helper로 fallback하지 않고 불일치 요청을 중단

같은 common directory의 `multi-github-account-operate.lock`은 `bind`와 `unbind`를 직렬화하는 비밀 없는 작업 잠금 파일
linked worktree가 같은 잠금을 공유하며 프로세스 종료 시 운영체제가 잠금을 해제

## 충돌과 복구

- 상태 파일과 local config가 모두 그대로면 반복 `bind`를 성공으로 처리
- 상태 파일 없이 관리 대상 local key가 하나라도 있으면 충돌로 중단
- 상태 파일과 local config가 다르면 `status` 실패, `unbind` 중단
- `unbind`는 모든 관리 key가 예상 값과 같은지 먼저 확인한 뒤 제거
- `bind`와 `unbind`는 공통 작업 잠금 안에서 각 변경 직전 config·state를 다시 확인
- 작업 잠금은 이 helper끼리만 조정하므로 `bind`·`unbind`가 진행되는 동안 외부 `git config` 편집 금지
- 중간 작업이 실패하면 현재 값이 helper가 마지막으로 확인한 값인 key만 명령 시작 전 값으로 복원
- 다른 프로세스가 바꾼 값은 덮어쓰지 않고 수동 복구가 필요한 key를 보고
- token 조회 실패 시 stderr에 일반 오류만 기록하고 captured stdout·stderr와 token은 폐기
