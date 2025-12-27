<template>
  <div class="list-container">
    <div class="page-header">
      <h2>📋 我的报销申请</h2>
      <button @click="loadReimbursements" class="refresh-button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
        </svg>
        刷新
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-message">
      <svg viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
      </svg>
      {{ error }}
    </div>
    
    <div v-else-if="reimbursements.length === 0" class="empty-message">
      <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
        <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
      </svg>
      <h3>还没有报销申请</h3>
      <p>您还没有提交过任何报销申请</p>
      <router-link to="/" class="link-button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        提交第一个申请
      </router-link>
    </div>
    
    <div v-else class="reimbursement-grid">
      <div v-for="item in reimbursements" :key="item.id" class="reimbursement-card">
        <div class="card-header">
          <div class="header-left">
            <h3>{{ item.reason }}</h3>
            <span class="amount">¥{{ item.amount }}</span>
          </div>
          <span :class="['status-badge', getStatusClass(item.status)]">
            <span class="status-icon">{{ getStatusIcon(item.status) }}</span>
            {{ getStatusText(item.status) }}
          </span>
        </div>
        
        <div class="card-body">
          <div class="info-grid">
            <div class="info-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <div>
                <span class="label">申请人</span>
                <span class="value">{{ item.real_name }}</span>
              </div>
            </div>
            <div class="info-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                <path d="M16 2v4M8 2v4M3 10h18"/>
              </svg>
              <div>
                <span class="label">提交时间</span>
                <span class="value">{{ formatDate(item.submission_date) }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="item.remarks" class="remarks">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
            </svg>
            <span>{{ item.remarks }}</span>
          </div>
          
          <div v-if="item.invoice_pdf" class="pdf-link-container">
            <a :href="item.invoice_pdf" target="_blank" class="pdf-link">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>
              </svg>
              查看发票PDF
            </a>
          </div>
        </div>
        
        <!-- 审核不通过 -->
        <div v-if="item.status === 'rejected' && item.rejection_reason" class="rejection-alert">
          <div class="alert-header">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <circle cx="12" cy="12" r="10"/>
              <path fill="white" d="M12 8v4m0 4h.01"/>
            </svg>
            <strong>审核未通过</strong>
          </div>
          <p class="rejection-reason">{{ item.rejection_reason }}</p>
          <button @click="handleResubmit(item.id)" class="resubmit-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 12a9 9 0 019-9 9.75 9.75 0 016.74 2.74L21 8"/>
              <path d="M21 3v5h-5"/>
            </svg>
            重新提交
          </button>
        </div>
        
        <!-- 审核通过 -->
        <div v-if="item.status === 'approved'" class="success-alert">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
            <path d="M22 4L12 14.01l-3-3"/>
          </svg>
          <span>审核已通过，报销已批准！</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const reimbursements = ref([]);
const loading = ref(true);
const error = ref('');

async function loadReimbursements() {
  loading.value = true;
  error.value = '';
  
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      router.push('/login');
      return;
    }
    
    const response = await axios.get('/api/reimbursements/', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    reimbursements.value = response.data;
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = '登录已过期，请重新登录';
      setTimeout(() => router.push('/login'), 2000);
    } else {
      error.value = '加载失败，请重试';
    }
  } finally {
    loading.value = false;
  }
}

function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function getStatusText(status) {
  const statusMap = {
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '未通过'
  };
  return statusMap[status] || status;
}

function getStatusIcon(status) {
  const iconMap = {
    'pending': '⏳',
    'approved': '✅',
    'rejected': '❌'
  };
  return iconMap[status] || '📝';
}

function getStatusClass(status) {
  return `status-${status}`;
}

function handleResubmit(id) {
  router.push('/');
  alert('请重新填写报销申请信息');
}

onMounted(() => {
  loadReimbursements();
});
</script>

<style scoped>
.list-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2.5rem 2rem;
  min-height: 80vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
}

h2 {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: -0.5px;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1.3rem;
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  color: #667eea;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-button svg {
  width: 18px;
  height: 18px;
}

.refresh-button:hover {
  border-color: #667eea;
  background: #f5f7ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.loading {
  text-align: center;
  padding: 5rem 2rem;
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 1.5rem;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading p {
  color: #666;
  font-size: 1.1rem;
  font-weight: 500;
}

.error-message {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  color: white;
  padding: 1.2rem;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  font-weight: 500;
  box-shadow: 0 4px 15px rgba(231, 76, 60, 0.25);
}

.error-message svg {
  width: 24px;
  height: 24px;
}

.empty-message {
  text-align: center;
  padding: 5rem 2rem;
}

.empty-icon {
  width: 100px;
  height: 100px;
  color: #d0d0d0;
  margin-bottom: 2rem;
}

.empty-message h3 {
  font-size: 1.6rem;
  color: #2c3e50;
  margin-bottom: 0.8rem;
}

.empty-message p {
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 2.5rem;
}

.link-button {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.9rem 1.8rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 1.05rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.link-button svg {
  width: 20px;
  height: 20px;
}

.link-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
}

.reimbursement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 2rem;
}

.reimbursement-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid #f0f0f0;
}

.reimbursement-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.12);
}

.card-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%);
  border-bottom: 1px solid #e8ecff;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-left {
  flex: 1;
}

.card-header h3 {
  margin: 0 0 0.6rem 0;
  color: #2c3e50;
  font-size: 1.3rem;
  font-weight: 700;
}

.amount {
  display: inline-block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-icon {
  font-size: 1.1rem;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-approved {
  background: #d4edda;
  color: #155724;
}

.status-rejected {
  background: #f8d7da;
  color: #721c24;
}

.card-body {
  padding: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.2rem;
  margin-bottom: 1.2rem;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 0.8rem;
}

.info-item svg {
  width: 20px;
  height: 20px;
  color: #667eea;
  flex-shrink: 0;
  margin-top: 0.2rem;
}

.info-item div {
  display: flex;
  flex-direction: column;
}

.info-item .label {
  font-size: 0.85rem;
  color: #888;
  margin-bottom: 0.2rem;
}

.info-item .value {
  font-weight: 600;
  color: #2c3e50;
}

.remarks {
  display: flex;
  gap: 0.8rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.95rem;
  color: #555;
  line-height: 1.6;
}

.remarks svg {
  width: 20px;
  height: 20px;
  color: #667eea;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.pdf-link-container {
  margin-top: 1.2rem;
}

.pdf-link {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 1.2rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.pdf-link svg {
  width: 18px;
  height: 18px;
}

.pdf-link:hover {
  background: #764ba2;
  transform: translateX(4px);
}

.rejection-alert {
  margin-top: 1.5rem;
  padding: 1.2rem;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
  border: 2px solid #f8d7da;
  border-radius: 12px;
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  margin-bottom: 0.8rem;
  color: #721c24;
}

.alert-header svg {
  width: 22px;
  height: 22px;
}

.rejection-reason {
  color: #721c24;
  margin: 0 0 1rem 0;
  line-height: 1.6;
  font-size: 0.95rem;
}

.resubmit-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.7rem 1.2rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.resubmit-btn svg {
  width: 16px;
  height: 16px;
}

.resubmit-btn:hover {
  background: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

.success-alert {
  margin-top: 1.5rem;
  padding: 1rem 1.2rem;
  background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
  border: 2px solid #c3e6cb;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: #155724;
  font-weight: 600;
}

.success-alert svg {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

@media (max-width: 768px) {
  .reimbursement-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1.5rem;
    align-items: flex-start;
  }
}
</style>
