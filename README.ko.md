<div align="center">

<img src="assets/claude.png" alt="Claude Code Multi-Agent" width="420">

# Claude Code 멀티 에이전트 시스템

**Claude Code를 위한 11개의 전문 에이전트 + 8개의 생산성 도구**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org)
[![Rust](https://img.shields.io/badge/Rust-1.75%2B-orange?style=flat-square&logo=rust)](https://www.rust-lang.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)](https://github.com/BcKmini/Claudecode-Agent)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Compatible-blueviolet?style=flat-square&logo=anthropic)](https://claude.ai/code)
[![Agents](https://img.shields.io/badge/Agents-11-green?style=flat-square)](#에이전트-구성)
[![Tools](https://img.shields.io/badge/Tools-8-informational?style=flat-square)](#도구)
[![Bilingual](https://img.shields.io/badge/Lang-EN%20%7C%20KO-orange?style=flat-square)](#)

**[English README](README.md)** · **[환경 세팅](docs/SETUP.ko.md)** · **[치트시트](docs/AGENT-CHEATSHEET.ko.md)** · **[하네스 가이드](docs/HARNESS-GUIDE.ko.md)** · **[MCP 가이드](docs/MCP-GUIDE.ko.md)** · **[연동 가이드](docs/INTEGRATION.ko.md)** · **[기여 가이드](docs/CONTRIBUTING.ko.md)**

</div>

---

## 이게 뭔가요?

**Claude Code**를 즉시 강화하는 도구 모음:

1. **11개의 전문 서브 에이전트** — 설계, 구현, 리뷰, 테스트, 보안, 하네스 설계, 파이프라인 관리 등 각자 하나에만 집중
2. **`snippet`** — 자주 쓰는 프롬프트를 저장하고 커맨드 한 번에 꺼내 쓰는 프롬프트 매니저
3. **`claude-handoff`** — 세션 전체 컨텍스트(git 상태, 할 일, 메모)를 저장하고 다음 세션에서 복원
4. **`claude-cost`** — 프롬프트 실행 전 비용 추정 및 실제 사용량 추적
5. **`claude-review-diff`** — git diff에서 구조화된 코드 리뷰 프롬프트 자동 생성
6. **`claude-remind`** — 세션 시작 시 TODO 미완료 항목을 자동으로 표시
7. **`claude-harness`** — 에이전트 하네스 정의를 검증하고 템플릿을 생성
8. **`claude-pipeline`** — 다단계 파이프라인 실행을 추적하고 보고서 생성
9. **`claude-lessons`** — 무엇이 왜 실패했고 어떻게 고쳤는지 기록하고, 세션을 넘나들며 검색

모든 도구는 Python CLI와 Claude Code 슬래시 커맨드로 제공됩니다. 핵심 도구는 단일 **Rust 바이너리**(`claude-tools`)로도 제공됩니다.

> **이중 언어 지원:** 모든 에이전트가 사용자의 언어를 감지해 영어(English)와 한국어로 응답합니다.

```
나                       Orchestrator
 │                           │
 └──► "OAuth 로그인 추가" ──► ├──► planner         (아키텍처 설계)
                             ├──► database-expert  (스키마 설계)
                             ├──► implementer      (코드 작성)
                             ├──► reviewer         (코드 리뷰)
                             └──► tester           (테스트 작성)
```

---

## 왜 하네스 엔지니어링인가? — 비용 대비 효과

> 벤치마크 시나리오: TypeScript 파일 하나에서 버그 수정.
> 개발자 단가: $60/hr · 가격: Sonnet 4.6 $3/$15 · Opus 4.7 $5/$25 per 1M tokens.

### 한눈에 보기

| 지표 | Vanilla Claude CLI | 이 하네스 | 변화 |
|------|:-----------------:|:--------:|:----:|
| PR diff 크기 | ~180줄 | ~25줄 | **−86%** |
| PR 리뷰 시간 | ~18분 | ~4분 | **−78%** |
| 첫 번째 승인율 | ~45% | ~85% | **+89%** |
| 재작업 발생률 | ~40% | ~10% | **−75%** |
| 버그 탐지 (리뷰 단계) | ✗ 없음 | ✓ 42–48% 탐지 | **+∞** |
| API 비용 (1회) | ~$0.039 | ~$0.049 | +26% |
| **총 엔지니어링 비용** *(API + 개발자 시간)* | **~$0.32** | **~$0.10** | **3.1× 절약** |

> API 비용은 소폭 증가하지만, 리뷰 시간과 재작업이 크게 줄어
> 총 비용(API + 사람 시간)은 **작업당 3배 저렴**합니다.

### 총 비용 구성

```
Vanilla Claude CLI  ████████████████████████████████  $0.32
                    ├─ API 비용       ██  $0.04
                    ├─ 리뷰 시간      ██████████████  $0.18
                    └─ 재작업 비용    ████████  $0.10

이 하네스           ████████  $0.10
                    ├─ API 비용       ███  $0.05
                    ├─ 리뷰 시간      ████  $0.04
                    └─ 재작업 비용    █  $0.01
```

### PR diff 크기

```
Vanilla  ██████████████████████████████████████  180줄
하네스   ████  25줄  (외과적 수정 프로토콜 적용)
```

### 리뷰 시간

```
Vanilla  ████████████████████  18분
하네스   ████  4분
```

*데이터 출처: Google DORA Report 2025 · Anthropic Engineering Blog · Stripe PR 속도 데이터 · DevToolsAcademy AI 코드 리뷰 벤치마크 2025*

---

## 빠른 시작

### 1. Claude Code 설치

```bash
npm install -g @anthropic-ai/claude-code
claude   # 처음 실행 시 Anthropic 계정 인증
```

### 2. 클론 및 설치

```powershell
# Windows
git clone https://github.com/BcKmini/Claudecode-Agent.git
cd Claudecode-Agent
powershell -ExecutionPolicy Bypass -File setup-agents.ps1
```

```bash
# macOS / Linux
git clone https://github.com/BcKmini/Claudecode-Agent.git
cd Claudecode-Agent
bash setup-agents.sh
```

### 3. 도구 설치 (한 번에)

```bash
make install            # 에이전트 + 슬래시 커맨드 + Python 도구
make install-rust       # 선택: Rust 바이너리 (cargo 필요)
```

### 4. 확인

```
claude
/agents          # → 9개 에이전트 목록
/snippet list    # → 기본 스니펫 목록
```

---

## 에이전트 구성

| # | 에이전트 | 모델 | 자율성 | 역할 |
|---|---------|------|:---:|------|
| 00 | **orchestrator** | Opus | L2 | 작업 분해 및 서브 에이전트 위임 총괄 |
| 01 | **planner** | Opus | L1 | 아키텍처·설계 결정 — 읽기 전용 |
| 02 | **implementer** | Sonnet | L2 | 실제 코드 작성·수정 |
| 03 | **reviewer** | Sonnet | L1 | 버그·보안·품질·성능 리뷰 — 읽기 전용 |
| 04 | **tester** | Sonnet | L2 | 유닛·통합·E2E 테스트 작성 |
| 05 | **security-auditor** | Opus | L1 | OWASP Top 10 기준 보안 감사 — 읽기 전용 |
| 06 | **performance-optimizer** | Sonnet | L2 | 성능 병목 분석 및 최적화 |
| 07 | **database-expert** | Sonnet | L2 | DB 스키마 설계·쿼리·마이그레이션 |
| 08 | **documenter** | Haiku | L3 | README·API 문서·인라인 주석 작성 |
| 09 | **harness-designer** | Opus | L1 | 타이트·느슨·적응형 AI 하네스 설계 |
| 10 | **pipeline-orchestrator** | Opus | L2 | 컨텍스트 격리 기반 다단계 파이프라인 실행 관리 |

> **모든 에이전트가 이중 언어를 지원합니다** — 사용자 언어를 감지해 한국어 또는 영어로 응답합니다.

> 각 에이전트는 자기 역할에 관련된 컨텍스트만 가집니다. 병렬 실행(planner + security-auditor 동시)으로 작업 시간도 단축됩니다.

> **자율성**(L0 = 사람이 전부 담당 → L4 = 완전 자율)은 하네스 유형과 별개의 축입니다 — 출력이 얼마나 제약되는지가 아니라, 얼마나 사람이 확인해야 하는지를 나타냅니다. 자세한 내용은 [자율성 레벨](docs/HARNESS-GUIDE.ko.md#자율성-레벨-l0-l4) 참고.

> 바로 쓸 수 있는 프롬프트 24개 이상 → [AGENT-CHEATSHEET.ko.md](docs/AGENT-CHEATSHEET.ko.md)

---

## 도구

Claude Code가 기본으로 제공하지 않는 기능을 채우는 8가지 도구.

### 슬래시 커맨드 한눈에 보기

| 커맨드 | 기능 |
|--------|------|
| `/snippet` | 프롬프트 템플릿 실행·저장·목록 |
| `/handoff` | 세션 컨텍스트 저장/로드 |
| `/cost` | API 비용 추정 및 추적 |
| `/harness` | AI 하네스 정의 설계 및 검증 |
| `/pipeline` | 다단계 AI 파이프라인 실행 및 추적 |
| `/review-diff` | git diff 기반 코드 리뷰 프롬프트 |
| `/remind` | 세션 시작 시 TODO 미완료 항목 표시 |
| `/lessons` | 실패 원인과 해결법 기록 및 회상 |

---

### 도구 1 — `snippet` — 개인 프롬프트 매니저

Claude 프롬프트를 이름으로 저장하고, 한 커맨드로 꺼내 씁니다.

```bash
snippet list                                   # 전체 목록
snippet run full-pipeline | claude             # Claude에 바로 파이프
snippet save myfix "Fix {{BUG}} in {{FILE}}"   # 템플릿 변수 사용
snippet search security
snippet export my-backup.json
```

```
/snippet list
/snippet run full-pipeline
/snippet search security
```

**기본 스니펫 20개** — `full-pipeline`, `code-review`, `security-audit`, `write-tests`, `refactor`, `db-schema` 등. [snippets/defaults.json](snippets/defaults.json) 참고.

---

### 도구 2 — `claude-handoff` — 세션 연속성

세션 전체 컨텍스트를 저장하고 다음 세션에 바로 복원합니다.

```bash
claude-handoff save --note "OAuth 완료, 다음: 이메일 인증"
claude-handoff load | claude    # 바로 재개
claude-handoff list
claude-handoff clean --days 30
```

```
/handoff save
/handoff load
/handoff list
```

**핸드오프에 담기는 정보:** git 브랜치, 최근 커밋 5개, 워킹 트리 상태, diff stat, TODO.md 내용, 요약 메모, 재개 프롬프트.

---

### 도구 3 — `claude-cost` — 비용 추정 & 추적

실행 전에 프롬프트 비용을 확인하고 실제 사용량을 추적합니다.

```bash
claude-cost estimate --snippet full-pipeline --agents 9
claude-cost month
claude-cost set-budget 20.00
```

```
/cost estimate full-pipeline
/cost month
/cost agents
```

| 모델 | 입력 (100만 토큰) | 출력 (100만 토큰) |
|------|-----------------|-----------------|
| Opus | $15.00 | $75.00 |
| Sonnet | $3.00 | $15.00 |
| Haiku | $0.25 | $1.25 |

---

### 도구 4 — `claude-review-diff` — git diff 코드 리뷰

현재 git 변경사항을 구조화된 코드 리뷰 프롬프트로 변환해 Claude에 바로 파이프합니다.

```bash
claude-review-diff                       # 스테이징 전 변경사항 리뷰
claude-review-diff --staged              # 스테이징된 변경사항 리뷰
claude-review-diff --base main           # 브랜치를 main과 비교
claude-review-diff --focus security      # 보안 중점 리뷰
claude-review-diff | claude              # Claude에 바로 파이프
```

```
/review-diff
/review-diff --staged
/review-diff --base main --focus security
```

**Focus 옵션:** `security` · `performance` · `correctness` · `style` · `tests` · `all`

출력은 심각도 순 정렬: **Critical → Major → Minor → Nit**

---

### 도구 5 — `claude-remind` — 세션 시작 리마인더

TODO.md / TASKS.md / CLAUDE.md에서 미완료 체크박스(`- [ ]`)를 스캔해 세션 재개 프롬프트를 출력합니다.

```bash
claude-remind                # 미완료 항목 전체 + 재개 프롬프트
claude-remind --quiet        # 개수만 표시
claude-remind | claude       # Claude에 바로 파이프
```

```
/remind
/remind --quiet
```

**세션 종료/시작 워크플로우:**

```bash
# 세션 종료
claude-handoff save --note "Auth 완료, 다음: 이메일 인증"

# 세션 시작
claude-remind | claude         # 미완료 항목 확인
claude-handoff load | claude   # 전체 컨텍스트 복원
```

---

### 도구 6 — `claude-harness` — 하네스 검증기 & 템플릿 생성기

에이전트 하네스 정의를 검증하고 커맨드라인에서 하네스 템플릿을 생성합니다.

```bash
claude-harness check-all                         # agents/ 전체 에이전트 검증
claude-harness validate agents/09-harness-designer.md   # 단일 에이전트 검증
claude-harness template tight my-specialist      # 타이트 하네스 템플릿 출력
claude-harness template adaptive my-orchestrator # 적응형 하네스 템플릿 출력
claude-harness autonomy                          # L0-L4 자율성 레벨 참조표 출력
```

```
/harness design 슬로우 쿼리 탐지 및 패치 자동화
/harness validate agents/03-reviewer.md
/harness types
/harness autonomy
```

**에이전트별 검사 항목:**
- 역할이 명확히 스코프되어 있는가
- 출력 형식이 제약되어 있는가
- 금지 행동이 명시되어 있는가
- 도구 목록이 최소한인가
- 자율성 레벨(L0-L4)이 선언되어 있는가
- 이중 언어 지원이 있는가

---

### 도구 7 — `claude-pipeline` — 파이프라인 추적기 & 리포터

다단계 AI 파이프라인 실행을 추적하고, 단계별 결과를 기록하고, 마크다운 실행 보고서를 생성합니다.

```bash
claude-pipeline init slow-query-fix              # 파이프라인 생성 및 활성화
claude-pipeline stage "detection" start
claude-pipeline stage "detection" pass --note "슬로우 쿼리 3개 발견"
claude-pipeline stage "patch-gen" start
claude-pipeline stage "patch-gen" warn --note "1개 쿼리는 안전한 수정 불가"
claude-pipeline status                           # 실시간 상태 표시
claude-pipeline report                           # 마크다운 실행 보고서
claude-pipeline list                             # 저장된 모든 파이프라인
```

```
/pipeline run 슬로우 쿼리 분석 및 리뷰 루프 포함 패치 생성
/pipeline status
/pipeline stages
```

---

### 도구 8 — `claude-lessons` — 실패/교훈 기록

무엇이 왜 실패했고 어떻게 고쳤는지 기록해서, 다음 세션(또는 다른 에이전트)이 같은 실수를 반복하지 않게 합니다. 세션 단위로 정리되는 `claude-handoff`와 달리, 교훈은 무기한 누적되며 태그·키워드로 검색할 수 있습니다.

```bash
claude-lessons add --title "마이그레이션 타임아웃" --tags db,migration \
  --symptom "ALTER TABLE이 프로덕션을 4분간 잠금" \
  --cause "lock_timeout 미설정" \
  --fix "DDL 전에 SET lock_timeout='2s' 추가"
claude-lessons list --tag db
claude-lessons search lock_timeout
claude-lessons context | claude    # 최근 교훈을 새 세션에 파이프
```

```
/lessons add
/lessons list --tag db
/lessons context
```

**전형적인 워크플로우:**

```bash
# 까다로운 실패를 디버깅한 직후
claude-lessons add

# 같은 영역을 다시 건드리는 세션 시작 시
claude-lessons context --tag db | claude
```

---

### Rust 바이너리 — `claude-tools`

모든 도구를 의존성 없는 단일 바이너리로 컴파일 — Python 불필요.

```bash
cd rust && cargo build --release
# 또는: make install-rust

claude-tools snippet list
claude-tools handoff save --note "완료"
claude-tools cost month
claude-tools watch              # 실시간 비용 모니터
claude-tools watch --interval 5
claude-tools env                # 환경 헬스체크
```

**`claude-tools env` 출력:**

```
Claude Code Environment

  ✓ ANTHROPIC_API_KEY   sk-ant-…abcd
  ✓ ~/.claude/           exists
  ✓ ~/.claude/agents/    9 agents installed
  ✓ ~/.claude/commands/  5 commands: snippet, handoff, cost, review-diff, remind
  ✓ handoffs             3 saved, latest: 20250608-143022.md
  ✓ sessions             4 projects, 12 session files
```

---

## Makefile

```bash
make help           # 전체 타겟 목록
make install        # 에이전트 + 슬래시 커맨드 + Python 도구
make install-rust   # Rust 바이너리 빌드 및 설치
make build          # cargo build --release
make test           # 빠른 스모크 테스트 (추가 의존성 없음)
make tox            # 전체 Python 테스트 매트릭스(py38-py313) + lint + fmt-check
make msrv           # Rust 크레이트가 명시된 MSRV에서 빌드되는지 검증
make lint           # clippy (Rust)
make fmt            # rustfmt + ruff format (범위 한정 — CONTRIBUTING.ko.md 참고)
make status         # git log + 도구 설치 상태 확인
make env            # Claude 환경 헬스체크
make clean          # 빌드 아티팩트 제거
```

---

## 저장소 구조

```
claude-code-use/
├── Makefile                          ← 빌드 / 설치 / 테스트 / 정리
├── tox.ini                           ← Python 테스트 매트릭스 + lint + fmt-check
├── pyproject.toml                    ← ruff 설정 (이 저장소 스타일에 맞게 범위 한정)
├── install.sh                        ← 원라인 설치 스크립트
├── setup-agents.ps1                  ← Windows 빠른 설치
├── setup-agents.sh                   ← macOS / Linux 빠른 설치
│
├── agents/                           ← 에이전트 정의 → ~/.claude/agents/
│   ├── 00-orchestrator.md  ·  01-planner.md  ·  02-implementer.md
│   ├── 03-reviewer.md  ·  04-tester.md  ·  05-security-auditor.md
│   ├── 06-performance-optimizer.md  ·  07-database-expert.md
│   ├── 08-documenter.md
│   ├── 09-harness-designer.md        ← 하네스 설계 에이전트
│   └── 10-pipeline-orchestrator.md   ← 파이프라인 관리 에이전트
│
├── .claude/commands/                 ← 슬래시 커맨드 → ~/.claude/commands/
│   ├── snippet.md  ·  handoff.md  ·  cost.md
│   ├── review-diff.md  ·  remind.md
│   ├── harness.md  ·  pipeline.md
│   └── lessons.md                    ← 신규 /lessons
│
├── snippets/defaults.json            ← 기본 프롬프트 템플릿 20개
│
├── tools/
│   ├── snippet.py  ·  claude-handoff.py  ·  claude-cost.py
│   ├── claude-review-diff.py  ·  claude-remind.py
│   ├── claude-harness.py  ·  claude-pipeline.py
│   ├── claude-lessons.py             ← 신규 실패/교훈 기록
│   ├── install-tools.ps1  ·  install-tools.sh
│
├── tests/                            ← tools/*.py용 pytest 스위트
│   ├── conftest.py                   ← run_tool / home / git_repo 픽스처
│   └── test_*.py                     ← 도구당 파일 하나
│
├── rust/claude-tools/src/
│   ├── main.rs  ·  snippet.rs  ·  handoff.rs  ·  cost.rs
│   ├── watch.rs  ·  env.rs  ·  colors.rs
│
├── examples/
│   └── mcp-lessons-server.py         ← 신규 MCP 서버 예제
│
└── docs/
    ├── SETUP.md / SETUP.ko.md
    ├── AGENT-CHEATSHEET.md / .ko.md
    ├── HARNESS-GUIDE.md / .ko.md
    ├── MCP-GUIDE.md / .ko.md         ← 신규
    ├── INTEGRATION.md / .ko.md
    ├── CONTRIBUTING.md / .ko.md
    └── CLAUDE.md / .ko.md
```

---

## 컨텍스트 비용 관리

| 상황 | 명령 |
|------|------|
| 작업 단계 완료 후 | `/compact` |
| 완전히 다른 작업 시작 | `/clear` |
| 비용 확인 | `/cost` |
| 실시간 비용 모니터 | `claude-tools watch` |
| 환경 상태 확인 | `claude-tools env` |
| 미완료 작업으로 재개 | `claude-remind \| claude` |
| 전체 세션 복원 | `claude-handoff load \| claude` |
| 이 영역의 과거 실패 회상 | `claude-lessons context --tag X \| claude` |

---

## 트러블슈팅

**에이전트가 `/agents`에 안 보임**
```bash
ls ~/.claude/agents/*.md   # 파일 존재 확인 후 Claude Code 재시작
```

**Agent Teams가 작동 안 함**
```powershell
# Windows — "1" 이 출력되어야 함
[System.Environment]::GetEnvironmentVariable("CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS","User")
```
```bash
# macOS / Linux
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS   # "1" 이 출력되어야 함
```

**`make install-tools` 후 툴이 없다고 나올 때**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

**Windows에서 `make`가 없을 때**
```powershell
winget install GnuWin32.Make
```

---

## 전체 문서 목록

| 문서 | 한국어 | English |
|------|--------|---------|
| 환경 세팅 가이드 | [SETUP.ko.md](docs/SETUP.ko.md) | [SETUP.md](docs/SETUP.md) |
| 에이전트 치트시트 | [AGENT-CHEATSHEET.ko.md](docs/AGENT-CHEATSHEET.ko.md) | [AGENT-CHEATSHEET.md](docs/AGENT-CHEATSHEET.md) |
| 하네스 설계 가이드 | [HARNESS-GUIDE.ko.md](docs/HARNESS-GUIDE.ko.md) | [HARNESS-GUIDE.md](docs/HARNESS-GUIDE.md) |
| MCP 서버 가이드 | [MCP-GUIDE.ko.md](docs/MCP-GUIDE.ko.md) | [MCP-GUIDE.md](docs/MCP-GUIDE.md) |
| 통합 가이드 | [INTEGRATION.ko.md](docs/INTEGRATION.ko.md) | [INTEGRATION.md](docs/INTEGRATION.md) |
| 기여 가이드 | [CONTRIBUTING.ko.md](docs/CONTRIBUTING.ko.md) | [CONTRIBUTING.md](docs/CONTRIBUTING.md) |
| 코딩 가이드라인 | [CLAUDE.ko.md](docs/CLAUDE.ko.md) | [CLAUDE.md](docs/CLAUDE.md) |

---

## 기여하기

- **새 도구 아이디어** → [Feature Request](https://github.com/BcKmini/Claudecode-Agent/issues/new?template=feature_request.md)
- **버그 발견** → [Bug Report](https://github.com/BcKmini/Claudecode-Agent/issues/new?template=bug_report.md)
- **새 스니펫** → `snippets/defaults.json`에 추가 후 PR

전체 가이드 → [CONTRIBUTING.ko.md](docs/CONTRIBUTING.ko.md)

---

## 라이선스

[MIT](LICENSE)
