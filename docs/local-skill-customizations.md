# 외부 스킬의 승인된 개인 수정

이 저장소는 doc-coauthoring, find-skills, OpenAI Docs와 PDF의 승인된 개인 수정 근거와 비교용 patch를 유지보수한다.
System·plugin 관리 스킬의 설치본과 upstream 소유권은 기존 관리 주체에 남는다.
이 문서와 [비교용 patch](../patches/agent-autonomy-local.patch)는 설치 패키지가 아니며 `upstream-lock.json`의 재구성 파이프라인에 넣지 않는다.
Patch 내부의 당시 절대 경로는 원본 증거로 보존하며 현재 적용 대상을 뜻하지 않는다.

## 승인 및 버전 기록

2026-09-05 승인된 개인 수정은 기존 workspace-rules의 patch를 바이트 그대로 보존했다.
2026-09-06 검토에서 OpenAI Docs의 로컬 지침 검토 예외와 PDF의 필수 결함·미적 선호 구분이 활성 설치본에 누락되어, 당시 본문과 대조한 복원 대상으로 확인했다.
PDF patch의 대상은 당시 활성 버전 `26.904.11930`으로 갱신했으며 다른 upstream 지시는 보존한다.
이는 당시 확인 기록이며 현재 활성 버전이나 복원 완료를 보증하지 않는다.
이관 시 원본 revision·미commit 상태·파일 SHA-256은 [출처 기록](ownership-migration-source.json)에 보존했다.

## Upstream 갱신 후 대조

1. 실제 활성 package 경로·버전과 기존 개인 수정 확인
2. 승인 기록과 새 upstream의 해당 지시 비교
3. 승인된 의미가 누락된 부분에 한해 검토 가능한 diff 준비
4. 기존 승인 범위에 포함되는 적용과 관련 검증 수행
5. 비교 기준·적용 결과·검증 한계 기록

이전 patch를 새 upstream에 자동 적용하거나 더 새로운 지시를 통째로 덮어쓰지 않는다.
승인은 같은 대상·행위·환경·유효 조건에 한해 재사용하며 별도 운영·설치 권한을 추론하지 않는다.
일반 package provenance 통과만으로 이 네 외부 스킬의 개인 수정까지 검증됐다고 보고하지 않는다.
이번 소유권 이관은 설치본이나 활성 plugin을 변경하지 않는다.
