import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'

// Mock fetch globally
global.fetch = vi.fn()

// Mock router for testing
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: { template: '<div>Home</div>' } },
    { path: '/test', component: { template: '<div>Test</div>' } }
  ]
})

describe('App.vue', () => {
  let wrapper

  beforeEach(async () => {
    // Reset fetch mock
    vi.clearAllMocks()
    
    // Mock successful API response
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ status: 'healthy' })
    })
    
    router.push('/')
    await router.isReady()
    
    wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    })
  })

  it('renders without crashing', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('shows loading state initially', async () => {
    // Create a fresh wrapper to test initial loading state
    const freshWrapper = mount(App, {
      global: {
        plugins: [router]
      }
    })
    
    // Check for loading state before initialization completes
    expect(freshWrapper.find('[data-testid="global-loading"]').exists()).toBe(true)
    
    // Wait for initialization to complete
    await freshWrapper.vm.$nextTick()
    await new Promise(resolve => setTimeout(resolve, 100))
  })

  it('has correct app structure', () => {
    expect(wrapper.find('#app').exists()).toBe(true)
  })

  it('calls API health check on initialization', () => {
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/api/health'))
  })
})