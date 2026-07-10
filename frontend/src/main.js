// src/main.js
import { createApp } from 'vue'
import './style.css' // Theme LuNu Ocean + Tailwind v4
import App from './App.vue'
import router from './router' // Nạp cấu hình Router định tuyến

const app = createApp(App)

// Sử dụng Router cho toàn bộ dự án
app.use(router)

// Gắn app vào thẻ div có id="app" trong file index.html
app.mount('#app')