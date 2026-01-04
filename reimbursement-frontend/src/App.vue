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
    notices.value = []  // 清空注意事项
    // 先跳转再刷新，确保页面完全重置
    router.push('/login').then(() => {
      window.location.reload()
    })
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
  /* 山东大学经典深蓝配色 */
  background: linear-gradient(135deg, #0a2463 0%, #1e40af 50%, #3b82f6 100%);
  color: white;
  padding: 1.2rem 0;
  box-shadow: 0 4px 16px rgba(10, 36, 99, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
  border-bottom: 2px solid rgba(251, 191, 36, 0.3); /* 金色装饰 */
}

.wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}

h1 {
  margin: 0;
  font-size: 1.85rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  background: linear-gradient(to right, #ffffff, #fbbf24);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.username {
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0.5rem 1.2rem;
  background: rgba(251, 191, 36, 0.15);
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 6px;
  backdrop-filter: blur(10px);
  color: #fef3c7;
}

.logout-btn {
  padding: 0.5rem 1.2rem;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1));
  color: white;
  border: 1px solid rgba(251, 191, 36, 0.4);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.35), rgba(251, 191, 36, 0.2));
  border-color: rgba(251, 191, 36, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
}

nav {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

nav a {
  color: rgba(255, 255, 255, 0.95);
  text-decoration: none;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  font-size: 0.95rem;
  font-weight: 500;
  position: relative;
  border: 1px solid transparent;
}

nav a::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, #fbbf24, #f59e0b);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

nav a:hover::before {
  transform: scaleX(1);
}

nav a:hover {
  background-color: rgba(251, 191, 36, 0.15);
  border-color: rgba(251, 191, 36, 0.3);
  color: white;
}

nav a.router-link-exact-active {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.25), rgba(251, 191, 36, 0.15));
  border-color: rgba(251, 191, 36, 0.4);
  color: white;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.2);
}

nav a.router-link-exact-active::before {
  transform: scaleX(1);
}
</style>

<style>
.notices-container {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(254, 249, 235, 0.95));
  border-radius: 10px;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(10, 36, 99, 0.1), 0 0 0 1px rgba(251, 191, 36, 0.2);
  margin-top: 1.5rem;
  border: 2px solid rgba(251, 191, 36, 0.3);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
}

.notices-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, #0a2463, #3b82f6, #fbbf24);
}

.section-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #0a2463;
  margin: 0 0 1.2rem 0;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 1.3rem;
  background: linear-gradient(to bottom, #0a2463, #fbbf24);
  border-radius: 2px;
  box-shadow: 0 0 8px rgba(251, 191, 36, 0.4);
}

.notice-item {
  padding: 1.1rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(248, 250, 252, 0.8));
  border-radius: 8px;
  margin-bottom: 0.85rem;
  border-left: 3px solid #3b82f6;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.notice-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  width: 0;
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.08), rgba(59, 130, 246, 0.05));
  transition: width 0.3s ease;
}

.notice-item:hover::before {
  width: 100%;
}

.notice-item:hover {
  background: linear-gradient(135deg, rgba(254, 249, 235, 0.95), rgba(241, 245, 249, 0.9));
  border-left-color: #fbbf24;
  transform: translateX(6px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.notice-item:last-child {
  margin-bottom: 0;
}

.notice-title {
  margin: 0 0 0.6rem 0;
  font-size: 1rem;
  color: #0a2463;
  font-weight: 700;
  position: relative;
  z-index: 1;
}

.notice-content {
  margin: 0;
  color: #475569;
  line-height: 1.7;
  font-size: 0.9rem;
  white-space: pre-wrap;
  position: relative;
  z-index: 1;
}
</style>
