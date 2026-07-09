<script setup>
import { t } from '../i18n.js'

const tools = [
  { key: 'snippet', cmd: '/snippet run full-pipeline', icon: '💾' },
  { key: 'handoff', cmd: '/handoff save', icon: '🔄' },
  { key: 'cost', cmd: '/cost estimate full-pipeline', icon: '💰' },
  { key: 'review', cmd: '/review-diff --focus security', icon: '🔬' },
  { key: 'remind', cmd: '/remind', icon: '⏰' },
  { key: 'harness', cmd: '/harness validate agents/03-reviewer.md', icon: '🎛️' },
  { key: 'pipeline', cmd: '/pipeline status', icon: '📊' },
]
</script>

<template>
  <section id="tools">
    <div class="container">
      <h2 class="section-title" v-reveal>{{ t.tools.title }}</h2>
      <p class="section-subtitle" v-reveal="80">{{ t.tools.subtitle }}</p>

      <div class="grid">
        <div v-for="(tool, i) in tools" :key="tool.key" class="card tool" v-reveal="(i % 3) * 80">
          <div class="tool-head">
            <span class="icon">{{ tool.icon }}</span>
            <h3>{{ t.tools.items[tool.key].name }}</h3>
          </div>
          <p>{{ t.tools.items[tool.key].desc }}</p>
          <code>{{ tool.cmd }}</code>
        </div>

        <div class="card tool rust" v-reveal="240">
          <div class="tool-head">
            <span class="icon">🦀</span>
            <h3>{{ t.tools.rust }}</h3>
          </div>
          <p>{{ t.tools.rustDesc }}</p>
          <code>claude-tools watch</code>
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

.tool {
  display: flex;
  flex-direction: column;
  padding: 24px;
}

.tool-head {
  display: flex;
  align-items: center;
  gap: 11px;
  margin-bottom: 12px;
}

.icon {
  font-size: 1.4rem;
}

.tool h3 {
  font-family: var(--mono);
  font-size: 0.94rem;
  color: var(--accent-soft);
  letter-spacing: -0.01em;
}

.tool p {
  color: var(--text-dim);
  font-size: 0.87rem;
  flex: 1;
  margin-bottom: 16px;
}

.tool code {
  font-family: var(--mono);
  font-size: 0.78rem;
  color: #c8c8d8;
  background: #0d0d14;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  overflow-x: auto;
  white-space: nowrap;
}

.tool.rust {
  border-color: rgba(255, 165, 100, 0.35);
  background: linear-gradient(160deg, rgba(230, 126, 34, 0.07), rgba(255, 255, 255, 0.02));
}

.tool.rust h3 {
  font-family: inherit;
  color: var(--text);
  font-size: 0.98rem;
}

@media (max-width: 1020px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 560px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
