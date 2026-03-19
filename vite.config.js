import { defineConfig } from 'vite'
import htmlIncludePlugin from './vite-plugin-html-include.js'

export default defineConfig({
  plugins: [htmlIncludePlugin()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      }
    },
    allowedHosts: [
      'daniele-unoverhauled-donnishly.ngrok-free.dev',
      '.ngrok-free.dev',
      '.ngrok.io',
      'localhost'
    ]
  }
})