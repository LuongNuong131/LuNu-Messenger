<template>
  <div class="relative min-h-screen bg-[#040b16] text-[#eaf6ff] overflow-hidden">

    <!-- Ánh trăng nền -->
    <div class="moon-glow w-[520px] h-[520px] -top-52 -right-40 pointer-events-none"></div>
    <div class="moon-glow w-[380px] h-[380px] -bottom-40 -left-32 pointer-events-none" style="animation-delay: 2s;"></div>

    <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 py-8">

      <!-- Header -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6 bg-[#0d1f38]/60 backdrop-blur-xl border border-cyan-400/20 p-6 rounded-2xl shadow-[0_0_60px_-15px_rgba(34,211,238,0.2)]">
        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-2xl shadow-lg shadow-cyan-500/30 shrink-0">
            ⚓
          </div>
          <div>
            <h1 class="font-display text-2xl sm:text-3xl font-bold bg-gradient-to-r from-cyan-300 via-blue-300 to-cyan-200 bg-clip-text text-transparent">
              Trung Tâm Chỉ Huy
            </h1>
            <p class="text-sm text-[#7d97b8] mt-0.5">Quyền lực tối cao dành riêng cho Admin</p>
          </div>
        </div>
        <router-link
          to="/"
          class="bg-[#14304f] hover:bg-[#1f3a5c] text-cyan-200 px-4 py-2.5 rounded-lg transition-colors border border-[#1f3a5c] text-sm font-semibold shrink-0"
        >
          ⬅ Quay lại Chat
        </router-link>
      </div>

      <!-- Thống kê nhanh -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div class="bg-[#0d1f38]/60 border border-[#1f3a5c] rounded-2xl p-5 flex items-center gap-4">
          <div class="w-11 h-11 rounded-xl bg-[#14304f] border border-[#1f3a5c] flex items-center justify-center text-xl shrink-0">🐚</div>
          <div>
            <p class="text-2xl font-bold font-display text-[#eaf6ff]">{{ users.length }}</p>
            <p class="text-xs text-[#7d97b8]">Tổng tài khoản</p>
          </div>
        </div>
        <div class="bg-[#0d1f38]/60 border border-[#1f3a5c] rounded-2xl p-5 flex items-center gap-4">
          <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-xl shrink-0 shadow-md shadow-cyan-500/20">👑</div>
          <div>
            <p class="text-2xl font-bold font-display text-[#eaf6ff]">{{ adminCount }}</p>
            <p class="text-xs text-[#7d97b8]">Quản trị viên</p>
          </div>
        </div>
        <div class="bg-[#0d1f38]/60 border border-[#1f3a5c] rounded-2xl p-5 flex items-center gap-4">
          <div class="w-11 h-11 rounded-xl bg-[#14304f] border border-[#1f3a5c] flex items-center justify-center text-xl shrink-0">👤</div>
          <div>
            <p class="text-2xl font-bold font-display text-[#eaf6ff]">{{ users.length - adminCount }}</p>
            <p class="text-xs text-[#7d97b8]">Người dùng thường</p>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex gap-3 mb-6">
        <button
          @click="activeTab = 'users'"
          :class="[
            'px-5 py-2.5 rounded-xl font-semibold text-sm transition-all border',
            activeTab === 'users'
              ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white border-transparent shadow-md shadow-cyan-500/20'
              : 'bg-[#0d1f38]/60 text-[#7d97b8] border-[#1f3a5c] hover:bg-[#14304f] hover:text-[#eaf6ff]'
          ]"
        >
          👥 Quản lý Người dùng
        </button>
        <button
          @click="activeTab = 'database'"
          :class="[
            'px-5 py-2.5 rounded-xl font-semibold text-sm transition-all border',
            activeTab === 'database'
              ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white border-transparent shadow-md shadow-cyan-500/20'
              : 'bg-[#0d1f38]/60 text-[#7d97b8] border-[#1f3a5c] hover:bg-[#14304f] hover:text-[#eaf6ff]'
          ]"
        >
          🗄️ Cơ sở dữ liệu
        </button>
      </div>

      <!-- Tab: Người dùng -->
      <div v-if="activeTab === 'users'" class="bg-[#0d1f38]/60 backdrop-blur-xl rounded-2xl border border-[#1f3a5c] overflow-hidden">
        <div class="p-4 border-b border-[#1f3a5c] flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
          <h2 class="text-base font-bold font-display text-[#eaf6ff]">Danh sách tài khoản hệ thống</h2>
          <div class="flex gap-2 items-center">
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-[#4a6180] text-sm">🔍</span>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Tìm theo username..."
                class="bg-[#081527] border border-[#1f3a5c] rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400/50 focus:border-cyan-400/50 text-[#eaf6ff] placeholder-[#4a6180] transition-all w-48"
              />
            </div>
            <button
              @click="fetchUsers"
              class="text-sm bg-[#14304f] hover:bg-[#1f3a5c] px-3 py-2 rounded-lg text-cyan-200 transition-colors border border-[#1f3a5c] font-medium shrink-0"
            >
              🔄 Làm mới
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead class="bg-[#081527] text-[#7d97b8] uppercase text-xs tracking-wide">
              <tr>
                <th class="px-6 py-3.5 font-semibold">ID</th>
                <th class="px-6 py-3.5 font-semibold">Username</th>
                <th class="px-6 py-3.5 font-semibold">Quyền</th>
                <th class="px-6 py-3.5 font-semibold">Ngày tạo</th>
                <th class="px-6 py-3.5 font-semibold text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[#1f3a5c]">
              <tr v-if="usersLoading">
                <td colspan="5" class="px-6 py-10 text-center text-[#7d97b8]">
                  <span class="inline-flex items-center gap-2">
                    <span class="w-4 h-4 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin"></span>
                    Đang tải dữ liệu...
                  </span>
                </td>
              </tr>
              <tr v-else-if="filteredUsers.length === 0">
                <td colspan="5" class="px-6 py-10 text-center text-[#4a6180] italic">
                  Không tìm thấy tài khoản nào khớp với "{{ searchQuery }}".
                </td>
              </tr>
              <tr
                v-for="user in filteredUsers"
                :key="user.id"
                class="hover:bg-[#14304f]/40 transition-colors"
              >
                <td class="px-6 py-4 text-[#7d97b8]">{{ user.id }}</td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div
                      class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0"
                      :style="{ background: avatarColor(user.username) }"
                    >
                      {{ initial(user.username) }}
                    </div>
                    <span class="font-semibold text-[#eaf6ff]">{{ user.username }}</span>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <span
                    :class="[
                      'px-2.5 py-1 rounded-full text-[11px] font-bold uppercase border',
                      user.role === 'admin'
                        ? 'bg-cyan-400/10 text-cyan-300 border-cyan-400/30'
                        : 'bg-[#14304f] text-[#7d97b8] border-[#1f3a5c]'
                    ]"
                  >
                    {{ user.role }}
                  </span>
                </td>
                <td class="px-6 py-4 text-[#7d97b8]">{{ formatDate(user.created_at) }}</td>
                <td class="px-6 py-4 text-center">
                  <template v-if="user.role !== 'admin'">
                    <button
                      @click="promoteUser(user.id, user.username)"
                      class="bg-amber-400/10 text-amber-300 hover:bg-amber-400 hover:text-[#081527] border border-amber-400/30 px-3 py-1.5 rounded-lg transition-all text-xs font-bold mr-2"
                    >
                      Cấp Admin
                    </button>
                    <button
                      @click="deleteUser(user.id, user.username)"
                      class="bg-rose-500/10 text-rose-300 hover:bg-rose-500 hover:text-white border border-rose-500/30 px-3 py-1.5 rounded-lg transition-all text-xs font-bold"
                    >
                      Xóa User
                    </button>
                  </template>
                  <span v-else class="text-[#4a6180] text-xs italic">Quyền lực tối cao</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab: Database -->
      <div v-if="activeTab === 'database'" class="flex flex-col md:flex-row gap-6">
        <div class="w-full md:w-1/4 bg-[#0d1f38]/60 backdrop-blur-xl rounded-2xl border border-[#1f3a5c] overflow-hidden h-fit">
          <div class="p-4 bg-[#081527] border-b border-[#1f3a5c]">
            <h2 class="text-sm font-bold font-display text-cyan-300">📋 Danh sách Bảng</h2>
          </div>
          <div class="p-2 space-y-1">
            <button
              v-for="table in tables"
              :key="table"
              @click="fetchTableData(table)"
              :class="[
                'w-full text-left px-4 py-3 rounded-xl text-sm font-medium transition-all',
                selectedTable === table
                  ? 'bg-gradient-to-r from-blue-600 to-cyan-500 text-white shadow-md shadow-cyan-500/20'
                  : 'hover:bg-[#14304f] text-[#7d97b8] hover:text-[#eaf6ff]'
              ]"
            >
              🗃️ {{ table }}
            </button>
            <p v-if="tables.length === 0" class="text-xs text-[#4a6180] italic px-4 py-3">Không có bảng nào.</p>
          </div>
        </div>

        <div class="w-full md:w-3/4 bg-[#0d1f38]/60 backdrop-blur-xl rounded-2xl border border-[#1f3a5c] overflow-hidden">
          <div class="p-4 bg-[#081527] border-b border-[#1f3a5c] flex justify-between items-center">
            <h2 class="text-sm font-bold font-display text-[#eaf6ff]">
              Dữ liệu bảng: <span class="text-cyan-300">{{ selectedTable || 'Chưa chọn' }}</span>
            </h2>
            <span v-if="tableData.rows.length" class="text-xs text-[#7d97b8]">Hiển thị tối đa 100 dòng</span>
          </div>

          <div class="overflow-x-auto p-4" v-if="selectedTable">
            <div v-if="tableLoading" class="flex items-center justify-center gap-2 text-[#7d97b8] py-16">
              <span class="w-4 h-4 border-2 border-cyan-400/30 border-t-cyan-400 rounded-full animate-spin"></span>
              Đang tải bảng dữ liệu...
            </div>
            <table v-else class="w-full text-left text-sm border-collapse">
              <thead class="bg-[#081527] text-[#7d97b8]">
                <tr>
                  <th v-for="col in tableData.columns" :key="col" class="px-4 py-3 border border-[#1f3a5c] font-semibold uppercase text-xs">
                    {{ col }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in tableData.rows" :key="index" class="hover:bg-[#14304f]/40 transition-colors">
                  <td v-for="col in tableData.columns" :key="col" class="px-4 py-3 border border-[#1f3a5c] max-w-[200px] truncate text-[#eaf6ff]">
                    {{ row[col] !== null ? row[col] : 'NULL' }}
                  </td>
                </tr>
                <tr v-if="tableData.rows.length === 0">
                  <td :colspan="tableData.columns.length" class="text-center py-8 text-[#4a6180] italic">
                    Bảng này hiện chưa có dữ liệu nào.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="flex flex-col items-center justify-center py-20 text-[#4a6180]">
            <span class="text-5xl mb-3">🗄️</span>
            <p>Vui lòng chọn một bảng bên trái để xem dữ liệu thô.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Toasts -->
    <div class="fixed bottom-6 right-6 z-50 flex flex-col gap-2 w-80 max-w-[calc(100vw-3rem)]">
      <transition-group name="toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="[
            'rounded-xl px-4 py-3 shadow-lg border backdrop-blur-xl flex items-center gap-3 text-sm font-medium',
            toast.type === 'success'
              ? 'bg-[#0d1f38]/90 border-cyan-400/30 text-[#eaf6ff]'
              : 'bg-rose-950/80 border-rose-500/30 text-rose-200'
          ]"
        >
          <span class="text-lg shrink-0">{{ toast.type === 'success' ? '✅' : '⚠️' }}</span>
          <span>{{ toast.message }}</span>
        </div>
      </transition-group>
    </div>

    <!-- Confirm modal -->
    <transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="relative z-10 bg-[#0d1f38] border border-cyan-400/20 rounded-2xl shadow-[0_0_60px_-15px_rgba(34,211,238,0.3)] w-full max-w-sm p-6">
          <h3 class="font-display text-lg font-bold text-[#eaf6ff] mb-2">{{ confirmModal.title }}</h3>
          <p class="text-sm text-[#7d97b8] mb-6 leading-relaxed">{{ confirmModal.message }}</p>
          <div class="flex justify-end gap-3">
            <button
              @click="handleConfirm(false)"
              class="px-4 py-2 rounded-lg text-sm font-semibold bg-[#14304f] hover:bg-[#1f3a5c] text-[#eaf6ff] transition-colors border border-[#1f3a5c]"
            >
              Hủy
            </button>
            <button
              @click="handleConfirm(true)"
              :class="[
                'px-4 py-2 rounded-lg text-sm font-bold transition-all',
                confirmModal.danger
                  ? 'bg-rose-600 hover:bg-rose-500 text-white shadow-md shadow-rose-500/20'
                  : 'bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white shadow-md shadow-cyan-500/20'
              ]"
            >
              {{ confirmModal.confirmLabel }}
            </button>
          </div>
        </div>
      </div>
    </transition>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const activeTab = ref('users')
const users = ref([])
const usersLoading = ref(false)
const searchQuery = ref('')

const tables = ref([])
const selectedTable = ref(null)
const tableData = ref({ columns: [], rows: [] })
const tableLoading = ref(false)

const adminCount = computed(() => users.value.filter(u => u.role === 'admin').length)

const filteredUsers = computed(() => {
  if (!searchQuery.value.trim()) return users.value
  const q = searchQuery.value.trim().toLowerCase()
  return users.value.filter(u => u.username.toLowerCase().includes(q))
})

// Bảng màu avatar theo phong cách đại dương, chọn theo hash tên user cho ổn định
const avatarPalette = [
  'linear-gradient(135deg,#3b82f6,#22d3ee)',
  'linear-gradient(135deg,#0891b2,#38bdf8)',
  'linear-gradient(135deg,#6366f1,#22d3ee)',
  'linear-gradient(135deg,#0ea5e9,#5eead4)',
  'linear-gradient(135deg,#2563eb,#67e8f9)'
]
const avatarColor = (username) => {
  let hash = 0
  for (let i = 0; i < username.length; i++) hash = username.charCodeAt(i) + ((hash << 5) - hash)
  return avatarPalette[Math.abs(hash) % avatarPalette.length]
}
const initial = (username) => username?.charAt(0)?.toUpperCase() || '?'

// ------- Toasts -------
const toasts = ref([])
let toastId = 0
const addToast = (message, type = 'success') => {
  const id = toastId++
  toasts.value.push({ id, message, type })
  setTimeout(() => {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }, 3000)
}

// ------- Confirm modal (dùng Promise thay cho window.confirm) -------
const confirmModal = ref({ show: false, title: '', message: '', confirmLabel: 'Xác nhận', danger: false, resolve: null })

const openConfirm = ({ title, message, confirmLabel = 'Xác nhận', danger = false }) => {
  return new Promise((resolve) => {
    confirmModal.value = { show: true, title, message, confirmLabel, danger, resolve }
  })
}

const handleConfirm = (result) => {
  confirmModal.value.resolve(result)
  confirmModal.value.show = false
}

// ------- API calls -------
const fetchUsers = async () => {
  usersLoading.value = true
  try {
    const res = await api.get('/admin/users')
    users.value = res.data
  } catch (error) {
    console.error('Lỗi lấy danh sách user:', error)
    addToast('Không thể tải danh sách người dùng.', 'error')
  } finally {
    usersLoading.value = false
  }
}

const deleteUser = async (id, username) => {
  const ok = await openConfirm({
    title: 'Xóa tài khoản?',
    message: `Bạn có chắc chắn muốn xóa vĩnh viễn tài khoản "${username}"? Hành động này không thể hoàn tác.`,
    confirmLabel: 'Xóa vĩnh viễn',
    danger: true
  })
  if (!ok) return

  try {
    await api.delete(`/admin/users/${id}`)
    addToast(`Đã xóa tài khoản "${username}".`, 'success')
    fetchUsers()
  } catch (error) {
    console.error('Lỗi xóa user:', error)
    addToast('Xóa thất bại, vui lòng thử lại.', 'error')
  }
}

const promoteUser = async (id, username) => {
  const ok = await openConfirm({
    title: 'Thăng cấp Admin?',
    message: `Bạn có chắc chắn muốn thăng cấp "${username}" làm Admin hệ thống không?`,
    confirmLabel: 'Thăng cấp'
  })
  if (!ok) return

  try {
    await api.put(`/admin/users/${id}/promote`)
    addToast(`Đã thăng cấp "${username}" thành Admin.`, 'success')
    fetchUsers()
  } catch (error) {
    console.error('Lỗi cấp quyền:', error)
    addToast('Thăng cấp thất bại!', 'error')
  }
}

const fetchTables = async () => {
  try {
    const res = await api.get('/admin/db/tables')
    tables.value = res.data
  } catch (error) {
    console.error('Lỗi lấy danh sách bảng:', error)
    addToast('Không thể tải danh sách bảng.', 'error')
  }
}

const fetchTableData = async (tableName) => {
  selectedTable.value = tableName
  tableData.value = { columns: [], rows: [] }
  tableLoading.value = true
  try {
    const res = await api.get(`/admin/db/table/${tableName}`)
    tableData.value = res.data
  } catch (error) {
    console.error('Lỗi lấy dữ liệu bảng:', error)
    addToast('Không thể tải dữ liệu bảng.', 'error')
  } finally {
    tableLoading.value = false
  }
}

const formatDate = (isoString) => {
  if (!isoString) return ''
  const date = new Date(isoString)
  return date.toLocaleString('vi-VN')
}

onMounted(() => {
  fetchUsers()
  fetchTables()
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

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(40px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(40px) scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>