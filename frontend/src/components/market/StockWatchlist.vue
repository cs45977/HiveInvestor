<template>
  <div class="bg-white p-4 rounded-lg shadow">
    <h3 class="text-lg font-bold mb-4">Market Overview</h3>
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4">
      <div v-for="stock in quotes" :key="stock.symbol" class="text-center p-2 border rounded hover:bg-gray-50">
        <div class="font-bold">{{ stock.symbol }}</div>
        <div :class="getColor(stock.change)">${{ stock.price.toFixed(2) }}</div>
        <div :class="getColor(stock.change)" class="text-xs">
          {{ stock.change > 0 ? '+' : '' }}{{ stock.change.toFixed(2) }} ({{ stock.percent_change.toFixed(2) }}%)
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getQuote } from '../../services/portfolio';

const symbols = (import.meta.env.VITE_WATCHLIST_SYMBOLS || 'AAPL,MSFT,GOOG,AMZN,NVDA,TSLA,META').split(',');
const quotes = ref([]);
const loading = ref(true);

const fetchQuotes = async () => {
  try {
    const promises = symbols.map(sym => getQuote(sym.trim()));
    const results = await Promise.all(promises);
    quotes.value = results;
  } catch (error) {
    console.error('Failed to fetch watchlist:', error);
  } finally {
    loading.value = false;
  }
};

const getColor = (change) => {
  if (change > 0) return 'text-green-600';
  if (change < 0) return 'text-red-600';
  return 'text-gray-600';
};

onMounted(fetchQuotes);
</script>
