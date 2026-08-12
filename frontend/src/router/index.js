import { createRouter, createWebHashHistory } from 'vue-router'
import { getCurrentUser } from '@/services/auth'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/DashboardView.vue')
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: () => import('../views/LeaderboardView.vue')
    },
    {
      path: '/trade',
      name: 'trade',
      component: () => import('../views/AdvancedTradeView.vue')
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAdmin: true }
    }
  ]
})

// Guard runs on every navigation to /admin. This is UX only, not a security
// boundary -- the real enforcement is server-side (require_admin dependency
// in the backend), since a client-side check can always be bypassed by
// hitting the API directly. This just avoids showing the admin page to a
// user who will immediately get 403s from every call it makes.
router.beforeEach(async (to) => {
  if (!to.meta.requiresAdmin) return true

  const token = localStorage.getItem('token')
  if (!token) return { name: 'login' }

  try {
    const user = await getCurrentUser()
    if (user?.role !== 'admin') {
      return { name: 'dashboard' }
    }
  } catch (err) {
    return { name: 'login' }
  }

  return true
})

export default router
