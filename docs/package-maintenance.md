# 자체 스킬과 출처 도구 유지보수

`parallel-worktree-development`는 workspace-rules에서 이관한 자체 스킬이다.
`upstream-lock.json`에 등록된 공개 upstream 수정 패키지와 별도로 관리하며 `update-patch.py`에 전달하지 않는다.
필수 workflow와 소유권 경계는 package 안에 포함하고, GitHub 작업은 설치된 `github-operations`로 연결한다.

## 출처와 권리

[이관 출처](ownership-migration-source.json)는 승인된 작업 트리의 기준 revision, 미commit 상태와 원본 해시를 보존한다.
원본 workspace-rules snapshot에 별도 LICENSE 파일이 없으므로 이관한 스킬과 provenance 도구에 MIT 등 새 라이선스를 부여하지 않는다.
기존 공개 패키지의 개별 라이선스는 그대로 유지한다.
재배포 권한은 이 기록 자체로 부여되지 않는다.

## 독립 provenance 도구

`scripts/skill-provenance.py` 버전 `2.0.0`은 Python 3 표준 라이브러리와 Git만 사용하며 다른 checkout에 의존하지 않는다.
`write PACKAGE`, `check PACKAGE --installed PATH`, `--version` 인터페이스를 제공한다.
새 기록은 schema 2이며 canonical repository locator, 저장소 상대 package 경로, 기준 revision, 미commit 여부와 SHA-256 inventory를 담는다.
HTTPS 원격 URL 또는 안정적인 `urn:` 식별자를 사용하며 인증정보나 로컬 절대 경로는 기록하지 않는다.
`--repository`가 없으면 Git의 `skill.provenanceRepository`, `remote.origin.url` 순서로 확인한다.
이 저장소는 원격이 없는 로컬 소유자이므로 `urn:local-repository:developer-skills`를 명시한다.

저장소 루트에서 다음 명령으로 선택한 패키지의 최종 bytes를 기록·검증한다.

```bash
python3 scripts/skill-provenance.py --version
python3 scripts/skill-provenance.py write skills/parallel-worktree-development --repository urn:local-repository:developer-skills
python3 scripts/skill-provenance.py check skills/parallel-worktree-development --repository urn:local-repository:developer-skills
python3 -B -m unittest discover -s tests -p test_skill_provenance.py
python3 scripts/validate.py
```

출처 기록은 자기 자신의 bytes와 Git·Python 캐시를 inventory에서 제외한다.
Package 내부 symlink는 지원하지 않는다.
미commit 여부는 기록 생성 시 저장소 전체 상태이며 출처 기록 파일 자체의 변경은 제외한다.
검증은 source locator·bytes와 기준 revision의 HEAD 조상 관계를 확인하므로 얕은 clone에서는 해당 history를 확보해야 한다.
이 검사는 cryptographic 서명이나 작성자 인증을 제공하지 않는다.
동일 repository locator와 상대 package 경로라면 checkout 이동과 실행 cwd 변경을 허용한다.
기존 schema 없는 기록은 기존 절대 경로 검증으로 읽으며 경로가 달라지면 검토 후 `write`로 재생성한다.
내용이 그대로인 기존 패키지의 기록을 이관만을 이유로 덮어쓰지 않는다.

소비 저장소는 도구를 정확한 bytes로 vendor하고 버전·SHA-256·소유 저장소·원본 revision을 별도 기록한다.
갱신은 소유 저장소에서 수정·검증한 뒤 소비 저장소가 검토하여 동일 파일로 교체하는 방식이다.
소비 저장소에서 별도 fork를 유지하거나 실행 시 소유 저장소 checkout 경로를 호출하지 않는다.

## 패키지 갱신과 설치

자체 스킬은 해당 package를 직접 수정하고 Skill Creator의 `quick_validate.py`, Markdown 검사, package 내부 링크 검사와 provenance를 검증한다.
공개 upstream 패키지는 기존 patch 재구성 검증을 별도로 유지한다.
`validate.py`는 두 분류의 모든 package가 명시되어 있는지 검사하지만 자체 스킬을 upstream patch로 재구성하지 않는다.
새 파일과 참조가 최종 패키지 안에 포함된 뒤 provenance를 재생성한다.

전역 설치는 별도 승인 범위에서 README의 Skills CLI 절차를 사용하며 설치 경로의 실제 bytes까지 비교한다.
이관 commit이나 로컬 검증만으로 기존 설치본이 갱신되었다고 보고하지 않는다.
