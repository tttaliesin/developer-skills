# GitHub repository and pull request recipes

이 문서는 repository 생성·push와 pull request(PR) 생성·check·merge를 수행하는 command recipe다. 먼저
[GitHub 운영 규칙](github-operations.md)과
[공통 GitHub command 규칙](github-operation-recipes.md)을 적용한다.

## Private repository를 생성하고 push한다

`origin`이 없고 사용자가 local repository를 private GitHub repository로 만들도록 요청했다면 다음
명령으로 생성과 remote 연결을 수행한다. `--remote=origin`은 이 생성 명령이 명시적으로 만드는 remote
이름이며, 이후 대상 repository URL과 다시 대조한다.

```bash
gh repo create <OWNER/REPO> \
  --private \
  --source=. \
  --remote=origin
```

`origin`이 이미 의도한 GitHub URL을 가리키면 remote를 다시 만들지 않고 GitHub repository만 생성한다.

```bash
gh repo create <OWNER/REPO> --private
```

생성 후 repository와 local remote를 각각 확인하고 `<TARGET_REMOTE>`를 확정한다.

```bash
gh repo view <OWNER/REPO> \
  --json nameWithOwner,visibility,url,defaultBranchRef
git remote -v
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py resolve-remote \
  --repository . \
  --target-url <TARGET_REPOSITORY_URL>
```

명령의 출력 remote를 `<TARGET_REMOTE>`로 기록한다. 사용자가 push까지 요청했을 때만 대상 branch를
그 verified remote로 전송한다.

```bash
git push --set-upstream <TARGET_REMOTE> <BRANCH>
```

Local과 remote branch가 같은 commit을 가리키는지 두 SHA를 비교한다.

```bash
git rev-parse <BRANCH>
git ls-remote --exit-code --heads <TARGET_REMOTE> refs/heads/<BRANCH>
```

`gh repo create --push`는 생성과 push를 하나의 명령으로 요청한 경우에만 사용할 수 있다. 부분 실패 후
repository가 이미 생성됐을 수 있으므로 `gh repo view`, `git remote -v`와 verified remote mapping으로
상태를 확인한 뒤 남은 remote 연결 또는 push만 수행한다.

Head branch가 다른 repository에 있으면 branch repository의 verified remote에 push하고,
`gh pr list`·`gh pr create`의 head를 `<HEAD_OWNER>:<HEAD>`로 명시한다. 같은 repository의 head는
`<HEAD>`만 사용한다.

## Pull request를 생성한다

먼저 head branch를 push한다. 같은 repository의 같은 base·head 조합으로 이미 생성된 PR이 있는지
조회한다.

```bash
gh pr list -R <OWNER/REPO> \
  --head <HEAD> \
  --base <BASE> \
  --state all \
  --json number,state,url,baseRefName,headRefName,headRefOid,mergedAt
```

기존 open PR이 없고 생성이 요청 범위에 포함되면 prompt가 생기지 않도록 중요한 값을 명시한다.

```bash
gh pr create -R <OWNER/REPO> \
  --base <BASE> \
  --head <HEAD> \
  --title "<TITLE>" \
  --body-file <BODY_FILE>
```

반환된 URL을 사용해 실제 base·head와 상태를 검증한다.

```bash
gh pr view <PR_URL> -R <OWNER/REPO> \
  --json number,url,state,baseRefName,headRefName,headRefOid,title
```

현재 check 상태만 조회할 때는 구조화된 결과를 사용한다. PR 생성이나 check 조회만 요청받았다면
merge하지 않는다.

```bash
gh pr checks <PR_URL> -R <OWNER/REPO> \
  --required \
  --json name,state,bucket,workflow,link
```

## Pull request를 merge한다

Merge는 별도의 remote mutation이다. PR 생성이나 check 조회 요청만으로 승인됐다고 해석하지 않는다.
특정 issue 해결 요청에는 정상 merge와 해당 issue branch 정리가 포함된다. Merge 전에 대상, 현재 head
commit, review, check와 repository merge 설정을 조회한다.

```bash
gh pr view <PR_URL> -R <OWNER/REPO> \
  --json number,url,state,isDraft,baseRefName,headRefName,headRefOid,reviewDecision,mergeable,mergeStateStatus
gh pr checks <PR_URL> -R <OWNER/REPO> \
  --required \
  --json name,state,bucket,workflow,link
gh repo view <OWNER/REPO> \
  --json mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed,deleteBranchOnMerge,viewerDefaultMergeMethod
```

조회한 `headRefOid`를 `<PR_HEAD_SHA>`로 보존한다. Repository가 허용하는 merge strategy 중 하나를
명시하고, head가 바뀌었으면 merge하지 않는다. Merge 명령에 branch 삭제 option을 넣지 않고, 실제
병합 뒤 expected SHA cleanup 절차를 별도로 수행한다.

```bash
gh pr merge <PR_URL> -R <OWNER/REPO> \
  --squash \
  --match-head-commit <PR_HEAD_SHA>
```

Required check가 아직 끝나지 않았고 repository가 auto-merge를 허용하면 issue 해결 lifecycle이나
완료 대기를 포함한 merge 요청에서 `--auto`를 사용할 수 있다. Auto-merge 등록 시점에는 아직 merge가
완료되지 않았으므로 branch 삭제 option을 붙이지 않으며, 등록 성공을 merge나 branch 정리 완료로
보고하지 않는다.

```bash
gh pr merge <PR_URL> -R <OWNER/REPO> \
  --squash \
  --auto \
  --match-head-commit <PR_HEAD_SHA>
```

Base branch가 merge queue를 요구하면 strategy를 지정하지 않는다. Required check가 끝나지 않은
상태에서는 auto-merge가 설정되고, 끝난 상태에서는 queue에 들어갈 수 있으므로 명령 성공을 즉시
merge 완료로 보고하지 않는다. Merge queue에서는 branch 삭제 option을 사용하지 않는다.

```bash
gh pr merge <PR_URL> -R <OWNER/REPO> \
  --match-head-commit <PR_HEAD_SHA>
```

`--admin`은 branch protection이나 merge queue를 우회하므로 사용자가 그 우회를 명시적으로 요청하고
권한이 확인된 경우에만 사용한다.

## 실제 merge를 기다리고 검증한다

Issue 해결 요청은 자동 required check와 merge queue의 진행을 bounded wait로 추적한다. 다음 조회를
반복하되, merge 완료, terminal failure, 사람 review·외부 권한 gate 또는 실행 환경의 대기 한계 중
하나에 도달하면 멈춘다.

```bash
gh pr view <PR_URL> -R <OWNER/REPO> \
  --json number,url,state,mergedAt,mergedBy,mergeCommit,autoMergeRequest,headRefName,headRefOid
```

Queue 또는 auto-merge가 대기 중이면 완료로 보고하지 않는다. 사람 gate나 진전 없는 상태에서는
`--admin`으로 우회하지 않고 verified pending state를 보고한다.

Merge가 완료되면 PR에 실제로 포함된 마지막 head commit을 `<MERGED_HEAD_SHA>`로 확인한다. 이 값은
branch ref가 merge 뒤 새 commit으로 이동했는지 판정하는 기준이다.

```bash
gh pr view <PR_URL> -R <OWNER/REPO> \
  --json state,mergedAt,commits \
  --jq '{state: .state, mergedAt: .mergedAt, mergedHead: .commits[-1].oid}'
```

## Auto-merge와 merge queue branch를 안전하게 정리한다

Direct merge, auto-merge와 merge queue 모두 실제 merge를 확인한 뒤 issue branch만 정리한다. Merge
명령에 `--delete-branch`를 넣지 않는다. Squash와 rebase merge에서는 original branch commit이 base의
조상이 아닐 수 있으므로 ancestry 기반 `git branch -d`도 사용하지 않는다.

Branch cleanup은 확인된 merged head SHA, branch repository의 verified remote와 worktree 경계를
함께 받아 helper로 수행한다.

```bash
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py cleanup \
  --repository . \
  --local-branch <LOCAL_BRANCH> \
  --remote <BRANCH_REMOTE> \
  --remote-branch <BRANCH> \
  --expected-sha <MERGED_HEAD_SHA> \
  --target-url <BRANCH_REPOSITORY_URL>
```

별도 worktree를 제거할 때만 `--worktree <WORKTREE_PATH>`를 추가한다. Helper는 tracked·untracked·
ignored 파일과 다른 worktree 사용을 먼저 검사하고, local ref는 expected-old-SHA와 함께 삭제하며
remote ref는 expected-SHA lease로 삭제한다.

Helper가 실패하면 force 삭제나 다른 remote로 재시도하지 않는다. Branch가 merge 뒤 전진했거나
worktree에 파일이 남아 있으면 merge 완료와 branch cleanup 미완료를 분리해 보고한다.

## Merge와 workflow run을 분리한다

Merge가 workflow 실행을 보장하지는 않는다. Workflow의 실제 `on` event와 branch 조건이 merge 결과를
대상으로 할 때만 merge commit SHA로 후속 run을 찾는다. 예를 들어 base branch의 `push`를 trigger로
사용한다면 다음처럼 확인한다.

```bash
gh run list -R <OWNER/REPO> \
  --commit <SHA> \
  --event push \
  --json databaseId,status,conclusion,headSha,url,workflowName,event
```

Merge queue의 pre-merge 검사는 `merge_group`, PR 검사는 `pull_request`처럼 서로 다른 event와 SHA를
사용할 수 있다. 설정되지 않은 run을 기다리지 말고 workflow YAML의 trigger에 맞는 event와 commit을
사용한다. Run의 완료 감시와 실패 진단은
[Release와 workflow recipes](github-release-workflow-recipes.md)를 따른다.
