<template>
  <div id="support-page" class="page">
    <HeaderComponent title="智护童行" />
    
    <main class="container mx-auto px-6 py-12">
      <div class="max-w-6xl mx-auto">
        <!-- 页面标题 -->
        <div class="text-center mb-12">
          <h1 class="text-3xl md:text-4xl font-bold mb-4">成长对策室</h1>
          <p class="text-gray-600 text-lg">个性化成长方案与专业指导，助力孩子健康成长</p>
        </div>

        <!-- 功能导航标签 -->
        <div class="mb-8">
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8">
              <button 
                v-for="tab in functionTabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="{'border-emerald-500 text-emerald-600 bg-emerald-50': activeTab === tab.id, 'border-transparent text-gray-500 hover:text-gray-700': activeTab !== tab.id}"
                class="whitespace-nowrap py-3 px-1 border-b-2 font-medium text-sm"
              >
                <i :data-lucide="tab.icon" class="w-4 h-4 inline mr-2"></i>
                {{ tab.name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- 功能内容区域 -->
        <div class="min-h-[600px]">
          <!-- 测评反馈分析 -->
          <div v-if="activeTab === 'assessment'" class="space-y-6">
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-xl font-semibold mb-4">儿童照护能力评估</h3>
              <p class="text-gray-600 mb-6">通过专业量表评估您的照护能力，获得个性化反馈建议</p>
              
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="scale in assessmentScales" :key="scale.id" class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer" @click="startAssessment(scale)">
                  <div class="flex items-center mb-3">
                    <i :data-lucide="scale.icon" class="w-5 h-5 text-blue-600 mr-2"></i>
                    <h4 class="font-medium">{{ scale.name }}</h4>
                  </div>
                  <p class="text-sm text-gray-600 mb-3">{{ scale.description }}</p>
                  <div class="flex justify-between items-center text-xs text-gray-500">
                    <span>{{ scale.questions }}题</span>
                    <span>{{ scale.duration }}分钟</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 历史评估记录 -->
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-xl font-semibold mb-4">评估历史</h3>
              <div v-if="assessmentHistory.length === 0" class="text-center py-8 text-gray-500">
                <i data-lucide="clipboard-list" class="w-12 h-12 mx-auto mb-3 text-gray-400"></i>
                <p>暂无评估记录，开始您的第一次评估吧！</p>
              </div>
              <div v-else class="space-y-3">
                <div v-for="record in assessmentHistory" :key="record.id" class="flex justify-between items-center p-3 border rounded hover:bg-gray-50">
                  <div>
                    <h4 class="font-medium">{{ record.scaleName }}</h4>
                    <p class="text-sm text-gray-600">{{ record.date }} | 得分: {{ record.score }}/{{ record.totalScore }}</p>
                  </div>
                  <button class="text-blue-600 hover:text-blue-800 text-sm">查看详情</button>
                </div>
              </div>
            </div>
          </div>

          <!-- 个性化干预方案 -->
          <div v-if="activeTab === 'intervention'" class="space-y-6">
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-xl font-semibold mb-4">AI智能推荐方案</h3>
              <p class="text-gray-600 mb-6">基于您的评估结果，为您推荐最适合的个性化干预方案</p>
              
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div v-for="plan in interventionPlans" :key="plan.id" class="border rounded-lg p-6 hover:shadow-md transition-shadow">
                  <div class="flex items-start justify-between mb-4">
                    <div class="flex items-center">
                      <div :class="`w-3 h-3 rounded-full mr-3 ${plan.priority === 'high' ? 'bg-red-500' : plan.priority === 'medium' ? 'bg-yellow-500' : 'bg-green-500'}`"></div>
                      <h4 class="font-semibold">{{ plan.title }}</h4>
                    </div>
                    <span :class="`px-2 py-1 rounded text-xs ${plan.priority === 'high' ? 'bg-red-100 text-red-800' : plan.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}`">
                      {{ plan.priority === 'high' ? '高优先级' : plan.priority === 'medium' ? '中优先级' : '低优先级' }}
                    </span>
                  </div>
                  <p class="text-gray-600 mb-4">{{ plan.description }}</p>
                  <div class="space-y-2 mb-4">
                    <div v-for="step in plan.steps.slice(0, 3)" :key="step" class="flex items-center text-sm text-gray-600">
                      <i data-lucide="check-circle" class="w-4 h-4 text-green-500 mr-2"></i>
                      {{ step }}
                    </div>
                  </div>
                  <button class="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600 transition-colors" @click="selectPlan(plan)">
                    选择此方案
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 成长奖励 -->
          <div v-if="activeTab === 'rewards'" class="space-y-6">
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-xl font-semibold mb-4">成长奖励体系</h3>
              <p class="text-gray-600 mb-6">通过完成学习任务和实践活动，获得成长积分和家庭大礼包</p>
              
              <!-- 积分统计 -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-lg text-center">
                  <i data-lucide="star" class="w-8 h-8 mx-auto mb-2"></i>
                  <h4 class="font-semibold">当前积分</h4>
                  <p class="text-2xl font-bold">{{ userStats.currentPoints }}</p>
                </div>
                <div class="bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-lg text-center">
                  <i data-lucide="trophy" class="w-8 h-8 mx-auto mb-2"></i>
                  <h4 class="font-semibold">已获奖励</h4>
                  <p class="text-2xl font-bold">{{ userStats.rewardsEarned }}</p>
                </div>
                <div class="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-4 rounded-lg text-center">
                  <i data-lucide="calendar-check" class="w-8 h-8 mx-auto mb-2"></i>
                  <h4 class="font-semibold">连续学习</h4>
                  <p class="text-2xl font-bold">{{ userStats.streakDays }}天</p>
                </div>
              </div>
              
              <!-- 可兑换奖励 -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="reward in availableRewards" :key="reward.id" class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div class="text-center mb-4">
                    <i :data-lucide="reward.icon" class="w-12 h-12 mx-auto mb-2 text-yellow-500"></i>
                    <h4 class="font-semibold">{{ reward.name }}</h4>
                  </div>
                  <p class="text-sm text-gray-600 mb-4">{{ reward.description }}</p>
                  <div class="flex justify-between items-center mb-3">
                    <span class="text-sm text-gray-500">需要积分:</span>
                    <span class="font-semibold text-blue-600">{{ reward.points }}</span>
                  </div>
                  <button 
                    :disabled="userStats.currentPoints < reward.points"
                    :class="userStats.currentPoints >= reward.points ? 'bg-yellow-500 hover:bg-yellow-600 text-white' : 'bg-gray-300 text-gray-500 cursor-not-allowed'"
                    class="w-full py-2 rounded transition-colors"
                    @click="claimReward(reward)"
                  >
                    {{ userStats.currentPoints >= reward.points ? '立即兑换' : '积分不足' }}
                  </button>
                </div>
              </div>
            </div>
            
            <!-- 案例分析 -->
            <div class="bg-white rounded-lg shadow-sm border p-6">
              <h3 class="text-xl font-semibold mb-4">成功案例分析</h3>
              <div class="space-y-4">
                <div v-for="caseStudy in caseStudies" :key="caseStudy.id" class="border-l-4 border-green-500 pl-4 py-2">
                  <h4 class="font-medium text-green-800">{{ caseStudy.title }}</h4>
                  <p class="text-sm text-gray-600 mt-1">{{ caseStudy.summary }}</p>
                  <button class="text-green-600 hover:text-green-800 text-sm mt-2">查看详细案例 →</button>
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
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import HeaderComponent from './HeaderComponent.vue'

export default {
  name: 'SupportPage',
  components: {
    HeaderComponent
  },
  emits: ['navigate'],
  setup() {
    const activeTab = ref('assessment')
    
    // 功能标签页
    const functionTabs = [
      { id: 'assessment', name: '测评反馈分析', icon: 'clipboard-list' },
      { id: 'intervention', name: '个性化干预方案', icon: 'brain' },
      { id: 'rewards', name: '成长奖励', icon: 'gift' }
    ]
    
    // 评估量表数据
    const assessmentScales = [
      {
        id: 1,
        name: '儿童照护能力量表',
        description: '评估您在日常照护中的能力水平',
        icon: 'baby',
        questions: 25,
        duration: 10
      },
      {
        id: 2,
        name: '长处和困难问卷',
        description: '了解孩子的行为特点和情绪状态',
        icon: 'heart',
        questions: 30,
        duration: 15
      },
      {
        id: 3,
        name: '父母教育方式量表',
        description: '评估您的教育方式和养育理念',
        icon: 'users',
        questions: 20,
        duration: 8
      },
      {
        id: 4,
        name: '亲子关系量表',
        description: '评估亲子互动质量和关系亲密度',
        icon: 'heart-handshake',
        questions: 18,
        duration: 7
      },
      {
        id: 5,
        name: '父母自我效能感量表',
        description: '评估您对自己照护能力的信心程度',
        icon: 'shield-check',
        questions: 15,
        duration: 6
      },
      {
        id: 6,
        name: '父母教养能力量表',
        description: '综合评估您的教养能力和技巧',
        icon: 'graduation-cap',
        questions: 22,
        duration: 12
      }
    ]
    
    // 评估历史记录
    const assessmentHistory = reactive([])
    
    // 个性化干预方案
    const interventionPlans = [
      {
        id: 1,
        title: '早期亲子互动增强方案',
        description: '通过互动游戏和日常活动增强亲子关系',
        priority: 'high',
        steps: ['每日亲子阅读15分钟', '定期进行亲子游戏', '建立固定的交流时间', '共同参与家务劳动']
      },
      {
        id: 2,
        title: '情绪管理技巧培养',
        description: '帮助孩子学会识别和管理自己的情绪',
        priority: 'medium',
        steps: ['教孩子识别情绪', '练习深呼吸放松', '使用情绪表达卡片', '建立情绪日记']
      },
      {
        id: 3,
        title: '行为问题干预计划',
        description: '针对具体行为问题制定系统性干预策略',
        priority: 'high',
        steps: ['行为观察和记录', '分析行为触发因素', '制定干预策略', '定期评估效果']
      },
      {
        id: 4,
        title: '学习能力提升方案',
        description: '通过科学方法提升孩子的学习能力和效率',
        priority: 'medium',
        steps: ['评估学习风格', '制定个性化学习计划', '设置学习目标', '定期复习和强化']
      },
      {
        id: 5,
        title: '社交技能培养计划',
        description: '帮助孩子发展良好的社交技能和人际关系',
        priority: 'low',
        steps: ['角色扮演练习', '组织小组活动', '教授沟通技巧', '鼓励主动交友']
      },
      {
        id: 6,
        title: '生活自理能力训练',
        description: '培养孩子的独立生活能力和自理意识',
        priority: 'medium',
        steps: ['分阶段设置目标', '教授基本生活技能', '鼓励独立完成任务', '及时给予表扬']
      }
    ]
    
    // 用户统计数据
    const userStats = reactive({
      currentPoints: 1250,
      rewardsEarned: 3,
      streakDays: 7
    })
    
    // 可兑换奖励
    const availableRewards = [
      {
        id: 1,
        name: '专业照护指南',
        description: '精美的儿童照护指南手册',
        icon: 'book',
        points: 500
      },
      {
        id: 2,
        name: '亲子互动游戏包',
        description: '包含10个趣味亲子游戏的指导包',
        icon: 'gamepad-2',
        points: 800
      },
      {
        id: 3,
        name: '专家一对一咨询',
        description: '30分钟专家在线一对一咨询服务',
        icon: 'user-check',
        points: 1200
      },
      {
        id: 4,
        name: '家庭教育大礼包',
        description: '包含多种教育资源和实用工具',
        icon: 'gift',
        points: 1500
      },
      {
        id: 5,
        name: '个性化成长报告',
        description: '基于评估结果的详细成长分析报告',
        icon: 'file-text',
        points: 1000
      },
      {
        id: 6,
        name: '高级课程解锁',
        description: '解锁所有高级照护技能课程',
        icon: 'unlock',
        points: 2000
      }
    ]
    
    // 成功案例
    const caseStudies = [
      {
        id: 1,
        title: '小明的情绪管理成功案例',
        summary: '通过系统的情绪管理训练，5岁的小明在3个月内显著改善了情绪控制能力'  
      },
      {
        id: 2,
        title: '亲子关系改善的实践经验',
        summary: '王女士通过亲子互动增强方案，与8岁儿子的关系在2个月内得到显著改善'
      },
      {
        id: 3,
        title: '学习能力提升的成功案例',
        summary: '通过个性化学习方案，7岁的小华在学习成绩和学习兴趣方面都有了大幅提升'
      }
    ]

    // 交互方法
    const startAssessment = (scale) => {
      alert(`开始「${scale.name}」评估，预计时间${scale.duration}分钟`)
      // TODO: 实现评估流程
    }
    
    const selectPlan = (plan) => {
      alert(`您选择了「${plan.title}」方案，系统将为您制定详细的实施计划`)
      // TODO: 实现方案选择和实施流程
    }
    
    const claimReward = (reward) => {
      if (userStats.currentPoints >= reward.points) {
        userStats.currentPoints -= reward.points
        userStats.rewardsEarned += 1
        alert(`成功兑换「${reward.name}」！奖励将在系统内发放给您`)
        // TODO: 实现奖励发放流程
      }
    }

    onMounted(() => {
      if (window.lucide) {
        window.lucide.createIcons()
      }
    })

    return {
      activeTab,
      functionTabs,
      assessmentScales,
      assessmentHistory,
      interventionPlans,
      userStats,
      availableRewards,
      caseStudies,
      startAssessment,
      selectPlan,
      claimReward
    }
  }
}
</script>
