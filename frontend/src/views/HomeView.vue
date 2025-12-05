<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isDev = import.meta.env.DEV
const backendStatus = ref('Checking connection...')
const databaseStatus = ref('Checking...')
const databaseName = ref('')
const isConnected = ref(false)

const API_URL = import.meta.env.VITE_API_URL || '/api/v1'
// The status endpoint is at /api/status, not /api/v1/status in the current main.py
// Wait, looking at main.py: @app.get("/api/status")
// So if VITE_API_URL is https://.../api/v1, we need to strip /v1 or just use the base.
// Actually, VITE_API_URL in .env.production is https://...run.app
// So we should probably just use that base.
// Let's assume VITE_API_URL points to the root of the backend service for simplicity in this context,
// OR construct it carefully.
// If VITE_API_URL is https://host, then /api/status is correct.
// If VITE_API_URL is https://host/api/v1 (common convention), then we need to go up.
// Let's check .env.production content again? I wrote it as https://...run.app
// So it is the root.

onMounted(async () => {
  try {
    // If VITE_API_URL is defined (prod), use it. Otherwise relative (dev).
    const baseUrl = import.meta.env.VITE_API_URL || ''
    const response = await axios.get(`${baseUrl}/api/status`)
    
    if (response.data.status) {
      backendStatus.value = response.data.status
      databaseStatus.value = response.data.database_status
      databaseName.value = response.data.database_name
      isConnected.value = true
    }
  } catch (error) {
    backendStatus.value = 'Connection Failed'
    databaseStatus.value = 'Unknown'
    isConnected.value = false
    console.error('Backend status check failed:', error)
  }
})
</script>

<template>
  <main>
    <h1>Welcome to HiveInvestor</h1>
    <div class="text-center mt-4">
      <p class="text-sm font-bold text-gray-500">System Status</p>
      <div class="mt-2 p-4 bg-gray-100 rounded-lg inline-block">
        <p :class="{'text-green-600': isConnected, 'text-red-500': !isConnected}">
          <span class="font-semibold">Backend:</span> {{ backendStatus }}
        </p>
        <p v-if="isConnected" :class="{'text-green-600': databaseStatus === 'Connected', 'text-red-500': databaseStatus !== 'Connected'}">
          <span class="font-semibold">Database ({{ databaseName }}):</span> {{ databaseStatus }}
        </p>
      </div>
    </div>
  </main>
</template>
