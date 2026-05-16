<template>
  <div class="register-page">
    <div class="register-card">
      <h2>用户注册</h2>

      <form @submit.prevent="handleRegister">
        <div class="form-item">
          <label>用户名</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            autocomplete="username"
          />
        </div>

        <div class="form-item">
          <label>密码</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入密码（至少8位）"
            autocomplete="new-password"
          />
        </div>

        <div class="form-item">
          <label>确认密码</label>
          <input
            v-model="form.password_confirm"
            type="password"
            placeholder="请再次输入密码"
            autocomplete="new-password"
          />
        </div>

        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

        <button type="submit" class="btn-register" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>

      <div class="form-footer">
        <span>已有账号？</span>
        <router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userAPI } from '@/api'

const router = useRouter()

const form = ref({
  username: '',
  password: '',
  password_confirm: ''
})

const loading = ref(false)
const errorMsg = ref('')

const handleRegister = async () => {
  errorMsg.value = ''

  if (!form.value.username || !form.value.password) {
    errorMsg.value = '请填写用户名和密码'
    return
  }

  if (form.value.password !== form.value.password_confirm) {
    errorMsg.value = '两次输入的密码不一致'
    return
  }

  if (form.value.password.length < 8) {
    errorMsg.value = '密码长度不能少于8位'
    return
  }

  loading.value = true

  try {
    await userAPI.register({
      username: form.value.username,
      password: form.value.password,
      password_confirm: form.value.password_confirm
    })
    // 注册成功后跳转到登录页
    router.push('/login')
  } catch (error) {
    errorMsg.value = error.message || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.register-card {
  background: #fff;
  border-radius: 8px;
  padding: 40px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.form-item input {
  width: 100%;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s;
}

.form-item input:focus {
  border-color: #409eff;
  outline: none;
}

.error-msg {
  color: #f56c6c;
  font-size: 14px;
  margin-bottom: 15px;
  text-align: center;
}

.btn-register {
  width: 100%;
  padding: 12px;
  background-color: #67c23a;
  color: #fff;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-register:hover:not(:disabled) {
  background-color: #85ce61;
}

.btn-register:disabled {
  background-color: #b3e19d;
  cursor: not-allowed;
}

.form-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 14px;
  color: #909399;
}

.form-footer a {
  color: #409eff;
  margin-left: 5px;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>