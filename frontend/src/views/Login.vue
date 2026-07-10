<template>
  <div
    class="relative min-h-screen flex items-center justify-center overflow-hidden bg-abyss"
    @mousemove="onMouseMove"
  >
    <!-- Trăng soi mặt nước — bám nhẹ theo con trỏ, tạo chiều sâu -->
    <div
      class="moon-glow w-[560px] h-[560px] -top-40 -right-32 transition-transform duration-700 ease-out"
      :style="{ transform: `translate(${parallax.x * 1.2}px, ${parallax.y * 1.2}px)` }"
    ></div>
    <div
      class="moon-glow w-[380px] h-[380px] bottom-10 -left-24 transition-transform duration-700 ease-out"
      style="animation-delay: 2s;"
      :style="{ transform: `translate(${parallax.x * -0.8}px, ${parallax.y * -0.8}px)` }"
    ></div>

    <!-- Bong bóng nước trôi nổi -->
    <div class="bubble w-3 h-3 top-[20%] left-[15%]" style="animation-delay: 0s;"></div>
    <div class="bubble w-2 h-2 top-[35%] left-[80%]" style="animation-delay: 1.5s;"></div>
    <div class="bubble w-4 h-4 top-[65%] left-[25%]" style="animation-delay: 3s;"></div>
    <div class="bubble w-2 h-2 top-[50%] left-[60%]" style="animation-delay: 4.5s;"></div>
    <div class="bubble w-3 h-3 top-[15%] left-[50%]" style="animation-delay: 2.5s;"></div>

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

    <!-- Card đăng nhập -->
    <div class="relative z-10 glass-panel p-8 rounded-2xl shadow-[0_0_60px_-15px_rgba(34,211,238,0.25)] w-full max-w-md mx-4 hover-lift">

      <div class="text-center mb-8">
        <div class="relative inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-azure to-cyan-glow shadow-lg shadow-cyan-500/30 mb-4">
          <span class="text-2xl">🌊</span>
          <span class="absolute inset-0 rounded-2xl border border-white/20"></span>
        </div>
        <h1 class="font-display text-4xl font-bold mb-2 tracking-tight bg-gradient-to-r from-cyan-300 via-blue-300 to-cyan-200 bg-clip-text text-transparent">
          LuNu Messenger
        </h1>
        <p class="text-mist text-sm">Bắt sóng và trò chuyện tức thì</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label for="login-username" class="block text-foam text-sm font-medium mb-2">Tên đăng nhập</label>
          <div class="glow-ring rounded-lg">
            <input
              id="login-username"
              v-model="username"
              type="text"
              required
              autocomplete="username"
              class="w-full px-4 py-3 rounded-lg bg-depth-900 border border-tide-line text-foam placeholder-mist-dim focus:outline-none focus:border-cyan-glow/60 transition-all"
              placeholder="Nhập username của bạn..."
            />
          </div>
        </div>

        <div>
          <label for="login-password" class="block text-foam text-sm font-medium mb-2">Mật khẩu</label>
          <div class="glow-ring rounded-lg relative">
            <input
              id="login-password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              required
              autocomplete="current-password"
              class="w-full px-4 py-3 pr-11 rounded-lg bg-depth-900 border border-tide-line text-foam placeholder-mist-dim focus:outline-none focus:border-cyan-glow/60 transition-all"
              placeholder="Nhập mật khẩu..."
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-0 top-0 h-full px-3 text-mist hover:text-cyan-glow transition-colors"
              :aria-label="showPassword ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'"
              tabindex="-1"
            >
              <span class="text-base">{{ showPassword ? '🙈' : '👁️' }}</span>
            </button>
          </div>
        </div>

        <transition name="fade-up">
          <div v-if="errorMsg" class="text-coral text-sm font-medium text-center bg-rose-950/40 border border-rose-500/20 py-2 rounded-lg">
            {{ errorMsg }}
          </div>
        </transition>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold py-3 px-4 rounded-lg shadow-lg shadow-cyan-500/20 transform transition-all hover:scale-[1.02] hover:shadow-cyan-400/30 active:scale-95 disabled:opacity-50 disabled:hover:scale-100"
        >
          <span v-if="!isLoading">Đăng Nhập Ngay</span>
          <span v-else class="inline-flex items-center gap-2">
            <span class="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin"></span>
            Đang xử lý...
          </span>
        </button>
      </form>

      <div class="mt-6 text-center text-mist text-sm">
        Chưa có tài khoản?
        <router-link to="/register" class="text-cyan-300 hover:text-cyan-200 font-semibold underline underline-offset-2 transition-colors">
          Đăng ký tại đây
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const isLoading = ref(false)
const showPassword = ref(false)
const router = useRouter()

// Hiệu ứng ánh trăng bám nhẹ theo con trỏ chuột — tạo chiều sâu cho nền
const parallax = reactive({ x: 0, y: 0 })
const onMouseMove = (e) => {
  const { innerWidth, innerHeight } = window
  parallax.x = (e.clientX / innerWidth - 0.5) * 30
  parallax.y = (e.clientY / innerHeight - 0.5) * 30
}

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

<style scoped>
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.2s ease;
}
.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

@media (prefers-reduced-motion: reduce) {
  .transition-transform {
    transition: none !important;
  }
}
</style>