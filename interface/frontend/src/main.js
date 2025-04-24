import './assets/main.css';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import socketService from './services/socketService.js';

const app = createApp(App);

// Make WS available globally as $socket
app.config.globalProperties.$socket = socketService;

// Start WS connection
socketService.connect();

app.use(createPinia());
app.use(router);
app.mount('#app');
