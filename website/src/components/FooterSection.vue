<script setup>
import { t, lang } from '../i18n.js'
import { computed } from 'vue'

const repo = 'https://github.com/BcKmini/claude-code-use'
const suffix = computed(() => (lang.value === 'ko' ? '.ko.md' : '.md'))

const docs = computed(() => [
  { key: 'setup', href: `${repo}/blob/main/docs/SETUP${suffix.value}` },
  { key: 'cheatsheet', href: `${repo}/blob/main/docs/AGENT-CHEATSHEET${suffix.value}` },
  { key: 'harness', href: `${repo}/blob/main/docs/HARNESS-GUIDE${suffix.value}` },
  { key: 'integration', href: `${repo}/blob/main/docs/INTEGRATION${suffix.value}` },
  { key: 'contributing', href: `${repo}/blob/main/docs/CONTRIBUTING${suffix.value}` },
])
</script>

<template>
  <footer>
    <div class="container footer-inner">
      <div class="brand-col">
        <div class="brand">
          <svg viewBox="0 0 64 64" width="24" height="24" aria-hidden="true">
            <circle cx="32" cy="20" r="7" fill="#D97757" />
            <circle cx="16" cy="44" r="5.5" fill="#E8956B" opacity="0.9" />
            <circle cx="32" cy="46" r="5.5" fill="#E8956B" opacity="0.75" />
            <circle cx="48" cy="44" r="5.5" fill="#E8956B" opacity="0.9" />
            <path d="M32 27 L16 39 M32 27 L32 40 M32 27 L48 39" stroke="#D97757" stroke-width="2.4" stroke-linecap="round" fill="none" />
          </svg>
          <span>claude-code-use</span>
        </div>
        <p class="made">{{ t.footer.made }} · {{ t.footer.license }}</p>
      </div>

      <div class="links-col">
        <h4>{{ t.footer.docs }}</h4>
        <a v-for="d in docs" :key="d.key" :href="d.href" target="_blank" rel="noopener">
          {{ t.footer[d.key] }}
        </a>
      </div>

      <div class="links-col">
        <h4>GitHub</h4>
        <a :href="repo" target="_blank" rel="noopener">Repository</a>
        <a :href="`${repo}/issues`" target="_blank" rel="noopener">Issues</a>
        <a :href="`${repo}/blob/main/LICENSE`" target="_blank" rel="noopener">{{ t.footer.license }}</a>
      </div>
    </div>
  </footer>
</template>

<style scoped>
footer {
  border-top: 1px solid var(--border);
  padding: 56px 0 48px;
  background: rgba(255, 255, 255, 0.015);
}

.footer-inner {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr;
  gap: 40px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 9px;
  font-weight: 700;
  margin-bottom: 12px;
}

.made {
  color: var(--text-faint);
  font-size: 0.85rem;
}

.links-col {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.links-col h4 {
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-faint);
  margin-bottom: 4px;
}

.links-col a {
  color: var(--text-dim);
  font-size: 0.9rem;
  transition: color 0.2s;
}

.links-col a:hover {
  color: var(--accent-soft);
}

@media (max-width: 700px) {
  .footer-inner {
    grid-template-columns: 1fr;
    gap: 32px;
  }
}
</style>
