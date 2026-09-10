# README 기준의 조사 근거

관찰일: 2026-09-10
목적: 스타가 많은 저장소의 README에서 재사용할 독자 과제를 찾고 [작성·판정 기준](reader-outcomes.md)으로 구체화

## 표본 선정과 해석 범위

[Trendshift의 GitHub trending repositories](https://trendshift.io/github-trending-repositories)에서 `All days`, `All languages`, `Show 25`로 표시된 일반 저장소 25개를 모집단으로 사용
광고인 Featured 항목은 제외하고 화면에 표시된 누적 스타 수로 다시 정렬해 상위 10개 선택
Trendshift의 해당 목록 기본 순서는 트렌딩 등장 횟수이며 누적 스타 순서와 구분
전체 GitHub 또는 Trendshift 전체 저장소의 스타 상위 10개라는 의미는 아님

표의 스타는 해당 화면의 반올림된 관찰값이며 현재 수치나 품질 점수가 아님
README는 조사 시점 기본 브랜치에서 해당 파일의 마지막 변경 commit을 확인한 뒤 고정 permalink로 읽은 원문
분석 범위는 소개, 시작 경로, 대표 사례, 탐색 구조와 관련 세부 절
외부 저장소 설치·명령 실행, 전체 자료 링크 점검과 실제 사용자 이해도 실험은 미수행

스타 수에는 프로젝트 연령·주제·노출·사용자 규모 등의 영향이 있으므로 README 품질이나 인과관계의 증거로 해석하지 않는 원칙
학습·자료 모음이 많은 목적 표본이며 앱·서비스 전체를 대표하는 통계 표본은 아님
아래는 유용한 설계와 반례의 관찰 기록이며 10개 문서 전체에 대한 합격 판정은 아님

## 표본과 원문

표본 내 누적 스타 내림차순이며 README 링크는 commit 고정 원문

| 저장소와 고정 원문 | 표시 스타 | 발견 경로 |
| --- | --- | --- |
| [codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x/blob/b916354a7a6d76ae4b313fd077a13666c2c24727/README.md) | 546.3k | [Trendshift 2841](https://trendshift.io/repositories/2841) |
| [public-apis/public-apis](https://github.com/public-apis/public-apis/blob/8d3f99c8dac264c3538ccfbabc4ffe2b09247a10/README.md) | 478.2k | [Trendshift 1677](https://trendshift.io/repositories/1677) |
| [freeCodeCamp/freeCodeCamp](https://github.com/freeCodeCamp/freeCodeCamp/blob/d2dead4b922d619ccaab7136dc36bbb31173a30d/README.md) | 455.2k | [Trendshift 1778](https://trendshift.io/repositories/1778) |
| [EbookFoundation/free-programming-books](https://github.com/EbookFoundation/free-programming-books/blob/ef1ed02b423e9fc3f0b41ccbcf55e887001ea1b0/README.md) | 396.4k | [Trendshift 2657](https://trendshift.io/repositories/2657) |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md) | 369.1k | [Trendshift 977](https://trendshift.io/repositories/977) |
| [jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university/blob/717298bf219a30d7fb0671285c5f057b1bb74b27/README.md) | 360.7k | [Trendshift 2366](https://trendshift.io/repositories/2366) |
| [obra/superpowers](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md) | 284.1k | [Trendshift 17415](https://trendshift.io/repositories/17415) |
| [practical-tutorials/project-based-learning](https://github.com/practical-tutorials/project-based-learning/blob/30badb256c62560fbc4786c30771e596f21b0f65/README.md) | 282.8k | [Trendshift 2804](https://trendshift.io/repositories/2804) |
| [microsoft/markitdown](https://github.com/microsoft/markitdown/blob/b6e8bbdce628d564c6af031b5f26cda6e818ea10/README.md) | 182.2k | [Trendshift 12961](https://trendshift.io/repositories/12961) |
| [ollama/ollama](https://github.com/ollama/ollama/blob/39df91c9826b3c0c83677f75cd230d8848d287c3/README.md) | 180.5k | [Trendshift 7239](https://trendshift.io/repositories/7239) |

## 관찰에서 기준으로

아래 위치는 위 표의 고정 원문 기준
관찰과 그로부터 도출한 작성 판단을 구분하며 README의 제품 주장을 독립 검증한 것으로 해석하지 않는 방식

| 사례와 관찰 위치 | 원문에서 확인한 설계 | 도출한 기준 |
| --- | --- | --- |
| [build-your-own-x, 3–44행](https://github.com/codecrafters-io/build-your-own-x/blob/b916354a7a6d76ae4b313fd077a13666c2c24727/README.md#L3-L44)과 기술별 목록 | 무엇을 만들어 배우는 자료인지 소개하고 구현 대상별로 분류 | 목적 식별과 과제 중심 탐색, 자료 자체가 결과 예시 |
| [public-apis, 72–150행](https://github.com/public-apis/public-apis/blob/8d3f99c8dac264c3538ccfbabc4ffe2b09247a10/README.md#L72-L150) | 주제별 색인과 API의 인증·HTTPS·CORS 비교 열 | 목록 독자의 선택에 필요한 속성 제공 |
| [freeCodeCamp, 7–44행](https://github.com/freeCodeCamp/freeCodeCamp/blob/d2dead4b922d619ccaab7136dc36bbb31173a30d/README.md#L7-L44)·[52–81행](https://github.com/freeCodeCamp/freeCodeCamp/blob/d2dead4b922d619ccaab7136dc36bbb31173a30d/README.md#L52-L81) | 학습 플랫폼과 과정 진입 링크를 먼저 제공하고 기여 안내는 별도 경로로 연결 | 주 독자의 첫 행동과 기여자 작업 분리 |
| [free-programming-books, 11–13행](https://github.com/EbookFoundation/free-programming-books/blob/ef1ed02b423e9fc3f0b41ccbcf55e887001ea1b0/README.md#L11-L13)·[70–124행](https://github.com/EbookFoundation/free-programming-books/blob/ef1ed02b423e9fc3f0b41ccbcf55e887001ea1b0/README.md#L70-L124) | 검색 진입점과 언어·주제별 자료 문서 연결 | 목록의 첫 사용은 설치보다 탐색 |
| [system-design-primer, 5–44행](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L5-L44)·[182–216행](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L182-L216)·[287–306행](https://github.com/donnemartin/system-design-primer/blob/ae9bbd7b02d90b9866215de185217d33f39ab733/README.md#L287-L306) | 준비 기간별 학습 경로와 해설·코드·다이어그램으로 이어지는 문제 목록 | 독자 조건에 맞는 경로 선택과 구체적인 학습 결과 |
| [coding-interview-university, 58–73행](https://github.com/jwasham/coding-interview-university/blob/717298bf219a30d7fb0671285c5f057b1bb74b27/README.md#L58-L73)·[219–258행](https://github.com/jwasham/coding-interview-university/blob/717298bf219a30d7fb0671285c5f057b1bb74b27/README.md#L219-L258) | 요구 배경지식·목표 분야와 Git 사용 여부별 진행 관리 안내 | 적합성 조건과 실제 독자 능력에 따른 시작 경로 |
| [superpowers, 49–117행](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L49-L117)·[261–311행](https://github.com/obra/superpowers/blob/b36e0829c6d0140e93cfef2ca599b1b07d4a7797/README.md#L261-L311) | 사용 환경별 설치 경로와 스킬별 역할·작업 흐름 설명 | 설치 대상 선택과 설치 후 기대 동작 구분 |
| [project-based-learning, 5–35행](https://github.com/practical-tutorials/project-based-learning/blob/30badb256c62560fbc4786c30771e596f21b0f65/README.md#L5-L35)·[368–401행](https://github.com/practical-tutorials/project-based-learning/blob/30badb256c62560fbc4786c30771e596f21b0f65/README.md#L368-L401) | 학습 목적과 언어별·하위 분야별 예제 분류 | 기술 선택에서 실제 학습 자료까지 이어지는 탐색 |
| [MarkItDown, 9–24행](https://github.com/microsoft/markitdown/blob/b6e8bbdce628d564c6af031b5f26cda6e818ea10/README.md#L9-L24)·[35–82행](https://github.com/microsoft/markitdown/blob/b6e8bbdce628d564c6af031b5f26cda6e818ea10/README.md#L35-L82)·[262–272행](https://github.com/microsoft/markitdown/blob/b6e8bbdce628d564c6af031b5f26cda6e818ea10/README.md#L262-L272) | 사용 목적과 변환 충실도 제약, 선행 조건, CLI·Python 예제 | 적합성·실행 안내·입출력의 구체성 |
| [Ollama, 7–58행](https://github.com/ollama/ollama/blob/39df91c9826b3c0c83677f75cd230d8848d287c3/README.md#L7-L58)·[78–105행](https://github.com/ollama/ollama/blob/39df91c9826b3c0c83677f75cd230d8848d287c3/README.md#L78-L105)·[145–151행](https://github.com/ollama/ollama/blob/39df91c9826b3c0c83677f75cd230d8848d287c3/README.md#L145-L151) | 환경별 설치, 실행 뒤 표시될 선택 안내, 모델 실행·API 예제와 문서 연결 | 첫 사용에서 보게 될 상태와 다음 작업 안내 |

## 그대로 복제하지 않을 부분

[public-apis의 1–24행](https://github.com/public-apis/public-apis/blob/8d3f99c8dac264c3538ccfbabc4ffe2b09247a10/README.md#L1-L24)은 APILayer 홍보가 저장소 자체의 설명보다 먼저 등장하는 구성
비교표의 장점과 별개로 주 독자의 목적 파악을 늦추는 배치는 모범 규칙으로 채택하지 않는 판단

[project-based-learning의 7행](https://github.com/practical-tutorials/project-based-learning/blob/30badb256c62560fbc4786c30771e596f21b0f65/README.md#L7)은 시작 단계로 fork를 안내하지만 자료 열람 자체에 fork가 필요한 근거는 없음
진행 상태를 직접 편집하려는 독자의 fork와 읽기만 하는 독자의 첫 행동을 구분하는 판단

긴 학습 자료나 카탈로그의 분량은 그 자체로 결함이 아니며 모든 도구 README가 같은 분량이어야 한다는 근거도 없음
상단 배너, 인기 배지, 기여자 이미지와 상업 서비스 안내는 프로젝트별 선택이고 품질 합격 요건에서 제외
스킬 모음의 운영 철학이나 특정 에이전트 절차도 README 작성 스킬의 실행 지시로 가져오지 않는 원칙

## 보충 근거와 유지 방법

[GitHub의 README 안내](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)는 프로젝트의 용도·유용성·시작·도움 경로를 주요 역할로 설명하고 긴 상세 문서의 분리와 제목 기반 자동 목차를 안내
이를 필수 절 이름이나 수동 목차의 일괄 요구로 해석하지 않고 독자 과제 중심 구성의 보충 근거로 사용

원문에서 관찰한 설계는 위 표에, 구체적인 충족·미충족·미확인 판정 절차는 이 스킬의 설계로 구분
새 사례나 실제 작성 실패가 기존 기준의 한계를 보여 줄 때 해당 기준과 근거를 좁게 갱신
스타 변화만으로 기준을 재작성하거나 새 순위를 품질 순위로 발표할 필요 없음
