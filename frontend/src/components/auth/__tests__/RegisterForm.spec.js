import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import RegisterForm from '../RegisterForm.vue'
import { useAuthStore } from '../../../stores/auth'

// Mock the auth store composable
vi.mock('../../../stores/auth', () => ({
  useAuthStore: vi.fn()
}))

describe('RegisterForm', () => {
  let registerAndLoginMock

  beforeEach(() => {
    vi.clearAllMocks()
    registerAndLoginMock = vi.fn()
    useAuthStore.mockReturnValue({
      registerAndLogin: registerAndLoginMock
    })
  })

  it('renders registration form correctly', () => {
    const wrapper = mount(RegisterForm)
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="text"]').exists()).toBe(true) // Username
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true)
  })

  it('displays error for invalid email format', async () => {
    const wrapper = mount(RegisterForm)
    await wrapper.find('input[type="email"]').setValue('invalid-email')
    await wrapper.find('input[type="email"]').trigger('blur') // Trigger blur to show error
    expect(wrapper.find('.email-error').exists()).toBe(true)
  })

  it('displays error if passwords do not match', async () => {
    const wrapper = mount(RegisterForm)
    await wrapper.find('#password').setValue('password123')
    await wrapper.find('#confirmPassword').setValue('password1234')
    await wrapper.find('#confirmPassword').trigger('blur')
    expect(wrapper.find('.password-match-error').exists()).toBe(true)
  })

  it('displays error for weak password (less than 8 chars)', async () => {
    const wrapper = mount(RegisterForm)
    await wrapper.find('#password').setValue('short')
    await wrapper.find('#password').trigger('blur')
    expect(wrapper.find('.password-strength-error').exists()).toBe(true)
  })

  it('displays error for weak password (no uppercase)', async () => {
    const wrapper = mount(RegisterForm)
    await wrapper.find('#password').setValue('password123!')
    await wrapper.find('#password').trigger('blur')
    expect(wrapper.find('.password-strength-error').exists()).toBe(true)
  })

  it('displays error for weak password (no number)', async () => {
    const wrapper = mount(RegisterForm)
    await wrapper.find('#password').setValue('Password!!!')
    await wrapper.find('#password').trigger('blur')
    expect(wrapper.find('.password-strength-error').exists()).toBe(true)
  })

  it('displays error for weak password (no special char)', async () => {
    const wrapper = mount(RegisterForm)
    await wrapper.find('#password').setValue('Password123')
    await wrapper.find('#password').trigger('blur')
    expect(wrapper.find('.password-strength-error').exists()).toBe(true)
  })

  it('does NOT display error for strong password', async () => {
    const wrapper = mount(RegisterForm)
    await wrapper.find('#password').setValue('StrongP@ss1')
    await wrapper.find('#password').trigger('blur')
    expect(wrapper.find('.password-strength-error').exists()).toBe(false)
  })

  it('handles successful registration submission', async () => {
    registerAndLoginMock.mockResolvedValue(true)
    const wrapper = mount(RegisterForm)

    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="text"]').setValue('testuser')
    await wrapper.find('#password').setValue('StrongP@ss1!')
    await wrapper.find('#confirmPassword').setValue('StrongP@ss1!')

    await wrapper.find('form').trigger('submit')

    expect(registerAndLoginMock).toHaveBeenCalledWith('test@example.com', 'testuser', 'StrongP@ss1!')
    // Success message is shown upon promise resolution
    await new Promise(resolve => setTimeout(resolve, 0))
    expect(wrapper.find('.success-message').text()).toBe('Registration successful!')
  })

  it('handles duplicate email error from API', async () => {
    registerAndLoginMock.mockRejectedValue({ response: { data: { detail: 'Email already registered' } } })
    const wrapper = mount(RegisterForm)

    await wrapper.find('input[type="email"]').setValue('duplicate@example.com')
    await wrapper.find('input[type="text"]').setValue('duplicateuser')
    await wrapper.find('#password').setValue('StrongP@ss1!')
    await wrapper.find('#confirmPassword').setValue('StrongP@ss1!')

    await wrapper.find('form').trigger('submit')
    
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(registerAndLoginMock).toHaveBeenCalled()
    expect(wrapper.find('.error-message').text()).toBe('Email already registered')
  })

  it('handles generic API error', async () => {
    registerAndLoginMock.mockRejectedValue(new Error('Network error'))
    const wrapper = mount(RegisterForm)

    await wrapper.find('input[type="email"]').setValue('generic@example.com')
    await wrapper.find('input[type="text"]').setValue('genericuser')
    await wrapper.find('#password').setValue('StrongP@ss1!')
    await wrapper.find('#confirmPassword').setValue('StrongP@ss1!')

    await wrapper.find('form').trigger('submit')
    
    await new Promise(resolve => setTimeout(resolve, 0))

    expect(registerAndLoginMock).toHaveBeenCalled()
    expect(wrapper.find('.error-message').text()).toBe('An unexpected error occurred.')
  })
})

