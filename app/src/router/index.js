import { createRouter, createWebHistory } from 'vue-router'
import App from '../app.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [{ path: '/', component: App }]
})

export default router
