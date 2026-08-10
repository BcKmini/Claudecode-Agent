[← README로 돌아가기](../README.md)

**[English](MCP-GUIDE.md)** · **한국어**

# MCP 서버 가이드

이 프로젝트의 모든 도구(`snippet`, `claude-handoff`, `claude-cost`, `claude-lessons` 등)는 직접 실행하고 대개 `claude`에 파이프하는 CLI입니다. **MCP 서버**는 이 수동 단계를 없앱니다 — 같은 기능을 Claude가 대화 중간에 직접 호출할 수 있는 도구로 노출시켜서, 사람이 명령어를 실행하고 출력을 붙여넣을 필요가 없게 만듭니다.

---

## 슬래시 커맨드 vs 수동 파이프 vs MCP — 언제 무엇을 쓸까

| | 사람이 실행 | Claude가 호출 | 적합한 상황 |
|---|---|---|---|
| **슬래시 커맨드** (`/lessons add`) | 예, Claude Code 안에서 | 아니오 | *언제* 실행할지 사람이 결정 — 명시적인 1회성 행동 |
| **수동 파이프** (`claude-lessons context \| claude`) | 예, 셸에서 | 아니오 | *새* 세션에 컨텍스트를 주입할 때 (아직 컨텍스트가 없음) |
| **MCP 서버** | 아니오 | 예, 대화 중간에 | Claude가 *언제* 필요한지 스스로 판단해야 하는, 이미 진행 중인 작업 안에서의 반복 조회 |

**경험칙:** 같은 CLI 명령을 여러 번 실행해서 결과를 Claude에 붙여넣고 있다면 MCP 서버 후보입니다. 반면 의도적인 체크포인트 행동(핸드오프 저장, 교훈 기록)이라면 슬래시 커맨드가 "누가 통제하는지"를 더 정직하게 드러냅니다 — 사람의 체크포인트를 자동화로 없애지 마세요 ([자율성 레벨](HARNESS-GUIDE.ko.md#자율성-레벨-l0-l4) 참고).

이 프로젝트에서 가장 명확한 후보는 `claude-lessons`입니다: 과거 실패를 회상하는 것은, 사람이 먼저 기억해서 실행해야 하는 게 아니라 Claude가 위험한 영역을 건드리기 직전에 스스로 트리거해야 하는 전형적인 조회 작업입니다.

---

## MCP 서버의 최소 구조

[Python MCP SDK](https://modelcontextprotocol.io)는 데코레이터 기반 서버(`FastMCP`)를 제공합니다 — 함수를 정의하고 데코레이터를 붙이면, docstring이 모델이 보는 도구 설명이 됩니다:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(arg: str) -> str:
    """모델이 이 도구를 언제 호출할지 판단하는 데 쓰는 한 줄 설명."""
    return do_something(arg)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

구조는 이게 전부입니다: `FastMCP` 인스턴스 하나, 기능마다 `@mcp.tool()` 함수 하나, Claude Code와 로컬로 연동할 때는 `stdio` 트랜스포트.

> **버전 주의:** 현재 `pip install mcp`는 이 API를 크게 바꾼 **2.x** 버전을 설치합니다 (`FastMCP` 위치/이름 변경). 이 가이드와 [`examples/mcp-lessons-server.py`](../examples/mcp-lessons-server.py)는 안정적으로 자리잡은 **1.x** 라인을 대상으로 합니다 — 2.x 마이그레이션 가이드를 읽지 않았다면 `pip install "mcp>=1.2,<2"`로 버전을 고정하세요.

---

## 실전 예제: MCP 서버로 만든 `claude-lessons`

[`examples/mcp-lessons-server.py`](../examples/mcp-lessons-server.py)는 `tools/claude-lessons.py`를 감싸서 3개의 도구를 노출합니다:

- `add_lesson(title, symptom, cause, fix, tags)`
- `search_lessons(query)`
- `recent_lessons(limit, tag)` — 실패 이력이 있는 영역을 건드리기 전에 자동으로 호출할 가치가 가장 큰 도구

파일명에 하이픈이 있어 일반적인 `import`가 안 되는 `tools/claude-lessons.py`를 파일 경로로 로드해서, 교훈 파일 형식을 다시 구현하지 않고 저장 함수를 그대로 재사용합니다 — 그래서 CLI와 MCP 서버가 교훈이 어디에 저장되고 어떤 형식인지에 대해 항상 일치합니다.

`tools/`가 아니라 `examples/`에 둔 이유는, `docs/CONTRIBUTING.md`가 `tools/` 아래 모든 것을 의존성 없는(stdlib only) 상태로 유지하도록 요구하는데 `mcp` 패키지는 외부 의존성이기 때문입니다.

### 실행해보기

```bash
pip install "mcp>=1.2,<2"
python3 examples/mcp-lessons-server.py   # stdio 서버 시작, 클라이언트 대기
```

### Claude Code에 등록

```bash
claude mcp add lessons -- python3 /path/to/examples/mcp-lessons-server.py
```

등록하면 `claude-lessons context | claude` 없이도, 실패 이력이 있는 영역을 작업하려 할 때 Claude가 `recent_lessons`를 직접 호출할 수 있습니다.

---

## 이 프로젝트의 다른 도구에 적용하기

같은 패턴은 사람이 파이프하는 대신 Claude가 직접 조회해야 하는 도구라면 어디든 적용됩니다:

| 도구 | MCP로 감쌀 가치가 있는가? | 이유 |
|---|---|---|
| `claude-lessons` | 예 (위 참고) | 반복적인 조회, 특히 읽기 경로는 위험도 낮음 |
| `claude-remind` | 경우에 따라 | 작업 시작 시 Claude가 호출하면 유용하지만 `/remind`로도 충분 |
| `claude-cost` | 읽기 전용 부분만 | 지출 조회는 괜찮지만 `set-budget`은 수동/슬래시 커맨드로 유지 |
| `claude-handoff save` | 아니오 | 핸드오프 저장은 의도적인 사람의 체크포인트 — 슬래시 커맨드 유지 |
| `claude-pipeline` | 아니오 | 단계 전환은 자동 트리거가 아니라 명시적이고 리뷰 가능해야 함 |

판단이 애매하면 **쓰기/변경 행동은 MCP 도구로 감싸지 않는 쪽을 기본값**으로 하세요 — 대화 중간에 조용히 호출될 수 있는 에이전트는, 사람이 명시적으로 입력하는 슬래시 커맨드보다 더 높은 자율성 레벨입니다 ([자율성 레벨](HARNESS-GUIDE.ko.md#자율성-레벨-l0-l4) 참고).

---

*참고:*
- *[`examples/mcp-lessons-server.py`](../examples/mcp-lessons-server.py) — 실행 가능한 예제*
- *[`tools/claude-lessons.py`](../tools/claude-lessons.py) — 이 서버가 감싸는 CLI*
- *[HARNESS-GUIDE.ko.md](HARNESS-GUIDE.ko.md) — 자율성 레벨과 하네스 설계*
