/**
 * 智护童行前端应用入口文件
 * 集成Vue Router和全局配置
 */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 创建Vue应用实例
const app = createApp(App)

// 使用Vue Router
app.use(router)

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue应用错误:', err)
  console.error('错误信息:', info)
  
  // 可以在这里添加错误上报逻辑
  if (typeof gtag !== 'undefined') {
    gtag('event', 'exception', {
      description: err.toString(),
      fatal: false
    })
  }
}

// 全局属性配置
app.config.globalProperties.$appName = '智护童行'
app.config.globalProperties.$version = '2.0.0'

// 开发环境配置
if (import.meta.env.DEV) {
  app.config.performance = true
  console.log('🚀 智护童行前端应用启动 (开发模式)')
  console.log('📦 Vue Router已集成')
  console.log('🎨 页面过渡动画已启用')
}

// 挂载应用
app.mount('#app')
