import { createApp } from 'vue'
import App from './App.vue'
import './style.css'

const app = createApp(App)

// v-reveal: fade-and-rise into view on scroll
const observer = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed')
        observer.unobserve(entry.target)
      }
    }
  },
  { threshold: 0.12 }
)

app.directive('reveal', {
  mounted(el, binding) {
    el.classList.add('reveal')
    if (binding.value) el.style.transitionDelay = `${binding.value}ms`
    observer.observe(el)
  },
})

app.mount('#app')
