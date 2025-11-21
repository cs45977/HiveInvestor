<script setup>
import { ref, onMounted, watch } from 'vue'
import { getLeaderboard } from '../services/portfolio'

const window = ref('1d')
const leaderboard = ref(null)
const loading = ref(false)
const error = ref(null)

const fetchLeaderboard = async () => {
    loading.value = true
    error.value = null
    leaderboard.value = null
    try {
        leaderboard.value = await getLeaderboard(window.value)
    } catch (e) {
        error.value = "Failed to fetch leaderboard. It might not be generated yet."
    } finally {
        loading.value = false
    }
}

onMounted(fetchLeaderboard)
watch(window, fetchLeaderboard)
</script>

<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Leaderboard</h1>
    
    <div class="mb-4">
        <select v-model="window" class="border p-2 rounded">
            <option value="1d">1 Day</option>
            <option value="7d">7 Days</option>
            <option value="30d">30 Days</option>
            <option value="90d">90 Days</option>
        </select>
    </div>

    <div v-if="loading" class="text-center">Loading...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    
    <div v-else-if="leaderboard && leaderboard.entries.length > 0" class="bg-white shadow rounded overflow-hidden">
        <table class="min-w-full leading-normal">
            <thead>
                <tr>
                    <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Rank</th>
                    <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">User</th>
                    <th class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider">PPG (%)</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="entry in leaderboard.entries" :key="entry.user_id">
                    <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm font-bold">{{ entry.rank }}</td>
                    <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">{{ entry.username }}</td>
                    <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm text-right" :class="{'text-green-600': entry.ppg > 0, 'text-red-600': entry.ppg < 0}">
                        {{ entry.ppg }}%
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else class="text-center text-gray-500">No data available for this period.</div>
  </div>
</template>
