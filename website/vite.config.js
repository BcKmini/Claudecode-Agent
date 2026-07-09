import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// GitHub Pages serves at /claude-code-use/
export default defineConfig({
  plugins: [vue()],
  base: '/claude-code-use/',
})
