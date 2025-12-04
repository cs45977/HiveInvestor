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
        :companyName="quoteData.companyName"
        :price="quoteData.price" 
        :change="quoteData.change" 
        :percentChange="quoteData.percentChange"
        :open="quoteData.open"
        :high="quoteData.high"
        :low="quoteData.low"
        :volume="quoteData.volume"
      />

      <!-- Chart Controls -->
      <div class="bg-gray-800 p-2 flex flex-wrap gap-4 items-center text-sm text-white">
        <!-- Timeframe -->
        <div class="flex gap-1">
            <button 
                v-for="tf in timeframes" 
                :key="tf.label"
                @click="timeframe = tf.label"
                :class="['px-2 py-1 rounded', timeframe === tf.label ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600']"
            >
                {{ tf.label }}
            </button>
        </div>
        
        <!-- Chart Type -->
        <div class="flex gap-1 border-l border-gray-600 pl-4">
            <button @click="chartType = 'Candlestick'" :class="['px-2 py-1 rounded', chartType === 'Candlestick' ? 'bg-blue-600' : 'bg-gray-700']">Candle</button>
            <button @click="chartType = 'Line'" :class="['px-2 py-1 rounded', chartType === 'Line' ? 'bg-blue-600' : 'bg-gray-700']">Line</button>
        </div>

        <!-- Overlays -->
        <div class="flex gap-4 border-l border-gray-600 pl-4 items-center">
            <div class="flex gap-2">
                <label v-for="idx in availableIndices" :key="idx.value" class="flex items-center gap-1 cursor-pointer">
                    <input type="checkbox" :value="idx.value" v-model="activeOverlays" />
                    {{ idx.label }}
                </label>
            </div>
            
            <div class="flex items-center gap-2 border-l border-gray-600 pl-4">
                <input 
                    v-if="!overlaySymbol"
                    type="text" 
                    v-model="overlaySymbolInput" 
                    @keyup.enter="addOverlay"
                    placeholder="Compare..." 
                    class="w-24 px-2 py-1 bg-gray-700 border border-gray-600 rounded text-white uppercase"
                />
                <div v-else class="flex items-center gap-2 bg-purple-900 px-2 py-1 rounded">
                    <span>{{ overlaySymbol }}</span>
                    <button @click="removeOverlay" class="text-xs text-red-400 hover:text-red-300">X</button>
                </div>
            </div>
        </div>
      </div>

      <TradingChart :seriesList="seriesList" />
    </div>

    <!-- Right Panel: Order Entry -->
    <div class="w-full md:w-1/3">
      <EnhancedTradeForm :symbol="activeSymbol" @submit-order="handleOrderSubmit" />
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center confirmation-modal z-50">
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
import { ref, reactive, onMounted, watch } from 'vue';
import QuoteHeader from '../components/trade/QuoteHeader.vue';
import TradingChart from '../components/trade/TradingChart.vue';
import EnhancedTradeForm from '../components/trade/EnhancedTradeForm.vue';
import { getQuote, executeTrade, getHistory } from '../services/portfolio';

const activeSymbol = ref('AAPL');
const searchQuery = ref('');
const quoteData = reactive({
  companyName: '',
  price: 0,
  change: 0,
  percentChange: 0,
  open: 0,
  high: 0,
  low: 0,
  volume: 0
});

// Charting State
const seriesList = ref([]);
const chartType = ref('Candlestick'); // 'Candlestick' or 'Line'
const timeframe = ref('1Y'); // Default
const activeOverlays = ref([]); // Array of strings: 'ES', 'NQ', 'YM'
const overlaySymbol = ref(''); 
const overlaySymbolInput = ref('');

const timeframes = [
  { label: '1D', resolution: '1', limit: 390 },
  { label: '5D', resolution: '5', limit: 390 }, // approx
  { label: '1M', resolution: '60', limit: 160 },
  { label: '3M', resolution: 'D', limit: 90 },
  { label: '1Y', resolution: 'D', limit: 252 },
  { label: '5Y', resolution: 'D', limit: 1260 },
];

const availableIndices = [
  { label: 'ES (S&P 500)', value: 'ES' },
  { label: 'NQ (Nasdaq)', value: 'NQ' },
  { label: 'YM (Dow)', value: 'YM' }
];

const fetchChartData = async () => {
  try {
    const tf = timeframes.find(t => t.label === timeframe.value) || timeframes[4];
    const mainHistory = await getHistory(activeSymbol.value, tf.resolution, tf.limit);
    
    const newSeries = [];
    
    // Main Series
    if (chartType.value === 'Candlestick') {
      newSeries.push({
        type: 'Candlestick',
        data: mainHistory.candles,
        options: { upColor: '#26a69a', downColor: '#ef5350', borderVisible: false, wickUpColor: '#26a69a', wickDownColor: '#ef5350' }
      });
    } else {
      newSeries.push({
        type: 'Line',
        data: mainHistory.candles.map(c => ({ time: c.time, value: c.close })),
        options: { color: '#2962FF', lineWidth: 3 }
      });
    }
    
    // Index Overlays
    const indexColors = { 'ES': '#FFA726', 'NQ': '#00BCD4', 'YM': '#E91E63' };
    
    for (const idx of activeOverlays.value) {
        const hist = await getHistory(idx, tf.resolution, tf.limit);
        newSeries.push({
            type: 'Line',
            data: hist.candles.map(c => ({ time: c.time, value: c.close })),
            options: { color: indexColors[idx] || '#FFF', lineWidth: 2, priceScaleId: 'left', title: idx }
        });
    }
    
    if (overlaySymbol.value) {
      const ovHistory = await getHistory(overlaySymbol.value, tf.resolution, tf.limit);
      newSeries.push({
        type: 'Line',
        data: ovHistory.candles.map(c => ({ time: c.time, value: c.close })),
        options: { color: '#AB47BC', lineWidth: 2, priceScaleId: 'left', title: overlaySymbol.value } 
      });
    }
    
    seriesList.value = newSeries;

  } catch (error) {
    console.error('Failed to fetch chart data:', error);
  }
};

const fetchQuote = async (symbol) => {
  try {
    const data = await getQuote(symbol);
    quoteData.companyName = data.company_name || '';
    quoteData.price = data.price;
    quoteData.change = data.change;
    quoteData.percentChange = data.percent_change;
    quoteData.open = data.price - data.change; 
    quoteData.high = data.price + 1.0;
    quoteData.low = data.price - 1.0;
    quoteData.volume = 1000000;
    
    await fetchChartData();

  } catch (error) {
    console.error('Failed to fetch quote:', error);
    alert(`Symbol '${symbol}' not found or service unavailable.`);
  }
};

const searchSymbol = () => {
  if (searchQuery.value) {
    activeSymbol.value = searchQuery.value.toUpperCase();
    fetchQuote(activeSymbol.value);
  }
};

const addOverlay = () => {
  if (overlaySymbolInput.value) {
    overlaySymbol.value = overlaySymbolInput.value.toUpperCase();
    fetchChartData();
    overlaySymbolInput.value = '';
  }
};

const removeOverlay = () => {
  overlaySymbol.value = '';
  fetchChartData();
};

// Watchers for controls
watch([timeframe, chartType, activeOverlays], fetchChartData, { deep: true });

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
    await executeTrade({
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
