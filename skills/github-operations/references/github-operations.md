# GitHub 운영 규칙

이 문서는 작업 대상 repository에서 과제를 GitHub issue로 추적할지 판단하고, `gh`와 `git`으로
issue를 끝까지 해결하거나 다른 GitHub 작업을 수행할 때 적용하는 권한, 진단, 실행과 검증 기준을
정의한다. 일반적인 GitHub CLI 명령 목록이 아니라, 사용자가 맡긴 작업의 범위를 보존하고 실제
증거에 따라 결과를 판단하기 위한 이 패키지의 공통 규칙이다.

## 완료 지점을 먼저 정한다

사용자가 원하는 결과, 현재 대화의 승인, 확인된 저장소 workflow로 납품 완료 지점을 먼저 정한다.
로컬 diff·검토 결과, 원격 branch 반영, PR 생성, 대상 branch 병합 중 해당 지점을 기존 작업 문맥에 명시하고, 그 뒤에 Issue 추적 필요성을 별도로 판단한다.
Issue가 없다고 로컬 전용으로 축소하거나 Issue를 만든다고 접수만으로 중단하지 않는다.
작은 수정도 원격 반영이 필요할 수 있고 큰 검토도 로컬 결과만 요구할 수 있다.

확인된 목적과 같은 범위의 기존 승인을 재사용하며 단계마다 재승인을 요구하지 않는다.
완료 지점이나 권한이 실질적으로 불명확해 결과가 달라질 때만 필요한 선택을 확인한다.
원격이 존재한다는 이유만으로 모든 수정을 push하거나, 사용자가 매번 push라는 단어를 쓰지 않았다는 이유만으로 이미 승인된 원격 단계를 생략하지 않는다.
Push, PR 생성, PR merge, release, 배포는 서로 다른 행위다.
대상 ref와 실제 CI·배포 trigger를 확인해 각 행위의 영향과 승인을 판단하고, 필요한 check·review·보호 규칙을 우회하지 않는다.

제한을 전달할 때는 근거와 대상·행위·작업 범위를 함께 유지한다.
이전 작업의 로컬 전용 조건을 다음 작업에 자동 적용하거나, 조정자가 worker에게 맡긴 좁은 범위를 사용자의 전체 요청에 대한 금지로 바꾸지 않는다.
Coordinator와 Git owner는 분담 이후에도 남은 승인된 납품 단계를 이어갈 책임을 유지한다.

## 납품과 추적 경로를 선택한다

요청한 결과에 따라 다음 mode 중 하나를 선택한다.

- **구현:** 정해진 완료 지점까지 필요한 변경·통합·검증과 승인된 원격 반영 수행

  명시적인 local diff나 review-only 결과도 유효한 납품 상태다.
  로컬 전용이 완료 지점이면 원격 변경을 추가하지 않으며, 원격 반영이 포함된 요청이면 로컬 commit에서 끝내지 않는다.

- **과제 접수:** 기능 구현이나 구조 개선처럼 결과 중심의 과제를 issue로 추적할 가치가 있는지
  판단한다. 필요한 경우 과제를 독립적으로 완료·merge할 수 있는 issue로 나누고 생성한다.
- **Issue 해결:** 특정 issue를 해결하라는 요청을 해당 issue의 구현부터 merge와 정리까지 이어지는
  전체 delivery lifecycle로 수행한다.
- **명시적 GitHub 작업:** Issue 생성만, pull request(PR) 생성만, merge만, release 발행처럼 사용자가
  지정한 operation과 그 정상적인 필수 단계만 수행한다.

Operation 이름보다 요청한 결과를 우선한다. Issue 생성만 요청했다면 구현을 시작하지 않고, PR 생성만
요청했다면 merge하지 않는다. 반대로 특정 issue를 해결하라는 요청에는 commit, push, PR 생성과 정상
merge를 각각 다시 요청할 필요가 없다.

Issue 필요성은 위에서 정한 납품 완료 지점과 독립적으로 판정한다.
접수만 승인되었으면 issue 생성 후 멈춘다.
이미 승인된 구현의 추적을 위해 Issue를 만들었으면 그 구현과 납품을 이어가며 새 Issue 번호를 사용한 재요청을 요구하지 않는다.
명시적으로 로컬 구현·diff·검토를 요청한 작업은 그 납품 범위로 진행하며 Issue lifecycle을 추가하지 않는다.
그 밖의 일반 과제는 아래 기준으로 durable Issue 추적의 필요성을 판단한다.
Issue 추적이 불필요해도 확정된 원격 반영 범위는 유지한다.
Issue 생성 자체는 추가 구현·PR·merge 권한을 만들지 않으며, 기존 구현·납품 권한을 줄이지도 않는다.
같은 범위의 기존 승인은 후속 요청과 skill 전환에서도 유지하며 다시 묻지 않는다.
접수만 승인된 경우에는 생성한 issue, 중단 규칙과 이후 구현에 필요한 승인 범위를 함께 보고한다.
실제 승인이나 외부 gate 때문에 납품이 남으면 이유·담당자·재개 조건을 명시하며, 추적 절차 자체를 새 중단 조건으로 만들지 않는다.

## Issue로 추적할 과제를 판정한다

다음 중 하나 이상이 작업 결과의 추적·검토·재개에 실질적으로 필요하면 issue를 사용한다.

- 둘 이상의 독립적으로 완료·merge 가능한 결과나 선후 의존 관계가 있다.
- 여러 session, 담당자 또는 review 단계를 거치며 범위와 완료 조건을 지속적으로 공유해야 한다.
- 사용자 동작, public contract, migration, 보안, 운영 또는 rollback 판단처럼 변경 근거와 수용 결과를
  장기 보존할 가치가 있다.
- 작업이 중단되거나 일부만 완료됐을 때 남은 범위를 repository 안에서 재개해야 한다.

한 session에서 하나의 좁은 변경과 검증으로 끝나고 별도 조정·추적 가치가 없는 atomic task는 issue를
강제하지 않는다. 파일 수나 코드 줄 수만으로 issue 필요성을 판정하지 않는다.

Issue로 나눌 때는 각 issue가 독립적인 사용자·운영 결과와 merge 가능한 경계를 갖게 한다. 각 body에는
최소한 다음 내용을 포함한다.

- 이 issue가 만들어야 하는 결과와 범위
- 관찰 가능한 acceptance criteria
- 완료를 확인할 validation 방법
- 선행·후행 issue 또는 외부 의존 관계
- 오해할 가능성이 있을 때만 명시하는 제외 범위

구현 순서의 모든 세부 단계를 issue로 만들거나, 같은 결과를 여러 issue가 동시에 소유하게 하지 않는다.
사용자 요구에 없는 기능·정책을 acceptance criteria로 발명하지 않는다. 대상 repository와 issue
tracking 사용 여부를 확인할 수 없으면 원격 issue를 추측해 만들지 않는다.

## 요청한 작업을 권한의 경계로 삼는다

사용자가 요청한 작업은 확정된 완료 지점에 필요한 범위로 수행한다.
Issue 분할과 생성은 추적 절차이며 기존 납품 범위를 확대하거나 축소하지 않는다.
Repository 생성, push, PR 생성처럼 명시적으로 한정한 operation은 그 operation과 정상적인 필수 단계까지만 수행한다.

특정 issue를 “해결”, “완료”, “처리”하라는 요청은 다음 lifecycle을 정상 작업 범위로 승인한다.

```text
issue와 기존 연결 작업 확인
→ 연결 development branch 생성·checkout 또는 기존 branch 재사용
→ 범위 안의 구현·test
→ 논리적 commit·push
→ issue를 닫는 PR 생성
→ required check 확인과 범위 안의 실패 수정
→ repository 정책에 맞는 merge
→ branch 정리
→ PR merge와 issue close 검증
```

## 로컬 통합과 완료를 확인한다

구현을 시작하거나 worker에게 보내기 전에 최종 납품 경로·worktree, branch와 base revision 또는 의도한 local diff, 통합 책임자를 기존 작업 문맥에 명시한다.
중간 integration worktree와 사용자에게 전달할 checkout이 다르면 두 위치와 남은 이전 책임을 구분한다.
통합 책임자는 skill 전환 뒤에도 최종 위치에서 합의한 결과가 검증되거나 추적 가능한 pending 인계가 수락될 때까지 책임을 유지한다.
공유 checkout은 승인된 단일 writer로 사용할 수 있으며 협업 자체가 새 worktree를 요구하지 않는다.

Worker의 검증 통과나 commit 생성은 사용자 작업의 완료가 아니다.
Git history 통합이 납품 조건이면 목적지의 base와 기존 변경을 확인하고 승인된 Git 통합 절차로 worker 변경을 반영한 revision과 관련 검증을 최종 위치에서 확인한다.
파일 복사만으로 Git history가 통합됐다고 주장하지 않는다.
반대로 명시적인 local diff나 review-only 납품에는 commit을 강제하지 않으며 정확한 경로·base·diff 또는 검토 결과와 검증 범위를 보고한다.
Atomic task에 Issue·commit·원격 변경을 일괄 요구하지 않는다.
무관한 dirty 파일을 납품 commit에 포함하거나 commit·stash·reset·discard로 정리하지 않는다.

최종 수용은 합의한 위치의 Git root·branch·HEAD와 요청 범위의 diff, 검증 결과 및 기존 변경 보존을 확인한 뒤 판단한다.
Worker 경로의 결과만 있고 최종 목적지가 아직 이전 상태라면 통합 미완료다.
로컬 통합과 원격 반영은 별도 검증 단계다.
요청한 완료 지점에 원격 반영이 포함되면 local 검증 후 기존 승인에 따라 push·PR·merge 중 필요한 단계를 이어가고 실제 원격 SHA·PR·병합 상태를 확인해야 전체 완료다.
로컬 전용 endpoint에는 원격 단계를 추가하지 않는다.
설치본도 납품 범위라면 정본의 Git 상태와 승인된 설치 파일의 반영 여부를 각각 검증한다.

남은 통합·정리는 이유, 담당자, 재개 조건과 현재 완료·대기 상태를 기존 작업에 남긴다.
Worker가 끝났거나 idle이라는 이유로 의무를 지우거나 worktree를 삭제하지 않는다.
완료 판정은 합의한 납품 검증 이후에만 하며 남은 의무를 다른 task로 명시적으로 이전하면 수신 task에서 계속 추적한다.
인계로 담당 assignment가 끝나더라도 사용자 결과가 아직 납품되지 않았으면 전체 완료로 표시하지 않는다.
Cleanup은 이미 승인된 범위에서 Git owner의 기존 safety helper와 dirty·ignored 파일 및 process 소유권 검증을 따른다.
소유권이나 안전 조건이 불명확하면 정리만 pending으로 남기고 완료된 구현과 구분한다.

## 병렬 local 구현은 별도 skill로 handoff한다

Issue 추적 여부와 parallel worktree 실행 여부는 별도 판단이다. 독립 slice가 둘 이상이라는
사실만으로 parallel 실행이나 Issue 생성을 자동 승인하지 않는다. Issue가 필요하면 먼저 이
문서의 Issue 절차를 선택하되, Issue 유무로 납품 완료 지점이나 원격 반영 범위를 바꾸지 않는다.

Substantive implementation이 서로 독립된 slice 둘 이상으로 나뉘고 격리 worktree가 실제로
효율을 높일 때만 `$parallel-worktree-development` skill로 local 작업을 handoff한다. Handoff에는
repository, Issue(해당하는 경우), base revision, 최종 납품 경로·worktree, integration branch 또는 합의한 local diff, 통합 책임자, acceptance criteria, validation 명령과 remote mutation 경계를 포함한다.

- `github-operations`는 Issue 판정·lifecycle, linked branch, push, PR, merge, release, workflow,
  Issue close와 remote/local branch cleanup을 계속 소유한다.
- `parallel-worktree-development`는 worker worktree, local commit, slice integration과 통합 후
  verification만 소유한다.
- Parallel skill은 Issue를 새로 만들거나, branch lifecycle을 복제하거나, remote ref를 변경하지
  않는다. 합의한 최종 위치의 통합 revision 또는 명시적인 local diff와 verification 증거를 반환한다.
  목적지 통합이 남았으면 완료가 아닌 pending handoff로 반환한다.
  Git owner는 통합 결과를 확인한 뒤 기존 승인에 포함된 원격 단계를 이어가며 최종 완료 지점을 검증한다.

이 lifecycle도 issue의 제품 요구와 repository 정책을 바꾸는 권한은 아니다. 다음 작업은 별도 요청이나
승인이 필요하다.

- `--admin`으로 branch protection, required review 또는 merge queue를 우회한다.
- Issue 범위와 acceptance criteria를 실질적으로 바꾸거나 unrelated repository를 변경한다.
- Production 배포, release 발행, visibility 변경 또는 별도 운영 resource를 변경한다.
- Issue branch가 아닌 다른 branch나 unrelated resource를 삭제한다.

Required review, 외부 check 또는 권한 때문에 merge를 완료할 수 없으면 우회하지 않는다. 현재 PR과
대기 조건을 검증해 보고하고, 실제 merge·issue close가 일어나기 전에는 issue 해결을 완료로 판정하지
않는다.

자동 required check처럼 진행 상태를 관찰할 수 있는 gate는 issue 해결 요청에 포함된 bounded wait로
추적한다. Check가 성공·실패의 terminal state에 도달하거나, 사람 review·외부 권한처럼 agent가 해결할
수 없는 gate가 확인되거나, 관찰 기간 동안 진전이 없어 실행 환경의 대기 한계에 도달하면 중단한다.
실패는 issue 범위 안에서만 수정하고, 사람 gate나 정체 상태는 pending으로 보고한다.

이 문서의 `확인`과 `검증`은 기본적으로 기존 대화와 파일·도구 증거를 통한 확인을 뜻한다.
사용자 응답이 필요한 경우에만 질문하며, 이미 확정된 값을 다시 승인받지 않는다.
대상을 현재 repository와 명령 인자에서 확정할 수 있으면 진행한다. Owner, repository 이름, visibility,
base branch처럼 잘못 선택했을 때 다른 원격 상태를 바꾸는 값이 불명확하면 실제 변경 직전에 확인한다.
조회나 진단을 이유로 요청과 무관한 외부 변경을 추가하지 않는다.

## 요청한 명령에서 시작한다

GitHub 작업 전에 현재 Git root, branch와 remote처럼 대상을 식별하는 데 필요한 local 상태를 확인할 수
있다. 그러나 `gh auth status`를 모든 `gh` 작업의 관성적인 preflight로 실행하지 않는다. 이 명령은
사용자가 인증 진단을 요청했거나, 실제 대상 명령이 인증 관련 오류로 실패했고 원인을 좁히는 데 필요한
경우에만 사용한다.

`gh auth status`의 결과는 그 진단이 확인한 credential 상태에 관한 증거다. 아직 실행하지 않은 특정
GitHub 작업이 반드시 실패한다는 증거로 확대하지 않는다. 요청한 작업을 시도하지 않았다면
“불가능하다”고 단정하지 말고, 무엇을 확인했고 무엇은 확인하지 않았는지 구분한다.

사용자가 `gh` 사용을 지정했다면 가능한 GitHub 작업은 `gh`로 수행한다. 인증 문제를 우회하기 위해
임의로 raw API, 다른 credential 또는 다른 계정으로 전환하지 않는다. `git`은 local history와
remote ref 전송에, `gh`는 repository·pull request·issue·workflow 같은 GitHub resource 작업에
사용한다.

## 오류의 원인을 증거로 구분한다

명령이 실패하면 실행한 대상 명령과 핵심 오류를 보존하고 다음 원인을 섞지 않는다.

- 인증 credential이 없거나 거부됐다.
- 인증된 identity에 필요한 repository 또는 operation 권한이 없다.
- Repository, branch, argument 또는 resource 상태가 요청과 맞지 않는다.
- Network, DNS, proxy 또는 sandbox가 GitHub 연결을 막았다.
- GitHub service 또는 API가 일시적으로 실패했다.

Sandbox나 network 제한으로 실패한 명령은 해당 실행 환경의 승인 절차로 같은 작업을 다시 시도할 수
있다. 이를 GitHub 인증 실패라고 보고하지 않는다. 반대로 GitHub가 반환한 인증·권한 오류를 network
문제로 바꾸어 설명하지 않는다.

## 변경은 좁게 수행하고 검증한다

외부 상태를 바꾸기 직전에 명령의 owner, repository, branch와 operation을 확인한다. Secret, token,
private key와 credential 값을 명령 출력, 문서, commit 또는 대화에 노출하지 않는다. 오류 진단에서도
credential 자체를 출력하는 명령이나 option을 사용하지 않는다.

Branch를 만들거나 checkout하기 전에 worktree 상태를 `--ignored` 포함으로 확인한다. 현재 issue와 무관한
uncommitted change나 ignored 파일을 새 branch로 옮기거나 commit·stash·discard하지 않는다. Branch 전환은
`skills/github-operations/scripts/git-safety.py switch` 또는 동등한 `git switch --no-overwrite-ignore`로
수행하고, 안전한 별도 worktree를 만들 수 있으면 기존 checkout을 보존한 채 그 경계를 사용한다. 안전한
분리가 불가능하거나 변경 소유권이 불명확하면 checkout 전에 중단해 기존 변경과 필요한 선택을 보고한다.

완료 여부는 작업에 맞는 직접 증거로 검증한다. 예를 들어 repository 생성은 반환된 repository 식별자와
visibility를, push는 대상 remote branch의 갱신을, PR 생성은 number·URL·base/head를 확인한다. PR
merge는 merge commit과 최종 상태를 확인하며, merge queue나 auto-merge의 대기 상태를 완료로
보고하지 않는다. 성공 메시지를 얻기 위해 요청하지 않은 후속 변경을 만들지 않는다.

Issue 해결에서는 PR, branch와 issue 상태를 각각 검증한다. Default branch가 아닌 base를 대상으로 한
PR의 closing keyword는 issue를 자동으로 닫지 않으므로, PR link나 merge만 보고 issue close를
가정하지 않는다. Direct merge, auto-merge와 merge queue는 branch 정리 시점과 허용 option이 다르지만,
모든 경로의 branch cleanup은 실제 merged head SHA, verified remote와 worktree 상태를 확인하는
`git-safety.py cleanup`을 사용한다.

Merge와 workflow 실행은 별도 상태다. Merge가 완료됐더라도 workflow의 실제 trigger와 branch 조건이
맞아야 run이 생성된다. Merge commit, workflow event와 run ID를 연결해 검증하고, 설정되지 않은 run을
기다리거나 registry push 자체를 배포 성공으로 해석하지 않는다.

부분적으로 완료됐으면 완료된 local·remote 상태와 남은 작업을 나눈다. 실패 후 재시도가 duplicate
repository, PR, issue, comment 또는 release를 만들 수 있으면 기존 resource를 먼저 조회하거나
idempotent한 방법을 사용한다.

## Command recipe를 선택한다

모든 명령 작업은 먼저 [공통 GitHub command 규칙](github-operation-recipes.md)을 적용한다. 그런 다음
과제 접수·issue 해결에는 [Issue delivery recipes](github-issue-delivery-recipes.md), repository·push·PR
작업에는 [Repository와 PR recipes](github-repository-pr-recipes.md), release·workflow run에는
[Release와 workflow recipes](github-release-workflow-recipes.md)의 해당 절만 사용한다. Recipe는 이
문서의 권한을 확대하지 않으며, 전체 `gh` manual을 대신하지 않는다.
