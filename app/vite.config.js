import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    watch: {
      usePolling: true
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})

/* export default defineConfig(({ command, mode, ssrBuild }) => {
  if (command === 'serve') {
    return {
      plugins: [vue()],
      server: {
        watch: {
          usePolling: true
        }
      },
      resolve: {
        alias: {
          '@': fileURLToPath(new URL('./src', import.meta.url))
        },
        define: {
          __APP_ENV__: env.APP_ENV
        }
      }
    }
  } else {
    // command === 'build'
    return {
      plugins: [vue()],
      resolve: {
        alias: {
          '@': fileURLToPath(new URL('./src', import.meta.url))
        }
      }
    }
  }
}) */