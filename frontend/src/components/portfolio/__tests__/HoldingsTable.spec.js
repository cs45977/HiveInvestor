import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HoldingsTable from '../HoldingsTable.vue'

describe('HoldingsTable', () => {
  it('displays holdings rows', () => {
    const holdings = [
        { symbol: 'AAPL', quantity: 10, average_price: 150.00 }
    ]
    const wrapper = mount(HoldingsTable, {
      props: { holdings }
    })
    expect(wrapper.text()).toContain('AAPL')
    expect(wrapper.text()).toContain('10')
    // formatted price
    expect(wrapper.text()).toContain('$150.00')
  })

  it('displays message when empty', () => {
    const wrapper = mount(HoldingsTable, {
      props: { holdings: [] }
    })
    expect(wrapper.text()).toContain('No holdings')
  })
})
