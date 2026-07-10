<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500">
    <div class="bg-white/10 backdrop-blur-lg border border-white/20 p-8 rounded-2xl shadow-2xl w-full max-w-md">
      
      <div class="text-center mb-8">
        <h1 class="text-4xl font-extrabold text-white mb-2 tracking-wider">LuNu Messenger</h1>
        <p class="text-white/80">Tạo tài khoản mới hoàn toàn miễn phí</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-5">
        <div>
          <label class="block text-white text-sm font-medium mb-2">Tên đăng nhập</label>
          <input 
            v-model="username" 
            type="text" 
            required
            class="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/10 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-pink-300 transition-all"
            placeholder="Tên tài khoản viết liền không dấu..."
          />
        </div>

        <div>
          <label class="block text-white text-sm font-medium mb-2">Mật khẩu</label>
          <input 
            v-model="password" 
            type="password" 
            required
            class="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/10 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-pink-300 transition-all"
            placeholder="Nhập mật khẩu an toàn..."
          />
        </div>

        <div>
          <label class="block text-white text-sm font-medium mb-2">Xác nhận mật khẩu</label>
          <input 
            v-model="confirmPassword" 
            type="password" 
            required
            class="w-full px-4 py-3 rounded-lg bg-white/20 border border-white/10 text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-pink-300 transition-all"
            placeholder="Nhập lại mật khẩu giống phía trên..."
          />
        </div>

        <div v-if="errorMsg" class="text-red-300 text-sm font-semibold text-center bg-red-900/40 py-2 rounded">
          {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="text-green-200 text-sm font-semibold text-center bg-green-900/40 py-2 rounded">
          {{ successMsg }}
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-pink-500 to-orange-400 hover:from-pink-600 hover:to-orange-500 text-white font-bold py-3 px-4 rounded-lg shadow-lg transform transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50"
        >
          <span v-if="!isLoading">Đăng Ký Ngay</span>
          <span v-else>Đang tạo tài khoản...</span>
        </button>
      </form>

      <div class="mt-6 text-center text-white/80 text-sm">
        Đã có tài khoản rồi? 
        <router-link to="/login" class="text-pink-300 hover:text-white font-bold underline transition-colors">
          Đăng nhập ngay
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
const confirmPassword = ref('')
const errorMsg = ref('')
const successMsg = ref('')
const isLoading = ref(false)
const router = useRouter()

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Mật khẩu xác nhận không khớp cưng ơi!'
    return
  }

  isLoading.value = true
  errorMsg.value = ''
  successMsg.value = ''

  try {
    await api.post('/auth/register', {
      username: username.value,
      password: password.value
    })

    successMsg.value = 'Đăng ký thành công! Đang chuyển hướng...'
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (error) {
    if (error.response && error.response.data) {
      errorMsg.value = error.response.data.detail || 'Đăng ký thất bại.'
    } else {
      errorMsg.value = 'Không thể kết nối tới server backend.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>