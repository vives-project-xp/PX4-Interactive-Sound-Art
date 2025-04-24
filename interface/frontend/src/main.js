import './assets/main.css';
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './app.vue';
import router from './router';              // if used
import socketService from './services/socketService.js';

const app = createApp(App);

app.config.globalProperties.$socket = socketService;
socketService.connect();

app.use(createPinia());
app.use(router);
app.mount('#app');
