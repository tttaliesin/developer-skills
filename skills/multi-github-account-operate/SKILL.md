---
name: multi-github-account-operate
description: Bind one Git repository to one explicitly selected GitHub.com account for HTTPS Git credentials and `git gh` commands without switching global GitHub CLI authentication. Use when multiple authenticated GitHub accounts must remain isolated by repository. Do not use for SSH remotes, GitHub Enterprise, automatic login, or authorization bypass.
---

# Multi GitHub Account Operate

저장소별 Git·GitHub CLI 인증 계정 분리
GitHub.com HTTPS 저장소 하나와 이미 인증된 계정 하나만 명시적으로 연결하고, 전역 활성 계정은 변경하지 않는 방식

실제 GitHub 작업의 권한·대상·완료 지점은 `github-operations`에 위임
해당 스킬이 없으면 사용자 승인과 저장소 정책을 직접 확인한 뒤 필요한 작업만 수행

## 적용 전 확인

- Git 저장소, Python 3.10 이상, GitHub CLI 필요
- 선택 계정이 `gh auth`에 이미 등록된 상태 필요
- GitHub.com HTTPS remote만 지원하며 SSH와 GitHub Enterprise는 미지원
- `extensions.worktreeConfig=true`는 모든 worktree 설정이 Codex의 `codex.localEnvironmentConfigPath` 메타데이터만 포함할 때 지원하며 그 외 override는 거절
- 대상 repository URL·owner·repository·계정을 사용자 요청과 remote에서 각각 확인
- 기존 worktree 변경과 repo-local credential·alias 충돌 확인
- commit author와 인증 계정은 별도이며 `user.name`·`user.email` 자동 변경 금지

## 저장소 연결

먼저 [운영 절차](references/operation.md)를 읽고 helper 경로를 실제 설치 위치로 치환

```bash
python3 <SKILL_ROOT>/scripts/github_account_router.py bind \
  --repository <REPOSITORY> \
  --remote origin \
  --url https://github.com/<OWNER>/<REPOSITORY_NAME> \
  --account <ACCOUNT>
```

`bind`가 만드는 상태는 Git common directory의 비밀 없는 JSON·작업 잠금 파일과 repo-local `.git/config` 항목뿐
연결된 worktree가 같은 common directory와 설정을 공유하는 구조
기존 local helper 또는 `alias.gh`가 있으면 덮어쓰지 않고 중단

## 연결 사용

상태 조회에는 토큰 접근 없음

```bash
python3 <SKILL_ROOT>/scripts/github_account_router.py status --repository <REPOSITORY>
```

`bind`와 `status`는 구성 일치만 확인하며 선택 계정의 실제 인증 성공을 증명하지 않음
read-only 계정 확인이 필요하면 `git -C <REPOSITORY> gh api user --jq .login` 결과를 선택 계정과 대조

선택 계정으로 GitHub CLI 실행

```bash
git -C <REPOSITORY> gh repo view
```

`git gh`만 repo-local alias 적용 대상이며 일반 `gh`에는 영향 없음
wrapper는 저장된 계정의 토큰을 자식 프로세스 환경에만 전달하는 인증 라우터이며 보안 sandbox나 명령 승인 엔진이 아님
실제 owner·repository·operation과 권한은 호출자가 실행 직전에 재검증

HTTPS Git은 repo-local credential helper를 통해 같은 계정 사용
helper는 요청 host·path·username이 바인딩과 다르거나 토큰 조회가 실패하면 `quit=true`로 다른 helper·askpass fallback 차단

## 연결 해제

```bash
python3 <SKILL_ROOT>/scripts/github_account_router.py unbind --repository <REPOSITORY>
```

`unbind`는 자신이 설치한 local key가 그대로일 때만 제거
연결 뒤 다른 프로세스가 값을 바꿨으면 덮어쓰지 않고 중단

## 권한 경계

- token 영구 저장·로그·명령 인자 삽입 금지
- `gh auth token --hostname <HOST> --user <ACCOUNT>` 결과는 subprocess에서 capture하고 그대로 출력 금지
- 기존 token 환경 변수와 debug trace를 토큰 조회·`git gh` 자식에 전달 금지
- 다른 계정 fallback, 전역 `gh auth switch/login/logout`, 전역 Git config 변경 금지
- 자동 remote 생성·변경·게시·권한 확대 금지
- `user.name`·`user.email`은 사용자가 지정했거나 검증된 identity일 때만 별도 repo-local 설정
