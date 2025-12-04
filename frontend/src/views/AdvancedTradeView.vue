<template>
  <div class="container mx-auto p-4 h-screen flex flex-col md:flex-row gap-4">
    <!-- Left Panel: Research -->
    <div class="w-full md:w-2/3 flex flex-col">
      <!-- Symbol Search -->
      <div class="flex mb-4">
        <input 
          type="text" 
          v-model="searchQuery" 
          @keyup.enter="searchSymbol"
          placeholder="Enter symbol (e.g., AAPL)" 
          class="symbol-search flex-grow p-2 border rounded-l uppercase"
        />
        <button @click="searchSymbol" class="bg-blue-600 text-white px-4 py-2 rounded-r hover:bg-blue-700 font-bold">
          Search
        </button>
      </div>

      <QuoteHeader 
        :symbol="activeSymbol" 
        :price="quoteData.price" 
        :change="quoteData.change" 
        :percentChange="quoteData.percentChange"
        :open="quoteData.open"
        :high="quoteData.high"
        :low="quoteData.low"
        :volume="quoteData.volume"
      />
      <TradingChart :data="chartData" />
    </div>

    <!-- Right Panel: Order Entry -->
    <div class="w-full md:w-1/3">
      <EnhancedTradeForm :symbol="activeSymbol" @submit-order="handleOrderSubmit" />
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center confirmation-modal">
      <div class="bg-white p-6 rounded shadow-lg max-w-md w-full">
        <h3 class="text-xl font-bold mb-4">Confirm Order</h3>
        <p>Are you sure you want to place this order?</p>
        <div class="my-4 p-4 bg-gray-100 rounded">
          <p><strong>Action:</strong> {{ pendingOrder.type }}</p>
          <p><strong>Symbol:</strong> {{ activeSymbol }}</p>
          <p><strong>Quantity:</strong> {{ pendingOrder.quantity }}</p>
          <p><strong>Type:</strong> {{ pendingOrder.order_type }}</p>
          <p v-if="pendingOrder.limit_price"><strong>Limit Price:</strong> ${{ pendingOrder.limit_price }}</p>
          <p><strong>TIF:</strong> {{ pendingOrder.time_in_force }}</p>
        </div>
        <div class="flex justify-end gap-4">
          <button @click="showModal = false" class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400">Cancel</button>
          <button @click="confirmOrder" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 confirm-button">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import QuoteHeader from '../components/trade/QuoteHeader.vue';
import TradingChart from '../components/trade/TradingChart.vue';
import EnhancedTradeForm from '../components/trade/EnhancedTradeForm.vue';
import axios from 'axios';

const activeSymbol = ref('AAPL');
const searchQuery = ref('');
const quoteData = reactive({
  price: 0,
  change: 0,
  percentChange: 0,
  open: 0,
  high: 0,
  low: 0,
  volume: 0
});

// Dummy data for MVP (Chart data remains dummy as no backend endpoint for history yet)
const chartData = ref([
  { time: '2023-01-01', open: 145, high: 150, low: 144, close: 148 },
  { time: '2023-01-02', open: 148, high: 152, low: 147, close: 150 },
  { time: '2023-01-03', open: 150, high: 155, low: 149, close: 153 },
]);

const fetchQuote = async (symbol) => {
  try {
    const response = await axios.get(`/api/v1/market/quote/${symbol}`);
    const data = response.data;
    quoteData.price = data.price;
    quoteData.change = data.change;
    quoteData.percentChange = data.percent_change;
    // Mock extra fields if not in API response
    quoteData.open = data.price - data.change; 
    quoteData.high = data.price + 1.0;
    quoteData.low = data.price - 1.0;
    quoteData.volume = 1000000;
  } catch (error) {
    console.error('Failed to fetch quote:', error);
    // Reset or show error state
  }
};

const searchSymbol = () => {
  if (searchQuery.value) {
    activeSymbol.value = searchQuery.value.toUpperCase();
    fetchQuote(activeSymbol.value);
  }
};

onMounted(() => {
  fetchQuote(activeSymbol.value);
});

const showModal = ref(false);
const pendingOrder = ref({});

const handleOrderSubmit = (order) => {
  pendingOrder.value = order;
  showModal.value = true;
};

const confirmOrder = async () => {
  try {
    await axios.post('/api/v1/trade/', {
        symbol: activeSymbol.value, 
        ...pendingOrder.value
    });
    alert('Order Placed Successfully');
    showModal.value = false;
  } catch (error) {
    alert('Order Failed: ' + (error.response?.data?.detail || error.message));
    showModal.value = false;
  }
};
</script>
