import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TransactionHistory from '../TransactionHistory.vue'

describe('TransactionHistory', () => {
  it('displays transactions', () => {
    const transactions = [
        { id: '1', timestamp: '2023-01-01T00:00:00Z', type: 'BUY', symbol: 'AAPL', quantity: 10, price_per_share: 150, total_amount: 1510 }
    ]
    const wrapper = mount(TransactionHistory, {
      props: { transactions }
    })
    expect(wrapper.text()).toContain('BUY')
    expect(wrapper.text()).toContain('AAPL')
    expect(wrapper.text()).toContain('10')
  })

  it('displays empty message', () => {
    const wrapper = mount(TransactionHistory, {
      props: { transactions: [] }
    })
    expect(wrapper.text()).toContain('No transactions')
  })

  it('emits cancel-transaction event when cancel button clicked', async () => {
    const transactions = [
        { id: 'tx1', type: 'BUY', symbol: 'AAPL', quantity: 10, price_per_share: 150.00, total_amount: 1500.00, timestamp: '2023-01-01', status: 'PENDING' }
    ]
    const wrapper = mount(TransactionHistory, {
      props: { transactions }
    })
    
    const cancelButton = wrapper.find('button')
    expect(cancelButton.exists()).toBe(true)
    expect(cancelButton.text()).toBe('Cancel')
    
    await cancelButton.trigger('click')
    expect(wrapper.emitted('cancel-transaction')).toBeTruthy()
    expect(wrapper.emitted('cancel-transaction')[0]).toEqual(['tx1'])
  })
})
