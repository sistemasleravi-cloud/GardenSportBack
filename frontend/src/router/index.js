import { createRouter, createWebHistory } from 'vue-router'
import ReservaView from '../views/Public/ReservaView.vue'
import AdminView from '../views/Admin/AdminView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'reserva',
      component: ReservaView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView
    }
  ]
})

export default router