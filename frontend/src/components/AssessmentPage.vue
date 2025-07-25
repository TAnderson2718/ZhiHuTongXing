<template>
  <div id="assessment-page" class="page">
    <HeaderComponent title="智护童行" />
    
    <main class="container mx-auto px-6 py-12">
      <div class="max-w-4xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-12">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">自我评估</h1>
          <p class="text-gray-600 text-lg">了解您当前的照护知识水平，为个性化学习做准备</p>
        </div>

        <!-- 评估选项卡 -->
        <div class="mb-8">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button 
                v-for="tab in assessmentTabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="{'border-emerald-500 text-emerald-600 bg-emerald-50': activeTab === tab.id, 'border-transparent text-gray-500 hover:text-gray-700': activeTab !== tab.id}"
                class="tab-button whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm"
              >
                {{ tab.name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- 评估内容 -->
        <div class="bg-white rounded-lg shadow-sm border p-8">
          <!-- 基础知识评估 -->
          <div v-if="activeTab === 'basic'" class="space-y-8">
            <h2 class="text-2xl font-semibold mb-6">基础照护知识评估</h2>
            
            <div v-for="(question, index) in basicQuestions" :key="index" class="assessment-card bg-gray-50 p-6 rounded-lg">
              <h3 class="text-lg font-medium mb-4">{{ index + 1 }}. {{ question.title }}</h3>
              <div class="space-y-3">
                <label v-for="(option, optionIndex) in question.options" :key="optionIndex" class="flex items-center space-x-3 cursor-pointer">
                  <input 
                    type="radio" 
                    :name="`basic-q${index}`" 
                    :value="optionIndex"
                    v-model="basicAnswers[index]"
                    class="w-4 h-4 text-emerald-600 focus:ring-emerald-500"
                  >
                  <span class="text-gray-700">{{ option }}</span>
                </label>
              </div>
            </div>

            <div class="text-center">
              <button 
                @click="submitBasicAssessment"
                :disabled="!isBasicComplete"
                class="bg-emerald-500 text-white font-semibold px-8 py-3 rounded-full hover:bg-emerald-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                提交评估
              </button>
            </div>

            <!-- 评估结果 -->
            <div v-if="basicResult" class="mt-8 p-6 bg-blue-50 rounded-lg border border-blue-200">
              <h3 class="text-xl font-semibold mb-4 text-blue-800">评估结果</h3>
              <div class="space-y-3">
                <p class="text-blue-700">您的得分：<span class="font-bold">{{ basicResult.score }}/{{ basicQuestions.length }}</span></p>
                <p class="text-blue-700">{{ basicResult.feedback }}</p>
                <div class="mt-4">
                  <div class="w-full bg-blue-200 rounded-full h-3">
                    <div 
                      class="bg-blue-600 h-3 rounded-full transition-all duration-500"
                      :style="{width: `${(basicResult.score / basicQuestions.length) * 100}%`}"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 情景应对评估 -->
          <div v-if="activeTab === 'scenario'" class="space-y-8">
            <h2 class="text-2xl font-semibold mb-6">情景应对能力评估</h2>
            
            <div class="assessment-card bg-gray-50 p-6 rounded-lg">
              <h3 class="text-lg font-medium mb-4">情景题：孩子拒绝吃饭</h3>
              <p class="text-gray-700 mb-6">您的3岁孩子最近总是拒绝吃饭，每次吃饭时间都变成了"战争"。作为家长，您会如何处理这种情况？</p>
              
              <div class="space-y-3">
                <label v-for="(option, index) in scenarioOptions" :key="index" class="flex items-start space-x-3 cursor-pointer p-3 rounded hover:bg-white transition-colors">
                  <input 
                    type="radio" 
                    name="scenario-q1" 
                    :value="index"
                    v-model="scenarioAnswer"
                    class="w-4 h-4 text-emerald-600 focus:ring-emerald-500 mt-1"
                  >
                  <span class="text-gray-700">{{ option }}</span>
                </label>
              </div>
            </div>

            <div class="text-center">
              <button 
                @click="submitScenarioAssessment"
                :disabled="scenarioAnswer === null"
                class="bg-emerald-500 text-white font-semibold px-8 py-3 rounded-full hover:bg-emerald-600 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                提交评估
              </button>
            </div>

            <!-- 情景评估结果 -->
            <div v-if="scenarioResult" class="mt-8 p-6 rounded-lg border" :class="scenarioResult.class">
              <h3 class="text-xl font-semibold mb-4">评估反馈</h3>
              <div v-html="scenarioResult.feedback"></div>
            </div>
          </div>

          <!-- 知识水平测试 -->
          <div v-if="activeTab === 'knowledge'" class="space-y-8">
            <h2 class="text-2xl font-semibold mb-6">专业知识水平测试</h2>
            <div class="text-center py-12">
              <i data-lucide="construction" class="w-16 h-16 text-gray-400 mx-auto mb-4"></i>
              <h3 class="text-xl font-medium text-gray-600 mb-2">功能开发中</h3>
              <p class="text-gray-500">专业知识水平测试功能正在开发中，敬请期待！</p>
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
import { ref, reactive, computed, onMounted } from 'vue'
import HeaderComponent from './HeaderComponent.vue'

export default {
  name: 'AssessmentPage',
  components: {
    HeaderComponent
  },
  emits: ['navigate'],
  setup() {
    const activeTab = ref('basic')
    const basicAnswers = reactive({})
    const scenarioAnswer = ref(null)
    const basicResult = ref(null)
    const scenarioResult = ref(null)

    const assessmentTabs = [
      { id: 'basic', name: '基础知识' },
      { id: 'scenario', name: '情景应对' },
      { id: 'knowledge', name: '知识水平' }
    ]

    const basicQuestions = [
      {
        title: "婴儿的正常体温范围是？",
        options: ["36.0-37.0°C", "36.5-37.5°C", "37.0-38.0°C", "35.5-36.5°C"],
        correct: 1
      },
      {
        title: "6个月大的婴儿应该开始添加什么？",
        options: ["蜂蜜", "辅食", "牛奶", "果汁"],
        correct: 1
      },
      {
        title: "孩子发烧时，首先应该做什么？",
        options: ["立即用药", "物理降温", "去医院", "观察等待"],
        correct: 1
      },
      {
        title: "预防婴儿猝死综合征，正确的睡姿是？",
        options: ["侧卧", "俯卧", "仰卧", "任意姿势"],
        correct: 2
      }
    ]

    const scenarioOptions = [
      "强迫孩子吃饭，告诉他不吃就没有零食",
      "耐心引导，尝试不同的食物搭配和用餐环境",
      "让孩子饿一顿，下次自然就会吃了",
      "用玩具或电子设备分散注意力让孩子吃饭"
    ]

    const isBasicComplete = computed(() => {
      return Object.keys(basicAnswers).length === basicQuestions.length
    })

    const submitBasicAssessment = () => {
      let score = 0
      basicQuestions.forEach((question, index) => {
        if (basicAnswers[index] == question.correct) {
          score++
        }
      })

      let feedback = ''
      if (score === basicQuestions.length) {
        feedback = '优秀！您对基础照护知识掌握得很好，可以继续学习更高级的内容。'
      } else if (score >= basicQuestions.length * 0.7) {
        feedback = '良好！您有一定的基础知识，建议继续加强学习。'
      } else {
        feedback = '需要加强！建议您从基础知识开始系统学习。'
      }

      basicResult.value = { score, feedback }
    }

    const submitScenarioAssessment = () => {
      const feedbacks = [
        {
          class: 'bg-red-50 border-red-200',
          feedback: '<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4" role="alert"><p class="font-bold">需要注意！</p><p>强迫进食可能会加剧孩子的抗拒心理，甚至引发权力斗争，对建立健康的饮食习惯不利。</p></div>'
        },
        {
          class: 'bg-green-50 border-green-200',
          feedback: '<div class="bg-green-100 border-l-4 border-green-500 text-green-700 p-4" role="alert"><p class="font-bold">非常棒的应对！</p><p>耐心引导和创造良好的用餐环境是解决孩子拒绝吃饭问题的最佳方法。这样可以培养孩子对食物的兴趣，建立健康的饮食习惯。</p></div>'
        },
        {
          class: 'bg-yellow-50 border-yellow-200',
          feedback: '<div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4" role="alert"><p class="font-bold">可以理解，但有更好的方式。</p><p>虽然适度的饥饿感可能会增加孩子的食欲，但完全不给食物可能会影响孩子的营养摄入和情感安全感。</p></div>'
        },
        {
          class: 'bg-yellow-50 border-yellow-200',
          feedback: '<div class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4" role="alert"><p class="font-bold">可以尝试的方法。</p><p>分散注意力确实可能让孩子吃饭，但这种方法可能会影响孩子对食物的专注度和消化，建议偶尔使用。</p></div>'
        }
      ]

      scenarioResult.value = feedbacks[scenarioAnswer.value]
    }

    onMounted(() => {
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      activeTab,
      assessmentTabs,
      basicQuestions,
      basicAnswers,
      scenarioOptions,
      scenarioAnswer,
      basicResult,
      scenarioResult,
      isBasicComplete,
      submitBasicAssessment,
      submitScenarioAssessment
    }
  }
}
</script>
