<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
    
    <div class="bg-white/10 backdrop-blur-lg border border-white/20 p-8 rounded-2xl shadow-2xl w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-extrabold text-white mb-2 tracking-wider">LuNu Messenger</h1>
        <p class="text-white/80">Đăng nhập để bắt đầu trò chuyện</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-white text-sm font-medium mb-2">Tên đăng nhập</label>
          <input 
            v-model="username" 
            type="text" 
            required
            class="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/10 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-pink-300 transition-all"
            placeholder="Nhập username của bạn..."
          />
        </div>

        <div>
          <label class="block text-white text-sm font-medium mb-2">Mật khẩu</label>
          <input 
            v-model="password" 
            type="password" 
            required
            class="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/10 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-pink-300 transition-all"
            placeholder="Nhập mật khẩu..."
          />
        </div>

        <div v-if="errorMsg" class="text-red-300 text-sm font-semibold text-center bg-red-900/40 py-2 rounded">
          {{ errorMsg }}
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-pink-500 to-orange-400 hover:from-pink-600 hover:to-orange-500 text-white font-bold py-3 px-4 rounded-lg shadow-lg transform transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50"
        >
          <span v-if="!isLoading">Đăng Nhập Ngay</span>
          <span v-else>Đang xử lý...</span>
        </button>
      </form>

      <div class="mt-6 text-center text-white/80 text-sm">
        Chưa có tài khoản? 
        <router-link to="/register" class="text-pink-300 hover:text-white font-bold underline transition-colors">
          Đăng ký tại đây
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
const router = useRouter()

const handleLogin = async () => {
  isLoading.value = true
  errorMsg.value = ''
  
  try {
    // FastAPI (OAuth2PasswordRequestForm) yêu cầu gửi dữ liệu dạng x-www-form-urlencoded
    const params = new URLSearchParams()
    params.append('username', username.value)
    params.append('password', password.value)

    const response = await api.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    const token = response.data.access_token
    
    // Giải mã JWT Payload để lấy Role (Quyền) mà không cần gọi API thêm lần nữa
    const payloadBase64 = token.split('.')[1]
    const decodedPayload = JSON.parse(atob(payloadBase64))
    const userRole = decodedPayload.role

    // Lưu vào LocalStorage
    localStorage.setItem('access_token', token)
    localStorage.setItem('user_role', userRole)
    localStorage.setItem('username', username.value)

    // Chuyển hướng vào trang Chat
    router.push('/')
  } catch (error) {
    if (error.response && error.response.status === 401) {
      errorMsg.value = 'Sai username hoặc password rồi cưng ơi!'
    } else {
      errorMsg.value = 'Có lỗi xảy ra kết nối với máy chủ.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>