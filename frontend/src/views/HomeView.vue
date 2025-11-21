<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isDev = import.meta.env.DEV
const backendStatus = ref('Checking connection...')
const isConnected = ref(false)

onMounted(async () => {
  if (isDev) {
    try {
      const response = await axios.get('/api/status')
      if (response.data.status) {
        backendStatus.value = response.data.status
        isConnected.value = true
      }
    } catch (error) {
      backendStatus.value = 'Connection Failed'
      isConnected.value = false
      console.error('Backend status check failed:', error)
    }
  }
})
</script>

<template>
  <main>
    <h1>Welcome to HiveInvestor</h1>
    <div v-if="isDev" class="text-center mt-4">
      <p class="text-sm font-bold text-gray-500">Development Mode</p>
      <p :class="{'text-success': isConnected, 'text-red-500': !isConnected}">
        Backend: {{ backendStatus }}
      </p>
    </div>
  </main>
</template>
