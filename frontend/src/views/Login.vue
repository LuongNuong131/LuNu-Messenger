<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="auth-header">
        <div class="logo-icon">🌊</div>
        <h2>Đăng Nhập</h2>
        <p>Chào mừng LuNu quay trở lại!</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="input-group">
          <label>Tên đăng nhập</label>
          <input type="text" v-model="username" placeholder="Nhập tên đăng nhập" required />
        </div>
        
        <div class="input-group">
          <label>Mật khẩu</label>
          <input type="password" v-model="password" placeholder="Nhập mật khẩu" required />
        </div>
        
        <button type="submit" class="btn-primary">Vào thôi Cưng</button>
      </form>
      
      <div class="auth-footer">
        Chưa có tài khoản? <router-link to="/register">Đăng ký ngay</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const handleLogin = () => {
  // LuNu gọi API Login ở đây nhé
  console.log('Login logic here...', username.value)
  // router.push('/chat')
}
</script>

<style scoped>
.auth-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #001f4d 0%, #0052cc 100%);
  padding: 20px;
}

.auth-card {
  background: #ffffff;
  width: 100%;
  max-width: 420px;
  padding: 40px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  animation: slideUp 0.5s ease-out;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo-icon {
  font-size: 48px;
  margin-bottom: 10px;
}

.auth-header h2 {
  color: var(--primary-blue);
  font-size: 28px;
  margin-bottom: 8px;
}

.auth-header p {
  color: var(--text-muted);
  font-size: 15px;
}

.input-group {
  margin-bottom: 20px;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-main);
}

.auth-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 14px;
  color: var(--text-muted);
}

.auth-footer a {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 600;
}

.auth-footer a:hover {
  text-decoration: underline;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>