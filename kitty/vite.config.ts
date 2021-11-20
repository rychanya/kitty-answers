import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    manifest: true,
    outDir: "../answers/dist",
    emptyOutDir: true,
    rollupOptions: {
      input: "src/main.ts"
    }
  },
  base: "/web/",
  plugins: [vue()]
})
