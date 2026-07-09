<script setup>
import { t } from '../i18n.js'

const agents = [
  { num: '00', name: 'orchestrator', model: 'Opus', icon: '🧭' },
  { num: '01', name: 'planner', model: 'Opus', readOnly: true, icon: '📐' },
  { num: '02', name: 'implementer', model: 'Sonnet', icon: '⌨️' },
  { num: '03', name: 'reviewer', model: 'Sonnet', readOnly: true, icon: '🔍' },
  { num: '04', name: 'tester', model: 'Sonnet', icon: '🧪' },
  { num: '05', name: 'security-auditor', model: 'Opus', readOnly: true, icon: '🛡️' },
  { num: '06', name: 'performance-optimizer', model: 'Sonnet', icon: '🚀' },
  { num: '07', name: 'database-expert', model: 'Sonnet', icon: '🗄️' },
  { num: '08', name: 'documenter', model: 'Haiku', icon: '📝' },
  { num: '09', name: 'harness-designer', model: 'Opus', icon: '🎛️' },
  { num: '10', name: 'pipeline-orchestrator', model: 'Opus', icon: '🔗' },
]

const modelClass = { Opus: 'opus', Sonnet: 'sonnet', Haiku: 'haiku' }
</script>

<template>
  <section id="agents">
    <div class="container">
      <h2 class="section-title" v-reveal>{{ t.agents.title }}</h2>
      <p class="section-subtitle" v-reveal="80">{{ t.agents.subtitle }}</p>

      <div class="grid">
        <div v-for="(a, i) in agents" :key="a.name" class="card agent" v-reveal="(i % 4) * 70">
          <div class="head">
            <span class="icon">{{ a.icon }}</span>
            <span class="num">{{ a.num }}</span>
          </div>
          <h3>{{ a.name }}</h3>
          <p>{{ t.agents.roles[a.name] }}</p>
          <div class="badges">
            <span :class="['model', modelClass[a.model]]">{{ a.model }}</span>
            <span v-if="a.readOnly" class="ro">{{ t.agents.readOnly }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}

.agent {
  display: flex;
  flex-direction: column;
  padding: 22px;
}

.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.icon {
  font-size: 1.5rem;
}

.num {
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--text-faint);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 2px 8px;
}

.agent h3 {
  font-family: var(--mono);
  font-size: 0.98rem;
  letter-spacing: -0.01em;
  margin-bottom: 7px;
  color: var(--accent-soft);
}

.agent p {
  color: var(--text-dim);
  font-size: 0.86rem;
  flex: 1;
  margin-bottom: 16px;
}

.badges {
  display: flex;
  gap: 8px;
  align-items: center;
}

.model {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: 999px;
  letter-spacing: 0.03em;
}

.model.opus {
  color: var(--opus);
  background: rgba(192, 132, 252, 0.12);
  border: 1px solid rgba(192, 132, 252, 0.3);
}

.model.sonnet {
  color: var(--sonnet);
  background: rgba(217, 119, 87, 0.12);
  border: 1px solid rgba(217, 119, 87, 0.3);
}

.model.haiku {
  color: var(--haiku);
  background: rgba(74, 222, 128, 0.1);
  border: 1px solid rgba(74, 222, 128, 0.28);
}

.ro {
  font-size: 0.72rem;
  color: var(--text-faint);
  border: 1px dashed rgba(255, 255, 255, 0.18);
  padding: 3px 10px;
  border-radius: 999px;
}

@media (max-width: 1020px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 760px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 500px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
