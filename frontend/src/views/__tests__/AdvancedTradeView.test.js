import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import AdvancedTradeView from '../AdvancedTradeView.vue'
import { createTestingPinia } from '@pinia/testing'
import EnhancedTradeForm from '../../components/trade/EnhancedTradeForm.vue'

// Mock lightweight-charts
vi.mock('lightweight-charts', () => ({
  createChart: vi.fn(() => ({
    addCandlestickSeries: vi.fn(() => ({
      setData: vi.fn()
    })),
    remove: vi.fn(),
    applyOptions: vi.fn()
  }))
}))

describe('AdvancedTradeView', () => {
  it('renders the layout correctly', () => {
    const wrapper = mount(AdvancedTradeView, {
      global: {
        plugins: [createTestingPinia({ createSpy: vi.fn })]
      }
    })
    
    expect(wrapper.find('.quote-header').exists()).toBe(true)
    expect(wrapper.find('.trading-chart').exists()).toBe(true)
    expect(wrapper.find('.enhanced-trade-form').exists()).toBe(true)
  })

  it('shows confirmation modal on order submission', async () => {
    const wrapper = mount(AdvancedTradeView, {
      global: {
        plugins: [createTestingPinia({ createSpy: vi.fn })],
        stubs: {
          QuoteHeader: true,
          TradingChart: true,
          EnhancedTradeForm: true // Auto-stub works well for finding and emitting
        }
      }
    })
    
    // Unmock the manual mocks so stubs work
    
    // Trigger order submission
    await wrapper.findComponent({ name: 'EnhancedTradeForm' }).vm.$emit('submit-order', {
      type: 'BUY', order_type: 'MARKET', quantity: 10, symbol: 'AAPL'
    })
    
    // Expect modal to appear (assuming we add a class .confirmation-modal)
    expect(wrapper.find('.confirmation-modal').exists()).toBe(true)
  })
})
