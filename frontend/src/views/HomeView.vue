<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const isDev = import.meta.env.DEV
const backendStatus = ref('Checking connection...')
const dbStatus = ref('Checking connection...')
const isBackendConnected = ref(false)
const isDbConnected = ref(false)

onMounted(async () => {
  if (isDev) {
    try {
      const response = await axios.get('/api/status')
      if (response.data) {
        backendStatus.value = response.data.backend_status || 'Connected'
        isBackendConnected.value = true
        
        if (response.data.db_status) {
            dbStatus.value = response.data.db_status
            isDbConnected.value = response.data.db_status === 'Connected'
        } else {
             dbStatus.value = 'Unknown'
             isDbConnected.value = false
        }
      }
    } catch (error) {
      backendStatus.value = 'Connection Failed'
      dbStatus.value = 'Unreachable'
      isBackendConnected.value = false
      isDbConnected.value = false
      console.error('Backend status check failed:', error)
    }
  }
})
</script>

<template>
  <main>
    <h1>Welcome to HiveInvestor</h1>
    <div v-if="isDev" class="text-center mt-4 p-4 bg-gray-100 rounded shadow-sm inline-block">
      <p class="text-sm font-bold text-gray-500 mb-2 uppercase tracking-wide">Development Status</p>
      <div class="grid grid-cols-2 gap-4 text-left">
          <div>Backend:</div>
          <div :class="{'text-success font-bold': isBackendConnected, 'text-red-500 font-bold': !isBackendConnected}">
            {{ backendStatus }}
          </div>
          
          <div>Database:</div>
           <div :class="{'text-success font-bold': isDbConnected, 'text-red-500 font-bold': !isDbConnected}">
            {{ dbStatus }}
          </div>
      </div>
    </div>
  </main>
</template>
