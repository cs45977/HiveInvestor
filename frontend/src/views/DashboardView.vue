<script setup>
import { ref, onMounted } from 'vue'
import PortfolioSummary from '../components/portfolio/PortfolioSummary.vue'
import HoldingsTable from '../components/portfolio/HoldingsTable.vue'
import TradeForm from '../components/trade/TradeForm.vue'
import TransactionHistory from '../components/portfolio/TransactionHistory.vue'
import StockWatchlist from '../components/market/StockWatchlist.vue'
import { getPortfolio, getTransactions, getQuote } from '../services/portfolio'

const portfolio = ref(null)
const transactions = ref([])
const loading = ref(true)
const error = ref(null)

const fetchData = async () => {
  try {
    const [p, t] = await Promise.all([getPortfolio(), getTransactions()])
    
    // Enrich holdings with current price
    if (p && p.holdings) {
        const enrichedHoldings = await Promise.all(p.holdings.map(async (h) => {
            try {
                const quote = await getQuote(h.symbol);
                return { ...h, current_price: quote.price };
            } catch (e) {
                console.error(`Failed to fetch quote for ${h.symbol}`, e);
                return { ...h, current_price: h.average_price }; // Fallback
            }
        }));
        p.holdings = enrichedHoldings;
        
        // Recalculate total real-time value
        const holdingsValue = enrichedHoldings.reduce((sum, h) => sum + (h.quantity * h.current_price), 0);
        p.total_value = p.cash_balance + holdingsValue;
    }
    
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
    <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold">My Portfolio</h1>
    </div>
    
    <StockWatchlist class="mb-6" />
    
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
