// src/services/api.js
import axios from 'axios'

// Khởi tạo một instance của axios với đường dẫn gốc trỏ về Backend FastAPI
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor: Tự động can thiệp vào trước mỗi request gửi đi
api.interceptors.request.use(
  (config) => {
    // Lấy token từ localStorage
    const token = localStorage.getItem('access_token')
    
    // Nếu có token thì nhét vào Header Authorization
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api