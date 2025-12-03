<template>
  <div class="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-8">
      <h1 class="text-2xl font-bold text-center mb-6">User Profile</h1>
      <div v-if="message" class="mb-4 text-center font-bold" :class="{'text-green-500': isSuccess, 'text-red-500': !isSuccess}">
        {{ message }}
      </div>
      <form @submit.prevent="updateProfile">
        <div class="mb-4">
          <label for="email" class="block text-gray-700 text-sm font-bold mb-2">Email</label>
          <input
            id="email"
            type="email"
            :value="authStore.user?.email"
            disabled
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-500 bg-gray-100 leading-tight focus:outline-none focus:shadow-outline cursor-not-allowed"
          />
        </div>
        <div class="mb-6">
          <label for="username" class="block text-gray-700 text-sm font-bold mb-2">Username</label>
          <input
            id="username"
            type="text"
            v-model="username"
            class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          />
        </div>
        <div class="flex items-center justify-center">
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
          >
            Update Profile
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const router = useRouter();
const username = ref('');
const message = ref('');
const isSuccess = ref(false);

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login');
    return;
  }
  await authStore.fetchUser();
  if (authStore.user) {
    username.value = authStore.user.username;
  }
});

watch(() => authStore.user, (newUser) => {
  if (newUser) {
    username.value = newUser.username;
  }
});

const updateProfile = async () => {
  message.value = '';
  try {
    await authStore.updateUser({ username: username.value });
    message.value = 'Profile updated successfully';
    isSuccess.value = true;
  } catch (error) {
    message.value = error.message || 'Update failed';
    isSuccess.value = false;
  }
};
</script>
