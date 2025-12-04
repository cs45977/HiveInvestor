<template>
  <div class="bg-gray-800 text-white p-4 rounded-lg shadow mb-4 quote-header">
    <div class="flex justify-between items-center">
      <div>
        <div class="flex items-baseline gap-2">
           <h2 class="text-3xl font-bold !text-white text-left mb-0">{{ symbol }}</h2>
           <span class="text-gray-200 text-lg font-medium">{{ companyName }}</span>
        </div>
        <div class="text-4xl font-bold" :class="changeClass">
          ${{ price.toFixed(2) }}
        </div>
        <div :class="changeClass">
          {{ change > 0 ? '+' : '' }}{{ change.toFixed(2) }} ({{ percentChange.toFixed(2) }}%)
        </div>
      </div>
      <div class="grid grid-cols-2 gap-4 text-sm text-gray-300">
        <div>Open: <span class="text-white">{{ open.toFixed(2) }}</span></div>
        <div>High: <span class="text-white">{{ high.toFixed(2) }}</span></div>
        <div>Low: <span class="text-white">{{ low.toFixed(2) }}</span></div>
        <div>Vol: <span class="text-white">{{ volume.toLocaleString() }}</span></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  symbol: { type: String, required: true },
  companyName: { type: String, default: '' },
  price: { type: Number, required: true },
  change: { type: Number, default: 0 },
  percentChange: { type: Number, default: 0 },
  open: { type: Number, default: 0 },
  high: { type: Number, default: 0 },
  low: { type: Number, default: 0 },
  volume: { type: Number, default: 0 }
});

const changeClass = computed(() => {
  if (props.change > 0) return 'text-green-500';
  if (props.change < 0) return 'text-red-500';
  return 'text-gray-400';
});
</script>
