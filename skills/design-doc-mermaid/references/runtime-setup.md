# Mermaid 실행 환경

이 패키지는 `runtime/package.json`과 `runtime/package-lock.json`에 Mermaid CLI와 전이 의존성을 고정한다.
현재 고정 CLI 버전은 11.17.0이다.
일반 실행에는 이미 설치된 호환 renderer를 사용할 수 있으며, 고정 환경을 재현할 때는 두 파일을 함께 사용한다.

## 실행 환경 구성

Node.js/npm과 기존 Chrome이 필요하다.
승인된 설치 대상 디렉터리에 패키지의 `runtime/` 안에 있는 두 JSON 파일을 복사한 뒤, 그 디렉터리에서 다음 명령을 실행한다.

```bash
npm ci --ignore-scripts
```

이 명령은 CLI 의존성을 설치하며 브라우저 설치를 대신하지 않는다.
사용할 Chrome의 실행 경로는 Puppeteer 설정 파일의 `executablePath`로 지정한다.
개인 실행 경로와 설치 결과는 스킬 정본에 기록하지 않는다.
CLI 경로는 helper의 `--mmdc` 인자, `DESIGN_DOC_MERMAID_MMDC` 또는 PATH로 전달할 수 있다.
Puppeteer 설정은 `--puppeteer-config`로 전달한다.
host 설정 파일의 위치와 필드는 [로컬 실행 절차](guides/resilient-workflow.md)에 있다.
설치 후 CLI의 `--version`을 확인하고 실제 다이어그램을 렌더링해 CLI·브라우저 연결을 검증한다.
