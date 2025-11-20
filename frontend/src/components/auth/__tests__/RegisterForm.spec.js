import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import RegisterForm from '../RegisterForm.vue'
import { register } from '../../../services/auth'
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
  register: vi.fn()
}))

describe('RegisterForm', () => {
  beforeEach(() => {
    vi.clearAllMocks()
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
    const mockPush = vi.fn()
    useRouter.mockReturnValue({ push: mockPush })

    register.mockResolvedValue({ id: 'user-id', email: 'test@example.com', username: 'testuser' })

    const wrapper = mount(RegisterForm)

    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="text"]').setValue('testuser')
    await wrapper.find('#password').setValue('StrongP@ss1!')
    await wrapper.find('#confirmPassword').setValue('StrongP@ss1!')

    await wrapper.find('form').trigger('submit')

    // Wait for promises to resolve
    await new Promise(resolve => setImmediate(resolve))
    
    expect(register).toHaveBeenCalledWith('test@example.com', 'testuser', 'StrongP@ss1!')
    expect(mockPush).toHaveBeenCalledWith('/') 
    expect(wrapper.find('.success-message').text()).toBe('Registration successful!')
  })

  it('handles duplicate email error from API', async () => {
     register.mockRejectedValue({ response: { data: { detail: 'Email already registered' } } })

    const wrapper = mount(RegisterForm)

    await wrapper.find('input[type="email"]').setValue('duplicate@example.com')
    await wrapper.find('input[type="text"]').setValue('duplicateuser')
    await wrapper.find('#password').setValue('StrongP@ss1!')
    await wrapper.find('#confirmPassword').setValue('StrongP@ss1!')

    await wrapper.find('form').trigger('submit')
    
    // Wait for promises to resolve
    await new Promise(resolve => setImmediate(resolve))

    expect(register).toHaveBeenCalled()
    expect(wrapper.find('.error-message').text()).toBe('Email already registered')
  })

  it('handles generic API error', async () => {
    register.mockRejectedValue(new Error('Network error'))

    const wrapper = mount(RegisterForm)

    await wrapper.find('input[type="email"]').setValue('generic@example.com')
    await wrapper.find('input[type="text"]').setValue('genericuser')
    await wrapper.find('#password').setValue('StrongP@ss1!')
    await wrapper.find('#confirmPassword').setValue('StrongP@ss1!')

    await wrapper.find('form').trigger('submit')
    
    // Wait for promises to resolve
    await new Promise(resolve => setImmediate(resolve))

    expect(register).toHaveBeenCalled()
    expect(wrapper.find('.error-message').text()).toBe('An unexpected error occurred.')
  })
})

