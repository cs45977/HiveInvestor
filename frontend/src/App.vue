<script setup>
import { RouterView, useRouter } from 'vue-router'
import { ref, onMounted, watch } from 'vue'
import { getCurrentUser } from '@/services/auth'

const router = useRouter()
const isLoggedIn = ref(false)
const isAdmin = ref(false)

const checkLoginStatus = async () => {
  isLoggedIn.value = !!localStorage.getItem('token')
  if (isLoggedIn.value) {
    try {
      const user = await getCurrentUser()
      isAdmin.value = user?.role === 'admin'
    } catch (err) {
      isAdmin.value = false
    }
  } else {
    isAdmin.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  isLoggedIn.value = false
  isAdmin.value = false
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
          <RouterLink v-if="isAdmin" to="/admin">Admin</RouterLink>
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