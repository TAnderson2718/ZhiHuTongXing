<template>
  <header class="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
    <div class="container mx-auto px-6 py-4 flex justify-between items-center">
      <!-- Logo和标题 -->
      <router-link to="/" class="flex items-center space-x-2 hover:opacity-80 transition-opacity">
        <div class="w-8 h-8 bg-teal-500 rounded-lg flex items-center justify-center">
          <i data-lucide="heart" class="w-5 h-5 text-white"></i>
        </div>
        <span class="text-xl font-bold text-gray-800">{{ title }}</span>
      </router-link>
      
      <!-- 导航菜单 -->
      <nav class="hidden md:flex space-x-8">
        <router-link 
          to="/" 
          class="nav-link"
          :class="{ 'nav-link-active': $route.path === '/' }"
        >
          首页
        </router-link>
        <router-link 
          to="/assessment" 
          class="nav-link"
          :class="{ 'nav-link-active': $route.path === '/assessment' }"
        >
          自我评估
        </router-link>
        <router-link 
          to="/knowledge" 
          class="nav-link"
          :class="{ 'nav-link-active': $route.path === '/knowledge' }"
        >
          知识学习
        </router-link>
        <router-link 
          to="/experience" 
          class="nav-link"
          :class="{ 'nav-link-active': $route.path === '/experience' }"
        >
          体验互动
        </router-link>
        <router-link 
          to="/support" 
          class="nav-link"
          :class="{ 'nav-link-active': $route.path === '/support' }"
        >
          成长对策室
        </router-link>
      </nav>
      
      <!-- 移动端菜单按钮 -->
      <div class="md:hidden">
        <button 
          @click="toggleMobileMenu" 
          class="text-gray-600 hover:text-teal-600 transition-colors"
        >
          <i data-lucide="menu" class="w-6 h-6"></i>
        </button>
      </div>
      
      <!-- 登录按钮 -->
      <div class="hidden md:block">
        <router-link 
          to="/account" 
          class="bg-teal-500 text-white font-semibold px-5 py-2 rounded-full hover:bg-teal-600 transition-all shadow-sm inline-block"
        >
          登录 / 注册
        </router-link>
      </div>
    </div>
    
    <!-- 移动端菜单 -->
    <div v-if="showMobileMenu" class="md:hidden bg-white border-t border-gray-200">
      <nav class="px-6 py-4 space-y-2">
        <router-link 
          to="/" 
          @click="closeMobileMenu"
          class="block py-2 text-gray-600 hover:text-teal-600 transition-colors"
        >
          首页
        </router-link>
        <router-link 
          to="/assessment" 
          @click="closeMobileMenu"
          class="block py-2 text-gray-600 hover:text-teal-600 transition-colors"
        >
          自我评估
        </router-link>
        <router-link 
          to="/knowledge" 
          @click="closeMobileMenu"
          class="block py-2 text-gray-600 hover:text-teal-600 transition-colors"
        >
          知识学习
        </router-link>
        <router-link 
          to="/experience" 
          @click="closeMobileMenu"
          class="block py-2 text-gray-600 hover:text-teal-600 transition-colors"
        >
          体验互动
        </router-link>
        <router-link 
          to="/support" 
          @click="closeMobileMenu"
          class="block py-2 text-gray-600 hover:text-teal-600 transition-colors"
        >
          成长对策室
        </router-link>
        <router-link 
          to="/account" 
          @click="closeMobileMenu"
          class="block py-2 text-teal-500 font-semibold hover:text-teal-600 transition-colors"
        >
          登录 / 注册
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'HeaderComponent',
  props: {
    title: {
      type: String,
      default: '智护童行'
    }
  },
  setup() {
    const showMobileMenu = ref(false)

    // 切换移动端菜单
    const toggleMobileMenu = () => {
      showMobileMenu.value = !showMobileMenu.value
    }

    // 关闭移动端菜单
    const closeMobileMenu = () => {
      showMobileMenu.value = false
    }

    // 监听窗口大小变化，大屏幕时自动关闭移动端菜单
    const handleResize = () => {
      if (window.innerWidth >= 768) {
        showMobileMenu.value = false
      }
    }

    onMounted(() => {
      window.addEventListener('resize', handleResize)
      
      // 初始化Lucide图标
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      showMobileMenu,
      toggleMobileMenu,
      closeMobileMenu
    }
  }
}
</script>

<style scoped>
/* 导航链接样式 */
.nav-link {
  @apply text-gray-600 hover:text-teal-600 transition-colors relative;
}

.nav-link-active {
  @apply text-teal-600 font-semibold;
}

.nav-link-active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #14b8a6;
  border-radius: 1px;
}

/* 移动端菜单动画 */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
