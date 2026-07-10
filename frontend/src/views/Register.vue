<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <div class="auth-header">
        <div class="logo-icon">💧</div>
        <h2>Tạo Tài Khoản</h2>
        <p>Bắt đầu kết nối với mọi người</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="input-group">
          <label>Tên đăng nhập</label>
          <input type="text" v-model="username" placeholder="Chọn tên đăng nhập" required />
        </div>

        <div class="input-group">
          <label>Email</label>
          <input type="email" v-model="email" placeholder="Nhập địa chỉ email" required />
        </div>
        
        <div class="input-group">
          <label>Mật khẩu</label>
          <input type="password" v-model="password" placeholder="Tạo mật khẩu mạnh" required />
        </div>
        
        <button type="submit" class="btn-primary">Đăng Ký</button>
      </form>
      
      <div class="auth-footer">
        Đã có tài khoản? <router-link to="/login">Đăng nhập</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const router = useRouter()

const handleRegister = () => {
  // LuNu gọi API Register ở đây nhé
  console.log('Register logic here...', username.value)
  // router.push('/login')
}
</script>

<style scoped>
/* CSS tương tự Login, ta có thể dùng chung class */
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

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>