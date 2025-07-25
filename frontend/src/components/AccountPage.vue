<template>
  <div id="account-page" class="page">
    <HeaderComponent title="智护童行" />
    
    <main class="container mx-auto px-6 py-12">
      <div class="max-w-4xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-12">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">个人档案</h1>
          <p class="text-gray-600 text-lg">记录您的学习历程，管理个人信息</p>
        </div>

        <!-- 用户信息卡片 -->
        <div class="bg-white rounded-lg shadow-sm border p-8 mb-8">
          <div class="flex items-center space-x-6 mb-6">
            <div class="w-20 h-20 bg-teal-100 rounded-full flex items-center justify-center">
              <i data-lucide="user" class="w-10 h-10 text-teal-600"></i>
            </div>
            <div>
              <h2 class="text-2xl font-semibold mb-2">{{ userInfo.name }}</h2>
              <p class="text-gray-600">{{ userInfo.email }}</p>
              <p class="text-sm text-gray-500">注册时间：{{ userInfo.registerDate }}</p>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="text-center p-4 bg-blue-50 rounded-lg">
              <div class="text-2xl font-bold text-blue-600 mb-1">{{ userStats.coursesCompleted }}</div>
              <div class="text-gray-600">已完成课程</div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg">
              <div class="text-2xl font-bold text-green-600 mb-1">{{ userStats.studyHours }}</div>
              <div class="text-gray-600">学习时长(小时)</div>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg">
              <div class="text-2xl font-bold text-purple-600 mb-1">{{ userStats.certificates }}</div>
              <div class="text-gray-600">获得证书</div>
            </div>
          </div>
        </div>

        <!-- 标签页导航 -->
        <div class="mb-8">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="{'border-blue-500 text-blue-600 bg-blue-50': activeTab === tab.id, 'border-transparent text-gray-500 hover:text-gray-700': activeTab !== tab.id}"
                class="archive-tab-button whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
              >
                {{ tab.name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- 学习记录 -->
        <div v-if="activeTab === 'learning'" class="bg-white rounded-lg shadow-sm border p-8">
          <h3 class="text-xl font-semibold mb-6">学习记录</h3>
          <div class="space-y-4">
            <div v-for="record in learningRecords" :key="record.id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div class="flex items-center space-x-4">
                <div :class="record.type === 'course' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'" class="w-10 h-10 rounded-full flex items-center justify-center">
                  <i :data-lucide="record.type === 'course' ? 'book-open' : 'gamepad-2'" class="w-5 h-5"></i>
                </div>
                <div>
                  <h4 class="font-medium">{{ record.title }}</h4>
                  <p class="text-sm text-gray-600">{{ record.date }}</p>
                </div>
              </div>
              <div class="text-right">
                <div class="text-sm font-medium" :class="record.status === 'completed' ? 'text-green-600' : 'text-yellow-600'">
                  {{ record.status === 'completed' ? '已完成' : '进行中' }}
                </div>
                <div class="text-xs text-gray-500">{{ record.progress }}%</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 成就徽章 -->
        <div v-if="activeTab === 'achievements'" class="bg-white rounded-lg shadow-sm border p-8">
          <h3 class="text-xl font-semibold mb-6">成就徽章</h3>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div v-for="achievement in achievements" :key="achievement.id" class="text-center p-4 rounded-lg" :class="achievement.earned ? 'bg-yellow-50 border border-yellow-200' : 'bg-gray-50 border border-gray-200'">
              <div class="w-16 h-16 mx-auto mb-3 rounded-full flex items-center justify-center" :class="achievement.earned ? 'bg-yellow-100' : 'bg-gray-100'">
                <i :data-lucide="achievement.icon" class="w-8 h-8" :class="achievement.earned ? 'text-yellow-600' : 'text-gray-400'"></i>
              </div>
              <h4 class="font-medium mb-1" :class="achievement.earned ? 'text-gray-800' : 'text-gray-400'">{{ achievement.name }}</h4>
              <p class="text-xs" :class="achievement.earned ? 'text-gray-600' : 'text-gray-400'">{{ achievement.description }}</p>
              <div v-if="achievement.earned" class="text-xs text-yellow-600 mt-2">{{ achievement.earnedDate }}</div>
            </div>
          </div>
        </div>

        <!-- 设置 -->
        <div v-if="activeTab === 'settings'" class="bg-white rounded-lg shadow-sm border p-8">
          <h3 class="text-xl font-semibold mb-6">账户设置</h3>
          <div class="space-y-6">
            <!-- 个人信息 -->
            <div>
              <h4 class="font-medium mb-4">个人信息</h4>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">姓名</label>
                  <input v-model="editableUserInfo.name" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
                  <input v-model="editableUserInfo.email" type="email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
              </div>
            </div>

            <!-- 通知设置 -->
            <div>
              <h4 class="font-medium mb-4">通知设置</h4>
              <div class="space-y-3">
                <label class="flex items-center">
                  <input v-model="notificationSettings.email" type="checkbox" class="mr-3">
                  <span>邮件通知</span>
                </label>
                <label class="flex items-center">
                  <input v-model="notificationSettings.push" type="checkbox" class="mr-3">
                  <span>推送通知</span>
                </label>
                <label class="flex items-center">
                  <input v-model="notificationSettings.weekly" type="checkbox" class="mr-3">
                  <span>每周学习报告</span>
                </label>
              </div>
            </div>

            <!-- 保存按钮 -->
            <div class="pt-4">
              <button @click="saveSettings" class="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition-colors">
                保存设置
              </button>
            </div>
          </div>
        </div>

        <!-- 返回按钮 -->
        <div class="text-center mt-8">
          <button 
            @click="$emit('navigate', 'home')"
            class="bg-gray-500 text-white font-semibold px-6 py-2 rounded-full hover:bg-gray-600 transition-colors"
          >
            返回首页
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import HeaderComponent from './HeaderComponent.vue'

export default {
  name: 'AccountPage',
  components: {
    HeaderComponent
  },
  emits: ['navigate'],
  setup() {
    const activeTab = ref('learning')

    const tabs = [
      { id: 'learning', name: '学习记录' },
      { id: 'achievements', name: '成就徽章' },
      { id: 'settings', name: '设置' }
    ]

    const userInfo = reactive({
      name: '张小明',
      email: 'zhangxiaoming@example.com',
      registerDate: '2024-01-15'
    })

    const editableUserInfo = reactive({
      name: userInfo.name,
      email: userInfo.email
    })

    const userStats = reactive({
      coursesCompleted: 8,
      studyHours: 25.5,
      certificates: 3
    })

    const notificationSettings = reactive({
      email: true,
      push: false,
      weekly: true
    })

    const learningRecords = [
      {
        id: 1,
        title: '新生儿护理基础',
        type: 'course',
        date: '2024-07-20',
        status: 'completed',
        progress: 100
      },
      {
        id: 2,
        title: '情景模拟游戏',
        type: 'game',
        date: '2024-07-22',
        status: 'completed',
        progress: 100
      },
      {
        id: 3,
        title: '婴幼儿营养与喂养',
        type: 'course',
        date: '2024-07-24',
        status: 'in_progress',
        progress: 65
      },
      {
        id: 4,
        title: '知识问答挑战',
        type: 'game',
        date: '2024-07-25',
        status: 'in_progress',
        progress: 80
      }
    ]

    const achievements = [
      {
        id: 1,
        name: '初学者',
        description: '完成第一个课程',
        icon: 'star',
        earned: true,
        earnedDate: '2024-07-20'
      },
      {
        id: 2,
        name: '知识达人',
        description: '完成5个课程',
        icon: 'book',
        earned: true,
        earnedDate: '2024-07-23'
      },
      {
        id: 3,
        name: '游戏高手',
        description: '完成10个互动游戏',
        icon: 'gamepad-2',
        earned: false,
        earnedDate: null
      },
      {
        id: 4,
        name: '学习之星',
        description: '连续学习7天',
        icon: 'trophy',
        earned: true,
        earnedDate: '2024-07-22'
      },
      {
        id: 5,
        name: '专家认证',
        description: '获得专业认证',
        icon: 'award',
        earned: false,
        earnedDate: null
      },
      {
        id: 6,
        name: '分享达人',
        description: '分享10次学习心得',
        icon: 'share',
        earned: false,
        earnedDate: null
      },
      {
        id: 7,
        name: '完美主义者',
        description: '所有测试满分',
        icon: 'target',
        earned: false,
        earnedDate: null
      },
      {
        id: 8,
        name: '社区贡献者',
        description: '帮助其他用户50次',
        icon: 'users',
        earned: false,
        earnedDate: null
      }
    ]

    const saveSettings = () => {
      // 这里可以调用API保存设置
      Object.assign(userInfo, editableUserInfo)
      alert('设置已保存！')
    }

    onMounted(() => {
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      activeTab,
      tabs,
      userInfo,
      editableUserInfo,
      userStats,
      notificationSettings,
      learningRecords,
      achievements,
      saveSettings
    }
  }
}
</script>
