<template>
  <div id="experience-page" class="page">
    <HeaderComponent title="智护童行" />
    
    <main class="container mx-auto px-6 py-12">
      <div class="max-w-4xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-12">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">体验互动</h1>
          <p class="text-gray-600 text-lg">通过游戏化学习提升您的照护技能</p>
        </div>

        <!-- 互动游戏列表 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          <!-- 情景模拟游戏 -->
          <div class="game-card bg-white rounded-2xl p-8 shadow-sm border hover:shadow-md transition-all cursor-pointer" @click="startGame('scenario')">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-6 mx-auto">
              <i data-lucide="play-circle" class="w-8 h-8 text-blue-600"></i>
            </div>
            <h3 class="text-xl font-semibold text-center mb-4">情景模拟</h3>
            <p class="text-gray-600 text-center mb-6">通过真实情景模拟，学习正确的应对方法</p>
            <div class="text-center">
              <span class="inline-block bg-blue-500 text-white px-6 py-2 rounded-full">开始游戏</span>
            </div>
          </div>

          <!-- 知识问答游戏 -->
          <div class="game-card bg-white rounded-2xl p-8 shadow-sm border hover:shadow-md transition-all cursor-pointer" @click="startGame('quiz')">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-6 mx-auto">
              <i data-lucide="help-circle" class="w-8 h-8 text-green-600"></i>
            </div>
            <h3 class="text-xl font-semibold text-center mb-4">知识问答</h3>
            <p class="text-gray-600 text-center mb-6">快速问答，检验您的照护知识掌握程度</p>
            <div class="text-center">
              <span class="inline-block bg-green-500 text-white px-6 py-2 rounded-full">开始游戏</span>
            </div>
          </div>

          <!-- 护理技能练习 -->
          <div class="game-card bg-white rounded-2xl p-8 shadow-sm border hover:shadow-md transition-all cursor-pointer" @click="startGame('skills')">
            <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mb-6 mx-auto">
              <i data-lucide="target" class="w-8 h-8 text-yellow-600"></i>
            </div>
            <h3 class="text-xl font-semibold text-center mb-4">技能练习</h3>
            <p class="text-gray-600 text-center mb-6">互动式技能训练，提升实际操作能力</p>
            <div class="text-center">
              <span class="inline-block bg-yellow-500 text-white px-6 py-2 rounded-full">开始练习</span>
            </div>
          </div>

          <!-- 安全知识挑战 -->
          <div class="game-card bg-white rounded-2xl p-8 shadow-sm border hover:shadow-md transition-all cursor-pointer" @click="startGame('safety')">
            <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-6 mx-auto">
              <i data-lucide="shield-alert" class="w-8 h-8 text-red-600"></i>
            </div>
            <h3 class="text-xl font-semibold text-center mb-4">安全挑战</h3>
            <p class="text-gray-600 text-center mb-6">学习识别和应对各种安全隐患</p>
            <div class="text-center">
              <span class="inline-block bg-red-500 text-white px-6 py-2 rounded-full">接受挑战</span>
            </div>
          </div>
        </div>

        <!-- 游戏统计 -->
        <div class="bg-white rounded-lg shadow-sm border p-8 mb-8">
          <h2 class="text-2xl font-semibold mb-6 text-center">游戏统计</h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div class="text-center">
              <div class="text-3xl font-bold text-blue-600 mb-2">{{ gameStats.totalGames }}</div>
              <div class="text-gray-600">总游戏次数</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-green-600 mb-2">{{ gameStats.correctAnswers }}%</div>
              <div class="text-gray-600">正确率</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-yellow-600 mb-2">{{ gameStats.skillPoints }}</div>
              <div class="text-gray-600">技能积分</div>
            </div>
            <div class="text-center">
              <div class="text-3xl font-bold text-purple-600 mb-2">{{ gameStats.achievements }}</div>
              <div class="text-gray-600">获得成就</div>
            </div>
          </div>
        </div>

        <!-- 返回按钮 -->
        <div class="text-center">
          <button 
            @click="$emit('navigate', 'home')"
            class="bg-gray-500 text-white font-semibold px-6 py-2 rounded-full hover:bg-gray-600 transition-colors"
          >
            返回首页
          </button>
        </div>
      </div>
    </main>

    <!-- 游戏模态框 -->
    <div v-if="currentGame" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold">{{ gameTitle }}</h2>
            <button @click="closeGame" class="text-gray-400 hover:text-gray-600">
              <i data-lucide="x" class="w-6 h-6"></i>
            </button>
          </div>

          <!-- 情景模拟游戏 -->
          <div v-if="currentGame === 'scenario'" class="space-y-6">
            <div class="bg-blue-50 p-6 rounded-lg">
              <h3 class="text-lg font-semibold mb-4">情景：孩子发烧了</h3>
              <p class="text-gray-700 mb-4">您的2岁孩子突然发烧到38.5°C，孩子显得很不舒服，您应该如何处理？</p>
              
              <div class="space-y-3">
                <button 
                  v-for="(option, index) in scenarioOptions" 
                  :key="index"
                  @click="selectScenarioOption(index)"
                  :class="{'bg-blue-500 text-white': selectedOption === index, 'bg-white border': selectedOption !== index}"
                  class="w-full p-3 rounded-lg text-left transition-colors hover:bg-blue-100"
                >
                  {{ option }}
                </button>
              </div>

              <div v-if="scenarioFeedback" class="mt-6 p-4 rounded-lg" :class="scenarioFeedback.class">
                <div v-html="scenarioFeedback.content"></div>
              </div>

              <div class="mt-6 text-center">
                <button 
                  @click="nextScenario"
                  class="bg-blue-500 text-white px-6 py-2 rounded-full hover:bg-blue-600 transition-colors"
                >
                  下一个情景
                </button>
              </div>
            </div>
          </div>

          <!-- 知识问答游戏 -->
          <div v-if="currentGame === 'quiz'" class="space-y-6">
            <div class="bg-green-50 p-6 rounded-lg">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold">问题 {{ quizCurrentQuestion + 1 }} / {{ quizQuestions.length }}</h3>
                <div class="text-sm text-gray-600">得分: {{ quizScore }}</div>
              </div>
              
              <p class="text-gray-700 mb-4">{{ quizQuestions[quizCurrentQuestion]?.question }}</p>
              
              <div class="space-y-3">
                <button 
                  v-for="(option, index) in quizQuestions[quizCurrentQuestion]?.options" 
                  :key="index"
                  @click="selectQuizOption(index)"
                  :class="{'bg-green-500 text-white': selectedQuizOption === index, 'bg-white border': selectedQuizOption !== index}"
                  class="w-full p-3 rounded-lg text-left transition-colors hover:bg-green-100"
                >
                  {{ option }}
                </button>
              </div>

              <div v-if="quizFeedback" class="mt-4 p-3 rounded" :class="quizFeedback.correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                {{ quizFeedback.message }}
              </div>

              <div class="mt-6 text-center">
                <button 
                  @click="nextQuizQuestion"
                  :disabled="selectedQuizOption === null"
                  class="bg-green-500 text-white px-6 py-2 rounded-full hover:bg-green-600 transition-colors disabled:bg-gray-400"
                >
                  {{ quizCurrentQuestion < quizQuestions.length - 1 ? '下一题' : '完成测试' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 其他游戏占位符 -->
          <div v-if="currentGame === 'skills' || currentGame === 'safety'" class="text-center py-12">
            <i data-lucide="construction" class="w-16 h-16 text-gray-400 mx-auto mb-4"></i>
            <h3 class="text-xl font-medium text-gray-600 mb-2">功能开发中</h3>
            <p class="text-gray-500">该游戏功能正在开发中，敬请期待！</p>
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
  name: 'ExperiencePage',
  components: {
    HeaderComponent
  },
  emits: ['navigate'],
  setup() {
    const currentGame = ref(null)
    const selectedOption = ref(null)
    const selectedQuizOption = ref(null)
    const scenarioFeedback = ref(null)
    const quizFeedback = ref(null)
    const quizCurrentQuestion = ref(0)
    const quizScore = ref(0)

    const gameStats = reactive({
      totalGames: 15,
      correctAnswers: 85,
      skillPoints: 1250,
      achievements: 8
    })

    const scenarioOptions = [
      "立即给孩子服用退烧药",
      "先进行物理降温，观察体温变化",
      "马上带孩子去医院",
      "让孩子多喝水，继续观察"
    ]

    const quizQuestions = [
      {
        question: "婴儿的正常体温范围是多少？",
        options: ["36.0-37.0°C", "36.5-37.5°C", "37.0-38.0°C", "35.5-36.5°C"],
        correct: 1
      },
      {
        question: "6个月大的婴儿应该开始添加什么？",
        options: ["蜂蜜", "辅食", "牛奶", "果汁"],
        correct: 1
      },
      {
        question: "预防婴儿猝死综合征，正确的睡姿是？",
        options: ["侧卧", "俯卧", "仰卧", "任意姿势"],
        correct: 2
      }
    ]

    const gameTitle = computed(() => {
      const titles = {
        scenario: '情景模拟游戏',
        quiz: '知识问答游戏',
        skills: '技能练习游戏',
        safety: '安全知识挑战'
      }
      return titles[currentGame.value] || ''
    })

    const startGame = (gameType) => {
      currentGame.value = gameType
      resetGameState()
    }

    const closeGame = () => {
      currentGame.value = null
      resetGameState()
    }

    const resetGameState = () => {
      selectedOption.value = null
      selectedQuizOption.value = null
      scenarioFeedback.value = null
      quizFeedback.value = null
      quizCurrentQuestion.value = 0
      quizScore.value = 0
    }

    const selectScenarioOption = (index) => {
      selectedOption.value = index
      
      const feedbacks = [
        {
          class: 'bg-yellow-100 border border-yellow-300',
          content: '<p class="font-semibold text-yellow-800">需要谨慎！</p><p class="text-yellow-700">直接用药可能不是最佳选择，建议先尝试物理降温。</p>'
        },
        {
          class: 'bg-green-100 border border-green-300',
          content: '<p class="font-semibold text-green-800">很好的选择！</p><p class="text-green-700">物理降温是处理发烧的首选方法，安全有效。</p>'
        },
        {
          class: 'bg-red-100 border border-red-300',
          content: '<p class="font-semibold text-red-800">过于紧张！</p><p class="text-red-700">38.5°C的发烧通常不需要立即就医，可以先在家处理。</p>'
        },
        {
          class: 'bg-blue-100 border border-blue-300',
          content: '<p class="font-semibold text-blue-800">部分正确！</p><p class="text-blue-700">多喝水是对的，但还需要配合物理降温措施。</p>'
        }
      ]
      
      scenarioFeedback.value = feedbacks[index]
    }

    const nextScenario = () => {
      // 这里可以加载下一个情景
      alert('恭喜完成情景模拟！')
      closeGame()
    }

    const selectQuizOption = (index) => {
      selectedQuizOption.value = index
      
      const currentQ = quizQuestions[quizCurrentQuestion.value]
      const isCorrect = index === currentQ.correct
      
      if (isCorrect) {
        quizScore.value += 10
        quizFeedback.value = {
          correct: true,
          message: '回答正确！'
        }
      } else {
        quizFeedback.value = {
          correct: false,
          message: `回答错误。正确答案是：${currentQ.options[currentQ.correct]}`
        }
      }
    }

    const nextQuizQuestion = () => {
      if (quizCurrentQuestion.value < quizQuestions.length - 1) {
        quizCurrentQuestion.value++
        selectedQuizOption.value = null
        quizFeedback.value = null
      } else {
        alert(`测试完成！您的得分是：${quizScore.value}分`)
        closeGame()
      }
    }

    onMounted(() => {
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      currentGame,
      gameTitle,
      gameStats,
      scenarioOptions,
      selectedOption,
      scenarioFeedback,
      quizQuestions,
      quizCurrentQuestion,
      quizScore,
      selectedQuizOption,
      quizFeedback,
      startGame,
      closeGame,
      selectScenarioOption,
      nextScenario,
      selectQuizOption,
      nextQuizQuestion
    }
  }
}
</script>
