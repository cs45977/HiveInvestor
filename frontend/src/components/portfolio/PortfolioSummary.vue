<script setup>
import { computed } from 'vue'

const props = defineProps({
  cash: {
    type: Number,
    required: true
  },
  totalValue: {
    type: Number,
    required: true
  }
})

const formattedCash = computed(() => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(props.cash)
})

const formattedTotal = computed(() => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(props.totalValue)
})
</script>

<template>
  <div class="grid grid-cols-2 gap-4 p-4 bg-white shadow rounded-lg">
    <div class="text-center">
        <h3 class="text-gray-500 text-sm uppercase">Cash Balance</h3>
        <p class="text-2xl font-bold text-green-600">{{ formattedCash }}</p>
    </div>
    <div class="text-center">
        <h3 class="text-gray-500 text-sm uppercase">Total Portfolio Value</h3>
        <p class="text-2xl font-bold text-blue-600">{{ formattedTotal }}</p>
    </div>
  </div>
</template>
