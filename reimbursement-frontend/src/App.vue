<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const router = useRouter()
const username = ref(localStorage.getItem('username') || '')
const notices = ref([])

const isLoggedIn = computed(() => {
  return !!localStorage.getItem('access_token')
})

async function loadNotices() {
  try {
    const response = await axios.get('/api/reimbursements/notices/')
    notices.value = response.data
  } catch (error) {
    console.error('加载注意事项失败:', error)
  }
}

function logout() {
  if (confirm('确定要退出登录吗？')) {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')
    username.value = ''
    router.push('/login')
  }
}

onMounted(() => {
  if (isLoggedIn.value) {
    loadNotices()
  }
})
</script>

<template>
  <header v-if="isLoggedIn">
    <div class="wrapper">
      <div class="header-content">
        <h1>报销管理系统</h1>
        <div class="user-info">
          <span class="username">👤 {{ username }}</span>
          <button @click="logout" class="logout-btn">退出</button>
        </div>
      </div>
      <nav>
        <RouterLink to="/">提交申请</RouterLink>
        <RouterLink to="/my-reimbursements">我的申请</RouterLink>
      </nav>

      <!-- 注意事项区域 -->
      <div v-if="notices.length > 0" class="notices-container">
        <h2 class="section-title">注意事项</h2>
        <div v-for="notice in notices" :key="notice.id" class="notice-item">
          <h3 class="notice-title">{{ notice.title }}</h3>
          <p class="notice-content">{{ notice.content }}</p>
        </div>
      </div>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.2rem;
}

h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.username {
  font-size: 1rem;
  font-weight: 500;
  padding: 0.6rem 1.2rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.logout-btn {
  padding: 0.6rem 1.4rem;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

nav {
  display: flex;
  justify-content: center;
  gap: 2.5rem;
}

nav a {
  color: white;
  text-decoration: none;
  padding: 0.7rem 1.5rem;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-size: 1rem;
  font-weight: 600;
  position: relative;
  overflow: hidden;
}

nav a::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 3px;
  background: white;
  transform: translateX(-50%);
  transition: width 0.3s ease;
}

nav a:hover::before {
  width: 80%;
}

nav a:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

nav a.router-link-exact-active {
  background-color: rgba(255, 255, 255, 0.25);
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

nav a.router-link-exact-active::before {
  width: 80%;
}
</style>

<style>
.notices-container {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  margin-top: 2rem;
}

.section-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 2rem 0;
  letter-spacing: 2px;
  position: relative;
  padding-bottom: 1rem;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.notice-item {
  padding: 1.3rem 1.5rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98) 0%, rgba(255, 255, 255, 0.95) 100%);
  border-radius: 12px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  border-left: 5px solid #ffd700;
  transition: all 0.3s ease;
}

.notice-item:hover {
  transform: translateX(5px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  border-left-color: #ffb700;
}

.notice-item:last-child {
  margin-bottom: 0;
}

.notice-title {
  margin: 0 0 0.8rem 0;
  font-size: 1.15rem;
  color: #2c3e50;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.notice-content {
  margin: 0;
  color: #555;
  line-height: 1.7;
  font-size: 0.95rem;
  white-space: pre-wrap;
}
</style>
