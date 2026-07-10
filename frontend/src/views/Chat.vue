<template>
  <div class="flex h-screen bg-[#040b16] text-[#eaf6ff] overflow-hidden">

    <!-- Sidebar -->
    <div class="w-80 bg-[#081527] border-r border-[#1f3a5c] flex flex-col shrink-0">
      <div class="p-4 border-b border-[#1f3a5c] flex justify-between items-center bg-[#0d1f38]">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-lg shrink-0 shadow-lg shadow-cyan-500/20">
            🌊
          </div>
          <div>
            <h2 class="font-display font-bold text-base text-[#eaf6ff] leading-tight">{{ myUsername }}</h2>
            <span class="text-[11px] text-[#7d97b8] capitalize">Quyền: {{ myRole }}</span>
          </div>
        </div>
        <div class="flex gap-2">
          <router-link v-if="myRole === 'admin'" to="/admin" class="bg-[#14304f] hover:bg-[#1f3a5c] text-cyan-300 text-xs px-2.5 py-1.5 rounded-lg transition-colors border border-[#1f3a5c]">
            🔧 Admin
          </router-link>
          <button @click="handleLogout" class="bg-rose-950/60 hover:bg-rose-900/60 text-rose-300 text-xs px-2.5 py-1.5 rounded-lg transition-colors border border-rose-500/20">
            Thoát
          </button>
        </div>
      </div>

      <div class="p-3 border-b border-[#1f3a5c] bg-[#040b16]">
        <div class="relative">
          <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[#4a6180] text-sm">🔍</span>
          <input
            v-model="searchQuery"
            @input="searchUsers"
            type="text"
            placeholder="Tìm bạn bè hoặc hiển thị chat gần đây..."
            class="w-full bg-[#0d1f38] border border-[#1f3a5c] rounded-lg pl-9 pr-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400/50 transition-all text-[#eaf6ff] placeholder-[#4a6180]"
          />
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-2 space-y-1">
        <div v-if="displayUsers.length === 0" class="text-center text-[#4a6180] text-xs py-10">
          {{ searchQuery ? 'Không tìm thấy ai trên sóng.' : 'Chưa có cuộc trò chuyện nào gần đây.' }}
        </div>
        <button
          v-for="user in displayUsers"
          :key="user.id"
          @click="selectUser(user)"
          :class="[
            'w-full text-left p-3 rounded-xl flex items-center gap-3 transition-all group',
            activeUser?.id === user.id
              ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-md shadow-cyan-500/20'
              : 'hover:bg-[#14304f] bg-[#0d1f38]/60 text-[#eaf6ff]'
          ]"
        >
          <div
            class="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0"
            :style="{ background: avatarColor(user.username) }"
          >
            {{ initial(user.username) }}
          </div>
          <div class="min-w-0 flex-1">
            <p class="font-medium truncate">{{ user.username }}</p>
            <span :class="['text-[10px] capitalize', activeUser?.id === user.id ? 'text-white/70' : 'text-[#7d97b8]']">
              {{ user.role }}
            </span>
          </div>
        </button>
      </div>
    </div>

    <!-- Main chat panel -->
    <div class="flex-1 flex flex-col bg-[#040b16]">
      <template v-if="activeUser">
        <div class="p-4 border-b border-[#1f3a5c] bg-[#0d1f38] flex items-center shadow-md justify-between shrink-0">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-[#14304f] flex items-center justify-center text-lg border border-[#1f3a5c]">👤</div>
            <div>
              <h3 class="font-display font-bold text-[#eaf6ff] text-sm">{{ activeUser.username }}</h3>
              <p class="text-xs text-[#5eead4] flex items-center gap-2">
                <span class="sonar"></span>
                Đang bắt sóng (real-time)
              </p>
            </div>
          </div>
          <span class="text-[11px] text-[#7d97b8] bg-[#081527] px-3 py-1.5 rounded-full border border-[#1f3a5c]">
            ⏳ Tin nhắn tự hủy sau 60 phút
          </span>
        </div>

        <div ref="messageContainer" class="flex-1 overflow-y-auto p-4 space-y-4 bg-[#040b16]">
          <div
            v-for="msg in filteredMessages"
            :key="msg.id"
            :class="[
              'flex flex-col max-w-[70%] rounded-2xl p-3 shadow-md relative group',
              msg.sender_id === myId
                ? 'ml-auto bg-gradient-to-br from-blue-600 to-cyan-500 text-white rounded-tr-sm'
                : 'mr-auto bg-[#0d1f38] text-[#eaf6ff] border border-[#1f3a5c] rounded-tl-sm'
            ]"
          >
            <p v-if="msg.message_type === 'text'" class="text-sm whitespace-pre-wrap break-words">{{ msg.content }}</p>

            <div v-else-if="msg.message_type === 'image'" class="space-y-1">
              <img :src="apiBaseUrl + msg.file_url" class="max-w-xs max-h-48 rounded-lg object-cover cursor-pointer border border-black/10" alt="Hình ảnh" @click="openImageWindow(apiBaseUrl + msg.file_url)"/>
              <a :href="apiBaseUrl + msg.file_url" download class="block text-xs underline text-cyan-200 hover:text-white mt-1">📥 Tải ảnh gốc</a>
            </div>

            <div v-else-if="msg.message_type === 'file'" class="flex items-center gap-3 bg-black/20 p-2.5 rounded-lg border border-white/10">
              <span class="text-2xl">📁</span>
              <div class="overflow-hidden">
                <p class="text-xs font-semibold truncate max-w-[180px]">{{ msg.content }}</p>
                <a :href="apiBaseUrl + msg.file_url" download class="text-xs text-cyan-200 underline hover:text-white font-medium">Click để tải xuống máy</a>
              </div>
            </div>

            <div class="flex items-center justify-between mt-1.5 gap-4">
              <span class="text-[10px] opacity-60">{{ formatTime(msg.created_at) }}</span>
              <span class="text-[10px] font-mono font-bold bg-black/25 px-1.5 py-0.5 rounded text-amber-300 shadow-inner">
                {{ getCountdown(msg.created_at) }}
              </span>
            </div>
          </div>
        </div>

        <div class="p-4 border-t border-[#1f3a5c] bg-[#0d1f38]/80 backdrop-blur flex items-center gap-3 shrink-0">
          <button @click="$refs.fileInput.click()" class="bg-[#14304f] hover:bg-[#1f3a5c] text-lg text-cyan-200 p-2.5 rounded-lg transition-colors border border-[#1f3a5c]" title="Gửi File hoặc Hình ảnh">
            📎
          </button>
          <input type="file" ref="fileInput" @change="handleFileUpload" class="hidden" />

          <input
            v-model="newMessage"
            @keyup.enter="sendTextMessage"
            type="text"
            placeholder="Nhập nội dung tin nhắn..."
            class="flex-1 bg-[#040b16] border border-[#1f3a5c] rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400/50 text-[#eaf6ff] placeholder-[#4a6180] transition-all"
          />

          <button @click="sendTextMessage" class="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 font-bold px-5 py-3 rounded-lg shadow-md shadow-cyan-500/20 transition-all text-sm text-white">
            Gửi
          </button>
        </div>
      </template>

      <template v-else>
        <div class="flex-1 flex flex-col items-center justify-center text-[#4a6180] relative overflow-hidden">
          <div class="moon-glow w-96 h-96 top-1/4 left-1/2 -translate-x-1/2"></div>
          <span class="text-6xl mb-4 relative z-10">🌊</span>
          <h2 class="font-display text-xl font-bold text-[#7d97b8] relative z-10">LuNu Messenger</h2>
          <p class="text-sm mt-1 text-[#4a6180] relative z-10">Hãy tìm kiếm một tài khoản ở thanh bên trái để bắt đầu trò chuyện real-time.</p>
        </div>
      </template>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const wsBaseUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

const router = useRouter()

const myUsername = ref(localStorage.getItem('username') || '')
const myRole = ref(localStorage.getItem('user_role') || 'user')
const myId = ref(0) 

const searchQuery = ref('')
const searchResults = ref([])
const recentChats = ref([]) 
const activeUser = ref(null)
const newMessage = ref('')
const allMessages = ref([]) 
const messageContainer = ref(null)
const fileInput = ref(null)

const currentTime = ref(Date.now()) 
let timerInterval = null
let ws = null

// Hàm trợ thủ xử lý múi giờ: Ép trình duyệt hiểu đây là chuẩn UTC bằng cách thêm chữ 'Z'
const parseUTCDate = (isoString) => {
  if (!isoString) return new Date()
  return new Date(isoString.endsWith('Z') ? isoString : isoString + 'Z')
}

const displayUsers = computed(() => {
  return searchQuery.value.trim() ? searchResults.value : recentChats.value
})

const filteredMessages = computed(() => {
  if (!activeUser.value) return []
  return allMessages.value.filter(msg => 
    (msg.sender_id === myId.value && msg.receiver_id === activeUser.value.id) ||
    (msg.sender_id === activeUser.value.id && msg.receiver_id === myId.value)
  )
})

const scrollToBottom = async () => {
  await nextTick()
  if (messageContainer.value) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  }
}

const fetchRecentChats = async () => {
  try {
    const res = await api.get('/chat/recent')
    recentChats.value = res.data
  } catch (err) {
    console.error('Lỗi lấy danh sách chat gần đây:', err)
  }
}

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

const selectUser = async (user) => {
  activeUser.value = user
  try {
    const res = await api.get(`/chat/history/${user.id}`)
    
    if (res.data.length > 0) {
      const sampleMsg = res.data[0]
      myId.value = sampleMsg.sender_id === user.id ? sampleMsg.receiver_id : sampleMsg.sender_id
    }
    
    allMessages.value = res.data
    scrollToBottom()
  } catch (err) {
    console.error('Không thể lấy lịch sử chat:', err)
  }
}

const connectWebSocket = () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  ws = new WebSocket(`${wsBaseUrl}/chat/ws?token=${token}`)

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    
    if (!allMessages.value.some(m => m.id === data.id)) {
      allMessages.value.push(data)
    }
    
    fetchRecentChats()
    scrollToBottom()
  }

  ws.onclose = () => {
    setTimeout(connectWebSocket, 3000) 
  }
}

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

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file || !activeUser.value || !ws) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await api.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    const payload = {
      receiver_id: activeUser.value.id,
      content: res.data.filename, 
      message_type: res.data.message_type,
      file_url: res.data.file_url
    }

    ws.send(JSON.stringify(payload))
    fileInput.value.value = '' 
  } catch (err) {
    alert('Lỗi tải tệp tin lên máy chủ!')
  }
}

const formatTime = (isoString) => {
  const date = parseUTCDate(isoString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const getCountdown = (isoString) => {
  const created = parseUTCDate(isoString).getTime()
  const expire = created + 60 * 60 * 1000 
  const diff = expire - currentTime.value

  if (diff <= 0) return 'Đang bốc hơi...'

  const mins = Math.floor(diff / 60000)
  const secs = Math.floor((diff % 60000) / 1000)
  return `⏳ ${mins}p ${secs}s`
}

const openImageWindow = (url) => {
  window.open(url, '_blank')
}

const handleLogout = () => {
  if (ws) ws.close()
  if (timerInterval) clearInterval(timerInterval)
  localStorage.clear()
  router.push('/login')
}

onMounted(() => {
  connectWebSocket()
  fetchRecentChats()
  
  timerInterval = setInterval(() => {
    currentTime.value = Date.now()
    
    const originalLength = allMessages.value.length
    allMessages.value = allMessages.value.filter(msg => {
      const expire = parseUTCDate(msg.created_at).getTime() + 60 * 60 * 1000
      return expire > currentTime.value
    })
    
    if (originalLength > allMessages.value.length) {
      fetchRecentChats()
    }
  }, 1000)
})

onUnmounted(() => {
  if (ws) ws.close()
  if (timerInterval) clearInterval(timerInterval)
})
</script>

<style scoped>
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #1f3a5c;
  border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
  background: #22d3ee;
}
</style>