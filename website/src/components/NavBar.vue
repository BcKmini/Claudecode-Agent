<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { t, lang, setLang } from '../i18n.js'

const scrolled = ref(false)
const menuOpen = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 24
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

const links = [
  { href: '#benchmark', key: 'benchmark' },
  { href: '#pipeline', key: 'pipeline' },
  { href: '#agents', key: 'agents' },
  { href: '#tools', key: 'tools' },
  { href: '#start', key: 'start' },
]
</script>

<template>
  <header :class="['nav', { scrolled }]">
    <div class="container nav-inner">
      <a href="#" class="brand">
        <svg viewBox="0 0 64 64" width="26" height="26" aria-hidden="true">
          <circle cx="32" cy="20" r="7" fill="#D97757" />
          <circle cx="16" cy="44" r="5.5" fill="#E8956B" opacity="0.9" />
          <circle cx="32" cy="46" r="5.5" fill="#E8956B" opacity="0.75" />
          <circle cx="48" cy="44" r="5.5" fill="#E8956B" opacity="0.9" />
          <path d="M32 27 L16 39 M32 27 L32 40 M32 27 L48 39" stroke="#D97757" stroke-width="2.4" stroke-linecap="round" fill="none" />
        </svg>
        <span>claude-code-use</span>
      </a>

      <nav :class="['links', { open: menuOpen }]">
        <a v-for="l in links" :key="l.key" :href="l.href" @click="menuOpen = false">
          {{ t.nav[l.key] }}
        </a>
      </nav>

      <div class="actions">
        <div class="lang-toggle" role="group" aria-label="Language">
          <button :class="{ active: lang === 'en' }" @click="setLang('en')">EN</button>
          <button :class="{ active: lang === 'ko' }" @click="setLang('ko')">KO</button>
        </div>
        <a class="gh-btn" href="https://github.com/BcKmini/claude-code-use" target="_blank" rel="noopener">
          <svg viewBox="0 0 16 16" width="16" height="16" fill="currentColor" aria-hidden="true">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z" />
          </svg>
          <span>{{ t.nav.github }}</span>
        </a>
        <button class="menu-btn" @click="menuOpen = !menuOpen" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: 14px 0;
  transition: background 0.3s, border-color 0.3s, padding 0.3s;
  border-bottom: 1px solid transparent;
}

.nav.scrolled {
  background: rgba(10, 10, 15, 0.82);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom-color: var(--border);
  padding: 10px 0;
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 9px;
  font-weight: 700;
  font-size: 1.02rem;
  letter-spacing: -0.01em;
}

.links {
  display: flex;
  gap: 26px;
}

.links a {
  color: var(--text-dim);
  font-size: 0.92rem;
  font-weight: 500;
  transition: color 0.2s;
}

.links a:hover {
  color: var(--text);
}

.actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.lang-toggle {
  display: flex;
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}

.lang-toggle button {
  background: transparent;
  border: none;
  color: var(--text-faint);
  padding: 5px 10px;
  font-size: 0.78rem;
  font-weight: 700;
  transition: background 0.2s, color 0.2s;
}

.lang-toggle button.active {
  background: var(--accent);
  color: #fff;
}

.gh-btn {
  display: flex;
  align-items: center;
  gap: 7px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border);
  padding: 7px 14px;
  border-radius: 9px;
  font-size: 0.88rem;
  font-weight: 600;
  transition: background 0.2s, border-color 0.2s;
}

.gh-btn:hover {
  background: rgba(255, 255, 255, 0.11);
  border-color: rgba(255, 255, 255, 0.2);
}

.menu-btn {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  padding: 6px;
}

.menu-btn span {
  width: 20px;
  height: 2px;
  background: var(--text);
  border-radius: 2px;
}

@media (max-width: 860px) {
  .links {
    position: fixed;
    top: 58px;
    left: 0;
    right: 0;
    flex-direction: column;
    background: rgba(10, 10, 15, 0.97);
    backdrop-filter: blur(14px);
    padding: 22px 24px;
    gap: 18px;
    border-bottom: 1px solid var(--border);
    transform: translateY(-130%);
    transition: transform 0.3s ease;
  }

  .links.open {
    transform: none;
  }

  .menu-btn {
    display: flex;
  }

  .gh-btn span {
    display: none;
  }
}
</style>
