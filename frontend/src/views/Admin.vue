<template>
  <div class="admin-layout">
    <!-- Admin Sidebar -->
    <aside class="admin-sidebar">
      <div class="sidebar-logo">
        <h2>LuNu Admin</h2>
      </div>
      <nav class="admin-nav">
        <a href="#" class="nav-item active">Quản lý Người dùng</a>
        <a href="#" class="nav-item">Lịch sử Tin nhắn</a>
        <a href="#" class="nav-item">Cài đặt Hệ thống</a>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/chat" class="back-link">← Về trang Chat</router-link>
      </div>
    </aside>

    <!-- Admin Content -->
    <main class="admin-main">
      <header class="admin-header">
        <h1>Dashboard Thống Kê</h1>
        <div class="admin-profile">
          <span>Admin LuNu</span>
        </div>
      </header>

      <div class="admin-content">
        <div class="card-stats">
          <div class="stat-card">
            <h3>Tổng Người Dùng</h3>
            <p class="stat-num">1,204</p>
          </div>
          <div class="stat-card">
            <h3>Tin nhắn hôm nay</h3>
            <p class="stat-num">8,432</p>
          </div>
        </div>

        <div class="data-table-card">
          <div class="table-header">
            <h3>Danh sách Người dùng</h3>
            <button class="btn-primary" style="width: auto; padding: 8px 16px;">+ Thêm mới</button>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tên hiển thị</th>
                <th>Email</th>
                <th>Trạng thái</th>
                <th>Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>#1</td>
                <td>Trung Tình</td>
                <td>trungtinh@ai.com</td>
                <td><span class="badge active">Hoạt động</span></td>
                <td>
                  <button class="action-btn edit">Sửa</button>
                  <button class="action-btn delete">Xóa</button>
                </td>
              </tr>
              <!-- Render dữ liệu thật của LuNu vào đây -->
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// Nơi LuNu gọi API Fetch dữ liệu Admin
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: var(--bg-color);
}

/* Sidebar */
.admin-sidebar {
  width: 280px;
  background: #001f4d; /* Navy siêu đậm */
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-logo {
  padding: 24px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-logo h2 {
  font-size: 22px;
  color: var(--accent-blue);
}

.admin-nav {
  flex: 1;
  padding: 20px 0;
}

.nav-item {
  display: block;
  padding: 16px 24px;
  color: #a0b2c6;
  text-decoration: none;
  font-weight: 500;
  transition: 0.3s;
}

.nav-item:hover, .nav-item.active {
  background: rgba(0, 191, 255, 0.1);
  color: white;
  border-left: 4px solid var(--accent-blue);
}

.sidebar-footer {
  padding: 24px;
}

.back-link {
  color: #a0b2c6;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  color: white;
}

/* Main Content */
.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.admin-header {
  background: white;
  padding: 20px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.admin-header h1 {
  font-size: 20px;
  color: var(--text-main);
}

.admin-content {
  padding: 32px;
}

/* Stats */
.card-stats {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 24px;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  flex: 1;
  border-left: 4px solid var(--primary-blue);
}

.stat-card h3 {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.stat-num {
  font-size: 28px;
  font-weight: bold;
  color: var(--primary-blue);
}

/* Table */
.data-table-card {
  background: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.table-header {
  padding: 20px 24px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 16px 24px;
  text-align: left;
  border-bottom: 1px solid #f0f0f0;
}

.data-table th {
  background: #fafafa;
  font-weight: 600;
  color: var(--text-muted);
  font-size: 14px;
}

.badge {
  padding: 6px 12px;
  border-radius: 50px;
  font-size: 12px;
  font-weight: 600;
}

.badge.active {
  background: #e6f7ff;
  color: var(--primary-blue);
}

.action-btn {
  background: none;
  border: none;
  font-weight: 600;
  margin-right: 12px;
  font-size: 13px;
}

.action-btn.edit { color: var(--primary-blue); }
.action-btn.delete { color: #ff4d4f; }
</style>