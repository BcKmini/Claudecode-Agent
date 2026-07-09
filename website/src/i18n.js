import { ref, computed } from 'vue'

const stored = typeof localStorage !== 'undefined' && localStorage.getItem('lang')
const browserKo = typeof navigator !== 'undefined' && navigator.language?.startsWith('ko')
export const lang = ref(stored || (browserKo ? 'ko' : 'en'))

export function setLang(l) {
  lang.value = l
  try {
    localStorage.setItem('lang', l)
  } catch {}
}

const messages = {
  en: {
    nav: {
      agents: 'Agents',
      pipeline: 'Pipeline',
      tools: 'Tools',
      benchmark: 'Benchmark',
      start: 'Get Started',
      github: 'GitHub',
    },
    hero: {
      badge: 'Open Source · MIT License',
      title1: 'One prompt.',
      title2: 'Eleven specialists.',
      subtitle:
        'A drop-in multi-agent system for Claude Code — 11 specialized AI agents and 7 productivity tools that plan, build, review, test, and secure your code.',
      ctaPrimary: 'Get Started',
      ctaSecondary: 'View on GitHub',
      statAgents: 'Agents',
      statTools: 'Tools',
      statSnippets: 'Snippets',
      statLangs: 'Languages',
    },
    stats: {
      title: 'Why harness engineering?',
      subtitle:
        'Benchmark: fixing a bug in a single TypeScript file. API cost rises slightly — total engineering cost drops 3×.',
      diffSize: 'smaller PR diffs',
      diffDetail: '180 → 25 lines, surgical edit protocol',
      reviewTime: 'less review time',
      reviewDetail: '18 min → 4 min per PR',
      approval: 'first-pass approval',
      approvalDetail: 'up from ~45% with vanilla CLI',
      cost: 'cheaper per task',
      costDetail: 'total cost: API + human time',
      sources:
        'Sources: Google DORA Report 2025 · Anthropic Engineering Blog · Stripe PR velocity data',
    },
    agents: {
      title: 'The Agent Roster',
      subtitle:
        'Each agent is laser-focused on one job, carries only the context it needs, and runs in parallel when possible.',
      readOnly: 'read-only',
      roles: {
        orchestrator: 'Breaks down requests and delegates to sub-agents',
        planner: 'Architecture & design decisions',
        implementer: 'Writes and edits code',
        reviewer: 'Bug, security, quality, performance review',
        tester: 'Unit, integration, E2E test authoring',
        'security-auditor': 'OWASP Top 10 security audit',
        'performance-optimizer': 'Bottleneck analysis and optimization',
        'database-expert': 'Schema design, queries, migrations',
        documenter: 'README, API docs, inline comments',
        'harness-designer': 'Designs tight / loose / adaptive AI harnesses',
        'pipeline-orchestrator': 'Multi-stage pipelines with context isolation',
      },
    },
    pipeline: {
      title: 'The Pipeline',
      subtitle: 'You give one instruction. The orchestrator runs the full pipeline.',
      you: 'You',
      prompt: '"Add OAuth login"',
      stages: {
        planner: 'architecture',
        'database-expert': 'schema',
        implementer: 'code',
        reviewer: 'review',
        tester: 'tests',
      },
      isolation: 'Context isolation',
      isolationDesc:
        'Each agent receives only the validated output of the previous stage — no context rot, no error contamination.',
      parallel: 'Parallel execution',
      parallelDesc:
        'Independent stages (planner + security-auditor) run simultaneously, cutting wall-clock time.',
      gates: 'Quality gates',
      gatesDesc:
        'Every stage passes through review before the next begins. Bugs get caught at the reviewer stage, not in production.',
    },
    tools: {
      title: '7 Productivity Tools',
      subtitle:
        'Python CLIs + Claude Code slash commands. Core tools also ship as a single zero-dependency Rust binary.',
      items: {
        snippet: {
          name: 'snippet',
          desc: 'Personal prompt manager — save your best prompts by name, recall in one command. 20 built-in templates.',
        },
        handoff: {
          name: 'claude-handoff',
          desc: 'Save full session context — git state, TODOs, notes — and restore it in your next conversation.',
        },
        cost: {
          name: 'claude-cost',
          desc: 'Estimate API spend before running a prompt. Track actual usage from session logs. Set budgets.',
        },
        review: {
          name: 'claude-review-diff',
          desc: 'Turn your git diff into a structured code-review prompt. Findings grouped Critical → Nit.',
        },
        remind: {
          name: 'claude-remind',
          desc: 'Scan TODO.md for unchecked boxes and surface pending work at session start.',
        },
        harness: {
          name: 'claude-harness',
          desc: 'Validate agent harness definitions and generate tight / loose / adaptive templates.',
        },
        pipeline: {
          name: 'claude-pipeline',
          desc: 'Track multi-stage pipeline runs, log stage results, generate Markdown run reports.',
        },
      },
      rust: 'Also available as a single Rust binary',
      rustDesc: 'claude-tools — snippet, handoff, cost, live watch monitor, env health check. No Python required.',
    },
    start: {
      title: 'Get Started in 60 Seconds',
      step1: 'Install Claude Code',
      step2: 'Install the agents',
      step3: 'Verify',
      tab1: 'One-liner (macOS / Linux)',
      tab2: 'From source',
      copy: 'Copy',
      copied: 'Copied!',
      docs: 'Full setup guide',
    },
    footer: {
      docs: 'Documentation',
      setup: 'Setup Guide',
      cheatsheet: 'Agent Cheatsheet',
      harness: 'Harness Guide',
      integration: 'Integration',
      contributing: 'Contributing',
      license: 'MIT License',
      made: 'Built with Claude Code',
    },
  },
  ko: {
    nav: {
      agents: '에이전트',
      pipeline: '파이프라인',
      tools: '도구',
      benchmark: '벤치마크',
      start: '시작하기',
      github: 'GitHub',
    },
    hero: {
      badge: '오픈소스 · MIT 라이선스',
      title1: '프롬프트 하나,',
      title2: '전문가 열한 명.',
      subtitle:
        'Claude Code에 바로 꽂아 쓰는 멀티 에이전트 시스템 — 설계·구현·리뷰·테스트·보안을 담당하는 11개의 전문 AI 에이전트와 7개의 생산성 도구.',
      ctaPrimary: '시작하기',
      ctaSecondary: 'GitHub에서 보기',
      statAgents: '에이전트',
      statTools: '도구',
      statSnippets: '스니펫',
      statLangs: '언어 지원',
    },
    stats: {
      title: '왜 하네스 엔지니어링인가?',
      subtitle:
        '벤치마크: TypeScript 파일 하나의 버그 수정. API 비용은 소폭 올라가지만 — 총 엔지니어링 비용은 3배 줄어듭니다.',
      diffSize: 'PR diff 감소',
      diffDetail: '180줄 → 25줄, 외과적 수정 프로토콜',
      reviewTime: '리뷰 시간 감소',
      reviewDetail: 'PR당 18분 → 4분',
      approval: '첫 승인율',
      approvalDetail: '바닐라 CLI ~45% 대비',
      cost: '작업당 비용 절감',
      costDetail: '총 비용: API + 사람 시간',
      sources:
        '출처: Google DORA Report 2025 · Anthropic Engineering Blog · Stripe PR 속도 데이터',
    },
    agents: {
      title: '에이전트 구성',
      subtitle:
        '각 에이전트는 하나의 역할에만 집중하고, 필요한 컨텍스트만 갖고, 가능하면 병렬로 실행됩니다.',
      readOnly: '읽기 전용',
      roles: {
        orchestrator: '작업 분해 및 서브 에이전트 위임 총괄',
        planner: '아키텍처·설계 결정',
        implementer: '실제 코드 작성·수정',
        reviewer: '버그·보안·품질·성능 리뷰',
        tester: '유닛·통합·E2E 테스트 작성',
        'security-auditor': 'OWASP Top 10 보안 감사',
        'performance-optimizer': '성능 병목 분석 및 최적화',
        'database-expert': 'DB 스키마 설계·쿼리·마이그레이션',
        documenter: 'README·API 문서·인라인 주석',
        'harness-designer': '타이트·느슨·적응형 AI 하네스 설계',
        'pipeline-orchestrator': '컨텍스트 격리 기반 다단계 파이프라인',
      },
    },
    pipeline: {
      title: '파이프라인',
      subtitle: '지시는 한 번만. 오케스트레이터가 전체 파이프라인을 실행합니다.',
      you: '나',
      prompt: '"OAuth 로그인 추가해줘"',
      stages: {
        planner: '아키텍처',
        'database-expert': '스키마',
        implementer: '코드',
        reviewer: '리뷰',
        tester: '테스트',
      },
      isolation: '컨텍스트 격리',
      isolationDesc:
        '각 에이전트는 이전 단계의 검증된 출력만 전달받습니다 — 컨텍스트 부패 없음, 오류 전염 없음.',
      parallel: '병렬 실행',
      parallelDesc:
        '독립적인 단계(planner + security-auditor)는 동시에 실행되어 전체 소요 시간을 줄입니다.',
      gates: '품질 게이트',
      gatesDesc:
        '모든 단계는 리뷰를 통과해야 다음으로 넘어갑니다. 버그는 프로덕션이 아닌 리뷰 단계에서 잡힙니다.',
    },
    tools: {
      title: '7가지 생산성 도구',
      subtitle:
        'Python CLI + Claude Code 슬래시 커맨드. 핵심 도구는 의존성 없는 단일 Rust 바이너리로도 제공됩니다.',
      items: {
        snippet: {
          name: 'snippet',
          desc: '개인 프롬프트 매니저 — 자주 쓰는 프롬프트를 이름으로 저장하고 한 커맨드로 호출. 기본 템플릿 20개 내장.',
        },
        handoff: {
          name: 'claude-handoff',
          desc: '세션 전체 컨텍스트(git 상태, 할 일, 메모)를 저장하고 다음 대화에서 복원합니다.',
        },
        cost: {
          name: 'claude-cost',
          desc: '프롬프트 실행 전에 API 비용을 추정하고, 세션 로그로 실제 사용량 추적. 예산 설정 가능.',
        },
        review: {
          name: 'claude-review-diff',
          desc: 'git diff를 구조화된 코드 리뷰 프롬프트로 변환. Critical → Nit 심각도별 정리.',
        },
        remind: {
          name: 'claude-remind',
          desc: 'TODO.md의 미완료 체크박스를 스캔해 세션 시작 시 남은 작업을 표시합니다.',
        },
        harness: {
          name: 'claude-harness',
          desc: '에이전트 하네스 정의를 검증하고 타이트·느슨·적응형 템플릿을 생성합니다.',
        },
        pipeline: {
          name: 'claude-pipeline',
          desc: '다단계 파이프라인 실행을 추적하고 단계 결과를 기록, 마크다운 보고서를 생성합니다.',
        },
      },
      rust: '단일 Rust 바이너리로도 제공',
      rustDesc: 'claude-tools — snippet, handoff, cost, 실시간 watch 모니터, env 헬스체크. Python 불필요.',
    },
    start: {
      title: '60초 안에 시작하기',
      step1: 'Claude Code 설치',
      step2: '에이전트 설치',
      step3: '확인',
      tab1: '원라인 설치 (macOS / Linux)',
      tab2: '소스에서 빌드',
      copy: '복사',
      copied: '복사됨!',
      docs: '전체 세팅 가이드',
    },
    footer: {
      docs: '문서',
      setup: '환경 세팅 가이드',
      cheatsheet: '에이전트 치트시트',
      harness: '하네스 가이드',
      integration: '통합 가이드',
      contributing: '기여 가이드',
      license: 'MIT 라이선스',
      made: 'Claude Code로 제작',
    },
  },
}

export const t = computed(() => messages[lang.value])
