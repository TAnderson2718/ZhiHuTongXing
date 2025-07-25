/**
 * Vue Router 路由配置
 * 智护童行前端路由管理
 */
import { createRouter, createWebHistory } from 'vue-router'

// 懒加载组件
const HomePage = () => import('../views/HomePage.vue')
const AssessmentPage = () => import('../components/AssessmentPage.vue')
const KnowledgePage = () => import('../components/KnowledgePage.vue')
const ExperiencePage = () => import('../components/ExperiencePage.vue')
const SupportPage = () => import('../components/SupportPage.vue')
const AccountPage = () => import('../components/AccountPage.vue')

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: {
      title: '智护童行 - 专业的家庭照护教育平台',
      description: '从自我评估到专业学习，我们为您提供一站式家庭照护解决方案',
      requiresAuth: false
    }
  },
  {
    path: '/assessment',
    name: 'Assessment',
    component: AssessmentPage,
    meta: {
      title: '自我评估 - 智护童行',
      description: '了解您当前的照护知识水平',
      requiresAuth: false
    }
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: KnowledgePage,
    meta: {
      title: '知识学习 - 智护童行',
      description: '系统学习专业照护知识',
      requiresAuth: false
    }
  },
  {
    path: '/experience',
    name: 'Experience',
    component: ExperiencePage,
    meta: {
      title: '体验互动 - 智护童行',
      description: '通过游戏化学习提升技能',
      requiresAuth: false
    }
  },
  {
    path: '/support',
    name: 'Support',
    component: SupportPage,
    meta: {
      title: '成长对策室 - 智护童行',
      description: '测评反馈、个性化干预、成长奖励',
      requiresAuth: false
    }
  },
  {
    path: '/account',
    name: 'Account',
    component: AccountPage,
    meta: {
      title: '个人档案 - 智护童行',
      description: '记录您的学习历程',
      requiresAuth: false
    }
  },
  {
    path: '/growth-strategy',
    redirect: '/support',
    meta: {
      title: '成长对策室 - 智护童行'
    }
  },
  // 404 页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundPage.vue'),
    meta: {
      title: '页面未找到 - 智护童行'
    }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 路由切换时的滚动行为
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }
  
  // 设置页面描述
  if (to.meta.description) {
    const metaDescription = document.querySelector('meta[name="description"]')
    if (metaDescription) {
      metaDescription.setAttribute('content', to.meta.description)
    }
  }
  
  // 添加页面加载动画类
  document.body.classList.add('page-transitioning')
  
  next()
})

// 全局后置钩子
router.afterEach((to, from) => {
  // 移除页面加载动画类
  setTimeout(() => {
    document.body.classList.remove('page-transitioning')
  }, 300)
  
  // 初始化Lucide图标
  if (window.lucide) {
    setTimeout(() => {
      window.lucide.createIcons()
    }, 100)
  }
  
  // 页面访问统计 (可选)
  if (typeof gtag !== 'undefined') {
    gtag('config', 'GA_MEASUREMENT_ID', {
      page_path: to.path
    })
  }
})

export default router
