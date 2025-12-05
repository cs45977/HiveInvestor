<script setup>
import { RouterView, useRouter } from 'vue-router'
import { ref, onMounted, watch } from 'vue'

const router = useRouter()
const isLoggedIn = ref(false)

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('token')
}

const logout = () => {
  localStorage.removeItem('token')
  isLoggedIn.value = false
  router.push('/login')
}

onMounted(() => {
  checkLoginStatus()
})

// Watch for route changes to update login status (e.g. after login redirect)
watch(() => router.currentRoute.value, () => {
  checkLoginStatus()
})
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <template v-if="!isLoggedIn">
          <RouterLink to="/register">Register</RouterLink>
          <RouterLink to="/login">Login</RouterLink>
        </template>
        <template v-else>
          <RouterLink to="/dashboard">Dashboard</RouterLink>
          <RouterLink to="/trade">Trade</RouterLink>
          <RouterLink to="/leaderboard">Leaderboard</RouterLink>
          <a href="#" @click.prevent="logout">Logout</a>
        </template>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>