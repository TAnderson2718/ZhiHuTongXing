<template>
  <div>
    <!-- Loading状态 -->
    <div v-if="loading" class="min-h-screen flex items-center justify-center">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500 mx-auto mb-4"></div>
        <p class="text-gray-600">正在加载内容...</p>
      </div>
    </div>

    <!-- 首页内容 -->
    <div v-else>
      <HeaderComponent 
        :title="content.texts.main_title || '智护童行'"
        @navigate="navigateTo"
      />
      
      <main>
        <!-- Hero Section -->
        <section class="hero-gradient py-20 md:py-32">
          <div class="container mx-auto px-6 text-center">
            <h1 class="text-4xl md:text-6xl font-bold text-gray-800 mb-6">
              {{ content.texts.main_title || '智护童行' }}
            </h1>
            <p class="text-xl md:text-2xl text-gray-700 mb-8 max-w-3xl mx-auto">
              {{ content.texts.main_subtitle || '专业的家庭照护教育平台' }}
            </p>
            <p class="text-lg text-gray-600 mb-10 max-w-2xl mx-auto">
              {{ content.texts.main_description || '从自我评估到专业学习，我们为您提供一站式家庭照护解决方案' }}
            </p>
            <router-link 
              to="/assessment"
              class="bg-teal-500 text-white font-semibold px-8 py-4 rounded-full hover:bg-teal-600 transition-all shadow-lg text-lg inline-block"
            >
              开始体验
            </router-link>
          </div>
        </section>

        <!-- 功能展馆 -->
        <section id="halls" class="py-16 md:py-24 bg-white">
          <div class="container mx-auto px-6">
            <div class="text-center mb-12">
              <h2 class="text-3xl md:text-4xl font-bold">
                {{ content.texts.halls_title || '探索五大核心功能展馆' }}
              </h2>
              <p class="text-gray-600 mt-2 max-w-2xl mx-auto">
                {{ content.texts.halls_description || '从自我评估到专业学习，我们为您提供一站式家庭照护解决方案。' }}
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              <!-- 自我评估 -->
              <HallCard
                :title="content.texts.assessment_title || '自我评估'"
                :description="content.texts.assessment_description || '了解您当前的照护知识水平'"
                :icon="content.images.assessment_icon"
                color="blue"
                @click="navigateTo('/assessment')"
              />

              <!-- 知识学习 -->
              <HallCard
                :title="content.texts.knowledge_title || '知识学习'"
                :description="content.texts.knowledge_description || '系统学习专业照护知识'"
                :icon="content.images.knowledge_icon"
                color="green"
                @click="navigateTo('/knowledge')"
              />

              <!-- 体验互动 -->
              <HallCard
                :title="content.texts.experience_title || '体验互动'"
                :description="content.texts.experience_description || '通过游戏化学习提升技能'"
                :icon="content.images.experience_icon"
                color="yellow"
                @click="navigateTo('/experience')"
              />

              <!-- 成长对策室 -->
              <HallCard
                :title="content.texts.support_title || '成长对策室'"
                :description="content.texts.support_description || '测评反馈、个性化干预、成长奖励'"
                :icon="content.images.support_icon"
                color="purple"
                @click="navigateTo('/support')"
              />

              <!-- 个人档案 -->
              <HallCard
                :title="content.texts.archive_title || '个人档案'"
                :description="content.texts.archive_description || '记录您的学习历程'"
                :icon="content.images.archive_icon"
                color="indigo"
                @click="navigateTo('/account')"
              />
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import HeaderComponent from '../components/HeaderComponent.vue'
import HallCard from '../components/HallCard.vue'

export default {
  name: 'HomePage',
  components: {
    HeaderComponent,
    HallCard
  },
  setup() {
    const router = useRouter()
    const loading = ref(true)
    const content = reactive({
      texts: {},
      images: {}
    })

    // 加载内容数据
    const loadContent = async () => {
      try {
        const response = await axios.get('/api/content')
        if (response.data.success) {
          Object.assign(content.texts, response.data.data.texts)
          Object.assign(content.images, response.data.data.images)
        }
      } catch (error) {
        console.error('加载内容失败:', error)
        // 使用默认内容
        content.texts = {
          main_title: '智护童行',
          main_subtitle: '专业的家庭照护教育平台',
          main_description: '从自我评估到专业学习，我们为您提供一站式家庭照护解决方案',
          halls_title: '探索五大核心功能展馆',
          halls_description: '从自我评估到专业学习，我们为您提供一站式家庭照护解决方案。',
          assessment_title: '自我评估',
          assessment_description: '了解您当前的照护知识水平',
          knowledge_title: '知识学习',
          knowledge_description: '系统学习专业照护知识',
          experience_title: '体验互动',
          experience_description: '通过游戏化学习提升技能',
          support_title: '成长对策室',
          support_description: '测评反馈、个性化干预、成长奖励',
          archive_title: '个人档案',
          archive_description: '记录您的学习历程'
        }
      } finally {
        loading.value = false
      }
    }

    // 页面导航 - 使用Vue Router
    const navigateTo = (path) => {
      router.push(path)
    }

    onMounted(() => {
      loadContent()
      
      // 初始化Lucide图标
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      loading,
      content,
      navigateTo
    }
  }
}
</script>

<style scoped>
.hero-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
}

/* 页面过渡动画 */
.page-transitioning {
  opacity: 0.9;
  transition: opacity 0.3s ease-in-out;
}
</style>
