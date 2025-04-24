import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import io from 'socket.io-client' // Import socket.io-client

import App from './app.vue'
import router from './router' // Import the router

// Establish WebSocket connection
const socket = io('http://localhost:4000')

const app = createApp(App)

// Provide the socket instance globally
app.config.globalProperties.$socket = socket

app.use(createPinia())
app.use(router) // Use the router

app.mount('#app') // Mount the app instance after applying plugins