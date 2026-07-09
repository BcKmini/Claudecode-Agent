<script setup>
import { t } from '../i18n.js'

const stages = ['planner', 'database-expert', 'implementer', 'reviewer', 'tester']

const features = [
  { key: 'isolation', icon: '🔒' },
  { key: 'parallel', icon: '⚡' },
  { key: 'gates', icon: '✅' },
]
</script>

<template>
  <section id="pipeline">
    <div class="container">
      <h2 class="section-title" v-reveal>{{ t.pipeline.title }}</h2>
      <p class="section-subtitle" v-reveal="80">{{ t.pipeline.subtitle }}</p>

      <div class="flow" v-reveal="120">
        <div class="node you">
          <div class="node-label">{{ t.pipeline.you }}</div>
          <div class="node-sub">{{ t.pipeline.prompt }}</div>
        </div>
        <div class="connector" aria-hidden="true"><span class="pulse"></span></div>
        <div class="node orch">
          <div class="node-label">orchestrator</div>
          <div class="node-sub">Opus</div>
        </div>
        <div class="connector" aria-hidden="true"><span class="pulse d2"></span></div>
        <div class="stage-col">
          <div v-for="(s, i) in stages" :key="s" class="node stage" :style="{ animationDelay: i * 0.35 + 's' }">
            <div class="node-label">{{ s }}</div>
            <div class="node-sub">{{ t.pipeline.stages[s] }}</div>
          </div>
        </div>
      </div>

      <div class="features">
        <div v-for="(f, i) in features" :key="f.key" class="card feature" v-reveal="i * 90">
          <div class="icon">{{ f.icon }}</div>
          <h3>{{ t.pipeline[f.key] }}</h3>
          <p>{{ t.pipeline[f.key + 'Desc'] }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-bottom: 70px;
  flex-wrap: wrap;
}

.node {
  border: 1px solid var(--border);
  background: var(--bg-card);
  border-radius: 14px;
  padding: 16px 22px;
  text-align: center;
  min-width: 150px;
}

.node-label {
  font-family: var(--mono);
  font-weight: 700;
  font-size: 0.92rem;
}

.node-sub {
  font-size: 0.78rem;
  color: var(--text-faint);
  margin-top: 2px;
}

.node.you {
  border-color: rgba(255, 255, 255, 0.18);
}

.node.orch {
  border-color: rgba(217, 119, 87, 0.5);
  background: linear-gradient(160deg, rgba(217, 119, 87, 0.12), rgba(255, 255, 255, 0.02));
  box-shadow: 0 0 40px -10px rgba(217, 119, 87, 0.35);
}

.node.orch .node-label {
  color: var(--accent-soft);
}

.connector {
  position: relative;
  width: 64px;
  height: 2px;
  background: linear-gradient(90deg, rgba(217, 119, 87, 0.15), rgba(217, 119, 87, 0.5));
  margin: 0 4px;
}

.pulse {
  position: absolute;
  top: -2.5px;
  left: 0;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
  animation: travel 1.8s linear infinite;
}

.pulse.d2 {
  animation-delay: 0.9s;
}

@keyframes travel {
  from { left: 0; opacity: 1; }
  85% { opacity: 1; }
  to { left: calc(100% - 7px); opacity: 0; }
}

.stage-col {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.node.stage {
  padding: 10px 20px;
  text-align: left;
  display: flex;
  align-items: baseline;
  gap: 12px;
  animation: glowStage 3.5s ease-in-out infinite;
}

.node.stage .node-sub {
  margin: 0;
}

@keyframes glowStage {
  0%, 100% { border-color: var(--border); }
  12% { border-color: rgba(217, 119, 87, 0.6); box-shadow: 0 0 18px -4px rgba(217, 119, 87, 0.4); }
  30% { border-color: var(--border); box-shadow: none; }
}

.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.feature .icon {
  font-size: 1.7rem;
  margin-bottom: 12px;
}

.feature h3 {
  font-size: 1.08rem;
  margin-bottom: 8px;
  letter-spacing: -0.01em;
}

.feature p {
  color: var(--text-dim);
  font-size: 0.92rem;
}

@media (max-width: 920px) {
  .flow {
    flex-direction: column;
    gap: 8px;
  }

  .connector {
    width: 2px;
    height: 40px;
    background: linear-gradient(180deg, rgba(217, 119, 87, 0.15), rgba(217, 119, 87, 0.5));
  }

  .pulse {
    animation: travelV 1.8s linear infinite;
    left: -2.5px;
    top: 0;
  }

  @keyframes travelV {
    from { top: 0; opacity: 1; }
    85% { opacity: 1; }
    to { top: calc(100% - 7px); opacity: 0; }
  }

  .features {
    grid-template-columns: 1fr;
  }
}
</style>
