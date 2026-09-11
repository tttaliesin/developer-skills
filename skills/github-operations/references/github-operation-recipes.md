# GitHub operation command rules

이 문서는 branch·worktree 변경이나 정리, GitHub resource mutation, raw API 사용, 결과가 불명확한
mutation 재시도에 필요한 대상 식별, worktree 보호, command 선택과 재시도 기준을 정의한다.
진입 지침의 공통 불변식을 적용한 뒤 현재 작업에 해당하는 절과 실제 operation recipe 하나만 읽는다.
단순한 read-only 조회에는 이 문서 전체를 선행 로드하지 않고 정확한 대상의 좁은 조회 명령에서 시작한다.

## 필요한 recipe를 선택한다

요청한 결과에 해당하는 문서만 읽는다.

- 과제의 issue 분할·생성, 특정 issue 해결과 연결 branch 작업은
  [Issue delivery recipes](github-issue-delivery-recipes.md)를 사용한다.
- Repository 생성·push와 pull request(PR) 생성·check·merge는
  [Repository와 PR recipes](github-repository-pr-recipes.md)를 사용한다.
- Release 발행과 workflow run 실행·진단은
  [Release와 workflow recipes](github-release-workflow-recipes.md)를 사용한다.

## Placeholder와 실행 위치

Command는 대상 local repository의 Git root에서 실행한다. 다음 placeholder를 실제 값으로 바꾸고,
공백이 포함된 값은 하나의 shell argument가 되도록 quote한다.

- `<OWNER/REPO>`: GitHub의 명시적인 repository 식별자
- `<TARGET_REPOSITORY_URL>`: 작업 대상 repository의 확인된 canonical URL
- `<BRANCH_REPOSITORY_URL>`: head branch가 존재하는 repository의 확인된 canonical URL
- `<TARGET_REMOTE>`: 작업 대상 repository와 URL이 일치하는 검증된 Git remote
- `<BRANCH_REMOTE>`: head branch repository와 URL이 일치하는 검증된 Git remote
- `<GITHUB_OPERATIONS_SKILL>`: 설치된 `github-operations` skill package의 경로
- `<BRANCH>`, `<LOCAL_BRANCH>`, `<BASE>`, `<HEAD>`, `<REF>`: local·remote branch, base, head 또는 Git
  ref
- `<BRANCH_REPO>`: issue에 연결할 branch를 생성할 GitHub repository
- `<WORKTREE_PATH>`: 기존 변경과 분리할 local Git worktree 경로
- `<MERGED_HEAD_SHA>`: 실제 병합된 PR head의 확인된 commit SHA
- `<BODY_FILE>`, `<NOTES_FILE>`, `<JSON_FILE>`: secret을 포함하지 않는 입력 파일
- `<PR_URL>`, `<ISSUE_URL>`, `<ISSUE>`, `<TAG>`, `<RUN_ID>`, `<WORKFLOW>`, `<SHA>`: 작업 결과나 입력
  식별자

다른 repository를 다룰 때는 current directory 추론에 의존하지 않고 `-R <OWNER/REPO>`를 쓴다.
Git 명령은 `origin`을 기본값으로 추측하지 말고 대상 URL과 일치하는 remote를 먼저 검증한다.
설치된 CLI에서 flag나 JSON field가 지원되는지 불확실하면 대상 명령의 `--help`를 확인한다. 이를 인증
preflight로 확대하지 않는다.

## 대상과 worktree를 식별한다

현재 local target과 기존 변경을 확인한다.

```bash
git rev-parse --show-toplevel
git branch --show-current
git remote -v
git status --short --ignored
```

GitHub repository의 identity와 visibility가 작업에 중요하면 필요한 field만 구조적으로 조회한다.

```bash
gh repo view <OWNER/REPO> \
  --json nameWithOwner,visibility,url,defaultBranchRef
```

확인된 repository URL과 일치하는 remote를 하나만 선택한다.

```bash
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py resolve-remote \
  --repository . \
  --target-url <TARGET_REPOSITORY_URL>
```

명령의 출력 remote를 `<TARGET_REMOTE>`로 기록하고 이후 fetch·push·ref 검증에 동일하게 사용한다.
Head branch가 다른 repository에 있으면 `<BRANCH_REPOSITORY_URL>`과 `<BRANCH_REMOTE>`를 별도로 확인한다.

`gh repo view`의 실패만으로 repository가 존재하지 않는다고 단정하지 않는다. 인증, 권한, target과
network 오류를 대상 명령의 실제 오류로 구분한다.

Worktree가 dirty이면 변경의 소유 범위를 먼저 판정한다.

- `git status --short`만으로 clean을 판정하지 않고 ignored 파일도 확인한다.
- 현재 linked issue branch에 있고 변경이 그 issue 범위이면 그대로 재개할 수 있다.
- 현재 issue와 무관한 변경이면 branch checkout, stash, commit, reset 또는 discard를 수행하지 않는다.
- 적절한 별도 worktree 경계를 만들 수 있으면 기존 checkout을 보존한 채 그 경계에서 작업한다.
- 안전한 분리가 불가능하거나 변경 소유권이 불명확하면 remote mutation 전에 중단하고 상태를 보고한다.
- 새 worktree 경로는 존재하지 않거나 비어 있어야 하며, 기존 ignored 파일이 있는 경로를 재사용하지 않는다.

Branch 전환은 ignored 파일을 덮어쓰지 않는 helper를 사용한다.

```bash
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py switch \
  --repository . \
  --branch <LOCAL_BRANCH>
```

`gh issue develop --checkout`과 `git switch`의 기본 overwrite 동작을 안전한 branch 전환으로 취급하지
않는다. 파괴적 branch·worktree cleanup은 확인된 merged SHA와 remote mapping을 함께 받는 helper로만
수행한다.

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
ignored 파일, 다른 worktree 사용, local ref SHA와 remote ref SHA를 확인한 뒤 expected-old-SHA
local deletion과 remote lease deletion만 수행한다.
외부 process의 동시 파일 변경은 OS 수준으로 잠그지 않으므로 cleanup 호출자는 local repository와
worktree의 독점 소유를 확인해야 한다. 독점 소유를 확인할 수 없으면 cleanup을 실행하지 않는다.

Issue delivery의 linked branch worktree와 parallel worker worktree는 같은 경계가 아니다.
Issue branch의 생성·checkout과 Issue lifecycle cleanup은
`github-operations`가 소유한다. 독립 local slice를 격리하는 worker worktree, worker local
branch와 commit 통합은 `$parallel-worktree-development` skill이 소유한다.
Worker는 push, PR, merge, Issue close 또는 remote ref cleanup을 수행하지 않는다.
통합 owner는 모든 worker commit을 integration worktree에서 검토·통합하고 전체 validation을
실행한 뒤, 결과를 `github-operations`로 돌려보낸다.

## `gh api`는 예외적으로 사용한다

First-class `gh` subcommand가 필요한 operation이나 field를 제공하지 않을 때만 `gh api`를 사용한다.
Field flag를 추가하면 기본 method가 `POST`로 바뀔 수 있으므로 조회와 변경 모두 method를 명시한다.

```bash
gh api --method GET <ENDPOINT> -F <KEY>=<VALUE>
gh api --method PATCH <ENDPOINT> --input <JSON_FILE>
```

변경 API를 호출한 뒤에는 별도 GET 또는 first-class view 명령으로 결과를 검증한다. 인증 우회를 위해
raw HTTP client나 다른 credential로 전환하지 않으며, credential이 포함될 수 있는 verbose request를
출력하지 않는다.

## 실패와 재시도를 판정한다

`gh`의 일반 exit code `0`은 성공, `1`은 실패, `2`는 취소, `4`는 인증 필요를 뜻한다. 일부 명령은
추가 code를 사용하므로 자동 분기를 만들기 전에 해당 명령의 `--help`를 확인한다. 예를 들어
`gh pr checks`의 `8`은 check가 pending임을 뜻한다.

Mutation 명령이 timeout이나 network 오류로 끝났으면 같은 create 명령을 즉시 반복하지 않는다.
Operation별 view·list 명령으로 resource가 생성됐는지 확인하고, 이미 생성됐으면 그 식별자를 이어서
사용한다. 조회 자체도 실패하면 확인되지 않은 상태를 명시하고 추가 mutation을 중단한다.
