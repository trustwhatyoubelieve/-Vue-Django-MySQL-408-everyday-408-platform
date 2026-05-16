<template>
  <div class="study-center-page">
    <div class="page-header">
      <h2>学习中心</h2>
    </div>

    <!-- ========== 1. 顶部统计卡片 ========== -->
    <div v-if="!overviewLoading" class="overview-cards">
      <div class="stat-card">
        <div class="stat-num">{{ overview.total_sessions || 0 }}</div>
        <div class="stat-label">累计练习次数</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ overview.total_answered_questions || 0 }}</div>
        <div class="stat-label">累计做题数</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ overview.total_correct_questions || 0 }}</div>
        <div class="stat-label">累计答对题数</div>
      </div>
      <div class="stat-card">
        <div class="stat-num accuracy">{{ formatPercent(overview.overall_accuracy) }}</div>
        <div class="stat-label">总正确率</div>
      </div>
      <div class="stat-card warn">
        <div class="stat-num">{{ overview.wrong_question_count || 0 }}</div>
        <div class="stat-label">错题本数量</div>
      </div>
      <div class="stat-card">
        <div class="stat-num">{{ overview.favorite_count || 0 }}</div>
        <div class="stat-label">收藏数量</div>
      </div>
    </div>
    <div v-else class="loading-row">
      <span>加载中...</span>
    </div>

    <!-- ========== 2. 课程统计 + 章节统计 ========== -->
    <div class="two-col">
      <!-- 课程统计 -->
      <div class="panel">
        <div class="panel-toolbar">
          <div class="panel-title" style="margin-bottom:0">课程维度统计</div>
          <label class="toggle-label">
            <input type="checkbox" v-model="showZeroCourse" @change="loadCourseStats" />
            显示未练习课程
          </label>
        </div>
        <div v-if="courseStatsLoading" class="empty-tip">加载中...</div>
        <div v-else-if="courseStats.length === 0" class="empty-tip">暂无课程</div>
        <div v-else class="course-list">
          <div
            v-for="c in courseStats"
            :key="c.course_id"
            class="course-item"
            :class="{
              active: selectedCourse?.course_id === c.course_id,
              'zero-data': c.answered_count === 0
            }"
            @click="selectCourse(c)"
          >
            <div class="course-name">
              {{ c.course_name }}
              <span v-if="c.answered_count === 0" class="zero-tag">未练习</span>
            </div>
            <div class="course-bar-wrap">
              <div class="course-bar">
                <div
                  class="course-bar-fill"
                  :class="{ 'bar-empty': c.answered_count === 0 }"
                  :style="{ width: formatPercent(c.accuracy) }"
                ></div>
              </div>
              <span class="course-pct">{{ formatPercent(c.accuracy) }}</span>
            </div>
            <div class="course-meta">
              <span>做题 {{ c.answered_count }} 题</span>
              <span>答对 {{ c.correct_count }} 题</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 章节统计 -->
      <div class="panel">
        <div class="panel-toolbar">
          <div class="panel-title" style="margin-bottom:0">
            章节维度统计
            <span v-if="selectedCourse" class="panel-subtitle">— {{ selectedCourse.course_name }}</span>
          </div>
          <label v-if="selectedCourse" class="toggle-label">
            <input type="checkbox" v-model="showZeroChapter" @change="loadChapterStats" />
            显示未练习章节
          </label>
        </div>
        <div v-if="chapterStatsLoading" class="empty-tip">加载中...</div>
        <div v-else-if="!selectedCourse" class="empty-tip">请从左侧选择一门课程</div>
        <div v-else-if="chapterStats.length === 0" class="empty-tip">该课程暂无章节数据</div>
        <div v-else class="chapter-list">
          <div
            v-for="ch in chapterStats"
            :key="ch.chapter_id"
            class="chapter-item"
            :class="{ 'zero-data': ch.answered_count === 0 }"
          >
            <div class="chapter-name">
              {{ ch.chapter_name }}
              <span v-if="ch.answered_count === 0" class="zero-tag">未练习</span>
            </div>
            <div class="chapter-bar-wrap">
              <div class="chapter-bar">
                <div
                  class="chapter-bar-fill"
                  :class="{ 'bar-empty': ch.answered_count === 0 }"
                  :style="{ width: formatPercent(ch.accuracy) }"
                ></div>
              </div>
              <span class="chapter-pct">{{ formatPercent(ch.accuracy) }}</span>
            </div>
            <div class="chapter-meta">
              <span>做题 {{ ch.answered_count }}</span>
              <span>正确 {{ ch.correct_count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ========== 3. 每日刷题统计 ========== -->
    <div class="panel">
      <div class="panel-toolbar">
        <div class="panel-title" style="margin-bottom:0">每日刷题统计</div>
        <div class="stats-legend">
          <span class="legend-item">
            <span class="legend-dot green"></span>正确率
          </span>
          <span class="legend-item">
            <span class="legend-dot orange"></span>刷题数
          </span>
        </div>
      </div>
      <div v-if="dailyStatsLoading" class="empty-tip">加载中...</div>
      <div v-else-if="dailyStats.length === 0" class="empty-tip">暂无刷题记录</div>
      <div v-else class="daily-stats-grid">
        <div
          v-for="day in dailyStats"
          :key="day.date"
          class="daily-card"
          :class="{ 'has-data': day.answered_count > 0 }"
        >
          <div class="daily-date">{{ formatDateShort(day.date) }}</div>
          <div class="daily-questions">
            <div class="daily-num" :class="{ highlight: day.answered_count > 0 }">{{ day.answered_count }}</div>
            <div class="daily-label">做题</div>
          </div>
          <div class="daily-accuracy">
            <div class="daily-num" :class="accuracyClass(day.accuracy)">{{ formatPercent(day.accuracy) }}</div>
            <div class="daily-label">正确率</div>
          </div>
          <div class="daily-duration">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <polyline points="12,6 12,12 16,14"/>
            </svg>
            <span>{{ day.study_duration_text }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ========== 4. 最近错题 + 最近收藏 ========== -->
    <div class="two-col">
      <!-- 最近错题 -->
      <div class="panel">
        <div class="panel-title">最近错题</div>
        <div v-if="recentWrongLoading" class="empty-tip">加载中...</div>
        <div v-else-if="recentWrong.length === 0" class="empty-tip">暂无错题</div>
        <div v-else class="mini-list">
          <div v-for="item in recentWrong" :key="item.wrong_question_id" class="mini-item">
            <span class="mini-id">{{ item.business_id }}</span>
            <span class="mini-stem">{{ item.stem_text || '[图片题]' }}</span>
            <span class="mini-count">错{{ item.wrong_count }}次</span>
          </div>
        </div>
      </div>

      <!-- 最近收藏 -->
      <div class="panel">
        <div class="panel-title">最近收藏</div>
        <div v-if="recentFavLoading" class="empty-tip">加载中...</div>
        <div v-else-if="recentFavorites.length === 0" class="empty-tip">暂无收藏</div>
        <div v-else class="mini-list">
          <div v-for="item in recentFavorites" :key="item.favorite_id" class="mini-item">
            <span class="mini-id">{{ item.business_id }}</span>
            <span class="mini-stem">{{ item.stem_text || '[图片题]' }}</span>
            <span class="mini-tag">★</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  getOverviewStats,
  getCourseStats,
  getChapterStats,
  getDailyPracticeStats,
  getRecentWrongQuestions,
  getRecentFavorites,
} from '@/api/stats'

// 总览
const overviewLoading = ref(false)
const overview = ref({})

// 课程统计
const courseStatsLoading = ref(false)
const courseStats = ref([])
const selectedCourse = ref(null)
const showZeroCourse = ref(false)

// 章节统计
const chapterStatsLoading = ref(false)
const chapterStats = ref([])
const showZeroChapter = ref(false)

// 每日刷题统计
const dailyStatsLoading = ref(false)
const dailyStats = ref([])

// 最近错题
const recentWrongLoading = ref(false)
const recentWrong = ref([])

// 最近收藏
const recentFavLoading = ref(false)
const recentFavorites = ref([])

// 加载总览
const loadOverview = async () => {
  overviewLoading.value = true
  try {
    const res = await getOverviewStats()
    overview.value = res.data || {}
  } catch (e) {
    console.error('加载总览失败', e)
  } finally {
    overviewLoading.value = false
  }
}

// 加载课程统计
const loadCourseStats = async () => {
  courseStatsLoading.value = true
  try {
    const res = await getCourseStats(showZeroCourse.value)
    courseStats.value = res.data || []
    // 默认选中第一门有数据的课，如果没有则选第一门
    const first = courseStats.value.find(c => c.answered_count > 0) || courseStats.value[0]
    if (first) {
      await selectCourse(first)
    } else {
      selectedCourse.value = null
      chapterStats.value = []
    }
  } catch (e) {
    console.error('加载课程统计失败', e)
  } finally {
    courseStatsLoading.value = false
  }
}

// 选择课程，加载章节统计
const selectCourse = async (course) => {
  selectedCourse.value = course
  chapterStatsLoading.value = true
  chapterStats.value = []
  try {
    const res = await getChapterStats(course.course_id, showZeroChapter.value)
    chapterStats.value = res.data || []
  } catch (e) {
    console.error('加载章节统计失败', e)
  } finally {
    chapterStatsLoading.value = false
  }
}

// 加载每日刷题统计
const loadDailyStats = async () => {
  dailyStatsLoading.value = true
  try {
    const res = await getDailyPracticeStats(6)
    dailyStats.value = res.data || []
  } catch (e) {
    console.error('加载每日刷题统计失败', e)
  } finally {
    dailyStatsLoading.value = false
  }
}

// 加载最近错题
const loadRecentWrong = async () => {
  recentWrongLoading.value = true
  try {
    const res = await getRecentWrongQuestions()
    recentWrong.value = res.data || []
  } catch (e) {
    console.error('加载最近错题失败', e)
  } finally {
    recentWrongLoading.value = false
  }
}

// 加载最近收藏
const loadRecentFavorites = async () => {
  recentFavLoading.value = true
  try {
    const res = await getRecentFavorites()
    recentFavorites.value = res.data || []
  } catch (e) {
    console.error('加载最近收藏失败', e)
  } finally {
    recentFavLoading.value = false
  }
}

// 格式化正确率
const formatPercent = (val) => {
  if (val === null || val === undefined) return '—'
  return `${Math.round(Number(val) * 100)}%`
}

// 格式化时间
const formatDate = (timeStr) => {
  if (!timeStr) return '—'
  const d = new Date(timeStr)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

// 格式化日期（短格式：MM-DD）
const formatDateShort = (dateStr) => {
  if (!dateStr) return '—'
  const parts = dateStr.split('-')
  if (parts.length !== 3) return dateStr
  return `${parseInt(parts[1])}月${parseInt(parts[2])}日`
}

// 正确率颜色类
const accuracyClass = (val) => {
  if (val === null || val === undefined || val === 0) return 'gray'
  if (val >= 0.7) return 'green'
  if (val >= 0.4) return 'orange'
  return 'red'
}

onMounted(() => {
  loadOverview()
  loadCourseStats()
  loadDailyStats()
  loadRecentWrong()
  loadRecentFavorites()
})
</script>

<style scoped>
.study-center-page {
  max-width: 1100px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 18px;
  color: #303133;
}

/* ========== 顶部统计卡片 ========== */
.overview-cards {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

@media (max-width: 900px) {
  .overview-cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

.stat-card {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.stat-card.warn {
  border-color: #f56c6c;
}

.stat-num {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-card.warn .stat-num {
  color: #f56c6c;
}

.stat-num.accuracy {
  color: #67c23a;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

/* ========== 通用面板 ========== */
.panel {
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.panel-title {
  font-size: 15px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 16px;
}

.panel-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.toggle-label {
  font-size: 12px;
  color: #606266;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.toggle-label input {
  cursor: pointer;
}

.panel-subtitle {
  font-weight: normal;
  font-size: 13px;
  color: #909399;
}

/* ========== 两栏布局 ========== */
.two-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .two-col {
    grid-template-columns: 1fr;
  }
}

/* ========== 课程统计 ========== */
.course-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.course-item {
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.course-item:hover {
  border-color: #409eff;
}

.course-item.active {
  border-color: #409eff;
  background: #ecf5ff;
}

.course-item.zero-data {
  border-color: #e4e7ed;
  opacity: 0.7;
}

.course-item.zero-data.active {
  border-color: #409eff;
  opacity: 1;
}

.zero-tag {
  font-size: 11px;
  background: #f4f4f5;
  color: #909399;
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: normal;
  margin-left: 6px;
}

.course-name {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.course-bar {
  flex: 1;
  height: 8px;
  background: #f0f9eb;
  border-radius: 4px;
  overflow: hidden;
}

.course-bar-fill {
  height: 100%;
  background: #67c23a;
  border-radius: 4px;
  transition: width 0.3s;
}

.course-bar-fill.bar-empty {
  background: #e4e7ed;
}

.course-pct {
  font-size: 13px;
  font-weight: bold;
  color: #67c23a;
  min-width: 40px;
  text-align: right;
}

.course-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

/* ========== 章节统计 ========== */
.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chapter-item {
  padding: 10px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
}

.chapter-name {
  font-size: 13px;
  color: #606266;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.chapter-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.chapter-bar {
  flex: 1;
  height: 6px;
  background: #f0f9eb;
  border-radius: 3px;
  overflow: hidden;
}

.chapter-bar-fill {
  height: 100%;
  background: #85ce61;
  border-radius: 3px;
  transition: width 0.3s;
}

.chapter-bar-fill.bar-empty {
  background: #e4e7ed;
}

.chapter-pct {
  font-size: 12px;
  font-weight: bold;
  color: #67c23a;
  min-width: 38px;
  text-align: right;
}

.chapter-meta {
  display: flex;
  gap: 12px;
  font-size: 11px;
  color: #c0c4cc;
}

/* ========== 每日刷题统计 ========== */
.stats-legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #909399;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.legend-dot.green { background: #67c23a; }
.legend-dot.orange { background: #e6a23c; }

.daily-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}

.daily-card {
  background: #f9fafb;
  border: 1.5px solid #eef1f7;
  border-radius: 14px;
  padding: 14px;
  transition: all 0.2s;
}

.daily-card.has-data {
  background: #fff;
  border-color: rgba(91, 108, 255, 0.15);
  box-shadow: 0 4px 12px rgba(80, 100, 180, 0.06);
}

.daily-card:hover {
  box-shadow: 0 6px 16px rgba(80, 100, 180, 0.12);
  transform: translateY(-1px);
}

.daily-date {
  font-size: 12px;
  color: #8a92b8;
  font-weight: 600;
  margin-bottom: 10px;
  text-align: center;
}

.daily-questions,
.daily-accuracy {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 8px;
}

.daily-num {
  font-size: 26px;
  font-weight: 800;
  color: #2d3562;
  line-height: 1.1;
}

.daily-num.highlight {
  background: linear-gradient(135deg, #5b6cff, #6b5fd6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.daily-num.green { color: #67c23a; }
.daily-num.orange { color: #e6a23c; }
.daily-num.red { color: #f56c6c; }
.daily-num.gray { color: #c0c4cc; }

.daily-label {
  font-size: 11px;
  color: #8a92b8;
  margin-top: 2px;
}

.daily-duration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 12px;
  color: #b0b5d0;
  border-top: 1px solid #eef1f7;
  padding-top: 8px;
  margin-top: 4px;
}

.daily-duration svg {
  width: 13px;
  height: 13px;
}

/* ========== 最近错题 / 收藏 ========== */
.mini-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mini-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border: 1px solid #f0f0f0;
  border-radius: 4px;
  font-size: 13px;
}

.mini-id {
  font-family: monospace;
  font-size: 12px;
  color: #909399;
  flex-shrink: 0;
}

.mini-stem {
  flex: 1;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mini-count {
  font-size: 12px;
  color: #f56c6c;
  flex-shrink: 0;
}

.mini-tag {
  color: #e6a23c;
  flex-shrink: 0;
}

/* ========== 空/加载 ========== */
.empty-tip {
  font-size: 13px;
  color: #c0c4cc;
  padding: 20px 0;
  text-align: center;
}

.loading-row {
  text-align: center;
  padding: 20px;
  color: #c0c4cc;
  font-size: 14px;
}
</style>
