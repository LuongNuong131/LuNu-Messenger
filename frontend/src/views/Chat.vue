<template>
  <div class="chat-layout">
    <!-- Sidebar Danh sách bạn bè (Nếu có) -->
    <aside class="chat-sidebar">
      <div class="sidebar-header">
        <h3>LuNu Messenger</h3>
      </div>
      <div class="contact-list">
        <!-- Vòng lặp user ở đây -->
        <div class="contact-item active">
          <div class="avatar">T</div>
          <div class="contact-info">
            <h4>Trung Tình</h4>
            <p>Tới đi cưng!</p>
          </div>
        </div>
      </div>
    </aside>

    <!-- Khu vực chat chính -->
    <main class="chat-main">
      <header class="chat-header">
        <div class="current-chat-info">
          <div class="avatar">T</div>
          <h2>Trung Tình</h2>
        </div>
        <button class="logout-btn" @click="logout">Đăng xuất</button>
      </header>

      <div class="messages-container" ref="messagesContainer">
        <!-- Vòng lặp tin nhắn ở đây -->
        <div class="message received">
          <div class="msg-bubble">Chào LuNu, hôm nay code mượt chứ?</div>
        </div>
        
        <div class="message sent">
          <div class="msg-bubble">Ngon lành cành đào luôn Trung Tình ơi! Xanh Thủy đẹp xuất sắc.</div>
        </div>
      </div>

      <div class="chat-input-area">
        <form @submit.prevent="sendMessage" class="input-wrapper">
          <input 
            type="text" 
            v-model="newMessage" 
            placeholder="Nhập tin nhắn..." 
          />
          <button type="submit" class="send-btn">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="currentColor"/>
            </svg>
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const newMessage = ref('')
const messagesContainer = ref(null)

const sendMessage = () => {
  if (!newMessage.value.trim()) return
  // Logic gửi tin nhắn (WebSocket hoặc API)
  console.log('Sending:', newMessage.value)
  newMessage.value = ''
  // Sau khi gửi nhớ scroll xuống cuối nhé
}

const logout = () => {
  console.log('Logging out...')
}
</script>

<style scoped>
.chat-layout {
  display: flex;
  height: 100vh;
  background-color: var(--bg-color);
  overflow: hidden;
}

/* Sidebar */
.chat-sidebar {
  width: 320px;
  background: #ffffff;
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px 20px;
  background: var(--primary-blue);
  color: white;
}

.contact-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.contact-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 5px;
}

.contact-item:hover {
  background: var(--secondary-blue);
}

.contact-item.active {
  background: var(--secondary-blue);
  border-left: 4px solid var(--primary-blue);
}

.avatar {
  width: 48px;
  height: 48px;
  background: var(--primary-blue);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
  margin-right: 16px;
}

.contact-info h4 {
  font-size: 16px;
  color: var(--text-main);
  margin-bottom: 4px;
}

.contact-info p {
  font-size: 13px;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

/* Main Chat Area */
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.chat-header {
  padding: 16px 24px;
  background: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  z-index: 10;
}

.current-chat-info {
  display: flex;
  align-items: center;
}

.current-chat-info h2 {
  font-size: 18px;
}

.logout-btn {
  background: transparent;
  color: #ff4d4f;
  font-weight: 600;
}

.messages-container {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Chat Bubbles */
.message {
  display: flex;
  max-width: 70%;
  animation: fadeIn 0.3s ease;
}

.message.received {
  align-self: flex-start;
}

.message.sent {
  align-self: flex-end;
}

.msg-bubble {
  padding: 14px 18px;
  font-size: 15px;
  line-height: 1.4;
  box-shadow: var(--shadow-sm);
}

.message.received .msg-bubble {
  background: #ffffff;
  color: var(--text-main);
  border-radius: 20px 20px 20px 4px;
  border: 1px solid #e0e0e0;
}

.message.sent .msg-bubble {
  background: var(--primary-blue);
  color: #ffffff;
  border-radius: 20px 20px 4px 20px;
}

/* Input Area */
.chat-input-area {
  padding: 20px 24px;
  background: #ffffff;
  border-top: 1px solid #e0e0e0;
}

.input-wrapper {
  display: flex;
  gap: 12px;
}

.input-wrapper input {
  border-radius: var(--radius-full);
  background: var(--bg-color);
  border: none;
  padding: 16px 24px;
}

.input-wrapper input:focus {
  background: #ffffff;
  box-shadow: 0 0 0 2px var(--accent-blue);
}

.send-btn {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--primary-blue);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.send-btn svg {
  width: 24px;
  height: 24px;
  margin-left: 4px;
}

.send-btn:hover {
  background: var(--primary-hover);
  transform: scale(1.05);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>