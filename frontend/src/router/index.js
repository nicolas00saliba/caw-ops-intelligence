import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('../components/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard',
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('../views/Projects.vue'),
      },
      {
        path: 'projects/new',
        name: 'NewProject',
        component: () => import('../views/ProjectForm.vue'),
      },
      {
        path: 'projects/:id',
        name: 'ProjectDetail',
        component: () => import('../views/ProjectDetail.vue'),
      },
      {
        path: 'projects/:id/edit',
        name: 'EditProject',
        component: () => import('../views/ProjectForm.vue'),
      },
      {
        path: 'risk-analysis',
        name: 'RiskAnalysis',
        component: () => import('../views/RiskAnalysis.vue'),
      },
      {
        path: 'about',
        name: 'About',
        component: () => import('../views/About.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('caw_token')
  if (to.meta.requiresAuth !== false && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
