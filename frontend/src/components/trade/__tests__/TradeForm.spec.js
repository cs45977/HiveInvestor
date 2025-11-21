import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import TradeForm from '../TradeForm.vue'
import { executeTrade, getQuote } from '../../../services/portfolio'

vi.mock('../../../services/portfolio', () => ({
    executeTrade: vi.fn(),
    getQuote: vi.fn()
}))

describe('TradeForm', () => {
  beforeEach(() => {
      vi.clearAllMocks()
  })

  it('submits trade successfully', async () => {
    executeTrade.mockResolvedValue({})
    const wrapper = mount(TradeForm)
    
    await wrapper.find('input[placeholder*="Symbol"]').setValue('AAPL')
    await wrapper.find('input[type="number"]').setValue(10)
    await wrapper.find('button').trigger('click')
    
    // Wait for promise
    await new Promise(resolve => setTimeout(resolve, 10))
    
    expect(executeTrade).toHaveBeenCalledWith({
        symbol: 'AAPL',
        quantity: 10,
        type: 'BUY'
    })
    
    expect(wrapper.find('.trade-success-message').exists()).toBe(true)
    expect(wrapper.emitted()['trade-executed']).toBeTruthy()
  })

  it('displays error on failure', async () => {
    executeTrade.mockRejectedValue({ response: { data: { detail: 'Insufficient funds' } } })
    const wrapper = mount(TradeForm)
    
    await wrapper.find('input[placeholder*="Symbol"]').setValue('AAPL')
    await wrapper.find('button').trigger('click')
    
    await new Promise(resolve => setTimeout(resolve, 10))
    
    expect(wrapper.find('.trade-error-message').text()).toBe('Insufficient funds')
  })
})
