<script setup>
import { ref, onMounted } from 'vue'
import PortfolioSummary from '../components/portfolio/PortfolioSummary.vue'
import HoldingsTable from '../components/portfolio/HoldingsTable.vue'
import TradeForm from '../components/trade/TradeForm.vue'
import TransactionHistory from '../components/portfolio/TransactionHistory.vue'
import { getPortfolio, getTransactions } from '../services/portfolio'

const portfolio = ref(null)
const transactions = ref([])
const loading = ref(true)
const error = ref(null)

const fetchData = async () => {
  try {
    const [p, t] = await Promise.all([getPortfolio(), getTransactions()])
    portfolio.value = p
    transactions.value = t
  } catch (err) {
    error.value = 'Failed to load dashboard data.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">My Portfolio</h1>
    
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    
    <div v-else-if="portfolio">
      <PortfolioSummary 
        :cash="portfolio.cash_balance" 
        :totalValue="portfolio.total_value" 
      />
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
          <div class="md:col-span-2">
             <HoldingsTable :holdings="portfolio.holdings" />
             <TransactionHistory :transactions="transactions" />
          </div>
          <div>
             <TradeForm @trade-executed="fetchData" />
          </div>
      </div>
    </div>
  </div>
</template>
