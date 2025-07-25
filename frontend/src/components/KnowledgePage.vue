<template>
  <div id="knowledge-page" class="page">
    <HeaderComponent title="智护童行" />
    
    <main class="container mx-auto px-6 py-12">
      <div class="max-w-6xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-12">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">知识学习</h1>
          <p class="text-gray-600 text-lg">系统学习专业照护知识，提升您的照护技能</p>
        </div>

        <!-- 课程标签页 -->
        <div class="mb-8">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button 
                v-for="tab in courseTabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="{'border-emerald-500 text-emerald-600 bg-emerald-50': activeTab === tab.id, 'border-transparent text-gray-500 hover:text-gray-700': activeTab !== tab.id}"
                class="course-tab-button whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
              >
                {{ tab.name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- 课程内容 -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- 课程列表 -->
          <div class="lg:col-span-2">
            <!-- 基础护理课程 -->
            <div v-if="activeTab === 'basic'" class="space-y-6">
              <div v-for="course in basicCourses" :key="course.id" class="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow cursor-pointer" @click="selectCourse(course)">
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <i :data-lucide="course.icon" class="w-6 h-6 text-blue-600"></i>
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold mb-2">{{ course.title }}</h3>
                    <p class="text-gray-600 mb-3">{{ course.description }}</p>
                    <div class="flex items-center justify-between">
                      <div class="flex items-center space-x-4 text-sm text-gray-500">
                        <span><i data-lucide="clock" class="w-4 h-4 inline mr-1"></i>{{ course.duration }}</span>
                        <span><i data-lucide="users" class="w-4 h-4 inline mr-1"></i>{{ course.level }}</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <div class="w-20 bg-gray-200 rounded-full h-2">
                          <div class="bg-blue-600 h-2 rounded-full" :style="{width: course.progress + '%'}"></div>
                        </div>
                        <span class="text-sm text-gray-500">{{ course.progress }}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 进阶技能课程 -->
            <div v-if="activeTab === 'advanced'" class="space-y-6">
              <div v-for="course in advancedCourses" :key="course.id" class="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow cursor-pointer" @click="selectCourse(course)">
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <i :data-lucide="course.icon" class="w-6 h-6 text-green-600"></i>
                  </div>
                  <div class="flex-1">
                    <h3 class="text-lg font-semibold mb-2">{{ course.title }}</h3>
                    <p class="text-gray-600 mb-3">{{ course.description }}</p>
                    <div class="flex items-center justify-between">
                      <div class="flex items-center space-x-4 text-sm text-gray-500">
                        <span><i data-lucide="clock" class="w-4 h-4 inline mr-1"></i>{{ course.duration }}</span>
                        <span><i data-lucide="users" class="w-4 h-4 inline mr-1"></i>{{ course.level }}</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <div class="w-20 bg-gray-200 rounded-full h-2">
                          <div class="bg-green-600 h-2 rounded-full" :style="{width: course.progress + '%'}"></div>
                        </div>
                        <span class="text-sm text-gray-500">{{ course.progress }}%</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 专题讲座 -->
            <div v-if="activeTab === 'lectures'" class="space-y-6">
              <!-- 视频列表 -->
              <div v-if="videos && videos.length > 0" class="space-y-6">
                <div v-for="video in videos" :key="video.id" class="bg-white rounded-lg shadow-sm border overflow-hidden">
                  <div class="aspect-video bg-gray-100">
                    <video 
                      v-if="video.file_path" 
                      :src="video.file_path" 
                      class="w-full h-full object-cover" 
                      controls 
                      :poster="video.thumbnail || ''"
                      preload="metadata"
                    >
                      您的浏览器不支持视频播放。
                    </video>
                    <div v-else class="w-full h-full flex items-center justify-center">
                      <i data-lucide="video-off" class="w-12 h-12 text-gray-400"></i>
                    </div>
                  </div>
                  <div class="p-6">
                    <h3 class="text-xl font-semibold mb-2">{{ video.title || '未命名视频' }}</h3>
                    <p class="text-gray-600 mb-4">{{ video.description || '暂无描述' }}</p>
                    <div class="flex items-center justify-between text-sm text-gray-500">
                      <div class="flex items-center space-x-4">
                        <span v-if="video.duration">
                          <i data-lucide="clock" class="w-4 h-4 inline mr-1"></i>
                          {{ formatDuration(video.duration) }}
                        </span>
                        <span v-if="video.file_size">
                          <i data-lucide="file" class="w-4 h-4 inline mr-1"></i>
                          {{ formatFileSize(video.file_size) }}
                        </span>
                      </div>
                      <span v-if="video.created_at">
                        <i data-lucide="calendar" class="w-4 h-4 inline mr-1"></i>
                        {{ formatDate(video.created_at) }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 无视频时的提示 -->
              <div v-else class="text-center py-12">
                <i data-lucide="video" class="w-16 h-16 text-gray-400 mx-auto mb-4"></i>
                <h3 class="text-xl font-medium text-gray-600 mb-2">专题讲座</h3>
                <p class="text-gray-500">暂无专家讲座视频，敬请期待！</p>
              </div>
            </div>
          </div>

          <!-- 侧边栏 -->
          <div class="space-y-6">
            <!-- 学习进度 -->
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-lg font-semibold mb-4">学习进度</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>基础护理</span>
                    <span>{{ overallProgress.basic }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" :style="{width: overallProgress.basic + '%'}"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>进阶技能</span>
                    <span>{{ overallProgress.advanced }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-600 h-2 rounded-full" :style="{width: overallProgress.advanced + '%'}"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 推荐课程 -->
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-lg font-semibold mb-4">推荐课程</h3>
              <div class="space-y-3">
                <div v-for="rec in recommendations" :key="rec.id" class="p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100 transition-colors" @click="selectCourse(rec)">
                  <h4 class="font-medium text-sm mb-1">{{ rec.title }}</h4>
                  <p class="text-xs text-gray-600">{{ rec.reason }}</p>
                </div>
              </div>
            </div>

            <!-- 学习统计 -->
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-lg font-semibold mb-4">学习统计</h3>
              <div class="space-y-3">
                <div class="flex justify-between">
                  <span class="text-gray-600">已完成课程</span>
                  <span class="font-semibold">{{ stats.completed }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">学习时长</span>
                  <span class="font-semibold">{{ stats.totalTime }}小时</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-600">获得证书</span>
                  <span class="font-semibold">{{ stats.certificates }}</span>
                </div>
              </div>
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

    <!-- 课程详情模态框 -->
    <div v-if="selectedCourse" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" @click="selectedCourse = null">
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto" @click.stop>
        <div class="p-6">
          <div class="flex justify-between items-start mb-4">
            <h2 class="text-2xl font-bold">{{ selectedCourse.title }}</h2>
            <button @click="selectedCourse = null" class="text-gray-400 hover:text-gray-600">
              <i data-lucide="x" class="w-6 h-6"></i>
            </button>
          </div>
          
          <div class="prose max-w-none">
            <p class="text-gray-600 mb-6">{{ selectedCourse.description }}</p>
            
            <h3>课程内容</h3>
            <ul>
              <li v-for="item in selectedCourse.content" :key="item">{{ item }}</li>
            </ul>
            
            <h3>学习目标</h3>
            <ul>
              <li v-for="goal in selectedCourse.goals" :key="goal">{{ goal }}</li>
            </ul>
          </div>
          
          <div class="flex justify-between items-center mt-6 pt-6 border-t">
            <div class="text-sm text-gray-500">
              <span class="mr-4"><i data-lucide="clock" class="w-4 h-4 inline mr-1"></i>{{ selectedCourse.duration }}</span>
              <span><i data-lucide="users" class="w-4 h-4 inline mr-1"></i>{{ selectedCourse.level }}</span>
            </div>
            <button class="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition-colors">
              开始学习
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import HeaderComponent from './HeaderComponent.vue'

export default {
  name: 'KnowledgePage',
  components: {
    HeaderComponent
  },
  emits: ['navigate'],
  setup() {
    const activeTab = ref('basic')
    const selectedCourse = ref(null)
    const videos = ref([])

    const courseTabs = [
      { id: 'basic', name: '基础护理' },
      { id: 'advanced', name: '进阶技能' },
      { id: 'lectures', name: '专题讲座' }
    ]

    const basicCourses = [
      {
        id: 1,
        title: '新生儿护理基础',
        description: '学习新生儿的基本护理知识，包括喂养、换尿布、洗澡等日常护理技能。',
        duration: '2小时',
        level: '初级',
        progress: 75,
        icon: 'baby',
        content: [
          '新生儿的生理特点',
          '正确的抱婴儿姿势',
          '母乳喂养技巧',
          '换尿布的步骤',
          '新生儿洗澡注意事项'
        ],
        goals: [
          '掌握新生儿基本护理技能',
          '了解新生儿的生理需求',
          '学会安全抱婴儿的方法'
        ]
      },
      {
        id: 2,
        title: '婴幼儿营养与喂养',
        description: '了解不同年龄段婴幼儿的营养需求，学习科学的喂养方法。',
        duration: '1.5小时',
        level: '初级',
        progress: 50,
        icon: 'utensils',
        content: [
          '婴幼儿营养需求',
          '辅食添加原则',
          '常见营养问题',
          '喂养时间安排',
          '食物过敏预防'
        ],
        goals: [
          '制定科学的喂养计划',
          '识别营养不良症状',
          '预防食物过敏'
        ]
      },
      {
        id: 3,
        title: '儿童安全防护',
        description: '学习家庭环境安全防护措施，预防儿童意外伤害。',
        duration: '1小时',
        level: '初级',
        progress: 25,
        icon: 'shield',
        content: [
          '家庭安全隐患排查',
          '常见意外伤害预防',
          '急救基本知识',
          '安全用品使用',
          '外出安全注意事项'
        ],
        goals: [
          '建立安全的家庭环境',
          '掌握基本急救技能',
          '提高安全意识'
        ]
      }
    ]

    const advancedCourses = [
      {
        id: 4,
        title: '儿童心理发展',
        description: '深入了解儿童心理发展规律，学习正确的教育引导方法。',
        duration: '3小时',
        level: '中级',
        progress: 0,
        icon: 'brain',
        content: [
          '儿童心理发展阶段',
          '情绪管理技巧',
          '行为问题应对',
          '亲子沟通方法',
          '性格培养策略'
        ],
        goals: [
          '理解儿童心理发展规律',
          '掌握有效沟通技巧',
          '培养孩子良好性格'
        ]
      },
      {
        id: 5,
        title: '特殊需求儿童护理',
        description: '学习特殊需求儿童的专业护理知识和技能。',
        duration: '4小时',
        level: '高级',
        progress: 0,
        icon: 'heart',
        content: [
          '特殊需求儿童识别',
          '专业护理技巧',
          '康复训练方法',
          '家庭支持策略',
          '资源获取途径'
        ],
        goals: [
          '提供专业护理服务',
          '制定个性化护理计划',
          '获得专业资源支持'
        ]
      }
    ]

    const overallProgress = computed(() => {
      const basicTotal = basicCourses.reduce((sum, course) => sum + course.progress, 0)
      const advancedTotal = advancedCourses.reduce((sum, course) => sum + course.progress, 0)
      
      return {
        basic: Math.round(basicTotal / basicCourses.length),
        advanced: Math.round(advancedTotal / advancedCourses.length)
      }
    })

    const recommendations = [
      {
        id: 1,
        title: '新生儿护理基础',
        reason: '基于您的评估结果推荐'
      },
      {
        id: 3,
        title: '儿童安全防护',
        reason: '热门课程，用户好评率高'
      }
    ]

    const stats = {
      completed: 2,
      totalTime: 8.5,
      certificates: 1
    }

    const selectCourse = (course) => {
      selectedCourse.value = course
    }

    // 加载视频数据
    const loadVideos = async () => {
      try {
        const response = await fetch('/api/content')
        const data = await response.json()
        if (data.success && data.data.videos) {
          videos.value = data.data.videos
        }
      } catch (error) {
        console.error('加载视频数据失败:', error)
      }
    }

    // 工具方法
    const formatFileSize = (bytes) => {
      if (!bytes) return '未知'
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(1024))
      return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
    }

    const formatDate = (dateString) => {
      if (!dateString) return '未知'
      return new Date(dateString).toLocaleDateString('zh-CN')
    }

    const formatDuration = (seconds) => {
      if (!seconds) return '未知'
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = Math.floor(seconds % 60)
      
      if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      } else {
        return `${minutes}:${secs.toString().padStart(2, '0')}`
      }
    }

    onMounted(async () => {
      await loadVideos()
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      activeTab,
      courseTabs,
      basicCourses,
      advancedCourses,
      overallProgress,
      recommendations,
      stats,
      selectedCourse,
      selectCourse,
      videos,
      formatFileSize,
      formatDate,
      formatDuration
    }
  }
}
</script>
