/**
 * Axios 封装
 *
 * - 自动从 localStorage 注入 Bearer token
 * - 统一响应格式解析（code/message/data）
 * - 401 时清理本地登录状态并跳转登录页
 */
import axios from 'axios'
import router from '@/router'
import { useUserStore } from '@/stores/user'

// 创建 axios 实例
const request = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：自动注入 token
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    const res = response.data
    // 统一格式：code !== 0 视为失败
    if (res.code !== undefined && res.code !== 0) {
      return Promise.reject(new Error(res.message || '请求失败'))
    }
    return res
  },
  (error) => {
    if (error.response) {
      const status = error.response.status

      if (status === 401) {
        // token 失效，清除本地登录状态并跳转登录页
        const userStore = useUserStore()
        userStore.clearLoginData()
        // 只有不在登录/注册页时才跳转
        if (!['/login', '/register'].includes(router.currentRoute.value.path)) {
          router.push('/login')
        }
      }

      // 从响应体中提取后端错误信息
      const data = error.response.data
      if (data && data.detail) {
        error.message = data.detail
      } else if (data && data.message) {
        error.message = data.message
      }
    } else if (error.request) {
      error.message = '网络连接失败，请检查后端服务是否启动'
    }

    console.error('请求失败:', error.message)
    return Promise.reject(error)
  }
)

// 导出便捷方法
export default {
  get: (url, params = {}, config = {}) => request.get(url, { params, ...config }),
  post: (url, data = {}, config = {}) => request.post(url, data, config),
  put: (url, data = {}, config = {}) => request.put(url, data, config),
  delete: (url, config = {}) => request.delete(url, config)
}