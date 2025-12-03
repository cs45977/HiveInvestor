import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import LoginForm from '../LoginForm.vue'
import { useAuthStore } from '../../../stores/auth'

// Mock the auth store composable
vi.mock('../../../stores/auth', () => ({
  useAuthStore: vi.fn()
}))

describe('LoginForm', () => {
  let loginMock

  beforeEach(() => {
    vi.clearAllMocks()
    loginMock = vi.fn()
    useAuthStore.mockReturnValue({
      login: loginMock
    })
  })

  it('renders login form correctly', () => {
    const wrapper = mount(LoginForm)
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('handles successful login', async () => {
    loginMock.mockResolvedValue(true)
    const wrapper = mount(LoginForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('input[type="password"]').setValue('password')
    await wrapper.find('form').trigger('submit')

    expect(loginMock).toHaveBeenCalledWith('user@example.com', 'password')
  })

  it('handles login failure', async () => {
    loginMock.mockRejectedValue(new Error('Invalid credentials'))
    const wrapper = mount(LoginForm)

    await wrapper.find('input[type="email"]').setValue('user@example.com')
    await wrapper.find('input[type="password"]').setValue('wrongpassword')
    await wrapper.find('form').trigger('submit')
    
    // Wait for promise rejection handling
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(loginMock).toHaveBeenCalled()
    expect(wrapper.find('.error-message').text()).toBe('Invalid credentials')
  })
})
