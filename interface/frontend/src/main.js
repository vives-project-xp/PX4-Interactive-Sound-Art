<<<<<<< HEAD
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import io from 'socket.io-client' // Import socket.io-client

import App from './app.vue'
import router from './router' // Import the router

// Establish WebSocket connection
// Make sure the backend URL is correct (adjust if needed)
const socket = io('http://localhost:4000')

const app = createApp(App)

// Provide the socket instance globally
app.config.globalProperties.$socket = socket

// Remove the duplicate createApp(App).mount('#app') line
// createApp(App).mount('#app') // This line was redundant

app.use(createPinia())
app.use(router) // Use the router

app.mount('#app') // Mount the app instance *after* applying plugins
=======
import './assets/main.css';
import { createApp } from 'vue';
import { createPinia } from 'pinia';

import router from './router';
import socketService from './services/socketService.js';

const app = createApp(App);

app.config.globalProperties.$socket = socketService;
socketService.connect();

app.use(createPinia());
app.use(router);
app.mount('#app');
>>>>>>> d30cca8852268da199c138b688e9a55109f7c233
