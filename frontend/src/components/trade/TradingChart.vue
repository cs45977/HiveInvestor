<template>
  <div ref="chartContainer" class="w-full h-96 bg-gray-900 rounded-lg shadow relative trading-chart"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { createChart, CandlestickSeries, LineSeries } from 'lightweight-charts';

const props = defineProps({
  seriesList: { type: Array, required: true } 
  // Array of { type: 'Candlestick'|'Line', data: [], options: {} }
});

const chartContainer = ref(null);
let chart = null;
let activeSeries = [];

onMounted(() => {
  if (chartContainer.value) {
    chart = createChart(chartContainer.value, {
      width: chartContainer.value.clientWidth,
      height: chartContainer.value.clientHeight,
      layout: { backgroundColor: '#111827', textColor: '#D1D5DB' },
      grid: { vertLines: { color: '#374151' }, horzLines: { color: '#374151' } },
      timeScale: { timeVisible: true, secondsVisible: false }
    });
    
    updateSeries();
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

const updateSeries = () => {
  if (!chart) return;
  
  // Remove old series
  activeSeries.forEach(s => chart.removeSeries(s));
  activeSeries = [];
  
  // Add new series
  props.seriesList.forEach(config => {
    let series;
    if (config.type === 'Candlestick') {
      series = chart.addSeries(CandlestickSeries, config.options || {});
    } else if (config.type === 'Line') {
      series = chart.addSeries(LineSeries, config.options || {});
    }
    
    if (series) {
      series.setData(config.data);
      activeSeries.push(series);
    }
  });
};

watch(() => props.seriesList, updateSeries, { deep: true });
</script>
