# GitHub issue delivery recipes

이 문서는 개발 과제를 durable issue로 접수하고, 특정 issue를 development branch부터 merge·정리까지
해결하는 command recipe다. 먼저 [GitHub 운영 규칙](github-operations.md)과
[공통 GitHub command 규칙](github-operation-recipes.md)을 적용한다.

## 과제를 issue로 접수한다

과제 접수 mode에서는 [GitHub 운영 규칙](github-operations.md)의 issue 필요성과 분할 기준을 먼저
적용한다. Atomic task라면 issue를 만들지 않고 원래 과제를 계속한다. 사용자가 issue 생성을 명시적으로
요청한 operation mode에서는 그 필요성을 다시 기각하지 않고 요청한 범위로 생성한다. 두 mode 모두
동일 목적의 열린 작업과 이미 완료된 작업을 먼저 검색한다.

```bash
gh issue list -R <OWNER/REPO> \
  --state all \
  --search 'in:title "<TITLE>"' \
  --json number,title,state,url
```

각 issue body는 다음 구조를 기본으로 하되, 내용이 없는 heading은 넣지 않는다.

```md
## 결과와 범위

<이 issue가 소유하는 독립적으로 merge 가능한 결과>

## Acceptance criteria

- <관찰 가능한 완료 조건>

## Validation

- <완료를 확인할 test 또는 검사>

## Dependencies

- <이 issue를 막는 선행 issue 또는 이 issue가 막는 후행 issue>
```

Issue를 생성하고 반환된 URL로 title과 body를 확인한다. 여러 issue의 번호를 알아야 의존 관계를 쓸 수
있다면 먼저 생성한 뒤 body file을 갱신한다.

```bash
gh issue create -R <OWNER/REPO> \
  --title "<TITLE>" \
  --body-file <BODY_FILE>
gh issue view <ISSUE_URL> -R <OWNER/REPO> \
  --json number,url,state,title,body
gh issue edit <ISSUE_URL> -R <OWNER/REPO> \
  --body-file <BODY_FILE>
```

접수만 승인된 경우 여기서 완료하고, 구현은 미완료임을 보고한다.
일반 구현의 추적을 위해 Issue를 추가한 경우에는 이미 확정한 구현·납품 범위대로 다음 단계를 이어간다.
Issue 번호를 새로 받았다는 이유로 특정 Issue 해결 요청을 다시 요구하지 않으며, 명시적인 접수 전용 요청은 그 범위를 유지한다.
같은 범위의 승인을 다시 요청하지 않는다.

## 특정 issue의 현재 상태를 판정한다

Issue, repository default branch와 연결된 PR·development branch를 먼저 확인한다.

```bash
gh issue view <ISSUE_URL> -R <OWNER/REPO> \
  --json number,url,state,title,body,closedByPullRequestsReferences
gh repo view <OWNER/REPO> \
  --json nameWithOwner,defaultBranchRef
gh issue develop --list <ISSUE_URL> -R <OWNER/REPO>
```

`closedByPullRequestsReferences`가 반환한 PR도 기존 linked work로 취급한다. 연결 branch를 확인할 수
있으면 같은 head의 기존 PR도 조회한다.

```bash
gh pr list -R <OWNER/REPO> \
  --head <BRANCH> \
  --state all \
  --json number,state,url,baseRefName,headRefName,headRefOid,mergedAt
```

조회 결과를 다음 상태로 구분한다.

| Issue 상태 | 관련 PR 상태 | 수행할 작업 |
| --- | --- | --- |
| `CLOSED` | `MERGED` | Merge 관계를 검증하고 새 branch나 PR을 만들지 않는다. |
| `CLOSED` | 없음 또는 미병합 `CLOSED` | 명시적인 reopen 의도가 없으면 현재 상태를 보고한다. |
| `OPEN` | `OPEN` | 기존 PR과 head branch를 재사용한다. |
| `OPEN` | `MERGED` | Default branch와 acceptance criteria를 검증하고 해결됐으면 issue를 닫는다. |
| `OPEN` | 미병합 `CLOSED` | Head와 scope가 유효하면 reopen하고, 아니면 새 PR 전에 재사용 불가 이유를 확인한다. |
| `OPEN` | 없음 | 연결 branch를 재사용하거나 새로 만든다. |

이미 merge된 결과가 issue를 실제로 해결한 경우에만 열린 issue를 닫는다.

```bash
gh issue close <ISSUE_URL> -R <OWNER/REPO> \
  --reason completed
```

미병합 closed PR을 안전하게 이어갈 수 있으면 같은 PR을 reopen한다.

```bash
gh pr reopen <PR_URL> -R <OWNER/REPO>
```

## Issue branch를 안전하게 준비한다

먼저 [공통 worktree 검사](github-operation-recipes.md)를 적용한다. Worktree가 clean하고 연결 branch가
없으면 default branch `<BASE>`에서 새 branch를 만들고, 안전한 checkout helper로 전환한다.
`--base`는 새 branch의 시작점뿐 아니라 이후 `gh pr create`가 사용할 PR base도 설정한다.

`gh issue develop --checkout`은 사용하지 않는다. 같은 repository에 branch를 만들면 다음처럼 실행하고,
다른 repository에 branch를 만들 때만 `--branch-repo <BRANCH_REPO>`를 추가한다.

```bash
gh issue develop <ISSUE_URL> -R <OWNER/REPO> \
  --base <BASE> \
  --name <BRANCH>
```

Head branch repository의 canonical URL과 일치하는 remote를 확인하고 `<BRANCH_REMOTE>`로 기록한다.

```bash
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py resolve-remote \
  --repository . \
  --target-url <BRANCH_REPOSITORY_URL>
```

연결 branch가 이미 있고 local branch도 있으면 verified remote에서 fetch한 뒤 안전하게 checkout한다.

```bash
git fetch <BRANCH_REMOTE> <BRANCH>
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py switch \
  --repository . \
  --branch <BRANCH>
git rev-parse HEAD
git rev-parse <BRANCH_REMOTE>/<BRANCH>
```

Local branch가 없으면 remote-tracking branch에서 만든다.

```bash
git fetch <BRANCH_REMOTE> <BRANCH>
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py switch \
  --repository . \
  --branch <LOCAL_BRANCH> \
  --track-start-point <BRANCH_REMOTE>/<BRANCH>
```

Local branch가 clean하고 remote보다 뒤에 있으면 fast-forward만 허용한다. SHA가 diverge했거나 issue-scoped
change와 충돌하면 force·reset하지 않고 차이를 먼저 해결한다.

```bash
git merge --ff-only <BRANCH_REMOTE>/<BRANCH>
```

현재 checkout에 unrelated uncommitted change가 있으면 branch를 전환하지 않는다. 안전한 별도 worktree
경계를 만들 수 있을 때는 branch 이름을 명시해 remote linked branch를 만든 뒤, 새롭고 비어 있는 경로에
그 branch를 추적한다.

```bash
gh issue develop <ISSUE_URL> -R <OWNER/REPO> \
  --base <BASE> \
  --name <BRANCH>
git fetch <BRANCH_REMOTE> <BRANCH>
git worktree add --track -b <LOCAL_BRANCH> \
  <WORKTREE_PATH> <BRANCH_REMOTE>/<BRANCH>
```

Worktree path나 local branch를 안전하게 정할 수 없으면 branch를 만들기 전에 중단한다. 기존 change를
자동 stash·commit·reset·discard하지 않는다.

Branch와 remote ref를 확인한다.

```bash
git branch --show-current
gh issue develop --list <ISSUE_URL> -R <OWNER/REPO>
git ls-remote --exit-code --heads <BRANCH_REMOTE> refs/heads/<BRANCH>
```

Fork나 다른 repository에 branch를 만들 때는 `--branch-repo <BRANCH_REPO>`를 사용하고, 이후 fetch·PR
head·push target 모두 branch repository의 `<BRANCH_REMOTE>`와 `<BRANCH_REPOSITORY_URL>`에 맞춘다. `origin`을
대상으로 추측하지 않는다.

## 구현하고 PR을 생성한다

Issue 범위 안에서 구현·test·논리적 commit을 완료한 뒤 verified branch remote에 push한다. Repository가
제공하는 validation command를 사용하고, local과 remote head SHA가 같은지 확인한다.

```bash
git push --set-upstream <BRANCH_REMOTE> <BRANCH>
git rev-parse HEAD
git ls-remote --exit-code --heads <BRANCH_REMOTE> refs/heads/<BRANCH>
```

기존 open PR이 없으면 summary, validation과 issue closing keyword를 body에 넣어 생성한다.

```md
## Summary

- <완료한 결과>

## Validation

- <실행한 검사와 결과>

Closes #<ISSUE>
```

다른 repository의 issue를 닫을 때는 `Closes <OWNER/REPO>#<ISSUE>`를 사용한다. Closing keyword는 PR이
issue repository의 default branch를 대상으로 할 때만 issue를 연결하고 merge 시 닫는다. 다른 base가
필요하면 자동 close를 가정하지 않는다.

같은 repository의 head branch는 `--head <BRANCH>`를 사용한다. 다른 repository의 head branch는
`--head <HEAD_OWNER>:<BRANCH>`로 owner를 명시하고, branch repository의 verified remote에 push했는지
확인한다.

```bash
gh pr create -R <OWNER/REPO> \
  --base <BASE> \
  --head <BRANCH> \
  --title "<TITLE>" \
  --body-file <BODY_FILE>
```

반환된 PR의 base, head와 issue link를 확인한다.

```bash
gh pr view <PR_URL> -R <OWNER/REPO> \
  --json number,url,state,baseRefName,headRefName,headRefOid,closingIssuesReferences
```

## Required check를 bounded wait로 처리한다

현재 required check를 구조적으로 조회한다.

```bash
gh pr checks <PR_URL> -R <OWNER/REPO> \
  --required \
  --json name,state,bucket,workflow,link
```

Issue 해결 요청에서는 자동 check가 pending이면 실행 환경의 bounded wait 안에서 terminal state까지
관찰한다. `--watch`를 사용할 때도 harness의 대기 한계를 넘겨 무기한 실행하지 않는다.

```bash
gh pr checks <PR_URL> -R <OWNER/REPO> \
  --required \
  --watch \
  --fail-fast \
  --interval 10
```

Check가 실패하면 issue 범위 안의 원인만 수정하고 다시 검증한다. Required review, 외부 권한 또는
관찰 기간 동안 진전이 없는 check는 우회하지 않고 verified pending state로 보고한다.

## Merge와 종료 상태를 검증한다

[Repository와 PR recipes](github-repository-pr-recipes.md)의 merge 절차에서 direct merge, auto-merge
또는 merge queue 중 repository 정책에 맞는 경로를 선택한다. 실제 merge와 안전한 branch 정리가 끝난
뒤 PR, issue와 branch 상태를 각각 확인한다.

```bash
gh pr view <PR_URL> -R <OWNER/REPO> \
  --json number,url,state,mergedAt,mergeCommit,headRefName,headRefOid
gh issue view <ISSUE_URL> -R <OWNER/REPO> \
  --json number,url,state,closedByPullRequestsReferences
```

`mergedAt`이 없거나 issue가 `OPEN`이면 완료로 보고하지 않는다. Default branch 반영과 acceptance
criteria를 검증했는데 closing keyword만 누락돼 issue가 열려 있으면 `completed`로 닫고 다시 확인한다.
Branch cleanup은 확인된 merged head SHA, branch repository remote와 worktree 경계를 함께 사용한다.

```bash
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py cleanup \
  --repository . \
  --local-branch <LOCAL_BRANCH> \
  --remote <BRANCH_REMOTE> \
  --remote-branch <BRANCH> \
  --expected-sha <MERGED_HEAD_SHA> \
  --target-url <BRANCH_REPOSITORY_URL>
```

별도 worktree를 제거할 때만 `--worktree <WORKTREE_PATH>`를 추가한다. Helper가 실패하면 force
삭제나 다른 remote로 재시도하지 않고, 완료된 merge와 미완료 cleanup을 분리해 보고한다.
