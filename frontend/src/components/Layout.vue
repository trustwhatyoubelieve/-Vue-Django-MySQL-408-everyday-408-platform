<template>
  <div class="layout">
    <!-- 顶部导航栏 -->
    <header class="navbar">
      <div class="navbar-content">
        <!-- Logo 区域 -->
        <div class="logo">
          <div class="logo-icon">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
              <rect width="28" height="28" rx="8" fill="url(#logoGradient)"/>
              <path d="M8 10h12M8 14h8M8 18h10" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <defs>
                <linearGradient id="logoGradient" x1="0" y1="0" x2="28" y2="28">
                  <stop offset="0%" stop-color="#667eea"/>
                  <stop offset="100%" stop-color="#764ba2"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <span class="logo-text">408 刷题系统</span>
        </div>

        <!-- 导航链接 -->
        <nav class="nav-links">
          <router-link to="/" class="nav-item" :class="{ active: isActive('/') }">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
              <polyline points="9,22 9,12 15,12 15,22"/>
            </svg>
            首页
          </router-link>

          <!-- 已登录显示功能入口 -->
          <template v-if="userStore.isLoggedIn">
            <router-link to="/question-bank" class="nav-item" :class="{ active: isActive('/question-bank') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              题库浏览
            </router-link>
            <router-link to="/practice-home" class="nav-item" :class="{ active: isActive('/practice') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 20h9"/>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
              在线练习
            </router-link>
            <router-link to="/wrong-questions" class="nav-item" :class="{ active: isActive('/wrong-questions') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              错题本
            </router-link>
            <router-link to="/recommendation" class="nav-item" :class="{ active: isActive('/recommendation') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 2L2 7l10 5 10-5-10-5z"/>
                <path d="M2 17l10 5 10-5"/>
                <path d="M2 12l10 5 10-5"/>
              </svg>
              智能推荐
            </router-link>
            <router-link to="/favorites" class="nav-item" :class="{ active: isActive('/favorites') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
              </svg>
              收藏夹
            </router-link>
            <router-link to="/study-center" class="nav-item" :class="{ active: isActive('/study-center') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
              学习中心
            </router-link>
            <router-link to="/mindmap" class="nav-item" :class="{ active: isActive('/mindmap') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="3"/>
                <line x1="12" y1="2" x2="12" y2="5"/>
                <line x1="12" y1="19" x2="12" y2="22"/>
                <line x1="2" y1="12" x2="5" y2="12"/>
                <line x1="19" y1="12" x2="22" y2="12"/>
              </svg>
              思维导图
            </router-link>

            <!-- 用户信息下拉 -->
            <div class="user-section">
              <div class="user-avatar">
                {{ userStore.userInfo?.username?.charAt(0) || 'U' }}
              </div>
              <span class="user-name">{{ userStore.userInfo?.username }}</span>
              <button class="btn-logout" @click="handleLogout">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16,17 21,12 16,7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                退出
              </button>
            </div>
          </template>

          <!-- 未登录显示登录注册 -->
          <template v-else>
            <router-link to="/login" class="nav-item" :class="{ active: isActive('/login') }">去登录</router-link>
            <router-link to="/register" class="nav-item" :class="{ active: isActive('/register') }">去注册</router-link>
          </template>
        </nav>

        <!-- 移动端菜单按钮 -->
        <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- 移动端菜单 -->
      <div class="mobile-menu" v-show="mobileMenuOpen">
        <router-link to="/" class="mobile-nav-item" :class="{ active: isActive('/') }">首页</router-link>
        <template v-if="userStore.isLoggedIn">
          <router-link to="/question-bank" class="mobile-nav-item" :class="{ active: isActive('/question-bank') }">题库浏览</router-link>
          <router-link to="/practice-home" class="mobile-nav-item" :class="{ active: isActive('/practice') }">在线练习</router-link>
          <router-link to="/wrong-questions" class="mobile-nav-item" :class="{ active: isActive('/wrong-questions') }">错题本</router-link>
          <router-link to="/recommendation" class="mobile-nav-item" :class="{ active: isActive('/recommendation') }">智能推荐</router-link>
          <router-link to="/favorites" class="mobile-nav-item" :class="{ active: isActive('/favorites') }">收藏夹</router-link>
          <router-link to="/study-center" class="mobile-nav-item" :class="{ active: isActive('/study-center') }">学习中心</router-link>
          <router-link to="/mindmap" class="mobile-nav-item" :class="{ active: isActive('/mindmap') }">思维导图</router-link>
          <button class="mobile-logout" @click="handleLogout">退出登录</button>
        </template>
        <template v-else>
          <router-link to="/login" class="mobile-nav-item" :class="{ active: isActive('/login') }">去登录</router-link>
          <router-link to="/register" class="mobile-nav-item" :class="{ active: isActive('/register') }">去注册</router-link>
        </template>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 底部 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-brand">
          <svg width="20" height="20" viewBox="0 0 28 28" fill="none">
            <rect width="28" height="28" rx="8" fill="url(#footerLogoGradient)"/>
            <path d="M8 10h12M8 14h8M8 18h10" stroke="white" stroke-width="2" stroke-linecap="round"/>
            <defs>
              <linearGradient id="footerLogoGradient" x1="0" y1="0" x2="28" y2="28">
                <stop offset="0%" stop-color="#667eea"/>
                <stop offset="100%" stop-color="#764ba2"/>
              </linearGradient>
            </defs>
          </svg>
          <span>408 刷题系统</span>
        </div>
        <p class="footer-text">基于 Vue + Django + MySQL 构建 | 服务于计算机考研 408 备考</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const mobileMenuOpen = ref(false)

// 判断当前路由是否激活
const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

const handleLogout = () => {
  userStore.clearLoginData()
  mobileMenuOpen.value = false
  router.push('/login')
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏 */
.navbar {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.6);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.08);
}

.navbar-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Logo 样式 */
.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  filter: drop-shadow(0 4px 8px rgba(102, 126, 234, 0.3));
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.5px;
}

/* 导航链接 */
.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  color: #606266;
  font-size: 14px;
  font-weight: 500;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-item:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.08);
}

.nav-item.active {
  color: #667eea;
  background: rgba(102, 126, 234, 0.12);
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.nav-icon {
  width: 18px;
  height: 18px;
}

/* 按钮样式 */
.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff !important;
  padding: 8px 20px !important;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
  transform: translateY(-1px);
}

.btn-secondary {
  background: #fff;
  color: #667eea !important;
  border: 1.5px solid rgba(102, 126, 234, 0.3);
  padding: 8px 20px !important;
}

.btn-secondary:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.04);
}

/* 用户信息区域 */
.user-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 12px;
  padding-left: 20px;
  border-left: 1px solid rgba(0, 0, 0, 0.08);
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
}

.user-name {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.btn-logout {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #fff;
  color: #909399;
  font-size: 13px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.btn-logout svg {
  width: 14px;
  height: 14px;
}

.btn-logout:hover {
  color: #f56c6c;
  border-color: rgba(245, 108, 108, 0.4);
  background: rgba(245, 108, 108, 0.04);
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  padding: 8px;
  background: none;
  border: none;
}

.mobile-menu-btn svg {
  width: 24px;
  height: 24px;
  color: #606266;
}

/* 移动端菜单 */
.mobile-menu {
  display: none;
  flex-direction: column;
  padding: 16px;
  background: #fff;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.mobile-nav-item {
  display: block;
  padding: 12px 16px;
  color: #606266;
  font-size: 15px;
  border-radius: 10px;
  transition: all 0.2s;
}

.mobile-nav-item:hover,
.mobile-nav-item.active {
  background: rgba(102, 126, 234, 0.08);
  color: #667eea;
}

.mobile-nav-item.active {
  font-weight: 600;
}

.mobile-logout {
  margin-top: 12px;
  padding: 12px 16px;
  background: none;
  color: #f56c6c;
  font-size: 15px;
  border-radius: 10px;
  text-align: left;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  width: 100%;
}

/* 底部 */
.footer {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.8);
  padding: 32px 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  text-align: center;
}

.footer-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 12px;
}

.footer-brand span {
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-text {
  font-size: 13px;
  color: #909399;
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar-content {
    padding: 0 16px;
    height: 60px;
  }

  .nav-links {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }

  .mobile-menu {
    display: flex;
  }

  .logo-text {
    font-size: 18px;
  }

  .footer {
    padding: 24px 0;
  }

  .footer-content {
    padding: 0 16px;
  }
}
</style>
