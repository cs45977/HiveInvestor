<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../../stores/auth'

const auth = useAuthStore()
const isConfigured = ref(true) // Default to true to avoid flash
const loading = ref(false)

const checkConfig = async () => {
  if (!auth.isAdmin.value) return

  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('/api/v1/admin/config-status', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    isConfigured.value = response.data.finnhub_configured
  } catch (error) {
    console.error("Failed to check config status:", error)
  } finally {
    loading.value = false
  }
}

onMounted(checkConfig)

// Re-check when auth state changes (e.g. login/logout)
watch(() => auth.isAdmin.value, (isAdmin) => {
    if (isAdmin) {
        checkConfig()
    }
})
</script>

<template>
  <div v-if="auth.isAdmin.value && !isConfigured && !loading" class="bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4 relative" role="alert">
    <p class="font-bold">Configuration Warning</p>
    <p>The Finnhub API is not configured. The application is running with <strong>mock data</strong>.</p>
    <p class="mt-2 text-sm">To configure real market data:</p>
    <ol class="list-decimal ml-5 text-sm mt-1">
        <li>Obtain an API key from <a href="https://finnhub.io/" target="_blank" class="underline text-blue-600">Finnhub.io</a>.</li>
        <li>Add the key to your environment variables or `backend/app/core/config.py` as `FINNHUB_API_KEY`.</li>
        <li>Restart the backend server.</li>
    </ol>
  </div>
</template>
