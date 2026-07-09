<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { t } from '../i18n.js'

const typed = ref('')
const doneLines = ref([])
const showCursor = ref(true)

const command = 'Use the orchestrator to add OAuth login'
const pipeline = [
  { agent: 'planner', note: 'architecture design', time: '12s' },
  { agent: 'database-expert', note: 'users + tokens schema', time: '9s' },
  { agent: 'implementer', note: '+184 −12 across 4 files', time: '41s' },
  { agent: 'reviewer', note: '2 issues found → fixed', time: '18s' },
  { agent: 'tester', note: '14 tests · all passing', time: '25s' },
]

let timers = []

function later(fn, ms) {
  timers.push(setTimeout(fn, ms))
}

function runDemo() {
  typed.value = ''
  doneLines.value = []
  let i = 0
  const typeNext = () => {
    if (i < command.length) {
      typed.value += command[i++]
      later(typeNext, 34 + Math.random() * 40)
    } else {
      later(revealStages, 500)
    }
  }
  let s = 0
  const revealStages = () => {
    if (s < pipeline.length) {
      doneLines.value.push(pipeline[s++])
      later(revealStages, 620)
    } else {
      doneLines.value.push({ agent: '✓ done', note: 'pipeline complete', time: '1m 45s', final: true })
      later(runDemo, 6000)
    }
  }
  typeNext()
}

onMounted(() => {
  runDemo()
  timers.push(setInterval(() => (showCursor.value = !showCursor.value), 530))
})

onUnmounted(() => timers.forEach((t) => clearTimeout(t)))
</script>

<template>
  <section class="hero">
    <div class="container hero-grid">
      <div class="hero-copy" v-reveal>
        <span class="badge">{{ t.hero.badge }}</span>
        <h1>
          {{ t.hero.title1 }}<br />
          <span class="grad">{{ t.hero.title2 }}</span>
        </h1>
        <p class="sub">{{ t.hero.subtitle }}</p>
        <div class="cta-row">
          <a href="#start" class="btn primary">{{ t.hero.ctaPrimary }}</a>
          <a href="https://github.com/BcKmini/claude-code-use" target="_blank" rel="noopener" class="btn ghost">
            <svg viewBox="0 0 16 16" width="17" height="17" fill="currentColor" aria-hidden="true">
              <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z" />
            </svg>
            {{ t.hero.ctaSecondary }}
          </a>
        </div>
        <div class="mini-stats">
          <div><strong>11</strong><span>{{ t.hero.statAgents }}</span></div>
          <div><strong>7</strong><span>{{ t.hero.statTools }}</span></div>
          <div><strong>20</strong><span>{{ t.hero.statSnippets }}</span></div>
          <div><strong>EN·KO</strong><span>{{ t.hero.statLangs }}</span></div>
        </div>
      </div>

      <div class="hero-term" v-reveal="150">
        <div class="term">
          <div class="term-bar">
            <span class="dot r"></span><span class="dot y"></span><span class="dot g"></span>
            <span class="term-title">claude</span>
          </div>
          <div class="term-body">
            <div class="term-line input">
              <span class="prompt-char">›</span>
              <span>{{ typed }}</span><span class="cursor" :class="{ off: !showCursor }">▋</span>
            </div>
            <transition-group name="stage" tag="div">
              <div
                v-for="line in doneLines"
                :key="line.agent"
                class="term-line stage-line"
                :class="{ final: line.final }"
              >
                <span class="agent-name">{{ line.final ? line.agent : '⏺ ' + line.agent }}</span>
                <span class="note">{{ line.note }}</span>
                <span class="time">{{ line.time }}</span>
              </div>
            </transition-group>
          </div>
        </div>
        <div class="term-glow" aria-hidden="true"></div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  padding: 170px 0 90px;
  overflow: hidden;
}

.hero-grid {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 56px;
  align-items: center;
}

.badge {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  color: var(--accent-soft);
  background: var(--accent-glow);
  border: 1px solid rgba(217, 119, 87, 0.3);
  padding: 5px 13px;
  border-radius: 999px;
  margin-bottom: 22px;
}

h1 {
  font-size: clamp(2.5rem, 5.5vw, 3.9rem);
  font-weight: 850;
  line-height: 1.08;
  letter-spacing: -0.03em;
  margin-bottom: 22px;
}

.grad {
  background: linear-gradient(120deg, var(--accent) 10%, var(--accent-soft) 55%, #f0b894);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sub {
  color: var(--text-dim);
  font-size: 1.12rem;
  max-width: 480px;
  margin-bottom: 32px;
}

.cta-row {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-bottom: 42px;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  padding: 13px 26px;
  border-radius: 12px;
  font-weight: 700;
  font-size: 0.98rem;
  transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
}

.btn.primary {
  background: linear-gradient(120deg, var(--accent), var(--accent-soft));
  color: #fff;
  box-shadow: 0 8px 28px -8px rgba(217, 119, 87, 0.55);
}

.btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px -8px rgba(217, 119, 87, 0.7);
}

.btn.ghost {
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text);
}

.btn.ghost:hover {
  background: rgba(255, 255, 255, 0.09);
  transform: translateY(-2px);
}

.mini-stats {
  display: flex;
  gap: 36px;
  flex-wrap: wrap;
}

.mini-stats div {
  display: flex;
  flex-direction: column;
}

.mini-stats strong {
  font-size: 1.55rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.mini-stats span {
  font-size: 0.82rem;
  color: var(--text-faint);
}

/* Terminal */
.hero-term {
  position: relative;
}

.term {
  position: relative;
  z-index: 1;
  background: rgba(13, 13, 20, 0.92);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 30px 80px -20px rgba(0, 0, 0, 0.7);
}

.term-bar {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.025);
}

.dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
}

.dot.r { background: #ff5f57; }
.dot.y { background: #febc2e; }
.dot.g { background: #28c840; }

.term-title {
  margin-left: 10px;
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--text-faint);
}

.term-body {
  padding: 20px;
  min-height: 300px;
  font-family: var(--mono);
  font-size: 0.86rem;
}

.term-line {
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 4px 0;
}

.term-line.input {
  color: #e8e8f0;
  margin-bottom: 10px;
}

.prompt-char {
  color: var(--accent);
  font-weight: 700;
}

.cursor {
  color: var(--accent);
  transition: opacity 0.1s;
}

.cursor.off {
  opacity: 0;
}

.stage-line .agent-name {
  color: var(--accent-soft);
  min-width: 175px;
  font-weight: 600;
}

.stage-line .note {
  color: var(--text-dim);
  flex: 1;
}

.stage-line .time {
  color: var(--text-faint);
  font-size: 0.78rem;
}

.stage-line.final .agent-name {
  color: #4ade80;
}

.stage-enter-active {
  transition: opacity 0.45s, transform 0.45s;
}

.stage-enter-from {
  opacity: 0;
  transform: translateX(-10px);
}

.term-glow {
  position: absolute;
  inset: -40px;
  background: radial-gradient(ellipse 60% 55% at 50% 50%, rgba(217, 119, 87, 0.14), transparent 70%);
  z-index: 0;
}

@media (max-width: 920px) {
  .hero {
    padding: 130px 0 60px;
  }

  .hero-grid {
    grid-template-columns: 1fr;
    gap: 44px;
  }

  .stage-line .agent-name {
    min-width: 130px;
  }

  .stage-line .note {
    display: none;
  }
}
</style>
