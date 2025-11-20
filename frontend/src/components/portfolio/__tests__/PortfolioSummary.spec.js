import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import PortfolioSummary from '../PortfolioSummary.vue'

describe('PortfolioSummary', () => {
  it('displays formatted currency', () => {
    const wrapper = mount(PortfolioSummary, {
      props: {
        cash: 100000.00,
        totalValue: 105000.00
      }
    })
    // Check for text presence. Formatting might vary slightly (e.g. space), so we check generally.
    expect(wrapper.text()).toContain('$100,000.00')
    expect(wrapper.text()).toContain('$105,000.00')
  })
})
