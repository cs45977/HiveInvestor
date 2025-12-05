<template>
  <div class="bg-white p-6 rounded-lg shadow enhanced-trade-form">
    <h3 class="text-xl font-bold mb-4">Order Entry: {{ symbol }}</h3>
    
    <div v-if="currentHolding && currentHolding.quantity > 0" class="mb-4 p-3 bg-blue-100 text-blue-800 rounded">
      You own: 
      <span class="font-bold">{{ currentHolding.quantity }} shares</span> 
      @ Avg. <span class="font-bold">${{ currentHolding.average_price.toFixed(2) }}</span>
    </div>

    <!-- Action Toggle -->
    <div class="flex mb-4">
      <button 
        @click="form.type = 'BUY'" 
        :class="['flex-1 py-2 font-bold rounded-l', form.type === 'BUY' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700']"
      >BUY</button>
      <button 
        @click="form.type = 'SELL'" 
        :class="['flex-1 py-2 font-bold rounded-r', form.type === 'SELL' ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-700']"
      >SELL</button>
    </div>

    <form @submit.prevent="handleSubmit">
      <!-- Order Type -->
      <div class="mb-4">
        <label class="block text-sm font-bold mb-1">Order Type</label>
        <select v-model="form.order_type" class="w-full p-2 border rounded">
          <option value="MARKET">Market</option>
          <option value="LIMIT">Limit</option>
        </select>
      </div>

      <!-- Quantity -->
      <div class="mb-4">
        <label class="block text-sm font-bold mb-1">Quantity</label>
        <input type="number" v-model.number="form.quantity" class="w-full p-2 border rounded" min="1" required />
      </div>

      <!-- Limit Price (Conditional) -->
      <div v-if="form.order_type === 'LIMIT'" class="mb-4">
        <label class="block text-sm font-bold mb-1">Limit Price</label>
        <input type="number" v-model.number="form.limit_price" class="w-full p-2 border rounded" step="0.01" required />
      </div>

      <!-- Time in Force -->
      <div class="mb-4">
        <label class="block text-sm font-bold mb-1">Time in Force</label>
        <select v-model="form.time_in_force" class="w-full p-2 border rounded">
          <option value="DAY">Day</option>
          <option value="GTC">Good-Til-Cancelled</option>
        </select>
      </div>

      <!-- Submit Button -->
      <button 
        type="submit" 
        class="w-full py-3 font-bold text-white rounded hover:opacity-90"
        :class="form.type === 'BUY' ? 'bg-green-600' : 'bg-red-600'"
      >
        Place {{ form.order_type }} {{ form.type }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';

const props = defineProps({
  symbol: { type: String, default: '' },
  currentHolding: { type: Object, default: null } // { quantity, average_price }
});

const emit = defineEmits(['submit-order']);

const form = reactive({
  type: 'BUY',
  order_type: 'MARKET',
  quantity: 1,
  limit_price: null,
  time_in_force: 'DAY'
});

const handleSubmit = () => {
  if (form.order_type === 'LIMIT' && (!form.limit_price || form.limit_price <= 0)) {
    alert('Limit Price is required for Limit Orders');
    return;
  }
  emit('submit-order', { ...form });
};
</script>
