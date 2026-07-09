<script setup>
import { ref, onMounted } from 'vue'
import { t } from '../i18n.js'

const root = ref(null)
const animated = ref(false)
const vals = ref({ diff: 0, review: 0, approval: 0, cost: 0 })

const targets = { diff: 86, review: 78, approval: 85, cost: 3.1 }

function animate() {
  const start = performance.now()
  const dur = 1400
  const tick = (now) => {
    const p = Math.min((now - start) / dur, 1)
    const ease = 1 - Math.pow(1 - p, 3)
    vals.value = {
      diff: Math.round(targets.diff * ease),
      review: Math.round(targets.review * ease),
      approval: Math.round(targets.approval * ease),
      cost: (targets.cost * ease).toFixed(1),
    }
    if (p < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

onMounted(() => {
  const obs = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting && !animated.value) {
        animated.value = true
        animate()
        obs.disconnect()
      }
    },
    { threshold: 0.3 }
  )
  obs.observe(root.value)
})
</script>

<template>
  <section id="benchmark" ref="root">
    <div class="container">
      <h2 class="section-title" v-reveal>{{ t.stats.title }}</h2>
      <p class="section-subtitle" v-reveal="80">{{ t.stats.subtitle }}</p>

      <div class="stats-grid">
        <div class="card stat" v-reveal="0">
          <div class="num">−{{ vals.diff }}<span class="unit">%</span></div>
          <div class="label">{{ t.stats.diffSize }}</div>
          <div class="detail">{{ t.stats.diffDetail }}</div>
          <div class="bar"><div class="fill" :style="{ width: vals.diff + '%' }"></div></div>
        </div>
        <div class="card stat" v-reveal="90">
          <div class="num">−{{ vals.review }}<span class="unit">%</span></div>
          <div class="label">{{ t.stats.reviewTime }}</div>
          <div class="detail">{{ t.stats.reviewDetail }}</div>
          <div class="bar"><div class="fill" :style="{ width: vals.review + '%' }"></div></div>
        </div>
        <div class="card stat" v-reveal="180">
          <div class="num">{{ vals.approval }}<span class="unit">%</span></div>
          <div class="label">{{ t.stats.approval }}</div>
          <div class="detail">{{ t.stats.approvalDetail }}</div>
          <div class="bar"><div class="fill" :style="{ width: vals.approval + '%' }"></div></div>
        </div>
        <div class="card stat highlight" v-reveal="270">
          <div class="num">{{ vals.cost }}<span class="unit">×</span></div>
          <div class="label">{{ t.stats.cost }}</div>
          <div class="detail">{{ t.stats.costDetail }}</div>
          <div class="bar"><div class="fill" style="width: 100%"></div></div>
        </div>
      </div>

      <p class="sources" v-reveal>{{ t.stats.sources }}</p>
    </div>
  </section>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat .num {
  font-size: 2.7rem;
  font-weight: 850;
  letter-spacing: -0.03em;
  line-height: 1.1;
  background: linear-gradient(120deg, var(--accent), var(--accent-soft));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  font-variant-numeric: tabular-nums;
}

.stat .unit {
  font-size: 1.6rem;
}

.stat .label {
  font-weight: 700;
  margin-top: 8px;
}

.stat .detail {
  color: var(--text-faint);
  font-size: 0.84rem;
  margin-top: 3px;
  min-height: 2.4em;
}

.bar {
  margin-top: 16px;
  height: 5px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.06);
  overflow: hidden;
}

.fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, var(--accent), var(--accent-soft));
  transition: width 0.2s linear;
}

.stat.highlight {
  border-color: rgba(217, 119, 87, 0.4);
  background: linear-gradient(160deg, rgba(217, 119, 87, 0.08), rgba(255, 255, 255, 0.02));
}

.sources {
  text-align: center;
  color: var(--text-faint);
  font-size: 0.8rem;
  margin-top: 40px;
}

@media (max-width: 920px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 520px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
