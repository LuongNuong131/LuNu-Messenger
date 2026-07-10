// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Chat from '../views/Chat.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/',
    name: 'Chat',
    component: Chat,
    meta: { requiresAuth: true } 
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- Middleware thế hệ mới (Không dùng next() nữa) ---
router.beforeEach((to, from) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !token) {
    // Chưa có token mà đòi vào trang chat/admin -> Bắt đăng nhập
    return '/login'
  } else if (to.meta.requiresAdmin && role !== 'admin') {
    // Không phải admin mà đòi vào trang quản trị -> Đuổi ra trang chat
    return '/'
  } else if ((to.name === 'Login' || to.name === 'Register') && token) {
    // Đã đăng nhập rồi mà cố vào lại Login/Register -> Đẩy vào trang chat
    return '/'
  }
  
  // Hợp lệ thì cho đi tiếp
  return true
})

export default router