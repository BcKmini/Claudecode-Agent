<script setup>
import { ref } from 'vue'
import { t } from '../i18n.js'

const tab = ref('oneliner')
const copiedIdx = ref(-1)

const steps = {
  install: 'npm install -g @anthropic-ai/claude-code\nclaude   # authenticate on first run',
  oneliner: 'curl -fsSL https://raw.githubusercontent.com/BcKmini/claude-code-use/main/install.sh | bash',
  source:
    'git clone https://github.com/BcKmini/claude-code-use.git\ncd claude-code-use\nbash install.sh          # agents + slash commands + Rust binary',
  verify: 'claude\n/agents          # → 11 agents listed\n/snippet list    # → built-in snippets',
}

async function copy(text, idx) {
  try {
    await navigator.clipboard.writeText(text)
    copiedIdx.value = idx
    setTimeout(() => (copiedIdx.value = -1), 1600)
  } catch {}
}
</script>

<template>
  <section id="start">
    <div class="container narrow">
      <h2 class="section-title" v-reveal>{{ t.start.title }}</h2>

      <div class="steps">
        <div class="step" v-reveal>
          <div class="step-head">
            <span class="n">1</span>
            <h3>{{ t.start.step1 }}</h3>
          </div>
          <div class="codeblock">
            <button class="copy-btn" @click="copy(steps.install, 0)">
              {{ copiedIdx === 0 ? t.start.copied : t.start.copy }}
            </button>
            <pre>{{ steps.install }}</pre>
          </div>
        </div>

        <div class="step" v-reveal="90">
          <div class="step-head">
            <span class="n">2</span>
            <h3>{{ t.start.step2 }}</h3>
          </div>
          <div class="tabs">
            <button :class="{ active: tab === 'oneliner' }" @click="tab = 'oneliner'">
              {{ t.start.tab1 }}
            </button>
            <button :class="{ active: tab === 'source' }" @click="tab = 'source'">
              {{ t.start.tab2 }}
            </button>
          </div>
          <div class="codeblock">
            <button class="copy-btn" @click="copy(steps[tab], 1)">
              {{ copiedIdx === 1 ? t.start.copied : t.start.copy }}
            </button>
            <pre>{{ steps[tab] }}</pre>
          </div>
        </div>

        <div class="step" v-reveal="180">
          <div class="step-head">
            <span class="n">3</span>
            <h3>{{ t.start.step3 }}</h3>
          </div>
          <div class="codeblock">
            <button class="copy-btn" @click="copy(steps.verify, 2)">
              {{ copiedIdx === 2 ? t.start.copied : t.start.copy }}
            </button>
            <pre>{{ steps.verify }}</pre>
          </div>
        </div>
      </div>

      <div class="docs-link" v-reveal>
        <a href="https://github.com/BcKmini/claude-code-use/blob/main/docs/SETUP.md" target="_blank" rel="noopener">
          {{ t.start.docs }} →
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.narrow {
  max-width: 780px;
}

.steps {
  display: flex;
  flex-direction: column;
  gap: 34px;
  margin-top: 50px;
}

.step-head {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 14px;
}

.n {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 10px;
  background: linear-gradient(120deg, var(--accent), var(--accent-soft));
  color: #fff;
  font-weight: 800;
  font-size: 0.95rem;
  flex-shrink: 0;
}

.step-head h3 {
  font-size: 1.12rem;
  letter-spacing: -0.01em;
}

.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.tabs button {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
  color: var(--text-dim);
  padding: 7px 16px;
  border-radius: 9px;
  font-size: 0.84rem;
  font-weight: 600;
  transition: all 0.2s;
}

.tabs button.active {
  background: var(--accent-glow);
  border-color: rgba(217, 119, 87, 0.45);
  color: var(--accent-soft);
}

.copy-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 2;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid var(--border);
  color: var(--text-dim);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 7px;
  transition: all 0.2s;
}

.copy-btn:hover {
  background: rgba(255, 255, 255, 0.13);
  color: var(--text);
}

.docs-link {
  text-align: center;
  margin-top: 44px;
}

.docs-link a {
  color: var(--accent-soft);
  font-weight: 600;
  transition: opacity 0.2s;
}

.docs-link a:hover {
  opacity: 0.8;
}
</style>
