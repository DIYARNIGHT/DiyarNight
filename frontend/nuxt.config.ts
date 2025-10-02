export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@nuxt/ui'
  ],
  ui: {
    global: true,
    icons: ['heroicons', 'mdi'],
    primary: 'yellow',
    gray: 'slate'
  },
  css: [
    '~/assets/css/main.css'
  ],
  app: {
    head: {
      title: 'SmartNet - Akıllı İnternet Yönetimi',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { 
          name: 'description', 
          content: 'Türkcel SmartNet ile fiber internet hizmetlerinizi kolayca yönetin. Kota takibi, hız testi, paket önerileri ve daha fazlası.' 
        }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { 
          rel: 'stylesheet', 
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' 
        }
      ]
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1',
      appName: 'Türkcel SmartNet',
      version: '1.0.0'
    }
  },
  tailwindcss: {
    config: {
      theme: {
        extend: {
          colors: {
            turkcell: {
              50: '#fef2f2',
              100: '#fee2e2',
              200: '#fecaca',
              300: '#fca5a5',
              400: '#f87171',
              500: '#ef4444',
              600: '#dc2626',
              700: '#b91c1c',
              800: '#991b1b',
              900: '#7f1d1d'
            }
          },
          fontFamily: {
            sans: ['Inter', 'system-ui', 'sans-serif']
          }
        }
      }
    }
  },
  nitro: {
    preset: 'node-server'
  }
})