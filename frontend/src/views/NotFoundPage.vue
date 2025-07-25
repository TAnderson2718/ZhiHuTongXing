<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <div class="mb-8">
        <i data-lucide="search-x" class="w-24 h-24 text-gray-400 mx-auto mb-4"></i>
        <h1 class="text-6xl font-bold text-gray-800 mb-4">404</h1>
        <h2 class="text-2xl font-semibold text-gray-600 mb-4">页面未找到</h2>
        <p class="text-gray-500 mb-8 max-w-md mx-auto">
          抱歉，您访问的页面不存在。可能是链接错误或页面已被移动。
        </p>
      </div>
      
      <div class="space-y-4">
        <router-link 
          to="/"
          class="inline-block bg-teal-500 text-white font-semibold px-6 py-3 rounded-full hover:bg-teal-600 transition-colors"
        >
          返回首页
        </router-link>
        
        <div class="text-sm text-gray-400">
          <p>或者尝试以下页面：</p>
          <div class="flex justify-center space-x-4 mt-2">
            <router-link to="/assessment" class="text-teal-500 hover:text-teal-600">自我评估</router-link>
            <router-link to="/knowledge" class="text-teal-500 hover:text-teal-600">知识学习</router-link>
            <router-link to="/support" class="text-teal-500 hover:text-teal-600">成长对策室</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'

export default {
  name: 'NotFoundPage',
  setup() {
    onMounted(() => {
      // 初始化Lucide图标
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })
  }
}
</script>
