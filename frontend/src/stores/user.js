/**
 * Pinia Store - 用户模块
 *
 * 管理用户登录状态、token 和用户信息。
 * token 持久化到 localStorage。
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // ========== state ==========
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  // userInfo 也要从 localStorage 恢复，避免刷新后丢失
  let _savedUser = null
  try {
    const _raw = localStorage.getItem('userInfo')
    if (_raw) _savedUser = JSON.parse(_raw)
  } catch {
    localStorage.removeItem('userInfo')
  }
  const userInfo = ref(_savedUser)

  // ========== getters ==========
  const isLoggedIn = computed(() => !!token.value)

  // ========== actions ==========

  /**
   * 设置登录数据（注册/登录成功后调用）
   * @param {object} data - { access, refresh, user }
   */
  function setLoginData(data) {
    token.value = data.access
    refreshToken.value = data.refresh
    userInfo.value = data.user
    localStorage.setItem('token', data.access)
    localStorage.setItem('refreshToken', data.refresh)
    localStorage.setItem('userInfo', JSON.stringify(data.user))
  }

  /**
   * 清除登录数据（退出登录或 token 过期时调用）
   */
  function clearLoginData() {
    token.value = ''
    refreshToken.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('userInfo')
  }

  /**
   * 设置用户信息
   * @param {object} info
   */
  function setUserInfo(info) {
    userInfo.value = info
    if (info) {
      localStorage.setItem('userInfo', JSON.stringify(info))
    } else {
      localStorage.removeItem('userInfo')
    }
  }

  return {
    token,
    refreshToken,
    userInfo,
    isLoggedIn,
    setLoginData,
    clearLoginData,
    setUserInfo
  }
})
