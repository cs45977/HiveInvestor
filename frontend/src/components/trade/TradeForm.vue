<script setup>
import { ref } from 'vue'
import { executeTrade, getQuote } from '../../services/portfolio'

const emit = defineEmits(['trade-executed'])
const symbol = ref('')
const quantity = ref(1)
const type = ref('BUY')
const message = ref('')
const error = ref('')
const loading = ref(false)
const quotePrice = ref(null)

const fetchQuote = async () => {
    if(!symbol.value) return
    try {
        const q = await getQuote(symbol.value)
        quotePrice.value = q.price
        error.value = ''
    } catch (e) {
        quotePrice.value = null
        // Don't show error immediately on typing, maybe just clear price
        console.error(e)
    }
}

const handleSubmit = async () => {
    loading.value = true
    message.value = ''
    error.value = ''
    try {
        await executeTrade({
            symbol: symbol.value,
            quantity: quantity.value,
            type: type.value
        })
        message.value = 'Trade executed successfully!'
        emit('trade-executed')
        // Reset form?
        quantity.value = 1
    } catch (e) {
        error.value = e.response?.data?.detail || 'Trade failed'
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <div class="bg-white p-4 rounded shadow mt-4">
    <h3 class="font-bold mb-2">Execute Trade</h3>
    <div v-if="message" class="text-green-500 mb-2 trade-success-message">{{ message }}</div>
    <div v-if="error" class="text-red-500 mb-2 trade-error-message">{{ error }}</div>
    
    <div class="flex gap-2 mb-2 flex-wrap">
        <input v-model="symbol" @blur="fetchQuote" placeholder="Symbol (e.g. AAPL)" class="border p-2 rounded uppercase" />
        <input v-model.number="quantity" type="number" min="1" placeholder="Qty" class="border p-2 rounded w-20" />
        <select v-model="type" class="border p-2 rounded">
            <option value="BUY">Buy</option>
            <option value="SELL">Sell</option>
        </select>
    </div>
    <div v-if="quotePrice" class="text-sm text-gray-600 mb-2">
        Current Price: ${{ quotePrice }}
    </div>
    <button @click="handleSubmit" :disabled="loading" class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50">
        {{ loading ? 'Processing...' : 'Submit Trade' }}
    </button>
  </div>
</template>
