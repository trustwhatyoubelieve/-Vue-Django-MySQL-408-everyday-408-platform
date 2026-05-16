<template>
  <div class="home-page">
    <!-- Hero 区域 -->
    <section class="hero-section">
      <div class="hero-background">
        <div class="hero-blob hero-blob-1"></div>
        <div class="hero-blob hero-blob-2"></div>
        <div class="hero-blob hero-blob-3"></div>
      </div>
      <div class="hero-container">
        <!-- 左侧内容 -->
        <div class="hero-content">
          <div class="hero-badge">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
            </svg>
            计算机考研必备工具
          </div>
          <h1 class="hero-title">
            408 <span class="gradient-text">刷题系统</span>
          </h1>
          <p class="hero-subtitle">
            高效刷题 · 智能练习 · 轻松上岸
          </p>
          <p class="hero-desc">
            <br/>
            服务于计算机考研 408 备考，四大科目全覆盖
          </p>
          <div class="hero-buttons">
            <button class="btn-primary-gradient" @click="goToPractice">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5,3 19,12 5,21"/>
              </svg>
              开始刷题
            </button>
            <button class="btn-secondary-outline" @click="goToQuestionBank">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              查看题库
            </button>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-number">2000+</span>
              <span class="stat-label">精选题目</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">4</span>
              <span class="stat-label">核心科目</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">100%</span>
              <span class="stat-label">覆盖考点</span>
            </div>
          </div>
        </div>

        <!-- 右侧装饰面板 -->
        <div class="hero-visual">
          <div class="glass-card main-card">
            <div class="card-header">
              <div class="card-title-row">
                <div class="card-icon card-icon-purple">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
                    <polyline points="22,4 12,14.01 9,11.01"/>
                  </svg>
                </div>
                <span>今日学习</span>
              </div>
              <span class="card-date">{{ currentDate }}</span>
            </div>
            <div class="progress-ring-container">
              <svg class="progress-ring" width="120" height="120">
                <circle class="progress-ring-bg" cx="60" cy="60" r="52"/>
                <circle class="progress-ring-fill" cx="60" cy="60" r="52" :style="{ strokeDashoffset: progressOffset }"/>
              </svg>
              <div class="progress-text">
                <span class="progress-value">78</span>
                <span class="progress-unit">%</span>
              </div>
            </div>
            <div class="progress-label">学习进度</div>
          </div>

          <div class="glass-card mini-card mini-card-1">
            <div class="mini-card-icon icon-blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <div class="mini-card-content">
              <span class="mini-card-value">128</span>
              <span class="mini-card-label">已做题目</span>
            </div>
          </div>

          <div class="glass-card mini-card mini-card-2">
            <div class="mini-card-icon icon-green">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="23,6 13.5,15.5 8.5,10.5 1,18"/>
                <polyline points="17,6 23,6 23,12"/>
              </svg>
            </div>
            <div class="mini-card-content">
              <span class="mini-card-value">78%</span>
              <span class="mini-card-label">正确率</span>
            </div>
          </div>

          <div class="glass-card mini-card mini-card-3">
            <div class="mini-card-icon icon-purple">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12,6 12,12 16,14"/>
              </svg>
            </div>
            <div class="mini-card-content">
              <span class="mini-card-value">12.5h</span>
              <span class="mini-card-label">学习时长</span>
            </div>
          </div>

          <div class="glass-card mini-card mini-card-4">
            <div class="mini-card-icon icon-orange">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
              </svg>
            </div>
            <div class="mini-card-content">
              <span class="mini-card-value">良好</span>
              <span class="mini-card-label">掌握程度</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 后端状态卡片 -->
    <!-- <section class="status-section">
      <div class="container">
        <div class="status-card" :class="healthStatus">
          <div class="status-left">
            <div class="status-indicator">
              <span class="status-dot"></span>
              <span class="status-icon-wrapper" v-if="healthStatus === 'success'">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <polyline points="20,6 9,17 4,12"/>
                </svg>
              </span>
              <span class="status-icon-wrapper error" v-else-if="healthStatus === 'error'">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                  <line x1="18" y1="6" x2="6" y2="18"/>
                  <line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </span>
              <span class="status-icon-wrapper loading" v-else>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M12 6v6l4 2"/>
                </svg>
              </span>
            </div>
            <div class="status-text">
              <span class="status-title">
                {{ healthStatus === 'loading' ? '正在连接后端...' : 
                   healthStatus === 'success' ? '后端连接正常' : '连接失败' }}
              </span>
              <span class="status-desc">
                {{ healthStatus === 'loading' ? '检查服务状态中...' :
                   healthStatus === 'success' ? backendMessage : errorMessage }}
              </span>
            </div>
          </div>
          <div class="status-decoration">
            <div class="decoration-bars">
              <span></span><span></span><span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
    </section> -->

    <!-- 功能区 -->
    <section class="features-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">系统功能</h2>
          <p class="section-desc">完整的学习工具，助力高效备考</p>
        </div>
        <div class="features-grid">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="feature-card"
            :class="{ clickable: feature.path }"
            @click="feature.path && $router.push(feature.path)"
          >
            <div class="feature-icon-wrap" :style="{ background: feature.bgColor }">
              <component :is="feature.icon" />
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.desc }}</p>
            <div class="feature-arrow">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12,5 19,12 12,19"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 学习进度区 -->
    <section class="progress-section">
      <div class="container">
        <div class="progress-wrapper">
          <div class="progress-header">
            <h2 class="section-title">学习进度</h2>
            <p class="section-desc">全面追踪你的408备考之旅</p>
          </div>
          <div class="subject-tabs">
            <template v-if="!subjectsLoading">
              <button
                v-for="(subject, index) in subjects"
                :key="index"
                class="subject-tab"
                :class="{ active: activeSubject === index }"
                @click="activeSubject = index"
              >
                <span class="subject-dot" :style="{ background: subject.color }"></span>
                {{ subject.name }}
              </button>
            </template>
            <template v-else>
              <div class="skeleton skeleton-tab"></div>
              <div class="skeleton skeleton-tab"></div>
              <div class="skeleton skeleton-tab"></div>
              <div class="skeleton skeleton-tab"></div>
            </template>
          </div>
          <div class="subject-detail">
            <template v-if="!subjectsLoading && subjects.length > 0">
            <div class="subject-progress-info">
              <div class="subject-stat">
                <span class="subject-stat-value">{{ subjects[activeSubject]?.completed ?? '--' }}</span>
                <span class="subject-stat-label">累计做题数</span>
              </div>
              <div class="subject-stat">
                <span class="subject-stat-value">{{ subjects[activeSubject]?.accuracy ?? '--' }}%</span>
                <span class="subject-stat-label">正确率</span>
              </div>
              <div class="subject-stat">
                <span class="subject-stat-value">{{ subjects[activeSubject]?.total ?? '--' }}</span>
                <span class="subject-stat-label">总题目数</span>
              </div>
            </div>
            <div class="subject-progress-bar">
              <div
                class="progress-fill"
                :style="{
                  width: (subjects[activeSubject]?.progress ?? 0) + '%',
                  background: subjects[activeSubject]?.color ?? '#667eea'
                }"
              ></div>
            </div>
            </template>
            <div v-else class="subject-loading">
              <div class="skeleton skeleton-stat"></div>
              <div class="skeleton skeleton-stat"></div>
              <div class="skeleton skeleton-stat"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 底部装饰 -->
    <div class="bottom-decoration">
      <div class="deco-blob deco-blob-1"></div>
      <div class="deco-blob deco-blob-2"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { healthAPI, getCourses, getCourseStats } from '@/api'

const router = useRouter()

// 当前日期
const currentDate = computed(() => {
  const now = new Date()
  return `${now.getMonth() + 1}月${now.getDate()}日 ${['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.getDay()]}`
})

// 学习进度环形图偏移
const progressOffset = computed(() => {
  const circumference = 2 * Math.PI * 52
  return circumference - (78 / 100) * circumference
})

// 健康状态
const healthStatus = ref('loading')
const backendMessage = ref('')
const errorMessage = ref('')

// 功能卡片
const QuestionBankIcon = {
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
    h('path', { d: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20' }),
    h('path', { d: 'M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z' }),
    h('line', { x1: '8', y1: '6', x2: '16', y2: '6' }),
    h('line', { x1: '8', y1: '10', x2: '14', y2: '10' })
  ])
}

const PracticeIcon = {
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
    h('path', { d: 'M12 20h9' }),
    h('path', { d: 'M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z' })
  ])
}

const AnalysisIcon = {
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
    h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }),
    h('polyline', { points: '14,2 14,8 20,8' }),
    h('line', { x1: '16', y1: '13', x2: '8', y2: '13' }),
    h('line', { x1: '16', y1: '17', x2: '8', y2: '17' }),
    h('polyline', { points: '10,9 9,9 8,9' })
  ])
}

const WrongBookIcon = {
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
    h('path', { d: 'M4 19.5A2.5 2.5 0 0 1 6.5 17H20' }),
    h('path', { d: 'M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z' }),
    h('line', { x1: '12', y1: '6', x2: '12', y2: '12' }),
    h('line', { x1: '12', y1: '16', x2: '12.01', y2: '16' })
  ])
}

const FavoriteIcon = {
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
    h('polygon', { points: '12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26' })
  ])
}

const StudyCenterIcon = {
  render: () => h('svg', { viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', 'stroke-width': '2' }, [
    h('line', { x1: '18', y1: '20', x2: '18', y2: '10' }),
    h('line', { x1: '12', y1: '20', x2: '12', y2: '4' }),
    h('line', { x1: '6', y1: '20', x2: '6', y2: '14' })
  ])
}

const features = [
  {
    icon: QuestionBankIcon,
    title: '题库浏览',
    desc: '按科目分类，支持多维度筛选题目',
    path: '/question-bank',
    bgColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  },
  {
    icon: PracticeIcon,
    title: '在线练习',
    desc: '随时随地练习真题，模拟真实考试',
    path: '/practice-home',
    bgColor: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
  },
  {
    icon: AnalysisIcon,
    title: '思维导图',
    desc: '详细解析帮助理解，深入掌握知识点',
    path: '/mindmap',
    bgColor: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
  },
  {
    icon: WrongBookIcon,
    title: '错题本',
    desc: '自动收录错题，针对性复习薄弱点',
    path: '/wrong-questions',
    bgColor: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  },
  {
    icon: FavoriteIcon,
    title: '收藏夹',
    desc: '收藏重要题目，方便日后回顾复习',
    path: '/favorites',
    bgColor: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
  },
  {
    icon: StudyCenterIcon,
    title: '学习中心',
    desc: '追踪学习进度，数据化分析能力',
    path: '/study-center',
    bgColor: 'linear-gradient(135deg, #d299c2 0%, #fef9d7 100%)'
  }
]

// 科目颜色映射
const subjectColors = ['#667eea', '#f093fb', '#4facfe', '#43e97b']

// 当前选中的科目索引
const activeSubject = ref(0)

// 科目数据（动态加载）
const subjects = ref([])

// 监听 subjects 变化，确保 activeSubject 不越界
watch(subjects, (newSubjects) => {
  if (newSubjects.length > 0 && activeSubject.value >= newSubjects.length) {
    activeSubject.value = 0
  }
})
const subjectsLoading = ref(true)

// 动态获取科目数据
const loadSubjectsData = async () => {
  try {
    const [coursesRes, statsRes] = await Promise.all([
      getCourses(),
      getCourseStats(true)
    ])

    subjects.value = (coursesRes.data || []).map(course => {
      const stat = (statsRes.data || []).find(s => s.course_id === course.id) || {}
      const answeredCount = stat.answered_count || 0
      const total = course.question_count || 0
      const accuracy = answeredCount > 0
        ? Math.round((stat.correct_count || 0) / answeredCount * 100)
        : 0
      const progress = total > 0 ? Math.round(answeredCount / total * 100) : 0
      return {
        name: course.name,
        color: course.color || subjectColors[(coursesRes.data || []).indexOf(course) % subjectColors.length],
        completed: answeredCount,
        accuracy: accuracy,
        total: total,
        progress: Math.min(progress, 100)
      }
    })
  } catch (error) {
    console.error('加载科目数据失败:', error)
    subjects.value = []
  } finally {
    subjectsLoading.value = false
  }
}

// 路由跳转
const goToPractice = () => {
  router.push('/practice-home')
}

const goToQuestionBank = () => {
  router.push('/question-bank')
}

// 检查后端状态
onMounted(async () => {
  try {
    const res = await healthAPI.check()
    healthStatus.value = 'success'
    backendMessage.value = res.message || 'Backend is running'
  } catch (error) {
    healthStatus.value = 'error'
    errorMessage.value = error.message || '无法连接到后端服务'
  }
  loadSubjectsData()
})
</script>

<style scoped>
/* 页面容器 */
.home-page {
  min-height: calc(100vh - 68px);
  position: relative;
  overflow: hidden;
}

/* 通用容器 */
.container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
}

/* ==================== Hero 区域 ==================== */
.hero-section {
  position: relative;
  padding: 60px 0 80px;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.hero-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.hero-blob-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  top: -200px;
  right: -100px;
  opacity: 0.15;
}

.hero-blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: -100px;
  left: -50px;
  opacity: 0.12;
}

.hero-blob-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  top: 50%;
  left: 30%;
  opacity: 0.1;
}

.hero-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 32px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  position: relative;
  z-index: 1;
}

/* Hero 左侧内容 */
.hero-content {
  animation: fadeInUp 0.8s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.2);
  border-radius: 50px;
  font-size: 13px;
  color: #667eea;
  font-weight: 500;
  margin-bottom: 24px;
}

.hero-badge svg {
  width: 14px;
  height: 14px;
}

.hero-title {
  font-size: 56px;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 16px;
  color: #1a1a2e;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 24px;
  font-weight: 500;
  color: #606266;
  margin-bottom: 20px;
  letter-spacing: 2px;
}

.hero-desc {
  font-size: 16px;
  color: #909399;
  line-height: 1.8;
  margin-bottom: 36px;
}

.hero-buttons {
  display: flex;
  gap: 16px;
  margin-bottom: 40px;
}

.btn-primary-gradient {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border-radius: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.35);
}

.btn-primary-gradient svg {
  width: 18px;
  height: 18px;
}

.btn-primary-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.45);
}

.btn-secondary-outline {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  background: rgba(255, 255, 255, 0.9);
  color: #667eea;
  font-size: 16px;
  font-weight: 600;
  border-radius: 14px;
  border: 2px solid rgba(102, 126, 234, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary-outline svg {
  width: 18px;
  height: 18px;
}

.btn-secondary-outline:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.05);
  transform: translateY(-2px);
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: rgba(0, 0, 0, 0.1);
}

/* Hero 右侧视觉区域 */
.hero-visual {
  position: relative;
  height: 400px;
  animation: fadeInUp 0.8s ease 0.2s both;
}

.glass-card {
  position: absolute;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.12);
}

.main-card {
  width: 260px;
  height: 280px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.card-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.card-icon {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon-purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-icon-purple svg {
  width: 18px;
  height: 18px;
  color: #fff;
}

.card-date {
  font-size: 12px;
  color: #909399;
}

.progress-ring-container {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 12px;
}

.progress-ring {
  transform: rotate(-90deg);
}

.progress-ring-bg {
  fill: none;
  stroke: #f0f0f0;
  stroke-width: 8;
}

.progress-ring-fill {
  fill: none;
  stroke: url(#progressGradient);
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 326.73;
  transition: stroke-dashoffset 1s ease;
}

.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.progress-value {
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.progress-unit {
  font-size: 16px;
  color: #909399;
}

.progress-label {
  font-size: 13px;
  color: #909399;
}

/* Mini 卡片 */
.mini-card {
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.mini-card-1 {
  top: 10px;
  left: 10px;
  animation: float 3s ease-in-out infinite;
}

.mini-card-2 {
  top: 60px;
  right: 0;
  animation: float 3s ease-in-out infinite 0.5s;
}

.mini-card-3 {
  bottom: 60px;
  left: 0;
  animation: float 3s ease-in-out infinite 1s;
}

.mini-card-4 {
  bottom: 10px;
  right: 10px;
  animation: float 3s ease-in-out infinite 1.5s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

.mini-card-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mini-card-icon svg {
  width: 20px;
  height: 20px;
  color: #fff;
}

.icon-blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.icon-green {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.icon-purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.icon-orange {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.mini-card-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.mini-card-value {
  font-size: 18px;
  font-weight: 700;
  color: #303133;
}

.mini-card-label {
  font-size: 12px;
  color: #909399;
}

/* ==================== 状态卡片 ==================== */
.status-section {
  padding: 0 0 40px;
}

.status-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 20px 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.status-card.success {
  border-color: rgba(103, 194, 58, 0.3);
}

.status-card.error {
  border-color: rgba(245, 108, 108, 0.3);
}

.status-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.status-indicator {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success .status-indicator {
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.15), rgba(103, 194, 58, 0.05));
}

.error .status-indicator {
  background: linear-gradient(135deg, rgba(245, 108, 108, 0.15), rgba(245, 108, 108, 0.05));
}

.loading .status-indicator {
  background: linear-gradient(135deg, rgba(230, 162, 60, 0.15), rgba(230, 162, 60, 0.05));
}

.status-dot {
  position: absolute;
  top: -2px;
  right: -2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid #fff;
}

.success .status-dot {
  background: #67c23a;
}

.error .status-dot {
  background: #f56c6c;
}

.loading .status-dot {
  background: #e6a23c;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.status-icon-wrapper {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-icon-wrapper svg {
  width: 20px;
  height: 20px;
}

.success .status-icon-wrapper {
  color: #67c23a;
}

.error .status-icon-wrapper {
  color: #f56c6c;
}

.loading .status-icon-wrapper {
  color: #e6a23c;
  animation: spin 1s linear infinite;
}

.loading .status-icon-wrapper svg {
  width: 20px;
  height: 20px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.status-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.status-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.status-desc {
  font-size: 13px;
  color: #909399;
}

.status-decoration {
  display: flex;
  align-items: center;
}

.decoration-bars {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 32px;
}

.decoration-bars span {
  width: 4px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
  opacity: 0.3;
}

.decoration-bars span:nth-child(1) { height: 40%; animation: barPulse 1.5s infinite; }
.decoration-bars span:nth-child(2) { height: 70%; animation: barPulse 1.5s infinite 0.2s; }
.decoration-bars span:nth-child(3) { height: 50%; animation: barPulse 1.5s infinite 0.4s; }
.decoration-bars span:nth-child(4) { height: 85%; animation: barPulse 1.5s infinite 0.6s; }
.decoration-bars span:nth-child(5) { height: 60%; animation: barPulse 1.5s infinite 0.8s; }

@keyframes barPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.7; }
}

/* ==================== 功能区 ==================== */
.features-section {
  padding: 20px 0 60px;
}

.section-header {
  text-align: center;
  margin-bottom: 48px;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 12px;
}

.section-desc {
  font-size: 16px;
  color: #909399;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  padding: 32px;
  position: relative;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.feature-card.clickable {
  cursor: pointer;
}

.feature-card.clickable:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.2);
}

.feature-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.feature-icon-wrap :deep(svg) {
  width: 28px;
  height: 28px;
  color: #fff;
}

.feature-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.feature-desc {
  font-size: 14px;
  color: #909399;
  line-height: 1.6;
}

.feature-arrow {
  position: absolute;
  bottom: 24px;
  right: 24px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(102, 126, 234, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: translateX(-8px);
  transition: all 0.3s ease;
}

.feature-card.clickable:hover .feature-arrow {
  opacity: 1;
  transform: translateX(0);
}

.feature-arrow svg {
  width: 16px;
  height: 16px;
  color: #667eea;
}

/* ==================== 学习进度区 ==================== */
.progress-section {
  padding: 40px 0 80px;
}

.progress-wrapper {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
  border-radius: 24px;
  padding: 48px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.progress-header {
  text-align: center;
  margin-bottom: 36px;
}

.progress-header .section-title {
  margin-bottom: 8px;
}

.subject-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 36px;
  flex-wrap: wrap;
}

.subject-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.8);
  border-radius: 50px;
  font-size: 14px;
  font-weight: 500;
  color: #606266;
  cursor: pointer;
  transition: all 0.3s ease;
}

.subject-tab:hover {
  background: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.subject-tab.active {
  background: #fff;
  border-color: transparent;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  color: #303133;
}

.subject-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.subject-detail {
  max-width: 600px;
  margin: 0 auto;
}

.subject-progress-info {
  display: flex;
  justify-content: center;
  gap: 48px;
  margin-bottom: 24px;
}

.subject-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.subject-stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
}

.subject-stat-label {
  font-size: 13px;
  color: #909399;
}

.subject-progress-bar {
  height: 8px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

.subject-loading {
  display: flex;
  gap: 32px;
  justify-content: center;
  align-items: center;
  height: 120px;
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 6px;
}

.skeleton-stat {
  width: 80px;
  height: 60px;
}

.skeleton-tab {
  width: 100px;
  height: 36px;
}

@keyframes skeleton-shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ==================== 底部装饰 ==================== */
.bottom-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 200px;
  pointer-events: none;
  overflow: hidden;
}

.deco-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.15;
}

.deco-blob-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  bottom: -100px;
  left: 10%;
}

.deco-blob-2 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: -50px;
  right: 15%;
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 1024px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 40px;
  }

  .hero-visual {
    height: 350px;
  }

  .hero-title {
    font-size: 42px;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 0 60px;
  }

  .hero-container {
    padding: 0 20px;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .hero-stats {
    flex-wrap: wrap;
    gap: 20px;
  }

  .container {
    padding: 0 20px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .feature-card {
    padding: 24px;
  }

  .progress-wrapper {
    padding: 32px 24px;
  }

  .subject-tabs {
    flex-direction: column;
    align-items: center;
  }

  .subject-progress-info {
    gap: 24px;
  }

  .status-card {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }

  .status-left {
    flex-direction: column;
  }
}
</style>
