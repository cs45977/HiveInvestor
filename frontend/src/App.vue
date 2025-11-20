<script setup>
import { onMounted, ref } from 'vue'

const apiMessage = ref('')
const connectionStatus = ref('connecting') // connecting, success, error

onMounted(async () => {
  try {
    const response = await fetch('/api/')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const data = await response.json()
    apiMessage.value = data.Hello
    connectionStatus.value = 'success'
  } catch (error) {
    console.error('Error fetching API:', error)
    apiMessage.value = 'Failed to fetch message from backend.'
    connectionStatus.value = 'error'
  }
})
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />
  </header>

  <main>
    <div class="greetings">
      <h1 class="green">Welcome to HiveInvestor!</h1>

      <div v-if="connectionStatus === 'connecting'" class="status-container">
        <h3>Attempting to connect to the backend... Please stand by.</h3>
        <img src="https://media.giphy.com/media/l0HlBOJa9QvDpP41a/giphy.gif" alt="Connecting..." class="status-gif" />
      </div>

      <div v-else-if="connectionStatus === 'success'" class="status-container success">
        <h3>Backend connection successful! Houston, we have a signal.</h3>
        <p>Backend says: "{{ apiMessage }}"</p>
        <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTk0YjQzMDJjYzZkYjZkYjYyZjM4MjM4ZDI3MjI2ZTMzMjI3ZGM4ZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7qE2UTm2q2v6g4gM/giphy.gif" alt="Success" class="status-gif" />
      </div>

      <div v-else-if="connectionStatus === 'error'" class="status-container error">
        <h3>Yikes! Could not connect to the backend.</h3>
        <p>Is the backend server running? It might be taking a coffee break.</p>
        <img src="https://media.giphy.com/media/3o7aD4grHwn87v5A4g/giphy.gif" alt="Error" class="status-gif" />
      </div>
    </div>
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

main {
  width: 100%;
}

.greetings {
  text-align: center;
}

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.status-container {
  margin-top: 2rem;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  border: 1px solid #ccc;
}

.status-container.success {
  background-color: #e0f2f1;
  border-color: #4caf50;
}

.status-container.error {
  background-color: #ffebee;
  border-color: #f44336;
}

.status-gif {
  margin-top: 1rem;
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  main {
    padding-left: calc(var(--section-gap) / 2);
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  .greetings {
    text-align: left;
  }
}
</style>
