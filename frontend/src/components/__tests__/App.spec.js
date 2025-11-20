import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import flushPromises from 'flush-promises'
import App from '../../App.vue'

// Mock the global fetch
global.fetch = vi.fn(() =>
  Promise.resolve({
    ok: true,
    json: () => Promise.resolve({ Hello: 'Test World' }),
  })
)

describe('App', () => {
  it('renders the welcome message', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('Welcome to HiveInvestor!')
  })

  it('displays success message and data after API call', async () => {
    const wrapper = mount(App)
    await flushPromises()
    expect(wrapper.text()).toContain('Backend connection successful!')
    expect(wrapper.text()).toContain('Backend says: "Test World"')
  })
})
