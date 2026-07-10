<template>
  <div class="flex h-screen bg-slate-900 text-slate-100 overflow-hidden">
    
    <div class="w-80 bg-slate-850 border-r border-slate-700 flex flex-col">
      <div class="p-4 border-b border-slate-700 flex justify-between items-center bg-slate-800">
        <div>
          <h2 class="font-bold text-lg text-pink-400">👋 {{ myUsername }}</h2>
          <span class="text-xs text-slate-400 capitalize">Quyền: {{ myRole }}</span>
        </div>
        <div class="flex gap-2">
          <router-link v-if="myRole === 'admin'" to="/admin" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs px-2 py-1.5 rounded transition-colors">
            🔧 Admin
          </router-link>
          <button @click="handleLogout" class="bg-red-600/80 hover:bg-red-700 text-white text-xs px-2 py-1.5 rounded transition-colors">
            Thoát
          </button>
        </div>
      </div>

      <div class="p-3 border-b border-slate-700 bg-slate-900">
        <input 
          v-model="searchQuery"
          @input="searchUsers"
          type="text"
          placeholder="Tìm tên bạn bè để chat..."
          class="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-pink-500 transition-all text-white"
        />
      </div>

      <div class="flex-1 overflow-y-auto p-2 space-y-1">
        <div v-if="searchResults.length === 0" class="text-center text-slate-500 text-xs py-8">
          Nhập chính xác hoặc một phần tên để tìm người trò chuyện.
        </div>
        <button
          v-for="user in searchResults"
          :key="user.id"
          @click="selectUser(user)"
          :class="['w-full text-left p-3 rounded-lg flex items-center justify-between transition-all', activeUser?.id === user.id ? 'bg-pink-600 text-white' : 'hover:bg-slate-800 bg-slate-800/40']"
        >
          <span class="font-medium">💬 {{ user.username }}</span>
          <span class="text-xs opacity-60 capitalize">{{ user.role }}</span>
        </button>
      </div>
    </div>

    <div class="flex-1 flex flex-col bg-slate-900">
      <template v-if="activeUser">
        <div class="p-4 border-b border-slate-700 bg-slate-800 flex items-center shadow-md">
          <span class="text-xl mr-2">👤</span>
          <div>
            <h3 class="font-bold text-white text-md">{{ activeUser.username }}</h3>
            <p class="text-xs text-green-400">Đang trực tuyến (Real-time)</p>
          </div>
        </div>

        <div ref="messageContainer" class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-950/40">
          <div 
            v-for="msg in filteredMessages" 
            :key="msg.id"
            :class="['flex flex-col max-w-[70%] rounded-2xl p-3 shadow-md relative group', msg.sender_id === myId ? 'ml-auto bg-pink-600 text-white rounded-tr-none' : 'mr-auto bg-slate-800 text-slate-100 rounded-tl-none']"
          >
            <p v-if="msg.message_type === 'text'" class="text-sm whitespace-pre-wrap break-words">{{ msg.content }}</p>

            <div v-else-if="msg.message_type === 'image'" class="space-y-1">
              <img :src="'http://localhost:8000' + msg.file_url" class="max-w-xs max-h-48 rounded-lg object-cover cursor-pointer border border-black/10" alt="Hình ảnh" @click="openImageWindow('http://localhost:8000' + msg.file_url)"/>
              <a :href="'http://localhost:8000' + msg.file_url" download class="block text-xs underline text-cyan-300 hover:text-white mt-1">📥 Tải ảnh gốc</a>
            </div>

            <div v-else-if="msg.message_type === 'file'" class="flex items-center gap-3 bg-black/20 p-2.5 rounded-lg border border-white/10">
              <span class="text-2xl">📁</span>
              <div class="overflow-hidden">
                <p class="text-xs font-semibold truncate max-w-[180px]">{{ msg.content }}</p>
                <a :href="'http://localhost:8000' + msg.file_url" download class="text-xs text-cyan-300 underline hover:text-white font-medium">Click để tải xuống máy</a>
              </div>
            </div>

            <span class="text-[10px] opacity-50 mt-1 self-end">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>

        <div class="p-4 border-t border-slate-700 bg-slate-800/80 backdrop-blur flex items-center gap-3">
          <button @click="$refs.fileInput.click()" class="bg-slate-700 hover:bg-slate-600 text-xl text-white p-2.5 rounded-lg transition-colors shadow-inner" title="Gửi File hoặc Hình ảnh">
            📎
          </button>
          <input type="file" ref="fileInput" @change="handleFileUpload" class="hidden" />

          <input 
            v-model="newMessage"
            @keyup.enter="sendTextMessage"
            type="text"
            placeholder="Nhập nội dung tin nhắn..."
            class="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 text-sm focus:outline-none focus:border-pink-500 text-white"
          />

          <button @click="sendTextMessage" class="bg-gradient-to-r from-pink-500 to-rose-500 hover:from-pink-600 hover:to-rose-600 font-bold px-5 py-3 rounded-lg shadow-md transition-all text-sm">
            Gửi
          </button>
        </div>
      </template>

      <template v-else>
        <div class="flex-1 flex flex-col items-center justify-center text-slate-500">
          <span class="text-6xl mb-4">💬</span>
          <h2 class="text-xl font-bold text-slate-400">LuNu Messenger</h2>
          <p class="text-sm mt-1 text-slate-500">Hãy tìm kiếm một tài khoản ở thanh bên trái để bắt đầu trò chuyện real-time.</p>
        </div>
      </template>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()

// Thông tin cá nhân lấy từ localStorage
const myUsername = ref(localStorage.getItem('username') || '')
const myRole = ref(localStorage.getItem('user_role') || 'user')
const myId = ref(0) // Sẽ bổ sung tự động khi nhận tin

const searchQuery = ref('')
const searchResults = ref([])
const activeUser = ref(null)
const newMessage = ref('')
const allMessages = ref([]) // Lưu kho chứa tin nhắn real-time tạm thời
const messageContainer = ref(null)
const fileInput = ref(null)

let ws = null

// Lọc tin nhắn chỉ hiển thị giữa mình và đối tác chat hiện tại
const filteredMessages = computed(() => {
  if (!activeUser.value) return []
  return allMessages.value.filter(msg => 
    (msg.sender_id === myId.value && msg.receiver_id === activeUser.value.id) ||
    (msg.sender_id === activeUser.value.id && msg.receiver_id === myId.value)
  )
})

// Tự động cuộn xuống đáy khi có tin nhắn mới
const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

// Hàm Tìm kiếm User ẩn danh bạ
const searchUsers = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }
  try {
    const res = await api.get(`/chat/users/search?keyword=${searchQuery.value}`)
    searchResults.value = res.data
  } catch (err) {
    console.error('Lỗi tìm kiếm user:', err)
  }
}

// Khi click vào một user để chat
const selectUser = async (user) => {
  activeUser.value = user
  try {
    // 1. Lấy lịch sử chat trong quá khứ (Tối đa 60 phút đổ lại, cũ hơn backend tự xóa)
    const res = await api.get(`/chat/history/${user.id}`)
    
    // Cập nhật lại danh sách tin nhắn hiện hữu
    // Định vị ID của bản thân dựa trên lịch sử tin nhắn cũ (nếu có)
    if (res.data.length > 0) {
      const sampleMsg = res.data[0]
      myId.value = sampleMsg.sender_id === user.id ? sampleMsg.receiver_id : sampleMsg.sender_id
    }
    
    // Nạp tin nhắn vào store hiển thị
    allMessages.value = res.data
    scrollToBottom()
  } catch (err) {
    console.error('Không thể lấy lịch sử chat:', err)
  }
}

// Kết nối cổng WebSocket Real-time
const connectWebSocket = () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  ws = new WebSocket(`ws://localhost:8000/chat/ws?token=${token}`)

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    
    // Cập nhật ID của mình nếu chưa có dữ liệu cấu hình
    if (myId.value === 0) {
      if (data.sender_id && data.content && data.sender_id !== activeUser.value?.id) {
         // Nhận dạng ID linh hoạt
      }
    }

    // Thêm tin nhắn mới nhận được vào mảng
    // Kiểm tra trùng lặp ID tin nhắn trước khi đẩy
    if (!allMessages.value.some(m => m.id === data.id)) {
      allMessages.value.push(data)
    }
    
    scrollToBottom()
  }

  ws.onclose = () => {
    console.log('Cổng WebSocket bị đóng, đang thử kết nối lại...')
    setTimeout(connectWebSocket, 3000) // Tự động kết nối lại sau 3s nếu đứt mạng
  }
}

// Gửi tin nhắn Text thường chữ thường
const sendTextMessage = () => {
  if (!newMessage.value.trim() || !activeUser.value || !ws) return

  const payload = {
    receiver_id: activeUser.value.id,
    content: newMessage.value,
    message_type: 'text',
    file_url: null
  }

  ws.send(JSON.stringify(payload))
  newMessage.value = ''
}

// Xử lý Upload file đính kèm hoặc hình ảnh ảnh
const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file || !activeUser.value || !ws) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    // 1. Đẩy file lên server lưu trữ cục bộ
    const res = await api.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // 2. Lấy link server trả về, đóng gói bắn tiếp qua WebSocket để đối phương nhận dạng lập tức
    const payload = {
      receiver_id: activeUser.value.id,
      content: res.data.filename, // Gửi kèm tên file gốc để hiển thị nút download cho đẹp
      message_type: res.data.message_type,
      file_url: res.data.file_url
    }

    ws.send(JSON.stringify(payload))
    fileInput.value.value = '' // Reset input file
  } catch (err) {
    alert('Lỗi tải tệp tin lên máy chủ!')
    console.error(err)
  }
}

// Định dạng thời gian hiển thị gọn gàng
const formatTime = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

// Mở tab mới xem ảnh phóng to full HD
const openImageWindow = (url) => {
  window.open(url, '_blank')
}

// Đăng xuất xóa bộ nhớ
const handleLogout = () => {
  if (ws) ws.close()
  localStorage.clear()
  router.push('/login')
}

onMounted(() => {
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) ws.close()
})
</script>

<style scoped>
/* Tùy biến thanh cuộn mượt mà kiểu tối giản cho các khu vực Chat */
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #475569;
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
  background: #db2777;
}
</style>