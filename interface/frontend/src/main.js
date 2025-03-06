import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router' // Import the router

const app = createApp(App)

createApp(App).mount('#app')

app.use(createPinia())
app.use(router) // Use the router

app.mount('#app')
