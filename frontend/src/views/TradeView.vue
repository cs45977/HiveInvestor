<script setup>
import TradeForm from '../components/trade/TradeForm.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const onTradeExecuted = () => {
    // Optionally redirect to dashboard or just show success
    // router.push('/dashboard')
}
</script>

<template>
  <main class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Trade</h1>
    <TradeForm @trade-executed="onTradeExecuted" />
  </main>
</template>
