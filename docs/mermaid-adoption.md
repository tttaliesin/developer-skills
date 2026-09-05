# Mermaid 스킬 적용 기록

2026-09-05 검토안 1~6과 고정 검증 runtime 구성을 적용했다.
표현 재량 확대안 7과 미검증 그림의 최종 문서 삽입 허용은 적용하지 않았다.

## 관리 범위

`design-doc-mermaid`는 다이어그램 모델링·근거·렌더링·로컬 이미지 변환을 담당한다.
Workspace-rules의 Markdown 작성 규칙에는 이 패키지로 연결하는 지침만 추가한다.
문서 언어·구조·접근성 정책과 외부 게시·운영 권한은 기존 소유자에게 남는다.
현재 작업은 로컬 구현·검증·전역 설치이며 원격 저장소 게시나 Issue lifecycle을 새로 시작하지 않는다.

## 출처와 승인 경계

Upstream은 `spillwavesolutions/design-doc-mermaid`의 `c36d83503d2ba9c1e51638dc2d8a34758a377dea`로 고정했다.
원본 README와 plugin metadata의 MIT 선언, Rick Hightower 저자 표기를 보존했다.
원본에 독립 LICENSE가 없어 선언과 출처를 NOTICE에 기록하고 표준 MIT 전문을 제공했다.
원본에 없는 저작권 연도를 추정하지 않았다.

Code-to-diagram의 Team Review → Approved? → Add to Documentation 조건과 PlantUML opt-in·유형 제한을 유지한다.
기존 승인은 대상·행위·환경·외부 효과·유효 조건이 일치할 때 재사용한다.
도구 통과나 에이전트 검토를 사람 승인으로 기록하지 않는다.
Unicode 기호와 고대비 표현 요건은 유지한다.

## 구현

- 외부 업로드·게시와 로컬 산출물 준비 분리
- 최종 문서 검증·사람 승인과 미검증 초안 구분
- 노드·관계의 근거, 추정·제안·미확인 상태 구분
- 템플릿의 사전 완료 체크 제거
- 도구 부재·브라우저 실패·문법·시간 초과·출력 오류 분류
- 중복 블록의 위치별 이미지 연결과 실제 이미지 생성 검증
- 임시 출력 검증 후 교체 및 실패 시 기존 파일 보존
- 목록 내부의 들여쓴 fence 거부와 비변경 영역 줄바꿈 보존
- 기존 출력·symlink 충돌 거부 및 별도 검토 문서 생성

원본의 문자열 입력·자동 파일명·배치 옵션을 명시적인 입력과 출력 경로로 바꿨다.
설치 패키지의 local workflow가 지원 CLI의 기준이며 upstream 명령과의 전체 호환성을 주장하지 않는다.
추출기는 들여쓰지 않은 최상위 backtick·tilde fence를 지원한다.
Blockquote·list container는 변환하지 않으며 들여쓴 Mermaid fence는 거부한다.
이 범위를 벗어난 문서는 해당 구조를 지원하는 parser나 별도 추출 검증이 필요하다.

## Runtime

`runtime/mermaid/package.json`과 lockfile로 Mermaid CLI 11.17.0 및 전이 의존성을 고정한다.
전용 host 경로에 `npm ci --ignore-scripts`로 설치하고 기존 Chrome을 사용한다.
전역 npm 설치, 브라우저 자동 다운로드, 브라우저 sandbox 완화는 하지 않는다.
Host의 `~/.config/developer-skills/mermaid-runtime.json`은 mmdc와 Puppeteer 설정 경로를 연결한다.
이 개인 경로는 전역 skill package의 정본 내용과 분리한다.

```bash
python3 skills/design-doc-mermaid/scripts/mermaid_to_image.py diagram.mmd diagram.svg
python3 skills/design-doc-mermaid/scripts/extract_mermaid.py source.md --replace-with-images \
  --output-markdown review-candidate.md --image-dir diagrams --image-format svg
```

## 검증

원본의 중복 블록 치환에서 두 번째 블록도 첫 이미지에 연결되고 이미지 파일이 생성되지 않는 결함을 재현했다.
11개 회귀 검사는 중복·외부 fence 예제·닫히지 않은 fence·목록 내부 fence·CRLF·기존 출력·symlink·문법/브라우저/도구 부재·배치 실패 보존을 검증한다.
독립 에이전트는 읽기 전용 게시 준비, 기존 승인 재사용, 민감 오류가 있는 브라우저 실패 시나리오를 검토했다.
발견된 목록 fence와 줄바꿈 보존 결함을 수정한 뒤 재검증했다.

고정 runtime과 기존 Chrome 152로 흐름·시퀀스·상태 예제의 SVG·PNG를 렌더링했다.
시퀀스 예제의 실제 문법 오류가 SYNTAX_ERROR로 분류되는 것도 확인했다.
투명 이미지의 어두운 배경 대비 문제를 보고 기본 배경을 흰색으로 보완했다.
예제는 도구 검증용 가상 시스템이며 실제 배포·기기 동작을 증명하지 않는다.
실제 GitHub·Obsidian·Confluence viewer 렌더링과 사람의 최종 시각 승인은 별도 미검증 범위다.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_mermaid_runtime.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate.py
```
