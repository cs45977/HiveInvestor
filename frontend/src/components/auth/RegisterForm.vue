<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../../services/auth'

const router = useRouter()
const email = ref('')
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const emailError = computed(() => {
  if (!email.value) return ''
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email.value) ? '' : 'Invalid email format'
})

const passwordMismatchError = computed(() => {
  if (!password.value || !confirmPassword.value) return ''
  return password.value === confirmPassword.value ? '' : 'Passwords do not match'
})

const passwordStrengthError = computed(() => {
  if (!password.value) return ''
  const errors = []
  if (password.value.length < 8) {
    errors.push('at least 8 characters')
  }
  if (!/[A-Z]/.test(password.value)) {
    errors.push('at least one uppercase letter')
  }
  if (!/[a-z]/.test(password.value)) {
    errors.push('at least one lowercase letter')
  }
  if (!/[0-9]/.test(password.value)) {
    errors.push('at least one number')
  }
  if (!/[^A-Za-z0-9]/.test(password.value)) {
    errors.push('at least one special character')
  }
  return errors.length ? `Password must contain: ${errors.join(', ')}` : ''
})

const isFormValid = computed(() => {
  return !emailError.value && !passwordMismatchError.value && !passwordStrengthError.value && email.value && username.value && password.value && confirmPassword.value
})

const handleSubmit = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  if (isFormValid.value) {
    try {
      await register(email.value, username.value, password.value)
      successMessage.value = 'Registration successful!'
      // Optionally delay redirect to show success message
      router.push('/')
    } catch (error) {
      if (error.response && error.response.data && error.response.data.detail) {
        errorMessage.value = error.response.data.detail
      } else {
        errorMessage.value = 'An unexpected error occurred.'
      }
    }
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
    <div v-if="errorMessage" class="error-message mb-4 text-red-500 font-bold text-center">
      {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="success-message mb-4 text-green-500 font-bold text-center">
      {{ successMessage }}
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
      <p v-if="emailError" class="email-error text-red-500 text-xs italic">{{ emailError }}</p>
    </div>
    <div class="mb-4">
      <label for="username" class="block text-gray-700 text-sm font-bold mb-2">Username:</label>
      <input
        type="text"
        id="username"
        v-model="username"
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
      <p v-if="passwordStrengthError" class="password-strength-error text-red-500 text-xs italic">{{ passwordStrengthError }}</p>
    </div>
    <div class="mb-6">
      <label for="confirmPassword" class="block text-gray-700 text-sm font-bold mb-2">Confirm Password:</label>
      <input
        type="password"
        id="confirmPassword"
        v-model="confirmPassword"
        class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
        required
      />
      <p v-if="passwordMismatchError" class="password-match-error text-red-500 text-xs italic">{{ passwordMismatchError }}</p>
    </div>
    <div class="flex items-center justify-between">
      <button
        type="submit"
        :disabled="!isFormValid"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline disabled:opacity-50"
      >
        Register
      </button>
    </div>
  </form>
</template>

<style scoped>
/* Add any component-specific styles here */
</style>
