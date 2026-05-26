import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true, // Esto obliga a Vite a detectar los cambios guardados en Windows
    },
    hmr: {
      clientPort: 5173 // Asegura que la conexión en tiempo real no se pierda
    }
  }
})