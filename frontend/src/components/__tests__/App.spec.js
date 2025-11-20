import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../../App.vue'
import { createRouter, createWebHistory, RouterLink, RouterView } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: { template: '<div>Home</div>' }
    },
    {
      path: '/register',
      component: { template: '<div>Register</div>' }
    },
    {
      path: '/login',
      component: { template: '<div>Login</div>' }
    }
  ]
})

describe('App', () => {
  it('renders the navigation links', async () => {
    router.push('/')
    await router.isReady()
    const wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    })
    expect(wrapper.find('header').exists()).toBe(true)
    expect(wrapper.find('nav').exists()).toBe(true)
    expect(wrapper.findAllComponents(RouterLink).length).toBe(3) // Home, Register, Login
  })

  // This test was originally for backend API call, which is not in App.vue anymore.
  // We'll update it to check for the presence of RouterView in the App.vue template
  // after the routing is set up.
  it('renders RouterView', async () => {
    router.push('/')
    await router.isReady()
    const wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    })
    expect(wrapper.findComponent(RouterView).exists()).toBe(true)
  })
})
