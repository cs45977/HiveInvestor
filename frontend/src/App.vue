<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import AdminConfigNotification from './components/admin/AdminConfigNotification.vue'

const auth = useAuthStore()
</script>

<template>
  <header>
    <div class="wrapper">
      <nav class="bg-gray-800 p-4 text-white flex justify-between items-center">
        <div class="flex items-center">
          <RouterLink to="/" class="text-white text-xl font-bold hover:text-gray-300">HiveInvestor</RouterLink>
          <RouterLink v-if="auth.authState.isAuthenticated" to="/dashboard" class="ml-4 hover:text-gray-300">Dashboard</RouterLink>
          <RouterLink v-if="auth.authState.isAuthenticated" to="/trade" class="ml-4 hover:text-gray-300">Trade</RouterLink>
          <RouterLink v-if="auth.authState.isAuthenticated" to="/leaderboard" class="ml-4 hover:text-gray-300">Leaderboard</RouterLink>
          <RouterLink v-if="auth.authState.isAuthenticated" to="/profile" class="ml-4 hover:text-gray-300">Profile</RouterLink>
          <RouterLink v-if="auth.authState.isAuthenticated && auth.isAdmin.value" to="/admin" class="ml-4 hover:text-gray-300">Admin</RouterLink>
        </div>
        <div class="flex items-center">
          <template v-if="auth.authState.isAuthenticated">
            <span class="mr-4">Logged in as: {{ auth.authState.user?.username }}</span>
            <button @click="auth.logout" class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">Logout</button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="mr-4 hover:text-gray-300">Login</RouterLink>
            <RouterLink to="/register" class="hover:text-gray-300">Register</RouterLink>
          </template>
        </div>
      </nav>
    </div>
  </header>

  <AdminConfigNotification />

  <RouterView />
</template>

<style scoped>
</style>