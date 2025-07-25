<template>
  <div class="hall-card bg-gray-50 rounded-2xl p-8 flex flex-col items-center text-center border border-gray-200 cursor-pointer" @click="$emit('click')">
    <div :class="iconClasses" class="w-16 h-16 rounded-full flex items-center justify-center mb-4">
      <img v-if="icon && icon.startsWith('/')" :src="icon" :alt="title" class="w-8 h-8" />
      <i v-else :data-lucide="defaultIcon" class="w-8 h-8 text-white"></i>
    </div>
    <h3 class="text-xl font-semibold mb-2">{{ title }}</h3>
    <p class="text-gray-600 mb-6">{{ description }}</p>
    <span :class="buttonClasses" class="mt-6 font-semibold px-6 py-2 rounded-full transition-colors">
      进入展馆
    </span>
  </div>
</template>

<script>
export default {
  name: 'HallCard',
  props: {
    title: {
      type: String,
      required: true
    },
    description: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      default: null
    },
    color: {
      type: String,
      default: 'blue',
      validator: (value) => ['blue', 'green', 'yellow', 'purple', 'indigo'].includes(value)
    }
  },
  emits: ['click'],
  computed: {
    iconClasses() {
      const colorMap = {
        blue: 'bg-blue-500',
        green: 'bg-green-500',
        yellow: 'bg-yellow-500',
        purple: 'bg-purple-500',
        indigo: 'bg-indigo-500'
      }
      return colorMap[this.color] || 'bg-blue-500'
    },
    buttonClasses() {
      const colorMap = {
        blue: 'bg-blue-500 text-white hover:bg-blue-600',
        green: 'bg-green-500 text-white hover:bg-green-600',
        yellow: 'bg-yellow-500 text-white hover:bg-yellow-600',
        purple: 'bg-purple-500 text-white hover:bg-purple-600',
        indigo: 'bg-indigo-500 text-white hover:bg-indigo-600'
      }
      return colorMap[this.color] || 'bg-blue-500 text-white hover:bg-blue-600'
    },
    defaultIcon() {
      const iconMap = {
        blue: 'clipboard-check',
        green: 'book-open',
        yellow: 'gamepad-2',
        purple: 'headphones',
        indigo: 'user'
      }
      return iconMap[this.color] || 'clipboard-check'
    }
  }
}
</script>
