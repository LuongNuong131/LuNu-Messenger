<template>
  <div class="relative flex h-[100dvh] bg-[#040b16] text-[#eaf6ff] overflow-hidden">

    <!-- Caustics — tín hiệu ánh sáng xuyên nước, phủ toàn màn hình -->
    <div class="caustics-layer"></div>

    <!-- Sidebar -->
    <div
      :class="[
        'relative z-10 w-full sm:w-80 bg-[#081527]/95 backdrop-blur-xl border-r border-[#1f3a5c] flex-col shrink-0',
        activeUser ? 'hidden sm:flex' : 'flex'
      ]"
    >
      <div class="hairline-glow relative p-4 border-b border-[#1f3a5c] flex justify-between items-center bg-gradient-to-b from-[#0d1f38] to-[#0a1a2e]">
        <div class="flex items-center gap-3 min-w-0">
          <div class="relative shrink-0">
            <div
              class="w-11 h-11 rounded-2xl flex items-center justify-center text-sm font-bold text-white shadow-lg shadow-cyan-500/25 ring-1 ring-white/10"
              :style="{ background: avatarColor(myUsername) }"
            >
              {{ initial(myUsername) }}
            </div>
            <span
              class="absolute -bottom-0.5 -right-0.5 w-3 h-3 rounded-full border-2 border-[#0d1f38]"
              :class="wsConnected ? 'bg-[#5eead4]' : 'bg-[#fb7185]'"
            ></span>
          </div>
          <div class="min-w-0">
            <h2 class="font-display font-bold text-base text-[#eaf6ff] leading-tight truncate">{{ myUsername }}</h2>
            <span class="text-[11px] text-[#7d97b8] flex items-center gap-1.5">
              {{ wsConnected ? 'Đang bắt sóng' : 'Mất kết nối, đang thử lại...' }}
            </span>
          </div>
        </div>
        <div class="flex gap-2 shrink-0">
          <router-link v-if="myRole === 'admin'" to="/admin" class="bg-[#14304f] hover:bg-[#1f3a5c] text-cyan-300 text-xs w-8 h-8 flex items-center justify-center rounded-xl transition-colors border border-[#1f3a5c] hover-lift" title="Trang quản trị">
            🔧
          </router-link>
          <button @click="handleLogout" class="bg-rose-950/50 hover:bg-rose-900/60 text-rose-300 text-xs px-3 h-8 rounded-xl transition-colors border border-rose-500/20 font-medium">
            Thoát
          </button>
        </div>
      </div>

      <div class="p-3 border-b border-[#1f3a5c] bg-[#040b16]/60">
        <div class="glow-ring relative rounded-xl">
          <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-[#4a6180] text-sm">🔍</span>
          <input
            v-model="searchQuery"
            @input="searchUsers"
            type="text"
            placeholder="Tìm bạn bè hoặc chat gần đây..."
            class="w-full bg-[#0d1f38] border border-[#1f3a5c] rounded-xl pl-9 pr-3 py-2.5 text-sm focus:outline-none focus:border-cyan-400/50 transition-all text-[#eaf6ff] placeholder-[#4a6180]"
          />
        </div>
      </div>

      <div class="flex-1 overflow-y-auto p-2.5 space-y-1">
        <div v-if="displayUsers.length === 0" class="text-center text-[#4a6180] text-xs py-12 px-6 leading-relaxed">
          {{ searchQuery ? 'Không tìm thấy ai trên sóng.' : 'Chưa có cuộc trò chuyện nào gần đây. Thử tìm một người bạn ở ô trên nhé.' }}
        </div>
        <button
          v-for="user in displayUsers"
          :key="user.id"
          @click="selectUser(user)"
          :class="[
            'relative w-full text-left p-2.5 rounded-2xl flex items-center gap-3 transition-all duration-200 group',
            activeUser?.id === user.id
              ? 'bg-gradient-to-r from-blue-600/90 to-cyan-500/90 text-white shadow-lg shadow-cyan-500/20'
              : 'hover:bg-[#0d1f38] text-[#eaf6ff]'
          ]"
        >
          <span
            v-if="activeUser?.id === user.id"
            class="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-1 rounded-full bg-[#5eead4]"
          ></span>
          <div
            class="w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0 ring-1 ring-white/10"
            :style="{ background: avatarColor(user.username) }"
          >
            {{ initial(user.username) }}
          </div>
          <div class="min-w-0 flex-1">
            <p class="font-medium truncate text-sm">{{ user.username }}</p>
            <span :class="['text-[10px] capitalize', activeUser?.id === user.id ? 'text-white/70' : 'text-[#7d97b8]']">
              {{ user.role }}
            </span>
          </div>
        </button>
      </div>
    </div>

    <!-- Main chat panel -->
    <div
      :class="['relative z-10 flex-1 flex-col bg-transparent relative', activeUser ? 'flex' : 'hidden sm:flex']"
      @dragover.prevent="isDragging = true"
      @dragenter.prevent="isDragging = true"
      @dragleave.prevent="onDragLeave"
      @drop.prevent="onDrop"
    >
      <template v-if="activeUser">
        <div class="hairline-glow relative p-3 sm:p-4 border-b border-[#1f3a5c] bg-[#0d1f38]/90 backdrop-blur-xl flex items-center justify-between shrink-0 gap-3">
          <div class="flex items-center gap-3 min-w-0">
            <button @click="activeUser = null" class="sm:hidden p-1.5 -ml-1 rounded-lg hover:bg-[#14304f] text-[#7d97b8] shrink-0" title="Quay lại danh sách">
              ←
            </button>
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0 ring-1 ring-white/10"
              :style="{ background: avatarColor(activeUser.username) }"
            >
              {{ initial(activeUser.username) }}
            </div>
            <div class="min-w-0">
              <h3 class="font-display font-bold text-[#eaf6ff] text-sm truncate">{{ activeUser.username }}</h3>
              <p class="text-xs text-[#5eead4] flex items-center gap-2">
                <span class="sonar"></span>
                Đang bắt sóng (real-time)
              </p>
            </div>
          </div>
          <span class="hidden md:inline-flex text-[11px] text-[#7d97b8] bg-[#081527]/80 px-3 py-1.5 rounded-full border border-[#1f3a5c] shrink-0">
            ⏳ Tin nhắn tự hủy sau 60 phút
          </span>
        </div>

        <div
          ref="messageContainer"
          @scroll="onScroll"
          class="flex-1 overflow-y-auto p-3 sm:p-5 space-y-1 scroll-smooth"
        >
          <div v-if="historyLoading" class="flex items-center justify-center gap-2 text-[#7d97b8] py-16 text-sm">
            <span class="w-4 h-4 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin"></span>
            Đang tải lịch sử trò chuyện...
          </div>

          <div v-else-if="filteredMessages.length === 0" class="relative flex flex-col items-center justify-center text-[#4a6180] py-20 text-center gap-3">
            <div class="moon-glow w-72 h-72 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"></div>
            <span class="relative z-10 text-5xl">💬</span>
            <p class="relative z-10 text-sm max-w-xs">Chưa có tin nhắn nào. Hãy là người bắt sóng đầu tiên!</p>
          </div>

          <template v-for="(group, gIdx) in groupedMessages" :key="gIdx">
            <div class="flex justify-center my-4 sticky top-0 z-10">
              <span class="text-[10px] font-semibold text-[#7d97b8] bg-[#0d1f38]/90 backdrop-blur px-3 py-1 rounded-full border border-[#1f3a5c] shadow-sm">
                {{ group.label }}
              </span>
            </div>

            <div
              v-for="msg in group.items"
              :key="msg.id"
              :class="[
                'flex flex-col max-w-[85%] sm:max-w-[65%] rounded-3xl p-3.5 shadow-lg relative group mb-2.5',
                msg.sender_id === myId
                  ? 'msg-sheen ml-auto bg-gradient-to-br from-blue-600 to-cyan-500 text-white rounded-tr-md shadow-cyan-500/20'
                  : 'mr-auto bg-[#0d1f38]/95 text-[#eaf6ff] border border-[#1f3a5c] rounded-tl-md shadow-black/20'
              ]"
            >
              <p v-if="msg.message_type === 'text'" class="text-sm whitespace-pre-wrap break-words leading-relaxed">{{ msg.content }}</p>

              <div v-else-if="msg.message_type === 'image'" class="space-y-1.5">
                <img
                  :src="apiBaseUrl + msg.file_url"
                  class="max-w-[220px] sm:max-w-xs max-h-56 rounded-xl object-cover cursor-zoom-in border border-black/10"
                  alt="Hình ảnh"
                  loading="lazy"
                  @click="openLightbox(apiBaseUrl + msg.file_url)"
                />
                <a :href="apiBaseUrl + msg.file_url" download class="block text-xs underline text-cyan-200 hover:text-white mt-1">📥 Tải ảnh gốc</a>
              </div>

              <div v-else-if="msg.message_type === 'file'" class="flex items-center gap-3 bg-black/20 p-2.5 rounded-xl border border-white/10 min-w-[180px]">
                <span class="text-2xl shrink-0">📁</span>
                <div class="overflow-hidden">
                  <p class="text-xs font-semibold truncate max-w-[180px]">{{ msg.content }}</p>
                  <a :href="apiBaseUrl + msg.file_url" download class="text-xs text-cyan-200 underline hover:text-white font-medium">Click để tải xuống máy</a>
                </div>
              </div>

              <div class="flex items-center justify-between mt-1.5 gap-4">
                <span class="text-[10px] opacity-60">{{ formatTime(msg.created_at) }}</span>
                <span class="text-[10px] font-mono font-bold bg-black/25 px-1.5 py-0.5 rounded-full text-amber-300 shadow-inner shrink-0">
                  {{ getCountdown(msg.created_at) }}
                </span>
              </div>
            </div>
          </template>
        </div>

        <!-- Nút cuộn xuống cuối -->
        <transition name="fade-up">
          <button
            v-if="showScrollBtn"
            @click="scrollToBottom(true)"
            class="absolute right-4 sm:right-6 bottom-24 bg-[#14304f]/90 backdrop-blur hover:bg-[#1f3a5c] border border-cyan-400/30 text-cyan-200 w-10 h-10 rounded-full shadow-lg shadow-black/30 flex items-center justify-center transition-colors hover-lift"
            title="Cuộn xuống tin nhắn mới nhất"
          >
            ↓
          </button>
        </transition>

        <!-- Overlay kéo-thả file -->
        <transition name="fade-up">
          <div
            v-if="isDragging"
            class="absolute inset-0 z-20 bg-[#040b16]/85 backdrop-blur-sm border-2 border-dashed border-cyan-400/60 rounded-2xl m-2 flex flex-col items-center justify-center gap-2 pointer-events-none"
          >
            <span class="text-4xl">📤</span>
            <p class="text-cyan-200 font-semibold text-sm">Thả tệp vào đây để gửi</p>
          </div>
        </transition>

        <div class="p-3 sm:p-4 border-t border-[#1f3a5c] bg-[#0d1f38]/85 backdrop-blur-xl flex items-end gap-2 sm:gap-3 shrink-0">
          <button @click="$refs.fileInput.click()" class="bg-[#14304f] hover:bg-[#1f3a5c] text-lg text-cyan-200 w-11 h-11 flex items-center justify-center rounded-xl transition-colors border border-[#1f3a5c] shrink-0 hover-lift" title="Gửi File hoặc Hình ảnh">
            📎
          </button>
          <input type="file" ref="fileInput" @change="handleFileUpload" class="hidden" />

          <div class="glow-ring flex-1 rounded-2xl">
            <textarea
              v-model="newMessage"
              @keydown.enter.exact.prevent="sendTextMessage"
              @input="autoGrow"
              ref="textInput"
              rows="1"
              placeholder="Nhập nội dung tin nhắn... (Enter để gửi, Shift+Enter xuống dòng)"
              class="w-full bg-[#040b16] border border-[#1f3a5c] rounded-2xl px-4 py-3 text-sm focus:outline-none focus:border-cyan-400/50 text-[#eaf6ff] placeholder-[#4a6180] transition-all resize-none max-h-32 leading-relaxed"
            ></textarea>
          </div>

          <button
            @click="sendTextMessage"
            :disabled="!newMessage.trim()"
            class="bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 font-bold w-11 h-11 sm:w-auto sm:px-5 rounded-2xl shadow-lg shadow-cyan-500/20 transition-all text-sm text-white shrink-0 disabled:opacity-40 disabled:hover:from-blue-600 disabled:hover:to-cyan-500 disabled:cursor-not-allowed flex items-center justify-center gap-1.5"
          >
            <span class="hidden sm:inline">Gửi</span>
            <span aria-hidden="true">➤</span>
          </button>
        </div>

        <div v-if="uploadProgress !== null" class="absolute left-0 right-0 bottom-0 h-0.5 bg-[#1f3a5c]">
          <div class="h-full bg-gradient-to-r from-cyan-400 to-blue-400 transition-all" :style="{ width: uploadProgress + '%' }"></div>
        </div>
      </template>

      <template v-else>
        <div class="flex-1 flex flex-col items-center justify-center text-[#4a6180] relative overflow-hidden px-6">
          <div class="moon-glow w-96 h-96 top-1/4 left-1/2 -translate-x-1/2"></div>
          <span class="text-6xl mb-4 relative z-10">🌊</span>
          <h2 class="font-display text-xl font-bold text-[#7d97b8] relative z-10">LuNu Messenger</h2>
          <p class="text-sm mt-1 text-[#4a6180] relative z-10 text-center max-w-xs">Hãy tìm kiếm một tài khoản ở thanh bên trái để bắt đầu trò chuyện real-time.</p>
        </div>
      </template>
    </div>

    <!-- Lightbox ảnh -->
    <transition name="fade-up">
      <div
        v-if="lightboxUrl"
        class="fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4"
        @click="lightboxUrl = null"
      >
        <img :src="lightboxUrl" class="max-w-full max-h-full rounded-xl shadow-2xl" @click.stop />
        <button @click="lightboxUrl = null" class="absolute top-4 right-4 sm:top-6 sm:right-6 w-10 h-10 rounded-full bg-white/10 hover:bg-white/20 text-white flex items-center justify-center text-xl backdrop-blur">
          ✕
        </button>
        <a
          :href="lightboxUrl"
          download
          @click.stop
          class="absolute bottom-4 sm:bottom-6 bg-[#14304f] hover:bg-[#1f3a5c] border border-cyan-400/30 text-cyan-200 px-4 py-2 rounded-xl text-sm font-semibold"
        >
          📥 Tải ảnh gốc
        </a>
      </div>
    </transition>

    <!-- Toast lỗi upload -->
    <transition name="fade-up">
      <div v-if="uploadError" class="fixed bottom-6 right-6 z-50 bg-rose-950/90 border border-rose-500/30 text-rose-200 px-4 py-3 rounded-2xl shadow-lg text-sm max-w-xs backdrop-blur">
        ⚠️ {{ uploadError }}
      </div>
    </transition>

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
const textInput = ref(null)

const historyLoading = ref(false)
const wsConnected = ref(false)
const isDragging = ref(false)
const showScrollBtn = ref(false)
const lightboxUrl = ref(null)
const uploadProgress = ref(null)
const uploadError = ref('')

const currentTime = ref(Date.now())
let timerInterval = null
let ws = null
let dragCounter = 0

// Hàm trợ thủ xử lý múi giờ: Ép trình duyệt hiểu đây là chuẩn UTC bằng cách thêm chữ 'Z'
const parseUTCDate = (isoString) => {
  if (!isoString) return new Date()
  return new Date(isoString.endsWith('Z') ? isoString : isoString + 'Z')
}

// Bảng màu avatar theo phong cách đại dương, chọn theo hash tên user cho ổn định
const avatarPalette = [
  'linear-gradient(135deg,#3b82f6,#22d3ee)',
  'linear-gradient(135deg,#0891b2,#38bdf8)',
  'linear-gradient(135deg,#6366f1,#22d3ee)',
  'linear-gradient(135deg,#0ea5e9,#5eead4)',
  'linear-gradient(135deg,#2563eb,#67e8f9)'
]
const avatarColor = (username) => {
  if (!username) return avatarPalette[0]
  let hash = 0
  for (let i = 0; i < username.length; i++) hash = username.charCodeAt(i) + ((hash << 5) - hash)
  return avatarPalette[Math.abs(hash) % avatarPalette.length]
}
const initial = (username) => username?.charAt(0)?.toUpperCase() || '?'

const displayUsers = computed(() => {
  return searchQuery.value.trim() ? searchResults.value : recentChats.value
})

const filteredMessages = computed(() => {
  if (!activeUser.value) return []
  return allMessages.value
    .filter(msg =>
      (msg.sender_id === myId.value && msg.receiver_id === activeUser.value.id) ||
      (msg.sender_id === activeUser.value.id && msg.receiver_id === myId.value)
    )
    .sort((a, b) => parseUTCDate(a.created_at) - parseUTCDate(b.created_at))
})

// Gộp tin nhắn theo ngày để chèn dòng phân cách "Hôm nay / Hôm qua / dd-mm-yyyy"
const dateLabel = (date) => {
  const today = new Date()
  const yesterday = new Date()
  yesterday.setDate(today.getDate() - 1)
  const sameDay = (a, b) => a.toDateString() === b.toDateString()

  if (sameDay(date, today)) return 'Hôm nay'
  if (sameDay(date, yesterday)) return 'Hôm qua'
  return date.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

const groupedMessages = computed(() => {
  const groups = []
  for (const msg of filteredMessages.value) {
    const label = dateLabel(parseUTCDate(msg.created_at))
    const lastGroup = groups[groups.length - 1]
    if (lastGroup && lastGroup.label === label) {
      lastGroup.items.push(msg)
    } else {
      groups.push({ label, items: [msg] })
    }
  }
  return groups
})

const isNearBottom = () => {
  const el = messageContainer.value
  if (!el) return true
  return el.scrollHeight - el.scrollTop - el.clientHeight < 120
}

const onScroll = () => {
  showScrollBtn.value = !isNearBottom()
}

const scrollToBottom = async (force = false) => {
  await nextTick()
  if (messageContainer.value && (force || isNearBottom())) {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    showScrollBtn.value = false
  }
}

const autoGrow = () => {
  const el = textInput.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = Math.min(el.scrollHeight, 128) + 'px'
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
  historyLoading.value = true
  try {
    const res = await api.get(`/chat/history/${user.id}`)

    if (res.data.length > 0) {
      const sampleMsg = res.data[0]
      myId.value = sampleMsg.sender_id === user.id ? sampleMsg.receiver_id : sampleMsg.sender_id
    }

    allMessages.value = res.data
    scrollToBottom(true)
  } catch (err) {
    console.error('Không thể lấy lịch sử chat:', err)
  } finally {
    historyLoading.value = false
  }
}

const connectWebSocket = () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  ws = new WebSocket(`${wsBaseUrl}/chat/ws?token=${token}`)

  ws.onopen = () => {
    wsConnected.value = true
  }

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)

    if (!allMessages.value.some(m => m.id === data.id)) {
      allMessages.value.push(data)
    }

    fetchRecentChats()
    scrollToBottom()
  }

  ws.onclose = () => {
    wsConnected.value = false
    setTimeout(connectWebSocket, 3000)
  }

  ws.onerror = () => {
    wsConnected.value = false
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
  nextTick(() => autoGrow())
}

const uploadFile = async (file) => {
  if (!file || !activeUser.value || !ws) return

  const formData = new FormData()
  formData.append('file', file)
  uploadProgress.value = 0
  uploadError.value = ''

  try {
    const res = await api.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (evt) => {
        if (evt.total) uploadProgress.value = Math.round((evt.loaded / evt.total) * 100)
      }
    })

    const payload = {
      receiver_id: activeUser.value.id,
      content: res.data.filename,
      message_type: res.data.message_type,
      file_url: res.data.file_url
    }

    ws.send(JSON.stringify(payload))
  } catch (err) {
    uploadError.value = 'Lỗi tải tệp tin lên máy chủ, thử lại xem sao.'
    setTimeout(() => (uploadError.value = ''), 4000)
  } finally {
    uploadProgress.value = null
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  await uploadFile(file)
  fileInput.value.value = ''
}

const onDragLeave = () => {
  dragCounter--
  if (dragCounter <= 0) {
    isDragging.value = false
    dragCounter = 0
  }
}

const onDrop = async (event) => {
  isDragging.value = false
  dragCounter = 0
  const file = event.dataTransfer?.files?.[0]
  if (file) await uploadFile(file)
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

const openLightbox = (url) => {
  lightboxUrl.value = url
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

  window.addEventListener('dragover', (e) => e.preventDefault())

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

.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.2s ease;
}
.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>