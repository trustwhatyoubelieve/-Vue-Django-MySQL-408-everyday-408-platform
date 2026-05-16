<template>
  <div class="question-bank-page">
    <!-- 页面背景装饰 -->
    <div class="page-bg">
      <div class="bg-blob bg-blob-1"></div>
      <div class="bg-blob bg-blob-2"></div>
    </div>

    <div class="page-container">
      <!-- 第一栏：左侧导航面板 -->
      <aside class="sidebar-panel">
        <div class="sidebar-card">
          <!-- Logo/标题 -->
          <div class="sidebar-header">
            <div class="sidebar-logo">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect width="24" height="24" rx="6" fill="url(#sbGrad)"/>
                <path d="M6 8h12M6 12h8M6 16h10" stroke="white" stroke-width="1.5" stroke-linecap="round"/>
                <defs>
                  <linearGradient id="sbGrad" x1="0" y1="0" x2="24" y2="24">
                    <stop offset="0%" stop-color="#667eea"/>
                    <stop offset="100%" stop-color="#764ba2"/>
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <h3>题库导航</h3>
          </div>

          <!-- 课程列表 -->
          <div class="nav-section">
            <div class="nav-section-header">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              <span>课程</span>
            </div>
            <div class="nav-list">
              <div
                v-for="course in courses"
                :key="course.id"
                class="nav-item"
                :class="{ active: selectedCourse?.id === course.id }"
                @click="selectCourse(course)"
              >
                <span class="nav-item-dot"></span>
                <span class="nav-item-text">{{ course.name }}</span>
              </div>
              <div v-if="courses.length === 0" class="nav-empty">暂无课程</div>
            </div>
          </div>

          <!-- 章节列表 -->
          <div v-if="selectedCourse" class="nav-section">
            <div class="nav-section-header">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="8" y1="6" x2="21" y2="6"/>
                <line x1="8" y1="12" x2="21" y2="12"/>
                <line x1="8" y1="18" x2="21" y2="18"/>
                <line x1="3" y1="6" x2="3.01" y2="6"/>
                <line x1="3" y1="12" x2="3.01" y2="12"/>
                <line x1="3" y1="18" x2="3.01" y2="18"/>
              </svg>
              <span>章节</span>
            </div>
            <div class="nav-list">
              <div
                v-for="chapter in chapters"
                :key="chapter.id"
                class="nav-item"
                :class="{ active: selectedChapter?.id === chapter.id }"
                @click="selectChapter(chapter)"
              >
                <span class="nav-item-dot"></span>
                <span class="nav-item-text">{{ chapter.name }}</span>
              </div>
              <div v-if="chapters.length === 0" class="nav-empty">暂无章节</div>
            </div>
          </div>

          <!-- 子章节列表 -->
          <div v-if="selectedChapter" class="nav-section">
            <div class="nav-section-header">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="9,18 15,12 9,6"/>
              </svg>
              <span>小节</span>
            </div>
            <div class="nav-list">
              <div
                v-for="sc in subchapters"
                :key="sc.id"
                class="nav-item sub-nav-item"
                :class="{ active: selectedSubchapter?.id === sc.id }"
                @click="selectSubChapter(sc)"
              >
                <span class="nav-item-text">{{ sc.name }}</span>
                <span class="nav-count-badge">{{ sc.question_count }}</span>
              </div>
              <div v-if="subchapters.length === 0" class="nav-empty">暂无小节</div>
            </div>
          </div>
        </div>
      </aside>

      <!-- 第二栏：中间主内容区 -->
      <main class="main-panel">
        <!-- 题目列表区域 -->
        <div class="list-section">
          <!-- 列表头部 -->
          <div class="list-header">
            <div class="list-title-row">
              <h2 class="list-title">{{ selectedSubchapter?.name || '题目列表' }}</h2>
              <span class="list-count" v-if="questions.length > 0">{{ questions.length }} 道题</span>
            </div>
            <!-- 状态图例 -->
            <div v-if="questions.length > 0" class="status-legend">
              <span class="legend-dot correct"></span><span class="legend-text">已做对</span>
              <span class="legend-dot wrong"></span><span class="legend-text">已做错</span>
              <span class="legend-dot unattempted"></span><span class="legend-text">未作答</span>
            </div>
            <button
              v-if="selectedSubchapter && questions.length > 0"
              class="btn-start-practice"
              @click="onStartPractice"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="5,3 19,12 5,21"/>
              </svg>
              开始练习
            </button>
          </div>

          <!-- 空状态提示 -->
          <div v-if="!selectedSubchapter" class="list-empty">
            <div class="empty-illustration">
              <svg viewBox="0 0 120 120" fill="none">
                <circle cx="60" cy="60" r="50" fill="#f0f2f8"/>
                <rect x="35" y="40" width="50" height="40" rx="4" fill="#667eea" opacity="0.2"/>
                <rect x="40" y="48" width="30" height="4" rx="2" fill="#667eea" opacity="0.4"/>
                <rect x="40" y="56" width="40" height="4" rx="2" fill="#667eea" opacity="0.3"/>
                <rect x="40" y="64" width="25" height="4" rx="2" fill="#667eea" opacity="0.3"/>
              </svg>
            </div>
            <p class="empty-text">请在左侧选择课程、章节和小节</p>
          </div>

          <!-- 题目列表 -->
          <div v-else-if="questions.length > 0" class="question-cards">
            <div
              v-for="(q, index) in questions"
              :key="q.id"
              class="question-card-item"
              :class="{ active: selectedQuestion?.id === q.id }"
              @click="selectQuestion(q)"
            >
              <div class="qc-left">
                <span class="qc-index">{{ index + 1 }}</span>
                <span class="qc-status-dot" :class="q.practice_status"></span>
              </div>
              <div class="qc-content">
                <div class="qc-meta">
                  <span class="qc-id">{{ q.business_id }}</span>
                  <span class="qc-type-badge" :class="q.question_type">
                    {{ typeLabel(q.question_type) }}
                  </span>
                  <span v-if="q.stem_image" class="qc-img-tag">含图</span>
                </div>
                <p class="qc-preview">{{ q.stem_preview }}</p>
              </div>
              <div class="qc-arrow">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="9,18 15,12 9,6"/>
                </svg>
              </div>
            </div>
          </div>

          <div v-else class="list-empty">
            <div class="empty-illustration">
              <svg viewBox="0 0 120 120" fill="none">
                <circle cx="60" cy="60" r="50" fill="#fef0f0"/>
                <text x="60" y="68" text-anchor="middle" font-size="32">📭</text>
              </svg>
            </div>
            <p class="empty-text">该小节暂无题目</p>
          </div>
        </div>

        <!-- 题目详情区域 -->
        <div v-if="questionDetail" class="detail-section">
          <div class="detail-card">
            <!-- 详情头部 -->
            <div class="detail-header">
              <div class="detail-title-row">
                <div class="detail-id-badge">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                  </svg>
                  <span>{{ questionDetail.business_id }}</span>
                </div>
                <span class="detail-type-badge" :class="questionDetail.question_type">
                  {{ typeLabel(questionDetail.question_type) }}
                </span>
              </div>
              <div class="detail-path">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
                <span>{{ questionDetail.course_name }} > {{ questionDetail.chapter_name }} > {{ questionDetail.subchapter_name }}</span>
              </div>
              <button
                class="btn-favorite"
                :class="{ favorited: favoriteStatus.is_favorited }"
                @click.stop="toggleFavorite"
              >
                <svg v-if="!favoriteStatus.is_favorited" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
                </svg>
                <svg v-else viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                  <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
                </svg>
                {{ favoriteStatus.is_favorited ? '已收藏' : '收藏' }}
              </button>
            </div>

            <!-- 题干区域 -->
            <div class="detail-body">
              <div class="detail-section-block">
                <div class="section-label">
                  <span class="label-dot"></span>
                  题干
                </div>
                <div v-if="questionDetail.stem_text" class="section-content stem-text">
                  {{ questionDetail.stem_text }}
                </div>
                <img v-if="questionDetail.stem_image" :src="questionDetail.stem_image" class="section-image" />
              </div>

              <!-- 选项区域 -->
              <div v-if="questionDetail.question_type === 'single_choice' && questionOptions.length > 0" class="detail-section-block">
                <div class="section-label">
                  <span class="label-dot"></span>
                  选项
                </div>
                <div class="options-list">
                  <div
                    v-for="opt in questionOptions"
                    :key="opt.key"
                    class="option-item"
                    :class="{ correct: opt.key === questionDetail.correct_answer }"
                  >
                    <span class="option-key">{{ opt.key }}.</span>
                    <span v-if="opt.text" class="option-text">{{ opt.text }}</span>
                    <img v-if="opt.image" :src="opt.image" class="option-image" />
                  </div>
                </div>
              </div>

              <!-- 解析区域 -->
              <div v-if="questionDetail.analysis_text || questionDetail.analysis_image" class="detail-section-block analysis-block">
                <div class="section-label analysis-label">
                  <span class="label-dot"></span>
                  答案解析
                </div>
                <div v-if="questionDetail.analysis_text" class="section-content analysis-text">
                  {{ questionDetail.analysis_text }}
                </div>
                <img v-if="questionDetail.analysis_image" :src="questionDetail.analysis_image" class="section-image" />
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- 第三栏：右侧辅助面板 -->
      <aside class="aside-panel">
        <!-- 答题卡 -->
        <div class="aside-card answer-sheet-card">
          <div class="aside-card-header">
            <h4>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <line x1="3" y1="9" x2="21" y2="9"/>
                <line x1="9" y1="21" x2="9" y2="9"/>
              </svg>
              答题卡
            </h4>
          </div>
          <div class="answer-legend">
            <div class="legend-item">
              <span class="legend-dot current"></span>
              <span>当前</span>
            </div>
            <div class="legend-item">
              <span class="legend-dot answered"></span>
              <span>已答</span>
            </div>
            <div class="legend-item">
              <span class="legend-dot unanswered"></span>
              <span>未答</span>
            </div>
          </div>
          <div class="answer-grid" v-if="questions.length > 0">
            <button
              v-for="(q, index) in questions"
              :key="q.id"
              class="answer-dot"
              :class="{
                current: selectedQuestion?.id === q.id,
                answered: answeredQuestions.has(q.id)
              }"
              @click="selectQuestion(q)"
              :title="`第${index + 1}题`"
            >
              {{ index + 1 }}
            </button>
          </div>
          <div v-else class="answer-empty">暂无题目</div>
        </div>

        <!-- 练习信息 -->
        <div class="aside-card info-card">
          <div class="aside-card-header">
            <h4>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              练习信息
            </h4>
          </div>
          <div class="info-list">
            <div class="info-item">
              <span class="info-label">题目类型</span>
              <span class="info-value">{{ selectedQuestion ? typeLabel(selectedQuestion.question_type) : '-' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">所属章节</span>
              <span class="info-value">{{ selectedSubchapter?.name || '-' }}</span>
            </div>
            <div class="info-item">
              <span class="info-label">题目总数</span>
              <span class="info-value">{{ questions.length }}</span>
            </div>
          </div>
        </div>

        <!-- 快捷操作 -->
        <div class="aside-card action-card">
          <div class="aside-card-header">
            <h4>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="13,2 3,14 12,14 11,22 21,10 12,10"/>
              </svg>
              快捷操作
            </h4>
          </div>
          <div class="action-list">
            <button class="action-btn" @click="goToPracticeHome">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 20h9"/>
                <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
              </svg>
              在线练习
            </button>
            <button class="action-btn" @click="goToWrongQuestions">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
              错题本
            </button>
            <button class="action-btn" @click="goToFavorites">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
              </svg>
              收藏夹
            </button>
          </div>
        </div>
      </aside>
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
  getQuestionDetail
} from '@/api/questionBank'
import { checkFavorite, addFavorite, removeFavorite } from '@/api/records'

const router = useRouter()
const courses = ref([])
const chapters = ref([])
const subchapters = ref([])
const questions = ref([])

const selectedCourse = ref(null)
const selectedChapter = ref(null)
const selectedSubchapter = ref(null)
const selectedQuestion = ref(null)
const questionDetail = ref(null)
const favoriteStatus = ref({ is_favorited: false, favorite_id: null })

// 已答题目的 ID 集合（模拟，已答状态）
const answeredQuestions = ref(new Set())

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
  selectedQuestion.value = null
  questionDetail.value = null
  chapters.value = []
  subchapters.value = []
  questions.value = []

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
  selectedQuestion.value = null
  questionDetail.value = null
  subchapters.value = []
  questions.value = []

  try {
    const res = await getSubChaptersByChapter(chapter.id)
    subchapters.value = res.data || []
    if (subchapters.value.length > 0) {
      selectSubChapter(subchapters.value[0])
    }
  } catch (e) {
    console.error('加载子章节失败', e)
  }
}

// 选择子章节
const selectSubChapter = async (sc) => {
  selectedSubchapter.value = sc
  selectedQuestion.value = null
  questionDetail.value = null
  questions.value = []

  try {
    const res = await getQuestionsBySubChapter(sc.id)
    questions.value = res.data || []
    if (questions.value.length > 0) {
      selectQuestion(questions.value[0])
    }
  } catch (e) {
    console.error('加载题目失败', e)
  }
}

// 选择题目
const selectQuestion = async (q) => {
  selectedQuestion.value = q
  favoriteStatus.value = { is_favorited: false, favorite_id: null }
  try {
    const res = await getQuestionDetail(q.id)
    questionDetail.value = res.data || null
    try {
      const favRes = await checkFavorite(q.id)
      favoriteStatus.value = favRes.data || { is_favorited: false, favorite_id: null }
    } catch (e) {
      favoriteStatus.value = { is_favorited: false, favorite_id: null }
    }
  } catch (e) {
    console.error('加载题目详情失败', e)
  }
}

// 切换收藏状态
const toggleFavorite = async () => {
  if (!questionDetail.value) return
  try {
    if (favoriteStatus.value.is_favorited) {
      await removeFavorite(favoriteStatus.value.favorite_id)
      favoriteStatus.value = { is_favorited: false, favorite_id: null }
    } else {
      const res = await addFavorite(questionDetail.value.id)
      favoriteStatus.value = { is_favorited: true, favorite_id: res.data?.favorite_id || null }
    }
  } catch (e) {
    console.error('收藏操作失败', e)
  }
}

// 开始练习
const onStartPractice = () => {
  if (!selectedSubchapter.value) {
    alert('请先选择一个子章节')
    return
  }
  router.push(`/practice/${selectedSubchapter.value.id}`)
}

// 路由跳转
const goToPracticeHome = () => router.push('/practice-home')
const goToWrongQuestions = () => router.push('/wrong-questions')
const goToFavorites = () => router.push('/favorites')

// 题型标签
const typeLabel = (type) => {
  return type === 'single_choice' ? '单选题' : '大题'
}

// 计算选项列表
const questionOptions = computed(() => {
  if (!questionDetail.value) return []
  return ['A', 'B', 'C', 'D'].map(key => ({
    key,
    text: questionDetail.value[`option_${key.toLowerCase()}_text`],
    image: questionDetail.value[`option_${key.toLowerCase()}_image`]
  })).filter(opt => opt.text || opt.image)
})

onMounted(() => {
  loadCourses()
})
</script>

<style scoped>
/* 页面容器 */
.question-bank-page {
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
  width: 500px;
  height: 500px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  top: -150px;
  right: -100px;
}

.bg-blob-2 {
  width: 400px;
  height: 400px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: -100px;
  left: -50px;
  opacity: 0.3;
}

/* 主容器 */
.page-container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 24px;
  display: grid;
  grid-template-columns: 280px 1fr 280px;
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
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 16px;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.sidebar-logo {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
}

.sidebar-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

/* 导航区块 */
.nav-section {
  margin-bottom: 20px;
}

.nav-section:last-child {
  margin-bottom: 0;
}

.nav-section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: #909399;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
  padding-left: 8px;
}

.nav-section-header svg {
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
  gap: 10px;
  padding: 10px 12px;
  border-radius: 12px;
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
  height: 20px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 0 3px 3px 0;
}

.nav-item-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #dcdfe6;
  transition: all 0.25s ease;
}

.nav-item.active .nav-item-dot {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 0 8px rgba(102, 126, 234, 0.4);
}

.nav-item-text {
  font-size: 14px;
  color: #606266;
  flex: 1;
  transition: color 0.25s ease;
}

.nav-item:hover .nav-item-text,
.nav-item.active .nav-item-text {
  color: #667eea;
}

.sub-nav-item {
  padding: 8px 12px;
}

.nav-count-badge {
  font-size: 11px;
  font-weight: 600;
  color: #67c23a;
  background: rgba(103, 194, 58, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
}

.nav-empty {
  font-size: 13px;
  color: #c0c4cc;
  padding: 8px 12px;
}

/* ==================== 中间主内容区 ==================== */
.main-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 题目列表区域 */
.list-section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.list-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.list-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.list-title {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a2e;
}

.list-count {
  font-size: 13px;
  color: #909399;
  background: #f0f2f8;
  padding: 4px 12px;
  border-radius: 20px;
}

.btn-start-practice {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}

.btn-start-practice svg {
  width: 16px;
  height: 16px;
}

.btn-start-practice:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

/* 空状态 */
.list-empty {
  text-align: center;
  padding: 60px 20px;
}

.empty-illustration {
  margin-bottom: 20px;
}

.empty-illustration svg {
  width: 120px;
  height: 120px;
}

.empty-text {
  font-size: 15px;
  color: #909399;
}

/* 题目卡片列表 */
.question-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.question-card-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border: 1.5px solid #f0f0f0;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.question-card-item:hover {
  border-color: rgba(102, 126, 234, 0.3);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.08);
  transform: translateX(4px);
}

.question-card-item.active {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.04) 0%, rgba(118, 75, 162, 0.04) 100%);
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.12);
}

.qc-left {
  flex-shrink: 0;
}

.qc-index {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: #f0f2f8;
  color: #606266;
  font-size: 13px;
  font-weight: 600;
  border-radius: 10px;
  transition: all 0.25s ease;
}

.question-card-item.active .qc-index {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.qc-content {
  flex: 1;
  min-width: 0;
}

.qc-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}

.qc-id {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-size: 12px;
  color: #909399;
}

.qc-type-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
}

.qc-type-badge.single_choice {
  background: rgba(64, 158, 255, 0.1);
  color: #409eff;
}

.qc-type-badge.big_question {
  background: rgba(230, 162, 60, 0.1);
  color: #e6a23c;
}

.qc-img-tag {
  font-size: 11px;
  color: #f56c6c;
  background: rgba(245, 108, 108, 0.1);
  padding: 3px 8px;
  border-radius: 20px;
}

/* 状态点 */
.qc-status-dot {
  display: block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 4px;
  border: 1.5px solid transparent;
}

.qc-status-dot.correct {
  background: #67c23a;
  box-shadow: 0 0 4px rgba(103, 194, 58, 0.4);
}

.qc-status-dot.wrong {
  background: #f56c6c;
  box-shadow: 0 0 4px rgba(245, 108, 108, 0.4);
}

.qc-status-dot.unattempted {
  background: #e4e7ed;
}

/* 状态图例 */
.status-legend {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.legend-dot.correct { background: #67c23a; }
.legend-dot.wrong { background: #f56c6c; }
.legend-dot.unattempted { background: #e4e7ed; }

.legend-text {
  font-size: 12px;
  color: #8a92b8;
  margin-right: 6px;
}

.qc-preview {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin: 0;
}

.qc-arrow {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c0c4cc;
  transition: all 0.25s ease;
}

.question-card-item:hover .qc-arrow,
.question-card-item.active .qc-arrow {
  color: #667eea;
  transform: translateX(4px);
}

.qc-arrow svg {
  width: 16px;
  height: 16px;
}

/* 题目详情区域 */
.detail-section {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.8);
  overflow: hidden;
}

.detail-card {
  padding: 28px;
}

.detail-header {
  padding-bottom: 20px;
  margin-bottom: 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.detail-title-row {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.detail-id-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.25);
}

.detail-id-badge svg {
  width: 16px;
  height: 16px;
}

.detail-type-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 5px 14px;
  border-radius: 20px;
}

.detail-type-badge.single_choice {
  background: rgba(64, 158, 255, 0.1);
  color: #409eff;
}

.detail-type-badge.big_question {
  background: rgba(230, 162, 60, 0.1);
  color: #e6a23c;
}

.detail-path {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #909399;
  margin-bottom: 16px;
}

.detail-path svg {
  width: 14px;
  height: 14px;
}

.btn-favorite {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #fff;
  color: #909399;
  font-size: 13px;
  border: 1.5px solid rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.btn-favorite svg {
  width: 14px;
  height: 14px;
}

.btn-favorite:hover {
  border-color: #e6a23c;
  color: #e6a23c;
  background: rgba(230, 162, 60, 0.04);
}

.btn-favorite.favorited {
  border-color: #e6a23c;
  color: #fff;
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  box-shadow: 0 2px 12px rgba(230, 162, 60, 0.3);
}

/* 详情内容 */
.detail-body {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.detail-section-block {
  position: relative;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #667eea;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.label-dot {
  width: 6px;
  height: 6px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
}

.section-content {
  font-size: 15px;
  color: #303133;
  line-height: 1.8;
  white-space: pre-wrap;
}

.section-image {
  max-width: 100%;
  border-radius: 12px;
  margin-top: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

/* 选项列表 */
.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  background: #f9fafb;
  border: 1.5px solid transparent;
  border-radius: 12px;
  transition: all 0.25s ease;
}

.option-item.correct {
  background: rgba(103, 194, 58, 0.08);
  border-color: rgba(103, 194, 58, 0.3);
}

.option-key {
  font-weight: 700;
  color: #667eea;
  font-size: 15px;
  flex-shrink: 0;
}

.option-item.correct .option-key {
  color: #67c23a;
}

.option-text {
  font-size: 14px;
  color: #303133;
  line-height: 1.6;
}

.option-image {
  max-width: 200px;
  border-radius: 8px;
  margin-top: 8px;
}

/* 解析区块 */
.analysis-block {
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.04) 0%, rgba(118, 75, 162, 0.04) 100%);
  padding: 20px;
  border-radius: 16px;
  border: 1px solid rgba(103, 194, 58, 0.1);
}

.analysis-label {
  color: #67c23a;
}

.analysis-label .label-dot {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.analysis-text {
  color: #606266;
}

/* ==================== 右侧辅助面板 ==================== */
.aside-panel {
  position: sticky;
  top: 92px;
  height: fit-content;
  max-height: calc(100vh - 116px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.aside-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.aside-card-header {
  margin-bottom: 16px;
}

.aside-card-header h4 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.aside-card-header svg {
  width: 18px;
  height: 18px;
  color: #667eea;
}

/* 答题卡 */
.answer-legend {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #909399;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.legend-dot.current {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4);
}

.legend-dot.answered {
  background: #67c23a;
}

.legend-dot.unanswered {
  background: #e4e7ed;
}

.answer-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.answer-dot {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: #909399;
  background: #f5f7fa;
  border: 1.5px solid transparent;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.answer-dot:hover {
  border-color: rgba(102, 126, 234, 0.3);
  color: #667eea;
}

.answer-dot.current {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.answer-dot.answered {
  background: rgba(103, 194, 58, 0.1);
  color: #67c23a;
}

.answer-empty {
  text-align: center;
  font-size: 13px;
  color: #c0c4cc;
  padding: 20px;
}

/* 练习信息 */
.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #f9fafb;
  border-radius: 10px;
}

.info-label {
  font-size: 13px;
  color: #909399;
}

.info-value {
  font-size: 13px;
  font-weight: 600;
  color: #303133;
}

/* 快捷操作 */
.action-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  background: #fff;
  color: #606266;
  font-size: 13px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.action-btn svg {
  width: 16px;
  height: 16px;
  color: #667eea;
}

.action-btn:hover {
  border-color: rgba(102, 126, 234, 0.3);
  background: rgba(102, 126, 234, 0.04);
  color: #667eea;
  transform: translateX(4px);
}

/* 滚动条美化 */
.sidebar-panel::-webkit-scrollbar,
.aside-panel::-webkit-scrollbar {
  width: 4px;
}

.sidebar-panel::-webkit-scrollbar-track,
.aside-panel::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-panel::-webkit-scrollbar-thumb,
.aside-panel::-webkit-scrollbar-thumb {
  background: rgba(102, 126, 234, 0.2);
  border-radius: 2px;
}

/* 响应式 */
@media (max-width: 1200px) {
  .page-container {
    grid-template-columns: 240px 1fr 240px;
    gap: 16px;
  }
}

@media (max-width: 1024px) {
  .page-container {
    grid-template-columns: 1fr;
  }

  .sidebar-panel,
  .aside-panel {
    position: static;
    max-height: none;
  }

  .answer-grid {
    grid-template-columns: repeat(8, 1fr);
  }
}
</style>
