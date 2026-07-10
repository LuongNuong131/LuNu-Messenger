<template>
  <div class="min-h-screen bg-slate-900 text-slate-100 p-6">
    <div class="max-w-6xl mx-auto flex justify-between items-center mb-8 bg-slate-800 p-4 rounded-xl shadow-lg border border-slate-700">
      <div>
        <h1 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-pink-500">
          ⚙️ Bảng Điều Khiển Quản Trị
        </h1>
        <p class="text-sm text-slate-400 mt-1">Quyền lực tối cao dành riêng cho Admin</p>
      </div>
      <router-link to="/" class="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded-lg transition-all shadow text-sm font-medium">
        ⬅ Quay lại Chat
      </router-link>
    </div>

    <div class="max-w-6xl mx-auto flex gap-4 mb-6">
      <button 
        @click="activeTab = 'users'"
        :class="['px-6 py-2 rounded-lg font-bold transition-all shadow-md', activeTab === 'users' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700']"
      >
        👥 Quản lý Người dùng
      </button>
      <button 
        @click="activeTab = 'database'"
        :class="['px-6 py-2 rounded-lg font-bold transition-all shadow-md', activeTab === 'database' ? 'bg-pink-600 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700']"
      >
        🗄️ Mini Database (DataGrip)
      </button>
    </div>

    <div v-if="activeTab === 'users'" class="max-w-6xl mx-auto bg-slate-800 rounded-xl shadow-xl border border-slate-700 overflow-hidden">
      <div class="p-4 bg-slate-800 border-b border-slate-700 flex justify-between items-center">
        <h2 class="text-lg font-bold text-white">Danh sách tài khoản hệ thống</h2>
        <button @click="fetchUsers" class="text-sm bg-indigo-500 hover:bg-indigo-600 px-3 py-1.5 rounded text-white transition-colors">
          🔄 Làm mới
        </button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm text-slate-300">
          <thead class="bg-slate-900/50 text-slate-400 uppercase font-semibold">
            <tr>
              <th class="px-6 py-4">ID</th>
              <th class="px-6 py-4">Username</th>
              <th class="px-6 py-4">Quyền (Role)</th>
              <th class="px-6 py-4">Ngày tạo</th>
              <th class="px-6 py-4 text-center">Thao tác</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
            <tr v-for="user in users" :key="user.id" class="hover:bg-slate-750 transition-colors">
              <td class="px-6 py-4">{{ user.id }}</td>
              <td class="px-6 py-4 font-bold text-white">{{ user.username }}</td>
              <td class="px-6 py-4">
                <span :class="['px-2 py-1 rounded text-xs font-bold uppercase', user.role === 'admin' ? 'bg-pink-900/50 text-pink-400' : 'bg-slate-700 text-slate-300']">
                  {{ user.role }}
                </span>
              </td>
              <td class="px-6 py-4">{{ formatDate(user.created_at) }}</td>
              <td class="px-6 py-4 text-center">
                <template v-if="user.role !== 'admin'">
                  <button 
                    @click="promoteUser(user.id, user.username)" 
                    class="bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500 hover:text-white px-3 py-1.5 rounded transition-all text-xs font-bold mr-2"
                  >
                    Cấp Admin
                  </button>
                  <button 
                    @click="deleteUser(user.id, user.username)" 
                    class="bg-red-500/20 text-red-400 hover:bg-red-500 hover:text-white px-3 py-1.5 rounded transition-all text-xs font-bold"
                  >
                    Xóa User
                  </button>
                </template>
                <span v-else class="text-slate-500 text-xs italic">Quyền lực tối cao</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="activeTab === 'database'" class="max-w-6xl mx-auto flex flex-col md:flex-row gap-6">
      <div class="w-full md:w-1/4 bg-slate-800 rounded-xl shadow-xl border border-slate-700 overflow-hidden h-fit">
        <div class="p-4 bg-slate-900/50 border-b border-slate-700">
          <h2 class="text-md font-bold text-pink-400">📋 Danh sách Bảng</h2>
        </div>
        <div class="p-2 space-y-1">
          <button 
            v-for="table in tables" 
            :key="table" 
            @click="fetchTableData(table)"
            :class="['w-full text-left px-4 py-3 rounded-lg text-sm font-medium transition-colors', selectedTable === table ? 'bg-pink-600 text-white' : 'hover:bg-slate-700 text-slate-300']"
          >
            🗃️ {{ table }}
          </button>
        </div>
      </div>

      <div class="w-full md:w-3/4 bg-slate-800 rounded-xl shadow-xl border border-slate-700 overflow-hidden">
        <div class="p-4 bg-slate-900/50 border-b border-slate-700 flex justify-between items-center">
          <h2 class="text-md font-bold text-white">
            Dữ liệu bảng: <span class="text-pink-400">{{ selectedTable || 'Chưa chọn' }}</span>
          </h2>
          <span v-if="tableData.rows.length" class="text-xs text-slate-400">Hiển thị tối đa 100 dòng</span>
        </div>
        
        <div class="overflow-x-auto p-4" v-if="selectedTable">
          <table class="w-full text-left text-sm text-slate-300 border-collapse">
            <thead class="bg-slate-900 text-slate-400">
              <tr>
                <th v-for="col in tableData.columns" :key="col" class="px-4 py-3 border border-slate-700 font-semibold uppercase text-xs">
                  {{ col }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, index) in tableData.rows" :key="index" class="hover:bg-slate-700 transition-colors">
                <td v-for="col in tableData.columns" :key="col" class="px-4 py-3 border border-slate-700 max-w-[200px] truncate">
                  {{ row[col] !== null ? row[col] : 'NULL' }}
                </td>
              </tr>
              <tr v-if="tableData.rows.length === 0">
                <td :colspan="tableData.columns.length" class="text-center py-8 text-slate-500 italic">
                  Bảng này hiện chưa có dữ liệu nào.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="flex flex-col items-center justify-center py-20 text-slate-500">
          <span class="text-5xl mb-3">🗄️</span>
          <p>Vui lòng chọn một bảng bên trái để xem dữ liệu thô.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const activeTab = ref('users')
const users = ref([])
const tables = ref([])
const selectedTable = ref(null)
const tableData = ref({ columns: [], rows: [] })

const fetchUsers = async () => {
  try {
    const res = await api.get('/admin/users')
    users.value = res.data
  } catch (error) {
    console.error("Lỗi lấy danh sách user:", error)
  }
}

const deleteUser = async (id, username) => {
  if (confirm(`Bạn có chắc chắn muốn xóa tài khoản "${username}" vĩnh viễn không?`)) {
    try {
      await api.delete(`/admin/users/${id}`)
      alert(`Đã xóa thành công user: ${username}`)
      fetchUsers() 
    } catch (error) {
      console.error("Lỗi xóa user:", error)
    }
  }
}

const promoteUser = async (id, username) => {
  if (confirm(`Bạn có chắc chắn muốn thăng cấp "${username}" làm Admin hệ thống không?`)) {
    try {
      await api.put(`/admin/users/${id}/promote`)
      alert(`Đã thăng cấp thành công cho: ${username}`)
      fetchUsers() 
    } catch (error) {
      console.error("Lỗi cấp quyền:", error)
      alert("Thăng cấp thất bại!")
    }
  }
}

const fetchTables = async () => {
  try {
    const res = await api.get('/admin/db/tables')
    tables.value = res.data
  } catch (error) {
    console.error("Lỗi lấy danh sách bảng:", error)
  }
}

const fetchTableData = async (tableName) => {
  selectedTable.value = tableName
  tableData.value = { columns: [], rows: [] } 
  try {
    const res = await api.get(`/admin/db/table/${tableName}`)
    tableData.value = res.data
  } catch (error) {
    console.error("Lỗi lấy dữ liệu bảng:", error)
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