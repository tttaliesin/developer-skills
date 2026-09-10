# GitHub release and workflow recipes

이 문서는 release 발행과 workflow run 실행·진단을 수행하는 command recipe다. 먼저
[GitHub 운영 규칙](github-operations.md)과
[공통 GitHub command 규칙](github-operation-recipes.md)을 적용한다.

## Release를 발행한다

Release 재시도 전에는 대상 repository URL과 일치하는 `<TARGET_REMOTE>`, tag와 기존 release를 모두
확인한다.

```bash
python3 <GITHUB_OPERATIONS_SKILL>/scripts/git-safety.py resolve-remote \
  --repository . \
  --target-url <TARGET_REPOSITORY_URL>
git ls-remote --exit-code --tags <TARGET_REMOTE> refs/tags/<TAG>
gh release view <TAG> -R <OWNER/REPO> \
  --json tagName,name,isDraft,isPrerelease,isImmutable,targetCommitish,url
```

기본 recipe는 remote에 이미 존재하는 tag만 release로 발행한다. `gh release create`가 tag를 암묵적으로
생성하게 하지 않으며, 새 tag 생성이 요청에 포함된 경우에만 별도 Git 절차로 tag를 만든다.

```bash
gh release create <TAG> -R <OWNER/REPO> \
  --verify-tag \
  --title "<TITLE>" \
  --notes-file <NOTES_FILE>
```

발행 결과는 다시 조회해 tag, draft·prerelease 상태와 URL을 확인한다.

```bash
gh release view <TAG> -R <OWNER/REPO> \
  --json tagName,name,isDraft,isPrerelease,isImmutable,targetCommitish,url
```

Asset 업로드, latest 변경, discussion 생성은 release 발행만으로 승인된 것으로 해석하지 않는다.

## Workflow run을 조회하고 진단한다

최근 run을 workflow와 commit으로 좁히고, 사람이 읽는 제목 대신 `databaseId`와 `headSha`로 대상을
확정한다.

```bash
gh run list -R <OWNER/REPO> \
  --workflow <WORKFLOW> \
  --commit <SHA> \
  --json databaseId,status,conclusion,headSha,url,workflowName,event
```

Run의 상태와 결론을 구조적으로 조회하고, 실패했을 때만 실패 step log를 읽는다.

```bash
gh run view <RUN_ID> -R <OWNER/REPO> \
  --json databaseId,status,conclusion,headSha,url,workflowName,event
gh run view <RUN_ID> -R <OWNER/REPO> --log-failed
```

사용자가 `workflow_dispatch` 실행을 요청했고 workflow가 이를 지원할 때만 명시적인 ref와 input으로
trigger한다.

```bash
gh workflow run <WORKFLOW> -R <OWNER/REPO> \
  --ref <REF> \
  -f <KEY>=<VALUE>
```

새 run은 즉시 목록에 보이지 않을 수 있다. `<REF>`의 SHA와 `event=workflow_dispatch`를 함께 사용해
bounded retry로 대상 run을 찾는다. 완료까지 감시하도록 요청받았으면 다음 명령을 사용할 수 있다.

```bash
gh run watch <RUN_ID> -R <OWNER/REPO> --compact --exit-status
```

`gh run watch`는 credential 종류에 따라 지원되지 않을 수 있다. `run list`나 `run view`가 성공했는데
watch만 실패하면 이를 GitHub 작업 전체의 인증 실패로 확대하지 않고 bounded `run view` polling으로
대체한다.
