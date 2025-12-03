import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'; // Import auth store

const app = createApp(App)

app.use(router)

// Initialize auth store and check auth state
const auth = useAuthStore();
auth.checkAuth(); 

app.mount('#app')
