<template>
  <div class="form-container">
    <h2>{{ isResubmit ? '📝 重新提交报销申请' : '💰 提交报销申请' }}</h2>
    
    <div v-if="isResubmit" class="resubmit-notice">
      <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
      </svg>
      <span>您正在修改被驳回的申请，请修改后重新提交</span>
    </div>
    
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
        <input id="invoice_pdf" type="file" @change="handleFileUpload" accept="application/pdf" :required="!isResubmit">
        <div v-if="isResubmit && !formData.invoice_pdf" class="info-text">
          💡 如需更换发票请重新上传，否则将保留原发票
        </div>
         <div v-if="errors.invoice_pdf" class="error-text">{{ errors.invoice_pdf[0] }}</div>
      </div>
      <div class="form-group">
        <label for="remarks">📋 备注（选填）</label>
        <textarea id="remarks" v-model="formData.remarks" placeholder="如有补充说明，请在此填写"></textarea>
      </div>
      <button type="submit" :disabled="isLoading">
        <span v-if="isLoading">⏳ 提交中...</span>
        <span v-else>✅ {{ isResubmit ? '重新提交审核' : '提交审核' }}</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const formData = ref({ real_name: '', reason: '', amount: '', remarks: '', invoice_pdf: null });
const errors = ref({});
const serverError = ref('');
const isLoading = ref(false);
const isResubmit = ref(false);
const resubmitId = ref(null);

// 检查是否是重新提交模式
onMounted(() => {
  if (route.query.resubmit === 'true' && route.query.id) {
    isResubmit.value = true;
    resubmitId.value = route.query.id;
    
    // 自动填充表单数据
    formData.value.real_name = route.query.realName || '';
    formData.value.reason = route.query.reason || '';
    formData.value.amount = route.query.amount || '';
    formData.value.remarks = route.query.remarks || '';
    
    // 清除URL参数以避免刷新时重复填充
    router.replace({ path: '/', query: {} });
  }
});

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
  
  try {
    const token = localStorage.getItem('access_token');
    
    if (isResubmit.value && resubmitId.value) {
      // 重新提交：使用PATCH更新现有申请（部分更新）
      const data = new FormData();
      
      // 添加基本字段
      data.append('real_name', formData.value.real_name);
      data.append('reason', formData.value.reason);
      data.append('amount', formData.value.amount);
      data.append('remarks', formData.value.remarks || '');
      
      // 只有在用户选择了新文件时才添加
      if (formData.value.invoice_pdf instanceof File) {
        data.append('invoice_pdf', formData.value.invoice_pdf);
      }
      
      await axios.patch(`/api/reimbursements/${resubmitId.value}/`, data, {
        headers: { 'Content-Type': 'multipart/form-data', 'Authorization': `Bearer ${token}` }
      });
      alert('✅ 重新提交成功！您的报销申请已更新，请等待审核。');
      // 跳转到我的申请页面
      router.push('/my-reimbursements');
    } else {
      // 新提交：使用POST创建新申请
      const data = new FormData();
      data.append('real_name', formData.value.real_name);
      data.append('reason', formData.value.reason);
      data.append('amount', formData.value.amount);
      if (formData.value.remarks) data.append('remarks', formData.value.remarks);
      
      // 新提交必须有发票
      if (formData.value.invoice_pdf) {
        data.append('invoice_pdf', formData.value.invoice_pdf);
      }
      
      await axios.post('/api/reimbursements/', data, {
        headers: { 'Content-Type': 'multipart/form-data', 'Authorization': `Bearer ${token}` }
      });
      alert('✅ 提交成功！您的报销申请已提交，请等待审核。');
      formData.value = { real_name: '', reason: '', amount: '', remarks: '', invoice_pdf: null };
      document.getElementById('invoice_pdf').value = null;
    }
  } catch (error) {
    if (error.response) {
      if (error.response.status === 400) {
        errors.value = error.response.data;
        serverError.value = '表单填写有误，请检查红色提示信息。';
      } else if (error.response.status === 401) {
        serverError.value = '您尚未登录或登录已过期。';
      } else if (error.response.status === 403) {
        serverError.value = error.response.data.detail || '没有权限修改此申请。';
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
  max-width: 680px; 
  margin: 2rem auto; 
  padding: 2rem; 
  background: rgba(255, 255, 255, 0.95);
  border-radius: 8px; 
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
}

h2 {
  color: #1e293b;
  margin-bottom: 1.75rem;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: -0.3px;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e5e7eb;
}

.form-group { 
  margin-bottom: 1.5rem; 
}

label { 
  display: block; 
  margin-bottom: 0.5rem; 
  font-weight: 500;
  color: #374151;
  font-size: 0.9rem;
}

input, textarea { 
  width: 100%; 
  padding: 0.75rem; 
  border: 1px solid #d1d5db; 
  border-radius: 6px; 
  box-sizing: border-box;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  background: white;
  font-family: inherit;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

input[type="file"] {
  padding: 0.75rem;
  background: #f9fafb;
  cursor: pointer;
  border: 1px dashed #d1d5db;
}

input[type="file"]:hover {
  border-color: #3b82f6;
  background: white;
}

textarea {
  min-height: 100px;
  resize: vertical;
  line-height: 1.6;
}

button { 
  width: 100%; 
  padding: 0.85rem; 
  background: #3b82f6;
  color: white; 
  border: none; 
  border-radius: 6px; 
  cursor: pointer; 
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s ease;
  margin-top: 1rem;
}

button:hover:not(:disabled) {
  background: #2563eb;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

button:active:not(:disabled) {
  transform: scale(0.98);
}

button:disabled { 
  background: #9ca3af;
  cursor: not-allowed;
}

.error-message { 
  color: #991b1b; 
  background: #fef2f2;
  padding: 0.75rem 1rem; 
  border-radius: 6px; 
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  border-left: 3px solid #dc2626;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #dc2626;
}

.error-text { 
  color: #dc2626; 
  font-size: 0.85rem; 
  margin-top: 0.4rem;
}

.resubmit-notice {
  background: #fef3c7;
  color: #92400e;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  border-left: 3px solid #f59e0b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.resubmit-notice svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: #f59e0b;
}

.info-text {
  color: #1e40af;
  font-size: 0.85rem;
  margin-top: 0.4rem;
}
</style>
