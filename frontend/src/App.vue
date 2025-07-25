<template>
  <div id="app">
    <!-- 全局加载状态 -->
    <div v-if="globalLoading" class="min-h-screen flex items-center justify-center" data-testid="global-loading">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500 mx-auto mb-4"></div>
        <p class="text-gray-600">正在初始化应用...</p>
      </div>
    </div>

    <!-- Vue Router 视图容器 -->
    <div v-else class="app-container">
      <!-- 页面过渡动画 -->
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="$route.path" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const globalLoading = ref(true)

    // 应用初始化
    const initializeApp = async () => {
      try {
        // 检查API连接
        const apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001'
        const response = await fetch(`${apiUrl}/api/health`)
        if (!response.ok) {
          console.warn('API服务连接异常，使用离线模式')
        }
      } catch (error) {
        console.warn('API服务不可用，使用离线模式:', error)
      } finally {
        globalLoading.value = false
      }
    }

    onMounted(() => {
      initializeApp()
      
      // 初始化Lucide图标
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      globalLoading
    }
  }
}
</script>

<style>
/* 全局样式 */
#app {
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
}

/* 页面过渡动画 */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease-in-out;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 页面加载状态样式 */
.page-transitioning {
  opacity: 0.9;
  transition: opacity 0.3s ease-in-out;
}

/* 响应式容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 640px) {
  .container {
    padding: 0 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 2rem;
  }
}
</style>
