import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import LoginForm from '../LoginForm.vue'
import { login } from '../../../services/auth'
import { useRouter } from 'vue-router'

// Mock the router
vi.mock('vue-router', () => ({
  useRouter: vi.fn(() => ({
    push: vi.fn()
  })),
  RouterLink: { template: '<a><slot /></a>' },
  RouterView: { template: '<div><slot /></div>' }
}))

// Mock the auth service
vi.mock('../../../services/auth', () => ({
  login: vi.fn()
}))

describe('LoginForm', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders login form correctly', () => {
    const wrapper = mount(LoginForm)
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('handles successful login', async () => {
    const mockPush = vi.fn()
    useRouter.mockReturnValue({ push: mockPush })
    login.mockResolvedValue({ access_token: 'fake-jwt-token', token_type: 'bearer' })

    const wrapper = mount(LoginForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('input[type="password"]').setValue('password')
    await wrapper.find('form').trigger('submit')

    await new Promise(resolve => setImmediate(resolve))

    expect(login).toHaveBeenCalledWith('user@example.com', 'password')
    expect(mockPush).toHaveBeenCalledWith('/')
    // We might also check if token was stored in localStorage, but that logic might be inside the service or component.
    // For now, we assume component handles it or service does. Ideally service does it.
  })

  it('handles login failure', async () => {
    login.mockRejectedValue(new Error('Invalid credentials'))

    const wrapper = mount(LoginForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('input[type="password"]').setValue('wrongpassword')
    await wrapper.find('form').trigger('submit')

    await new Promise(resolve => setImmediate(resolve))

    expect(login).toHaveBeenCalled()
    expect(wrapper.find('.error-message').text()).toBe('Invalid credentials')
  })
})
