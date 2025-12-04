<template>
  <div ref="chartContainer" class="w-full h-96 bg-gray-900 rounded-lg shadow relative trading-chart"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { createChart } from 'lightweight-charts';

const props = defineProps({
  data: { type: Array, required: true } // Array of { time, open, high, low, close }
});

const chartContainer = ref(null);
let chart = null;
let candlestickSeries = null;

onMounted(() => {
  if (chartContainer.value) {
    chart = createChart(chartContainer.value, {
      width: chartContainer.value.clientWidth,
      height: chartContainer.value.clientHeight,
      layout: { backgroundColor: '#111827', textColor: '#D1D5DB' },
      grid: { vertLines: { color: '#374151' }, horzLines: { color: '#374151' } },
    });
    candlestickSeries = chart.addCandlestickSeries();
    candlestickSeries.setData(props.data);
  }
  
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  if (chart) {
    chart.remove();
  }
  window.removeEventListener('resize', handleResize);
});

const handleResize = () => {
  if (chart && chartContainer.value) {
    chart.applyOptions({ width: chartContainer.value.clientWidth });
  }
};

watch(() => props.data, (newData) => {
  if (candlestickSeries) {
    candlestickSeries.setData(newData);
  }
});
</script>
