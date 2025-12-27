<template>
  <div class="form-container">
    <h2>💰 提交报销申请</h2>
    <form @submit.prevent="submitForm">
      <div v-if="serverError" class="error-message">
        <svg class="error-icon" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
        </svg>
        {{ serverError }}
      </div>
      <div class="form-group">
        <label for="real_name">👤 真实姓名</label>
        <input id="real_name" type="text" v-model="formData.real_name" required placeholder="请输入您的真实姓名">
        <div v-if="errors.real_name" class="error-text">{{ errors.real_name[0] }}</div>
      </div>
      <div class="form-group">
        <label for="reason">📝 报销事由</label>
        <input id="reason" type="text" v-model="formData.reason" required placeholder="如：差旅费、办公用品等">
        <div v-if="errors.reason" class="error-text">{{ errors.reason[0] }}</div>
      </div>
      <div class="form-group">
        <label for="amount">💵 金额 (元)</label>
        <input id="amount" type="number" step="0.01" v-model="formData.amount" required placeholder="0.00">
         <div v-if="errors.amount" class="error-text">{{ errors.amount[0] }}</div>
      </div>
      <div class="form-group">
        <label for="invoice_pdf">📎 发票 (PDF格式，最大50MB)</label>
        <input id="invoice_pdf" type="file" @change="handleFileUpload" accept="application/pdf" required>
         <div v-if="errors.invoice_pdf" class="error-text">{{ errors.invoice_pdf[0] }}</div>
      </div>
      <div class="form-group">
        <label for="remarks">📋 备注（选填）</label>
        <textarea id="remarks" v-model="formData.remarks" placeholder="如有补充说明，请在此填写"></textarea>
      </div>
      <button type="submit" :disabled="isLoading">
        <span v-if="isLoading">⏳ 提交中...</span>
        <span v-else>✅ 提交审核</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const formData = ref({ real_name: '', reason: '', amount: '', remarks: '', invoice_pdf: null });
const errors = ref({});
const serverError = ref('');
const isLoading = ref(false);

function handleFileUpload(event) {
  const file = event.target.files[0];
  if (file) {
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
      serverError.value = '文件太大！PDF发票文件不能超过50MB，请压缩后重新上传。';
      event.target.value = null;
      formData.value.invoice_pdf = null;
      return;
    }
    formData.value.invoice_pdf = file;
    serverError.value = '';
  }
}

async function submitForm() {
  isLoading.value = true;
  errors.value = {};
  serverError.value = '';
  
  // 创建FormData并只添加非空值
  let data = new FormData();
  for (let key in formData.value) {
    if (formData.value[key] !== null && formData.value[key] !== '') {
      data.append(key, formData.value[key]);
    }
  }
  
  try {
    const token = localStorage.getItem('access_token');
    await axios.post('/api/reimbursements/', data, {
      headers: { 'Content-Type': 'multipart/form-data', 'Authorization': `Bearer ${token}` }
    });
    alert('✅ 提交成功！您的报销申请已提交，请等待审核。');
    formData.value = { real_name: '', reason: '', amount: '', remarks: '', invoice_pdf: null };
    document.getElementById('invoice_pdf').value = null;
  } catch (error) {
    if (error.response) {
      if (error.response.status === 400) {
        errors.value = error.response.data;
        serverError.value = '表单填写有误，请检查红色提示信息。';
      } else if (error.response.status === 401) {
        serverError.value = '您尚未登录或登录已过期。';
      } else if (error.response.status === 413) {
        serverError.value = '文件太大！PDF发票文件不能超过50MB，请压缩后重新上传。';
      } else { 
        serverError.value = `提交失败: ${error.response.statusText}`; 
      }
    } else { 
      serverError.value = '网络连接问题或服务器无响应。'; 
    }
  } finally { 
    isLoading.value = false; 
  }
}
</script>

<style scoped>
.form-container { 
  max-width: 650px; 
  margin: 3rem auto; 
  padding: 2.5rem; 
  background: white;
  border-radius: 16px; 
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.form-container:hover {
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.12);
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2.5rem;
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.form-group { 
  margin-bottom: 2rem; 
}

label { 
  display: block; 
  margin-bottom: 0.7rem; 
  font-weight: 600;
  color: #444;
  font-size: 1rem;
}

input, textarea { 
  width: 100%; 
  padding: 1rem 1.2rem; 
  border: 2px solid #e8e8e8; 
  border-radius: 10px; 
  box-sizing: border-box;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fafafa;
  font-family: inherit;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

input[type="file"] {
  padding: 0.9rem;
  background: white;
  cursor: pointer;
  border: 2px dashed #d0d0d0;
}

input[type="file"]:hover {
  border-color: #667eea;
}

textarea {
  min-height: 120px;
  resize: vertical;
  line-height: 1.6;
}

button { 
  width: 100%; 
  padding: 1.2rem; 
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white; 
  border: none; 
  border-radius: 10px; 
  cursor: pointer; 
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 1rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5);
}

button:active:not(:disabled) {
  transform: translateY(-1px);
}

button:disabled { 
  background: linear-gradient(135deg, #ccc 0%, #aaa 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.error-message { 
  color: white; 
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  padding: 1rem 1.3rem; 
  border-radius: 10px; 
  margin-bottom: 2rem;
  font-weight: 500;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.25);
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.error-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.error-text { 
  color: #e74c3c; 
  font-size: 0.88rem; 
  margin-top: 0.5rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.error-text::before {
  content: '⚠️';
}
</style>
