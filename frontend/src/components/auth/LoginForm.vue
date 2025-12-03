<script setup>
import { ref } from 'vue'
// import { useRouter } from 'vue-router' // No longer needed as auth store handles navigation
// import { login } from '../../services/auth' // No longer needed as auth store encapsulates service call
import { useAuthStore } from '../../stores/auth'

// const router = useRouter() // No longer needed
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const errorMessage = ref('')

const handleSubmit = async () => {
  errorMessage.value = ''
  try {
    await auth.login(email.value, password.value) // Use store's login method
    // Navigation is handled by the auth store after successful login
  } catch (error) {
     if (error.response && error.response.data && error.response.data.detail) {
        errorMessage.value = error.response.data.detail
      } else if (error.message) {
          errorMessage.value = error.message
      } else {
        errorMessage.value = 'An unexpected error occurred.'
      }
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
    <div v-if="errorMessage" class="error-message mb-4 text-red-500 font-bold text-center">
      {{ errorMessage }}
    </div>
    <div class="mb-4">
      <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email:</label>
      <input
        type="email"
        id="email"
        v-model="email"
        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        required
      />
    </div>
    <div class="mb-6">
      <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password:</label>
      <input
        type="password"
        id="password"
        v-model="password"
        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
        required
      />
    </div>
    <div class="flex items-center justify-between">
      <button
        type="submit"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Login
      </button>
    </div>
  </form>
</template>

<style scoped>
/* Add any component-specific styles here */
</style>