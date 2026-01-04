<template>
  <div class="auth-container" :style="containerStyle">
    <div class="auth-box">
      <div class="logo-section">
        <div class="combined-logo">
          <div class="logo-circle">
            <span class="logo-text">CISLC</span>
          </div>
        </div>
        <h2>{{ isLogin ? '用户登录' : '用户注册' }}</h2>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
        
        <div class="form-group">
          <label for="username">用户名</label>
          <input 
            id="username" 
            type="text" 
            v-model="formData.username" 
            placeholder="请输入用户名"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input 
            id="password" 
            type="password" 
            v-model="formData.password" 
            placeholder="请输入密码"
            required
          >
        </div>
        
        <div v-if="!isLogin" class="form-group">
          <label for="password2">确认密码</label>
          <input 
            id="password2" 
            type="password" 
            v-model="formData.password2" 
            placeholder="请再次输入密码"
            required
          >
        </div>
        
        <div v-if="!isLogin" class="form-group">
          <label for="real_name">真实姓名</label>
          <input 
            id="real_name" 
            type="text" 
            v-model="formData.real_name" 
            placeholder="请输入您的真实姓名"
            required
          >
        </div>
        
        <div v-if="!isLogin" class="form-group">
          <label for="email">邮箱（可选）</label>
          <input 
            id="email" 
            type="email" 
            v-model="formData.email" 
            placeholder="example@email.com"
          >
        </div>
        
        <button type="submit" :disabled="isLoading" class="submit-btn">
          {{ isLoading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>
      
      <div class="switch-mode">
        <span v-if="isLogin">
          还没有账号？
          <a href="#" @click.prevent="toggleMode">立即注册</a>
        </span>
        <span v-else>
          已有账号？
          <a href="#" @click.prevent="toggleMode">去登录</a>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import bgImage from '@/assets/sdu_software.png';

const router = useRouter();
const isLogin = ref(true);
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const formData = ref({
  username: '',
  password: '',
  password2: '',
  email: '',
  real_name: ''
});

// 背景样式
const containerStyle = computed(() => ({
  backgroundImage: `linear-gradient(135deg, rgba(10, 36, 99, 0.35) 0%, rgba(30, 64, 175, 0.30) 50%, rgba(59, 130, 246, 0.25) 100%), url(${bgImage})`,
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  backgroundRepeat: 'no-repeat',
  backgroundAttachment: 'fixed'
}));

// 切换登录/注册模式
function toggleMode() {
  isLogin.value = !isLogin.value;
  errorMessage.value = '';
  successMessage.value = '';
  formData.value = {
    username: '',
    password: '',
    password2: '',
    email: '',
    real_name: ''
  };
}

// 处理表单提交
async function handleSubmit() {
  errorMessage.value = '';
  successMessage.value = '';
  
  // 表单验证
  if (!isLogin.value) {
    if (formData.value.password !== formData.value.password2) {
      errorMessage.value = '两次输入的密码不一致！';
      return;
    }
    if (formData.value.password.length < 6) {
      errorMessage.value = '密码长度至少6位！';
      return;
    }
  }
  
  isLoading.value = true;
  
  try {
    if (isLogin.value) {
      // 登录
      await handleLogin();
    } else {
      // 注册
      await handleRegister();
    }
  } catch (error) {
    console.error('操作失败:', error);
  } finally {
    isLoading.value = false;
  }
}

// 处理登录
async function handleLogin() {
  try {
    const response = await axios.post('/api/token/', {
      username: formData.value.username,
      password: formData.value.password
    });
    
    // 保存token
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    localStorage.setItem('username', formData.value.username);
    
    successMessage.value = '登录成功！';
    
    // 跳转到首页，使用replace避免缓存问题
    setTimeout(() => {
      router.push('/').then(() => {
        // 强制刷新页面以加载注意事项
        window.location.reload();
      });
    }, 1000);
  } catch (error) {
    if (error.response) {
      if (error.response.status === 401) {
        errorMessage.value = '用户名或密码错误！';
      } else {
        errorMessage.value = error.response.data.detail || '登录失败，请重试！';
      }
    } else {
      errorMessage.value = '网络连接失败，请检查网络！';
    }
  }
}

// 处理注册
async function handleRegister() {
  try {
    await axios.post('/api/register/', {
      username: formData.value.username,
      password: formData.value.password,
      email: formData.value.email,
      real_name: formData.value.real_name
    });
    
    successMessage.value = '注册成功！请登录。';
    
    // 切换到登录模式
    setTimeout(() => {
      isLogin.value = true;
      formData.value = {
        username: formData.value.username,
        password: '',
        password2: '',
        email: '',
        real_name: ''
      };
      successMessage.value = '';
    }, 2000);
  } catch (error) {
    if (error.response && error.response.data) {
      const errors = error.response.data;
      if (errors.username) {
        errorMessage.value = `用户名错误: ${errors.username[0]}`;
      } else if (errors.password) {
        errorMessage.value = `密码错误: ${errors.password[0]}`;
      } else if (errors.detail) {
        errorMessage.value = errors.detail;
      } else {
        errorMessage.value = '注册失败，请重试！';
      }
    } else {
      errorMessage.value = '网络连接失败，请检查网络！';
    }
  }
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  /* 山东大学校园实景背景 - 通过内联样式设置 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
}

.auth-box {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.28), rgba(254, 249, 235, 0.25));
  border-radius: 16px;
  padding: 2.5rem;
  box-shadow: 
    0 20px 60px rgba(10, 36, 99, 0.3), 
    0 0 0 1px rgba(251, 191, 36, 0.6),
    inset 0 1px 0 rgba(255, 255, 255, 0.5);
  width: 100%;
  max-width: 460px;
  position: relative;
  z-index: 1;
  border: 2px solid rgba(251, 191, 36, 0.5);
  backdrop-filter: blur(6px);
}

/* 添加顶部装饰 */
.auth-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(to right, #0a2463 0%, #3b82f6 50%, #fbbf24 100%);
  border-radius: 16px 16px 0 0;
}

/* Logo区域 */
.logo-section {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid rgba(59, 130, 246, 0.1);
}

.combined-logo {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.logo-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0a2463, #3b82f6);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 8px 24px rgba(10, 36, 99, 0.4),
    0 0 0 4px rgba(251, 191, 36, 0.2);
  position: relative;
  animation: pulse 3s ease-in-out infinite;
}

.logo-circle::after {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 50%;
  border: 2px solid rgba(251, 191, 36, 0.3);
  animation: rotate 6s linear infinite;
}

@keyframes pulse {
  0%, 100% {
    box-shadow: 
      0 8px 24px rgba(10, 36, 99, 0.4),
      0 0 0 4px rgba(251, 191, 36, 0.2);
  }
  50% {
    box-shadow: 
      0 12px 32px rgba(10, 36, 99, 0.5),
      0 0 0 6px rgba(251, 191, 36, 0.35);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.logo-text {
  font-size: 1.4rem;
  font-weight: 900;
  color: #fbbf24;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  font-family: 'Arial', 'Helvetica', sans-serif;
  letter-spacing: 1px;
}

h2 {
  text-align: center;
  color: #0a2463;
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 0 2px 4px rgba(10, 36, 99, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.6rem;
  font-weight: 600;
  color: #1e40af;
  font-size: 0.9rem;
}

input {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
  background: white;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15), 0 2px 8px rgba(59, 130, 246, 0.1);
}

input::placeholder {
  color: #9ca3af;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #1e40af 100%);
  background-size: 200% 100%;
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 0 4px 16px rgba(30, 64, 175, 0.4);
  letter-spacing: 1px;
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s;
}

.submit-btn:hover:not(:disabled)::before {
  left: 100%;
}

.submit-btn:hover:not(:disabled) {
  background-position: 100% 0;
  box-shadow: 0 8px 24px rgba(10, 36, 99, 0.6);
  transform: translateY(-2px);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.switch-mode {
  text-align: center;
  margin-top: 1.8rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(59, 130, 246, 0.1);
  color: #000000;
  font-size: 0.9rem;
}

.switch-mode a {
  color: #1e40af;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.switch-mode a:hover {
  color: #3b82f6;
  text-decoration: underline;
}

.error-message {
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  color: #991b1b;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  border-left: 4px solid #dc2626;
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(220, 38, 38, 0.1);
}

.success-message {
  background: linear-gradient(135deg, #d1fae5, #a7f3d0);
  color: #065f46;
  padding: 0.85rem 1rem;
  border-radius: 8px;
  margin-bottom: 1.2rem;
  border-left: 4px solid #059669;
  font-size: 0.9rem;
  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.1);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .auth-box {
    padding: 2rem 1.5rem;
  }
  
  .logo-circle {
    width: 70px;
    height: 70px;
  }
  
  .logo-text {
    font-size: 1.3rem;
  }
  
  h2 {
    font-size: 1.75rem;
  }
}
</style>
