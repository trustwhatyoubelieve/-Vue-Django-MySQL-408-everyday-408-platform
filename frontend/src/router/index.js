import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/question-bank',
    name: 'QuestionBank',
    component: () => import('../views/QuestionBankView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue'),
    meta: { guest: true }
  },
  {
    path: '/practice/:subchapterId',
    name: 'Practice',
    component: () => import('../views/PracticeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/practice-home',
    name: 'PracticeHome',
    component: () => import('../views/PracticeHomeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/wrong-questions',
    name: 'WrongQuestions',
    component: () => import('../views/WrongQuestionsView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('../views/FavoritesView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/study-center',
    name: 'StudyCenter',
    component: () => import('../views/StudyCenterView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/mindmap',
    name: 'MindMap',
    component: () => import('../views/MindMapView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/recommendation',
    name: 'Recommendation',
    component: () => import('../views/RecommendationView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isLoggedIn = !!userStore.token

  // 已登录用户不能访问 guest 页面（登录、注册）
  if (to.meta.guest && isLoggedIn) {
    next('/')
    return
  }

  // 需要登录的页面
  if (to.meta.requiresAuth && !isLoggedIn) {
    next('/login')
    return
  }

  next()
})

export default router