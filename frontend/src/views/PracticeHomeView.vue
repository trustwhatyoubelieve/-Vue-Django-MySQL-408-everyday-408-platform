<template>
  <div class="practice-home-page">
    <!-- 背景装饰 -->
    <div class="page-bg">
      <div class="bg-blob bg-blob-1"></div>
      <div class="bg-blob bg-blob-2"></div>
      <div class="bg-blob bg-blob-3"></div>
    </div>

    <div class="page-container">
      <!-- 左侧：导航面板 -->
      <aside class="sidebar-panel">
        <div class="sidebar-card">
          <div class="sidebar-header">
            <div class="sidebar-logo">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect width="24" height="24" rx="6" fill="url(#phGrad)"/>
                <path d="M6 8h12M6 12h8M6 16h10" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
                <defs>
                  <linearGradient id="phGrad" x1="0" y1="0" x2="24" y2="24">
                    <stop offset="0%" stop-color="#667eea"/>
                    <stop offset="100%" stop-color="#764ba2"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <div class="header-text">
              <h3>选择练习内容</h3>
              <p>408 科目全覆盖</p>
            </div>
          </div>

          <!-- 课程列表 -->
          <div class="nav-section">
            <div class="nav-section-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              课程
            </div>
            <div class="nav-list">
              <div
                v-for="course in courses"
                :key="course.id"
                class="nav-item"
                :class="{ active: selectedCourse?.id === course.id }"
                @click="selectCourse(course)"
              >
                <span class="nav-indicator"></span>
                <span class="nav-text">{{ course.name }}</span>
              </div>
              <div v-if="courses.length === 0" class="nav-empty">暂无课程</div>
            </div>
          </div>

          <!-- 章节列表 -->
          <div v-if="selectedCourse" class="nav-section">
            <div class="nav-section-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="8" y1="6" x2="21" y2="6"/>
                <line x1="8" y1="12" x2="21" y2="12"/>
                <line x1="8" y1="18" x2="21" y2="18"/>
                <line x1="3" y1="6" x2="3.01" y2="6"/>
                <line x1="3" y1="12" x2="3.01" y2="12"/>
                <line x1="3" y1="18" x2="3.01" y2="18"/>
              </svg>
              章节
            </div>
            <div class="nav-list">
              <div
                v-for="chapter in chapters"
                :key="chapter.id"
                class="nav-item"
                :class="{ active: selectedChapter?.id === chapter.id }"
                @click="selectChapter(chapter)"
              >
                <span class="nav-indicator"></span>
                <span class="nav-text">{{ chapter.name }}</span>
              </div>
              <div v-if="chapters.length === 0" class="nav-empty">暂无章节</div>
            </div>
          </div>

          <!-- 子章节列表 -->
          <div v-if="selectedChapter" class="nav-section">
            <div class="nav-section-label">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9,18 15,12 9,6"/>
              </svg>
              小节
            </div>
            <div class="nav-list">
              <div
                v-for="sc in subchapters"
                :key="sc.id"
                class="nav-item sub-nav-item"
                :class="{ active: selectedSubchapter?.id === sc.id }"
                @click="selectSubChapter(sc)"
              >
                <span class="nav-text">{{ sc.name }}</span>
                <span class="nav-count">{{ sc.answered_count > 0 ? sc.answered_count + ' / ' + sc.question_count : sc.question_count }}</span>
              </div>
              <div v-if="subchapters.length === 0" class="nav-empty">暂无小节</div>
            </div>
          </div>
        </div>
      </aside>

      <!-- 右侧：练习内容区 -->
      <main class="main-panel">
        <!-- 未选择子章节 -->
        <div v-if="!selectedSubchapter" class="empty-state">
          <div class="empty-illustration">
            <svg viewBox="0 0 200 200" fill="none">
              <!-- 背景圆 -->
              <circle cx="100" cy="100" r="80" fill="url(#emptyGrad)" opacity="0.1"/>
              <circle cx="100" cy="100" r="60" fill="url(#emptyGrad)" opacity="0.15"/>
              <!-- 书本图标 -->
              <rect x="60" y="70" width="80" height="60" rx="4" fill="#667eea" opacity="0.3"/>
              <rect x="65" y="75" width="70" height="50" rx="3" fill="white"/>
              <line x1="75" y1="88" x2="125" y2="88" stroke="#667eea" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
              <line x1="75" y1="98" x2="115" y2="98" stroke="#667eea" stroke-width="2" stroke-linecap="round" opacity="0.4"/>
              <line x1="75" y1="108" x2="120" y2="108" stroke="#667eea" stroke-width="2" stroke-linecap="round" opacity="0.3"/>
              <!-- 装饰点 -->
              <circle cx="50" cy="60" r="4" fill="#667eea" opacity="0.3"/>
              <circle cx="150" cy="80" r="3" fill="#764ba2" opacity="0.3"/>
              <circle cx="140" cy="140" r="5" fill="#667eea" opacity="0.2"/>
              <defs>
                <linearGradient id="emptyGrad" x1="0" y1="0" x2="200" y2="200">
                  <stop offset="0%" stop-color="#667eea"/>
                  <stop offset="100%" stop-color="#764ba2"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <h3>选择练习内容</h3>
          <p>在左侧选择课程、章节和小节后<br/>即可开始针对性练习</p>
          <div class="quick-tips">
            <div class="tip-item">
              <span class="tip-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>
                </svg>
              </span>
              <span>按章节练习</span>
            </div>
            <div class="tip-item">
              <span class="tip-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                </svg>
              </span>
              <span>专项突破</span>
            </div>
            <div class="tip-item">
              <span class="tip-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12,6 12,12 16,14"/>
                </svg>
              </span>
              <span>计时练习</span>
            </div>
          </div>
        </div>

        <!-- 已选子章节 - 有题目 -->
        <div v-else-if="selectedSubchapter && selectedSubchapter.question_count > 0" class="practice-panel">
          <!-- 面包屑 -->
          <div class="breadcrumb">
            <span class="breadcrumb-item">{{ selectedCourse?.name }}</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9,18 15,12 9,6"/>
            </svg>
            <span class="breadcrumb-item">{{ selectedChapter?.name }}</span>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9,18 15,12 9,6"/>
            </svg>
            <span class="breadcrumb-item current">{{ selectedSubchapter.name }}</span>
          </div>

          <!-- 主内容卡片 -->
          <div class="content-card">
            <div class="card-header-section">
              <div class="card-title-group">
                <div class="card-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
                  </svg>
                </div>
                <div>
                  <h2>{{ selectedSubchapter.name }}</h2>
                  <p>408 计算机学科专业基础 · 专项练习</p>
                </div>
              </div>
            </div>

            <!-- 统计信息 -->
            <div class="stats-grid">
              <div class="stat-card">
                <div class="stat-icon blue">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                  </svg>
                </div>
                <div class="stat-content">
                  <span class="stat-value">{{ selectedSubchapter.question_count }}</span>
                  <span class="stat-label">题目数量</span>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon purple">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>
                    <line x1="12" y1="17" x2="12.01" y2="17"/>
                  </svg>
                </div>
                <div class="stat-content">
                  <span class="stat-value">{{ singleChoiceCount }}</span>
                  <span class="stat-label">单选题</span>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon orange">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14,2 14,8 20,8"/>
                    <line x1="16" y1="13" x2="8" y2="13"/>
                    <line x1="16" y1="17" x2="8" y2="17"/>
                  </svg>
                </div>
                <div class="stat-content">
                  <span class="stat-value">{{ bigQuestionCount }}</span>
                  <span class="stat-label">大题</span>
                </div>
              </div>

              <div class="stat-card">
                <div class="stat-icon green">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <polyline points="12,6 12,12 16,14"/>
                  </svg>
                </div>
                <div class="stat-content">
                  <span class="stat-value">~{{ estimatedMinutes }}</span>
                  <span class="stat-label">预计分钟</span>
                </div>
              </div>
            </div>

            <!-- 进度指示 -->
            <div class="progress-section">
              <div class="progress-header">
                <span class="progress-label">学习进度</span>
                <span class="progress-value">{{ progressText }}</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
              </div>
            </div>

            <!-- 开始按钮 -->
            <div class="action-section">
              <button class="btn-start" @click="startPractice">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5,3 19,12 5,21"/>
                </svg>
                开始练习
              </button>
              <p class="action-tip">共 {{ selectedSubchapter.question_count }} 题，完成后查看详细报告</p>
            </div>
          </div>

          <!-- 知识点提示 -->
          <div class="tips-section">
            <div class="tip-card">
              <div class="tip-icon-wrapper">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
              </div>
              <div class="tip-content">
                <h4>练习建议</h4>
                <p>建议先通读知识点，再进行针对性练习，效果更佳</p>
              </div>
            </div>
            <div class="tip-card">
              <div class="tip-icon-wrapper purple">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                </svg>
              </div>
              <div class="tip-content">
                <h4>答题技巧</h4>
                <p>认真阅读题干，注意区分相似选项，三思而后答</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 已选子章节 - 无题目 -->
        <div v-else class="empty-state">
          <div class="empty-illustration">
            <svg viewBox="0 0 200 200" fill="none">
              <circle cx="100" cy="100" r="80" fill="#fef0f0" opacity="0.5"/>
              <text x="100" y="110" text-anchor="middle" font-size="48">📭</text>
            </svg>
          </div>
          <h3>该小节暂无题目</h3>
          <p>请联系管理员添加题目<br/>或选择其他小节进行练习</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  getCourses,
  getChaptersByCourse,
  getSubChaptersByChapter,
  getQuestionsBySubChapter,
} from '@/api/questionBank'
import { getSubChapterStats } from '@/api/stats'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 状态
const courses = ref([])
const chapters = ref([])
const subchapters = ref([])

const selectedCourse = ref(null)
const selectedChapter = ref(null)
const selectedSubchapter = ref(null)
const subchapterQuestions = ref([])
const chapterStats = ref([]) // 当前章节的统计（包含各子章节进度）

// 题型统计
const singleChoiceCount = computed(() =>
  subchapterQuestions.value.filter(q => q.question_type === 'single_choice').length
)
const bigQuestionCount = computed(() =>
  subchapterQuestions.value.filter(q => q.question_type === 'big_question').length
)

// 估算时间（每题约1分钟）
const estimatedMinutes = computed(() => Math.max(1, Math.round(selectedSubchapter.value?.question_count || 0)))

// 当前子章节的真实进度
const currentSubchapterProgress = computed(() => {
  const total = selectedSubchapter.value?.question_count || 0
  const answered = selectedSubchapter.value?.answered_count || 0
  const percent = total > 0 ? Math.round(answered / total * 100) : 0
  return { total, answered, percent }
})

// 进度百分比（驱动进度条）
const progressPercent = computed(() => currentSubchapterProgress.value.percent)

// 进度文字描述
const progressText = computed(() => {
  const { answered, total, percent } = currentSubchapterProgress.value
  if (total === 0) return '暂无题目'
  if (answered === 0) return '尚未开始'
  return `已做 ${answered} / ${total} 题 (${percent}%)`
})

// 加载课程
const loadCourses = async () => {
  try {
    const res = await getCourses()
    courses.value = res.data || []
    if (courses.value.length > 0) {
      selectCourse(courses.value[0])
    }
  } catch (e) {
    console.error('加载课程失败', e)
  }
}

// 选择课程
const selectCourse = async (course) => {
  selectedCourse.value = course
  selectedChapter.value = null
  selectedSubchapter.value = null
  chapters.value = []
  subchapters.value = []
  subchapterQuestions.value = []

  try {
    const res = await getChaptersByCourse(course.id)
    chapters.value = res.data || []
    if (chapters.value.length > 0) {
      selectChapter(chapters.value[0])
    }
  } catch (e) {
    console.error('加载章节失败', e)
  }
}

// 选择章节
const selectChapter = async (chapter) => {
  selectedChapter.value = chapter
  selectedSubchapter.value = null
  subchapters.value = []
  subchapterQuestions.value = []

  try {
    const [scRes, statsRes] = await Promise.all([
      getSubChaptersByChapter(chapter.id),
      getSubChapterStats(chapter.id, true)
    ])
    subchapters.value = scRes.data || []
    // 建立 subchapter_id -> stats 的映射，方便快速查找
    chapterStats.value = statsRes.data || []
    // 把已作答数回填到子章节列表（侧边栏显示用）
    subchapters.value.forEach(sc => {
      const stat = chapterStats.value.find(s => s.subchapter_id === sc.id)
      if (stat) {
        sc.answered_count = stat.answered_count
      }
    })
    if (subchapters.value.length > 0) {
      selectSubChapter(subchapters.value[0])
    }
  } catch (e) {
    console.error('加载子章节失败', e)
  }
}

// 根据子章节ID查找章节统计
const getSubchapterStats = (subchapterId) => {
  return chapterStats.value.find(s => s.subchapter_id === subchapterId) || {}
}

// 选择子章节，加载题目统计
const selectSubChapter = async (sc) => {
  try {
    const res = await getQuestionsBySubChapter(sc.id)
    subchapterQuestions.value = res.data || []
    const answeredCount = getSubchapterStats(sc.id).answered_count || 0
    // 优先用 API 返回的题目数，API 失败时 fallback 到元数据的 question_count
    const totalQuestions = subchapterQuestions.value.length || sc.question_count || 0
    selectedSubchapter.value = {
      ...sc,
      question_count: totalQuestions,
      answered_count: answeredCount
    }
  } catch (e) {
    console.error('加载题目列表失败', e)
    // API 失败时仍用元数据展示
    const answeredCount = getSubchapterStats(sc.id).answered_count || 0
    selectedSubchapter.value = {
      ...sc,
      question_count: sc.question_count || 0,
      answered_count: answeredCount
    }
  }
}

// 开始练习
const startPractice = () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  if (selectedSubchapter.value) {
    router.push(`/practice/${selectedSubchapter.value.id}`)
  }
}

onMounted(() => {
  loadCourses()
})
</script>

<style scoped>
/* 页面容器 */
.practice-home-page {
  min-height: calc(100vh - 68px);
  position: relative;
  padding: 24px 0;
}

/* 背景装饰 */
.page-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

.bg-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
}

.bg-blob-1 {
  width: 600px;
  height: 600px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  top: -200px;
  right: -150px;
}

.bg-blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: -100px;
  left: -50px;
  opacity: 0.3;
}

.bg-blob-3 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  top: 40%;
  left: 40%;
  opacity: 0.15;
}

/* 主容器 */
.page-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 24px;
  position: relative;
  z-index: 1;
}

/* ==================== 左侧导航面板 ==================== */
.sidebar-panel {
  position: sticky;
  top: 92px;
  height: fit-content;
  max-height: calc(100vh - 116px);
  overflow-y: auto;
}

.sidebar-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding-bottom: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.sidebar-logo {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.header-text h3 {
  font-size: 16px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 2px;
}

.header-text p {
  font-size: 12px;
  color: #909399;
}

/* 导航区块 */
.nav-section {
  margin-bottom: 20px;
}

.nav-section:last-child {
  margin-bottom: 0;
}

.nav-section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #909399;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
  padding-left: 4px;
}

.nav-section-label svg {
  width: 14px;
  height: 14px;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
}

.nav-item:hover {
  background: rgba(102, 126, 234, 0.06);
}

.nav-item.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(118, 75, 162, 0.12) 100%);
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 24px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 0 3px 3px 0;
}

.nav-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #dcdfe6;
  transition: all 0.25s ease;
}

.nav-item.active .nav-indicator {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 0 8px rgba(102, 126, 234, 0.4);
}

.nav-text {
  font-size: 14px;
  color: #606266;
  flex: 1;
  transition: color 0.25s ease;
}

.nav-item:hover .nav-text,
.nav-item.active .nav-text {
  color: #667eea;
}

.sub-nav-item {
  padding: 10px 14px;
}

.nav-count {
  font-size: 12px;
  font-weight: 600;
  color: #67c23a;
  background: rgba(103, 194, 58, 0.1);
  padding: 3px 10px;
  border-radius: 12px;
}

.nav-empty {
  font-size: 13px;
  color: #c0c4cc;
  padding: 10px 14px;
}

/* ==================== 右侧主内容区 ==================== */
.main-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 40px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.8);
  text-align: center;
}

.empty-illustration {
  margin-bottom: 28px;
}

.empty-illustration svg {
  width: 200px;
  height: 200px;
}

.empty-state h3 {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 12px;
}

.empty-state p {
  font-size: 15px;
  color: #909399;
  line-height: 1.7;
  margin-bottom: 32px;
}

.quick-tips {
  display: flex;
  gap: 24px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: rgba(102, 126, 234, 0.06);
  border-radius: 12px;
}

.tip-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tip-icon svg {
  width: 16px;
  height: 16px;
  color: #fff;
}

.tip-item span:last-child {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

/* 练习面板 */
.practice-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #909399;
}

.breadcrumb svg {
  width: 14px;
  height: 14px;
}

.breadcrumb-item {
  transition: color 0.2s;
}

.breadcrumb-item:hover {
  color: #667eea;
  cursor: pointer;
}

.breadcrumb-item.current {
  color: #667eea;
  font-weight: 600;
}

/* 主内容卡片 */
.content-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 28px;
  padding: 36px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.card-header-section {
  margin-bottom: 32px;
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 18px;
}

.card-icon {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.card-icon svg {
  width: 32px;
  height: 32px;
  color: #fff;
}

.card-title-group h2 {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 6px;
}

.card-title-group p {
  font-size: 14px;
  color: #909399;
}

/* 统计网格 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px;
  background: #f9fafb;
  border-radius: 16px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
  color: #fff;
}

.stat-icon.blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.stat-icon.purple { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.orange { background: linear-gradient(135deg, #fa709a, #fee140); }
.stat-icon.green { background: linear-gradient(135deg, #43e97b, #38f9d7); }

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

/* 进度指示 */
.progress-section {
  margin-bottom: 32px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.progress-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.progress-value {
  font-size: 14px;
  color: #667eea;
  font-weight: 600;
}

.progress-bar {
  height: 8px;
  background: #f0f2f8;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.6s ease;
}

/* 开始按钮 */
.action-section {
  text-align: center;
}

.btn-start {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 18px 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  border: none;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 28px rgba(102, 126, 234, 0.4);
}

.btn-start svg {
  width: 22px;
  height: 22px;
}

.btn-start:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 36px rgba(102, 126, 234, 0.5);
}

.action-tip {
  font-size: 13px;
  color: #909399;
  margin-top: 16px;
}

/* 提示卡片 */
.tips-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.tip-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.tip-icon-wrapper {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tip-icon-wrapper.purple {
  background: linear-gradient(135deg, #f093fb, #f5576c);
}

.tip-icon-wrapper svg {
  width: 22px;
  height: 22px;
  color: #fff;
}

.tip-content h4 {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 6px;
}

.tip-content p {
  font-size: 13px;
  color: #909399;
  line-height: 1.5;
}

/* 滚动条 */
.sidebar-panel::-webkit-scrollbar {
  width: 4px;
}

.sidebar-panel::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-panel::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.2);
  border-radius: 2px;
}

/* 响应式 */
@media (max-width: 1024px) {
  .page-container {
    grid-template-columns: 1fr;
  }

  .sidebar-panel {
    position: static;
    max-height: none;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .tips-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .page-container {
    padding: 0 16px;
  }

  .sidebar-card,
  .content-card,
  .empty-state {
    padding: 20px;
  }

  .card-title-group {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }

  .card-title-group h2 {
    font-size: 22px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .quick-tips {
    flex-direction: column;
    gap: 12px;
  }

  .btn-start {
    width: 100%;
    justify-content: center;
  }
}
</style>
