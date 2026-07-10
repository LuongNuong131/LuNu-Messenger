<template>
  <div class="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#040b16]">

    <!-- Trăng soi mặt nước -->
    <div class="moon-glow w-[520px] h-[520px] -top-40 -left-32"></div>
    <div class="moon-glow w-[360px] h-[360px] bottom-10 -right-24" style="animation-delay: 2s;"></div>

    <!-- Bong bóng nước trôi nổi -->
    <div class="bubble w-3 h-3 top-[25%] left-[80%]" style="animation-delay: 0s;"></div>
    <div class="bubble w-2 h-2 top-[40%] left-[10%]" style="animation-delay: 1.5s;"></div>
    <div class="bubble w-4 h-4 top-[70%] left-[70%]" style="animation-delay: 3s;"></div>
    <div class="bubble w-2 h-2 top-[55%] left-[40%]" style="animation-delay: 4.5s;"></div>
    <div class="bubble w-3 h-3 top-[18%] left-[45%]" style="animation-delay: 2.5s;"></div>

    <!-- Sóng đáy màn hình -->
    <div class="wave-wrap">
      <div class="wave-track layer-back">
        <svg class="wave-svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,60 C150,110 350,10 600,60 C850,110 1050,10 1200,60 L1200,120 L0,120 Z" fill="#3b82f6" />
        </svg>
        <svg class="wave-svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,60 C150,110 350,10 600,60 C850,110 1050,10 1200,60 L1200,120 L0,120 Z" fill="#3b82f6" />
        </svg>
      </div>
      <div class="wave-track layer-front">
        <svg class="wave-svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,70 C200,20 400,120 600,70 C800,20 1000,120 1200,70 L1200,120 L0,120 Z" fill="#22d3ee" />
        </svg>
        <svg class="wave-svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M0,70 C200,20 400,120 600,70 C800,20 1000,120 1200,70 L1200,120 L0,120 Z" fill="#22d3ee" />
        </svg>
      </div>
    </div>

    <!-- Card đăng ký -->
    <div class="relative z-10 bg-[#0d1f38]/60 backdrop-blur-xl border border-cyan-400/20 p-8 rounded-2xl shadow-[0_0_60px_-15px_rgba(34,211,238,0.25)] w-full max-w-md mx-4">

      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-400 shadow-lg shadow-cyan-500/30 mb-4">
          <span class="text-2xl">🌊</span>
        </div>
        <h1 class="font-display text-4xl font-bold mb-2 tracking-tight bg-gradient-to-r from-cyan-300 via-blue-300 to-cyan-200 bg-clip-text text-transparent">
          LuNu Messenger
        </h1>
        <p class="text-[#7d97b8] text-sm">Tạo tài khoản mới, hoàn toàn miễn phí</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-[#eaf6ff] text-sm font-medium mb-2">Tên đăng nhập</label>
          <input
            v-model="username"
            type="text"
            required
            class="w-full px-4 py-3 rounded-lg bg-[#081527] border border-[#1f3a5c] text-[#eaf6ff] placeholder-[#4a6180] focus:outline-none focus:ring-2 focus:ring-cyan-400/60 focus:border-cyan-400/60 transition-all"
            placeholder="Tên tài khoản viết liền không dấu..."
          />
        </div>

        <div>
          <label class="block text-[#eaf6ff] text-sm font-medium mb-2">Mật khẩu</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-3 rounded-lg bg-[#081527] border border-[#1f3a5c] text-[#eaf6ff] placeholder-[#4a6180] focus:outline-none focus:ring-2 focus:ring-cyan-400/60 focus:border-cyan-400/60 transition-all"
            placeholder="Nhập mật khẩu an toàn..."
          />
        </div>

        <div>
          <label class="block text-[#eaf6ff] text-sm font-medium mb-2">Xác nhận mật khẩu</label>
          <input
            v-model="confirmPassword"
            type="password"
            required
            class="w-full px-4 py-3 rounded-lg bg-[#081527] border border-[#1f3a5c] text-[#eaf6ff] placeholder-[#4a6180] focus:outline-none focus:ring-2 focus:ring-cyan-400/60 focus:border-cyan-400/60 transition-all"
            placeholder="Nhập lại mật khẩu giống phía trên..."
          />
        </div>

        <div v-if="errorMsg" class="text-rose-300 text-sm font-medium text-center bg-rose-950/40 border border-rose-500/20 py-2 rounded-lg">
          {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="text-emerald-300 text-sm font-medium text-center bg-emerald-950/40 border border-emerald-500/20 py-2 rounded-lg">
          {{ successMsg }}
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold py-3 px-4 rounded-lg shadow-lg shadow-cyan-500/20 transform transition-all hover:scale-[1.02] hover:shadow-cyan-400/30 active:scale-95 disabled:opacity-50 disabled:hover:scale-100"
        >
          <span v-if="!isLoading">Đăng Ký Ngay</span>
          <span v-else class="inline-flex items-center gap-2">
            <span class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
            Đang tạo tài khoản...
          </span>
        </button>
      </form>

      <div class="mt-6 text-center text-[#7d97b8] text-sm">
        Đã có tài khoản rồi?
        <router-link to="/login" class="text-cyan-300 hover:text-cyan-200 font-semibold underline underline-offset-2 transition-colors">
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