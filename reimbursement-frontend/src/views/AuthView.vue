<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>{{ isLogin ? '用户登录' : '用户注册' }}</h2>
      
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
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

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
    
    // 跳转到首页
    setTimeout(() => {
      router.push('/');
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
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-box {
  background: white;
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 420px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #555;
}

input {
  width: 100%;
  padding: 0.9rem;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.switch-mode {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.switch-mode a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.switch-mode a:hover {
  text-decoration: underline;
}

.error-message {
  background-color: #fee;
  color: #c33;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  border-left: 4px solid #c33;
}

.success-message {
  background-color: #efe;
  color: #3c3;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  border-left: 4px solid #3c3;
}
</style>
