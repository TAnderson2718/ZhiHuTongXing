import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createMemoryHistory, createRouter } from 'vue-router'
import router from '../router/index.js'

describe('Router Configuration', () => {
  it('should have correct route definitions', () => {
    const routes = router.getRoutes()
    
    expect(routes.find(route => route.path === '/')).toBeDefined()
    expect(routes.find(route => route.path === '/assessment')).toBeDefined()
    expect(routes.find(route => route.path === '/knowledge')).toBeDefined()
    expect(routes.find(route => route.path === '/experience')).toBeDefined()
    expect(routes.find(route => route.path === '/support')).toBeDefined()
    expect(routes.find(route => route.path === '/account')).toBeDefined()
  })

  it('should redirect /growth-strategy to /support', async () => {
    const testRouter = createRouter({
      history: createMemoryHistory(),
      routes: router.getRoutes()
    })

    await testRouter.push('/growth-strategy')
    expect(testRouter.currentRoute.value.path).toBe('/support')
  })

  it('should handle 404 routes', async () => {
    const testRouter = createRouter({
      history: createMemoryHistory(),
      routes: router.getRoutes()
    })

    await testRouter.push('/non-existent-route')
    expect(testRouter.currentRoute.value.name).toBe('NotFound')
  })
})