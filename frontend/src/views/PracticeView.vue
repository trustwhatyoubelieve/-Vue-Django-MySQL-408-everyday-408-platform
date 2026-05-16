<template>
  <div class="practice-page">
    <!-- 背景装饰 -->
    <div class="page-bg">
      <div class="bg-blob bg-blob-1"></div>
      <div class="bg-blob bg-blob-2"></div>
    </div>

    <!-- Loading 状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-card">
        <div class="loading-spinner"></div>
        <p class="loading-text">{{ loadingTip }}</p>
      </div>
    </div>

    <!-- 无题目状态 -->
    <div v-else-if="noQuestions" class="empty-container">
      <div class="empty-card">
        <div class="empty-icon-wrapper">
          <svg viewBox="0 0 120 120" fill="none">
            <circle cx="60" cy="60" r="50" fill="#fef0f0"/>
            <rect x="35" y="40" width="50" height="40" rx="4" fill="#f56c6c" opacity="0.2"/>
            <text x="60" y="68" text-anchor="middle" font-size="32">📭</text>
          </svg>
        </div>
        <h3>暂无题目可练习</h3>
        <p>该子章节下还没有题目，请联系管理员添加。</p>
        <button class="btn-back" @click="goBack">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12,19 5,12 12,5"/>
          </svg>
          返回题库
        </button>
      </div>
    </div>

    <!-- 练习完成汇总 -->
    <div v-else-if="finished" class="result-container">
      <div class="result-card">
        <div class="result-header">
          <div class="result-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22,4 12,14.01 9,11.01"/>
            </svg>
          </div>
          <h2>练习完成</h2>
          <p>恭喜你完成了本次练习，继续加油！</p>
        </div>

        <div class="result-stats">
          <div class="stat-card">
            <div class="stat-icon blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ sessionInfo.total_count }}</span>
              <span class="stat-label">总题数</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon purple">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20,6 9,17 4,12"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ sessionInfo.answered_count }}</span>
              <span class="stat-label">已答题</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon green">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                <line x1="9" y1="9" x2="9.01" y2="9"/>
                <line x1="15" y1="9" x2="15.01" y2="9"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-value correct">{{ sessionInfo.correct_count }}</span>
              <span class="stat-label">正确</span>
            </div>
          </div>

          <div class="stat-card highlight">
            <div class="stat-icon orange">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="20" x2="12" y2="10"/>
                <line x1="18" y1="20" x2="18" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="16"/>
              </svg>
            </div>
            <div class="stat-info">
              <span class="stat-value accent">{{ accuracyText }}</span>
              <span class="stat-label">正确率</span>
            </div>
          </div>
        </div>

        <div class="result-actions">
          <button class="btn-primary-lg" @click="goBack">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            返回题库
          </button>
          <button class="btn-secondary-lg" @click="restartPractice">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="1,4 1,10 7,10"/>
              <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
            </svg>
            重新练习
          </button>
        </div>
      </div>
    </div>

    <!-- 练习主体 -->
    <template v-else>
      <div class="practice-container">
        <!-- 顶部状态栏 -->
        <div class="practice-header">
          <div class="header-left">
            <button class="btn-back-small" @click="confirmFinish">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="19" y1="12" x2="5" y2="12"/>
                <polyline points="12,19 5,12 12,5"/>
              </svg>
              返回
            </button>
            <div class="session-info">
              <h2 class="session-title">{{ sessionInfo.subchapter?.name }}</h2>
              <div class="session-meta">
                <span class="meta-item">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                    <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
                  </svg>
                  第 {{ currentIndex + 1 }} / {{ sessionInfo.total_count }} 题
                </span>
                <span class="meta-item answered">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20,6 9,17 4,12"/>
                  </svg>
                  已答 {{ sessionInfo.answered_count }}
                </span>
                <span class="meta-item correct">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                    <line x1="9" y1="9" x2="9.01" y2="9"/>
                    <line x1="15" y1="9" x2="15.01" y2="9"/>
                  </svg>
                  正确 {{ sessionInfo.correct_count }}
                </span>
              </div>
            </div>
          </div>

          <div class="header-right">
            <!-- 重置进度按钮 -->
            <button class="btn-reset-progress" @click="confirmReset">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="1,4 1,10 7,10"/>
                <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
              </svg>
              重置进度
            </button>
            <button class="btn-finish" @click="confirmFinish">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <polyline points="9,11 12,14 22,4"/>
              </svg>
              结束练习
            </button>
          </div>
        </div>

        <!-- 主体内容区 -->
        <div class="practice-main">
          <!-- 左侧：题目内容 -->
          <div class="question-area">
            <div class="question-card">
              <!-- 题号和题型 -->
              <div class="question-meta">
                <div class="meta-left">
                  <span class="q-number">{{ currentQuestion?.business_id }}</span>
                  <span class="q-type-tag" :class="currentQuestion?.question_type">
                    {{ typeLabel(currentQuestion?.question_type) }}
                  </span>
                  <!-- 已锁定提示 -->
                  <span v-if="currentQuestion?.is_locked" class="q-locked-tag">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                    </svg>
                    已作答
                  </span>
                </div>
                <button
                  class="btn-favorite-q"
                  :class="{ favorited: currentFavorite }"
                  @click="toggleFavoriteQ"
                >
                  <svg v-if="!currentFavorite" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2">
                    <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
                  </svg>
                </button>
              </div>

              <!-- 题干 -->
              <div class="question-stem">
                <p v-if="currentQuestion?.stem_text" class="stem-text">{{ currentQuestion.stem_text }}</p>
                <img v-if="currentQuestion?.stem_image" :src="currentQuestion.stem_image" class="stem-image" />
              </div>

              <!-- 选项 -->
              <div v-if="currentQuestion?.question_type === 'single_choice'" class="question-options">
                <div
                  v-for="opt in questionOptions"
                  :key="opt.key"
                  class="option-card"
                  :class="{
                    selected: selectedAnswer === opt.key,
                    correct: submitted && opt.key === submittedResult?.correct_answer,
                    wrong: submitted && selectedAnswer === opt.key && !submittedResult?.is_correct,
                    dimmed: submitted && opt.key !== selectedAnswer && opt.key !== submittedResult?.correct_answer,
                  }"
                  @click="selectOption(opt.key)"
                >
                  <span class="opt-key">{{ opt.key }}</span>
                  <div class="opt-content">
                    <span v-if="opt.text" class="opt-text">{{ opt.text }}</span>
                    <img v-if="opt.image" :src="opt.image" class="opt-image" />
                  </div>
                  <span v-if="submitted && opt.key === submittedResult?.correct_answer" class="opt-badge correct-badge">正确答案</span>
                  <span v-if="submitted && selectedAnswer === opt.key && !submittedResult?.is_correct" class="opt-badge wrong-badge">你的答案</span>
                </div>
              </div>

              <!-- 大题 -->
              <div v-if="currentQuestion?.question_type === 'big_question'" class="big-question-tip">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
                <span>本题为分析题/简答题，请在草稿纸作答后查看答案进行对照学习。</span>
              </div>

              <!-- 锁定题目的提示 -->
              <div v-if="submitted && currentQuestion?.is_locked" class="locked-tip">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <span>该题已作答并锁定，如需重新练习请先点击上方「重置进度」按钮</span>
              </div>

              <!-- 答案解析区域（提交后显示） -->
              <div v-if="submitted" class="answer-feedback-section">
                <!-- 结果标签 -->
                <div class="feedback-header">
                  <div class="feedback-result-badge" :class="submittedResult?.is_correct === true ? 'badge-correct' : submittedResult?.is_correct === false ? 'badge-wrong' : 'badge-neutral'">
                    <svg v-if="submittedResult?.is_correct === true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20,6 9,17 4,12"/>
                    </svg>
                    <svg v-else-if="submittedResult?.is_correct === false" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <line x1="18" y1="6" x2="6" y2="18"/>
                      <line x1="6" y1="6" x2="18" y2="18"/>
                    </svg>
                    <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="8" x2="12" y2="12"/>
                      <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    {{ submittedResult?.is_correct === true ? '回答正确' : submittedResult?.is_correct === false ? '回答错误' : '已学习' }}
                  </div>
                </div>

                <!-- 正确答案 -->
                <div v-if="submittedResult?.correct_answer" class="feedback-correct-answer">
                  <div class="feedback-label">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="20,6 9,17 4,12"/>
                    </svg>
                    正确答案
                  </div>
                  <div class="correct-answer-value">{{ submittedResult.correct_answer }}</div>
                </div>

                <!-- 解析 -->
                <div v-if="submittedResult?.analysis_text || submittedResult?.analysis_image" class="feedback-analysis">
                  <div class="feedback-label">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="12" y1="16" x2="12" y2="12"/>
                      <line x1="12" y1="8" x2="12.01" y2="8"/>
                    </svg>
                    题目解析
                  </div>
                  <div v-if="submittedResult?.analysis_text" class="analysis-text">{{ submittedResult.analysis_text }}</div>
                  <img v-if="submittedResult?.analysis_image" :src="submittedResult.analysis_image" class="analysis-image" />
                </div>

                <!-- 无解析提示 -->
                <div v-if="!submittedResult?.analysis_text && !submittedResult?.analysis_image" class="feedback-no-analysis">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14,2 14,8 20,8"/>
                  </svg>
                  <span>暂无解析内容</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 右侧：辅助面板 -->
          <div class="sidebar-area">
            <!-- 答题卡 -->
            <div class="sidebar-card answer-sheet">
              <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                  <line x1="3" y1="9" x2="21" y2="9"/>
                  <line x1="9" y1="21" x2="9" y2="9"/>
                </svg>
                答题卡
              </div>
              <div class="answer-legend">
                <span class="legend-pill current">当前</span>
                <span class="legend-pill correct">正确</span>
                <span class="legend-pill wrong">错误</span>
                <span class="legend-pill unanswered">未答</span>
              </div>
              <div class="answer-grid">
                <button
                  v-for="(qid, idx) in questionIds"
                  :key="qid"
                  class="answer-btn"
                  :class="{
                    current: idx === currentIndex,
                    correct: progressMap[qid] === 'correct',
                    wrong: progressMap[qid] === 'wrong',
                    unattempted: progressMap[qid] === 'unattempted'
                  }"
                  @click="jumpTo(idx)"
                >
                  {{ idx + 1 }}
                </button>
              </div>
            </div>

            <!-- 计时器 -->
            <div class="sidebar-card timer-card">
              <div class="sidebar-card-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <polyline points="12,6 12,12 16,14"/>
                </svg>
                练习时长
              </div>
              <div class="timer-display">{{ formattedTime }}</div>
              <div class="timer-controls">
                <button class="timer-btn" @click="toggleTimer">
                  <svg v-if="timerRunning" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="6" y="4" width="4" height="16"/>
                    <rect x="14" y="4" width="4" height="16"/>
                  </svg>
                  <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polygon points="5,3 19,12 5,21"/>
                  </svg>
                  {{ timerRunning ? '暂停' : '继续' }}
                </button>
                <button class="timer-btn reset" @click="resetTimer">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="1,4 1,10 7,10"/>
                    <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>
                  </svg>
                  重置
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 底部操作栏 -->
        <div class="practice-footer">
          <button
            class="btn-nav-footer prev"
            :disabled="currentIndex === 0"
            @click="goPrev"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12,19 5,12 12,5"/>
            </svg>
            上一题
          </button>

          <div class="footer-center">
            <div class="progress-dots">
              <span
                v-for="(qid, idx) in questionIds"
                :key="idx"
                class="progress-dot"
                :class="{
                  current: idx === currentIndex,
                  correct: progressMap[qid] === 'correct',
                  wrong: progressMap[qid] === 'wrong',
                  unattempted: progressMap[qid] === 'unattempted'
                }"
              ></span>
            </div>
          </div>

          <!-- 未作答时可提交 -->
          <button
            v-if="!submitted && currentQuestion?.question_type === 'single_choice'"
            class="btn-submit-answer"
            :disabled="!selectedAnswer || currentQuestion?.is_locked"
            :title="currentQuestion?.is_locked ? '该题已作答，如需重做请先重置进度' : (!selectedAnswer ? '请先选择答案' : '')"
            @click="submitAnswer"
          >
            {{ currentQuestion?.is_locked ? '已锁定' : '提交答案' }}
          </button>

          <button
            v-else-if="!submitted && currentQuestion?.question_type === 'big_question'"
            class="btn-submit-answer"
            :disabled="currentQuestion?.is_locked"
            :title="currentQuestion?.is_locked ? '该题已作答，如需重做请先重置进度' : ''"
            @click="submitBigQuestion"
          >
            {{ currentQuestion?.is_locked ? '已锁定' : '我已作答' }}
          </button>

          <button
            v-else-if="submitted && !isLastQuestion"
            class="btn-nav-footer next"
            @click="goNext"
          >
            下一题
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"/>
              <polyline points="12,5 19,12 12,19"/>
            </svg>
          </button>

          <button
            v-else-if="submitted && isLastQuestion"
            class="btn-finish-practice"
            @click="goToFinish"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20,6 9,17 4,12"/>
            </svg>
            完成练习
          </button>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  startPractice,
  getPracticeSession,
  getPracticeQuestion,
  submitPracticeAnswer,
  finishPractice,
  resetSubchapterProgress,
} from '@/api/practice'
import { getQuestionsBySubChapter } from '@/api/questionBank'
import { checkFavorite, addFavorite, removeFavorite } from '@/api/records'
import { getQuestionDetail } from '@/api/questionBank'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// ========== 状态 ==========
const loading = ref(true)
const loadingTip = ref('正在加载...')
const noQuestions = ref(false)
const finished = ref(false)

const sessionInfo = ref({
  session_id: null,
  subchapter: null,
  total_count: 0,
  answered_count: 0,
  correct_count: 0,
})

const questionIds = ref([])
const currentIndex = ref(0)
const currentQuestion = ref(null)
const selectedAnswer = ref(null)
const submitted = ref(false)
const submittedResult = ref(null)

const pdfViewerLoading = ref(true)
const pdfViewerLoadError = ref(false)
const pdfRendered = ref(false)
const pdfRendered2 = ref(false)
const practicePdfCanvas = ref(null)
let pdfDoc = null

// 固定进度映射 { questionId: 'correct'|'wrong'|'unattempted' }
// 来自后端 SubchapterPracticeProgress 表
const progressMap = ref({})

// 收藏状态
const currentFavorite = ref(false)
const currentFavoriteId = ref(null)

// 计时器
const timerSeconds = ref(0)
const timerRunning = ref(true)
let timerInterval = null

// ========== 计算属性 ==========
const isLastQuestion = computed(() => currentIndex.value === questionIds.value.length - 1)

// 当前题是否已锁定（绿色或红色题不能再次提交）
const currentLocked = computed(() => {
  const qid = questionIds.value[currentIndex.value]
  return !!qid && progressMap.value[qid] !== 'unattempted'
})

// 当前题的颜色状态
const currentStatus = computed(() => {
  const qid = questionIds.value[currentIndex.value]
  return progressMap.value[qid] || 'unattempted'
})

const accuracyText = computed(() => {
  const total = sessionInfo.value.total_count
  const correct = sessionInfo.value.correct_count
  if (!total) return '0%'
  return ((correct / total) * 100).toFixed(1) + '%'
})

const questionOptions = computed(() => {
  if (!currentQuestion.value) return []
  return ['A', 'B', 'C', 'D'].map(key => ({
    key,
    text: currentQuestion.value[`option_${key.toLowerCase()}_text`],
    image: currentQuestion.value[`option_${key.toLowerCase()}_image`]
  })).filter(opt => opt.text || opt.image)
})

const formattedTime = computed(() => {
  const h = Math.floor(timerSeconds.value / 3600)
  const m = Math.floor((timerSeconds.value % 3600) / 60)
  const s = timerSeconds.value % 60
  if (h > 0) {
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
  }
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

// ========== 方法 ==========
const typeLabel = (type) => {
  if (type === 'single_choice') return '单选题'
  if (type === 'big_question') return '大题'
  return type
}

const goBack = () => router.push('/question-bank')

const startTimer = () => {
  if (timerInterval) clearInterval(timerInterval)
  timerInterval = setInterval(() => {
    if (timerRunning.value) timerSeconds.value++
  }, 1000)
}

const stopTimer = () => {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

const toggleTimer = () => {
  timerRunning.value = !timerRunning.value
}

const resetTimer = () => {
  timerSeconds.value = 0
  timerRunning.value = true
}

const loadSession = async () => {
  const sessionId = sessionInfo.value.session_id
  try {
    const res = await getPracticeSession(sessionId)
    const data = res.data
    sessionInfo.value.total_count = data.total_count
    sessionInfo.value.answered_count = data.answered_count
    sessionInfo.value.correct_count = data.correct_count
    sessionInfo.value.subchapter = data.subchapter
    questionIds.value = data.question_ids || []
    // 从会话详情中也更新 progress_map
    if (data.progress_map) {
      progressMap.value = data.progress_map
    }
  } catch (e) {
    console.error('加载会话失败', e)
  }
}

const loadQuestion = async () => {
  const sessionId = sessionInfo.value.session_id
  const qid = questionIds.value[currentIndex.value]
  if (!qid) return

  // 切换题目时重置 PDF 预览状态
  pdfViewerLoading.value = true
  pdfViewerLoadError.value = false
  pdfRendered.value = false
  if (pdfDoc) {
    pdfDoc.destroy()
    pdfDoc = null
  }

  loadingTip.value = '正在加载题目...'
  try {
    const res = await getPracticeQuestion(sessionId, qid)
    currentQuestion.value = res.data

    // 如果后端返回了最新的锁定状态，同步更新 progressMap
    if (res.data.practice_status) {
      progressMap.value = {
        ...progressMap.value,
        [qid]: res.data.practice_status
      }
    }

    // 检查收藏状态
    try {
      const favRes = await checkFavorite(res.data.id)
      currentFavorite.value = favRes.data?.is_favorited || false
      currentFavoriteId.value = favRes.data?.favorite_id || null
    } catch {
      currentFavorite.value = false
      currentFavoriteId.value = null
    }

    // 如果是已锁定的题（绿色/红色），自动显示结果状态
    if (res.data.is_locked) {
      selectedAnswer.value = res.data.user_answer || null
      submitted.value = true
      submittedResult.value = {
        question_id: res.data.id,
        is_correct: res.data.is_correct,
        correct_answer: res.data.correct_answer,
        user_answer: res.data.user_answer,
        analysis_text: null,
        analysis_image: null,
      }
    } else {
      selectedAnswer.value = null
      submitted.value = false
      submittedResult.value = null
    }
  } catch (e) {
    console.error('加载题目失败', e)
  }
}

const toggleFavoriteQ = async () => {
  if (!currentQuestion.value) return
  try {
    if (currentFavorite.value) {
      await removeFavorite(currentFavoriteId.value)
      currentFavorite.value = false
      currentFavoriteId.value = null
    } else {
      const res = await addFavorite(currentQuestion.value.id)
      currentFavorite.value = true
      currentFavoriteId.value = res.data?.favorite_id || null
    }
  } catch (e) {
    console.error('收藏操作失败', e)
  }
}

const selectOption = (key) => {
  // 锁定题不能选择
  if (submitted.value || currentQuestion.value?.is_locked) return
  selectedAnswer.value = key
}

const submitAnswer = async () => {
  // 前端二次检查：锁定题不能提交
  if (currentQuestion.value?.is_locked) {
    alert('该题已作答，如需重做请先重置本子章节进度')
    return
  }
  if (!selectedAnswer.value) return

  const sessionId = sessionInfo.value.session_id
  const qid = currentQuestion.value.id
  try {
    const res = await submitPracticeAnswer(sessionId, {
      question_id: qid,
      user_answer: selectedAnswer.value
    })
    const result = res.data

    // 更新固定进度状态
    progressMap.value = {
      ...progressMap.value,
      [qid]: result.practice_status
    }

    submittedResult.value = {
      ...result,
      analysis_text: null,
      analysis_image: null,
    }
    submitted.value = true

    // 获取题目详情以显示解析
    try {
      const detailRes = await getQuestionDetail(qid)
      submittedResult.value.analysis_text = detailRes.data?.analysis_text || null
      submittedResult.value.analysis_image = detailRes.data?.analysis_image || null
    } catch (e) {
      console.error('获取题目详情失败', e)
    }

    await loadSession()
  } catch (e) {
    console.error('提交答案失败', e)
    alert('提交失败：' + (e.message || '未知错误'))
  }
}

const submitBigQuestion = async () => {
  if (currentQuestion.value?.is_locked) {
    alert('该题已作答，如需重做请先重置本子章节进度')
    return
  }

  const sessionId = sessionInfo.value.session_id
  const qid = currentQuestion.value.id
  try {
    const res = await submitPracticeAnswer(sessionId, {
      question_id: qid
    })
    const result = res.data

    progressMap.value = {
      ...progressMap.value,
      [qid]: result.practice_status
    }

    submittedResult.value = {
      ...result,
      analysis_text: null,
      analysis_image: null,
    }
    submitted.value = true

    await loadSession()
  } catch (e) {
    console.error('标记失败', e)
    alert('标记失败：' + (e.message || '未知错误'))
  }
}

const goNext = () => {
  if (currentIndex.value < questionIds.value.length - 1) {
    currentIndex.value++
    loadQuestion()
  }
}

const goPrev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    loadQuestion()
  }
}

const jumpTo = (idx) => {
  currentIndex.value = idx
  loadQuestion()
}

const goToFinish = () => doFinish()

const confirmFinish = () => {
  if (confirm('确定要结束练习吗？')) {
    doFinish()
  }
}

const restartPractice = () => {
  const subchapterId = sessionInfo.value.subchapter?.id
  if (subchapterId) {
    router.replace(`/practice/${subchapterId}`)
    window.location.reload()
  }
}

const confirmReset = () => {
  if (confirm('确定要重置本子章节的刷题进度吗？\n重置后所有题目状态将恢复为未作答（灰色），历史练习记录会保留。')) {
    doResetProgress()
  }
}

const doResetProgress = async () => {
  const subchapterId = sessionInfo.value.subchapter?.id
  if (!subchapterId) return
  try {
    await resetSubchapterProgress(subchapterId)
    // 重置成功后刷新页面状态
    progressMap.value = {}
    questionIds.value.forEach(qid => {
      progressMap.value[qid] = 'unattempted'
    })
    // 跳转到第一题
    currentIndex.value = 0
    submitted.value = false
    selectedAnswer.value = null
    submittedResult.value = null
    currentQuestion.value = null
    // 重置会话统计
    sessionInfo.value.answered_count = 0
    sessionInfo.value.correct_count = 0
    await loadQuestion()
    alert('进度已重置，所有题目恢复为未作答状态')
  } catch (e) {
    console.error('重置进度失败', e)
    alert('重置失败：' + (e.message || '未知错误'))
  }
}

const doFinish = async () => {
  stopTimer()
  const sessionId = sessionInfo.value.session_id
  try {
    await finishPractice(sessionId)
    finished.value = true
  } catch (e) {
    console.error('结束练习失败', e)
    alert('结束练习失败：' + (e.message || '未知错误'))
  }
}

// 根据 progress_map 找到第一道灰色题
const findFirstUnattempted = () => {
  const ids = questionIds.value
  for (let i = 0; i < ids.length; i++) {
    if (progressMap.value[ids[i]] === 'unattempted') {
      return i
    }
  }
  return 0 // 全部做完则定位到第一题
}

const init = async () => {
  loading.value = true
  const subchapterId = Number(route.params.subchapterId)

  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }

  try {
    const res = await startPractice(subchapterId)
    sessionInfo.value.session_id = res.data.session_id
    sessionInfo.value.subchapter = res.data.subchapter
    sessionInfo.value.total_count = res.data.total_count
    sessionInfo.value.answered_count = res.data.answered_count
    sessionInfo.value.correct_count = res.data.correct_count

    if (sessionInfo.value.total_count === 0) {
      noQuestions.value = true
      return
    }

    // 从 startPractice 获取 progress_map 并初始化 progressMap
    if (res.data.progress_map) {
      progressMap.value = res.data.progress_map
    }

    await loadSession()
    questionIds.value = questionIds.value.length > 0 ? questionIds.value : []

    if (questionIds.value.length === 0) {
      noQuestions.value = true
      return
    }

    // 默认跳转到第一道灰色题
    const firstUnattempted = findFirstUnattempted()
    currentIndex.value = firstUnattempted

    await loadQuestion()
    startTimer()
  } catch (e) {
    console.error('初始化练习失败', e)
    if (e.message && e.message.includes('暂无题目')) {
      noQuestions.value = true
    } else {
      alert('加载失败：' + (e.message || '未知错误'))
      router.push('/question-bank')
    }
  } finally {
    loading.value = false
  }
}

onMounted(init)
onUnmounted(async () => {
  stopTimer()
  if (pdfDoc) {
    pdfDoc.destroy()
    pdfDoc = null
  }
  // 如果练习还未主动结束（用户可能是关闭页面/跳转），自动结束 session
  // 这样 finished_at 才会被记录，时长统计才有数据
  if (!finished.value && sessionInfo.value.session_id) {
    try {
      await finishPractice(sessionInfo.value.session_id)
    } catch (_) {
      // 静默忽略，session 可能已经自动过期
    }
  }
})
</script>

<style scoped>
/* 页面容器 */
.practice-page {
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

/* 通用容器 */
.practice-container,
.loading-container,
.empty-container,
.result-container {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  position: relative;
  z-index: 1;
}

/* Loading */
.loading-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.loading-card {
  text-align: center;
  padding: 48px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid rgba(102, 126, 234, 0.15);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 15px;
  color: #909399;
}

/* 空状态 */
.empty-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}

.empty-card {
  text-align: center;
  padding: 60px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
  max-width: 400px;
}

.empty-icon-wrapper { margin-bottom: 24px; }
.empty-icon-wrapper svg { width: 120px; height: 120px; }

.empty-card h3 {
  font-size: 22px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 12px;
}

.empty-card p {
  font-size: 15px;
  color: #909399;
  margin-bottom: 28px;
}

.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}
.btn-back svg { width: 18px; height: 18px; }
.btn-back:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); }

/* 结果页 */
.result-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}

.result-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 28px;
  padding: 48px;
  box-shadow: 0 12px 48px rgba(102, 126, 234, 0.12);
  max-width: 560px;
  width: 100%;
  text-align: center;
}

.result-header { margin-bottom: 40px; }

.result-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, rgba(103, 194, 58, 0.15), rgba(103, 194, 58, 0.05));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
}
.result-icon svg { width: 40px; height: 40px; color: #67c23a; }

.result-header h2 { font-size: 28px; font-weight: 700; color: #303133; margin-bottom: 8px; }
.result-header p { font-size: 15px; color: #909399; }

.result-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}

.stat-card {
  background: #f9fafb;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  text-align: left;
}

.stat-card.highlight {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  border: 1px solid rgba(102, 126, 234, 0.15);
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.stat-icon svg { width: 22px; height: 22px; color: #fff; }
.stat-icon.blue { background: linear-gradient(135deg, #4facfe, #00f2fe); }
.stat-icon.purple { background: linear-gradient(135deg, #667eea, #764ba2); }
.stat-icon.green { background: linear-gradient(135deg, #43e97b, #38f9d7); }
.stat-icon.orange { background: linear-gradient(135deg, #fa709a, #fee140); }

.stat-info { display: flex; flex-direction: column; gap: 4px; }
.stat-value { font-size: 24px; font-weight: 700; color: #303133; }
.stat-value.correct { color: #67c23a; }
.stat-value.accent { color: #667eea; }
.stat-label { font-size: 12px; color: #909399; }

.result-actions { display: flex; gap: 12px; justify-content: center; }

.btn-primary-lg,
.btn-secondary-lg {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  font-size: 15px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.btn-primary-lg {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  border: none;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}
.btn-primary-lg:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); }
.btn-secondary-lg {
  background: #fff;
  color: #606266;
  border: 1.5px solid rgba(0, 0, 0, 0.1);
}
.btn-secondary-lg:hover { border-color: #667eea; color: #667eea; }
.btn-primary-lg svg, .btn-secondary-lg svg { width: 18px; height: 18px; }

/* 练习主体 */
.practice-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  margin-bottom: 24px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.06);
}

.header-left { display: flex; align-items: center; gap: 20px; }

.btn-back-small {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #f5f7fa;
  color: #606266;
  font-size: 13px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
}
.btn-back-small svg { width: 16px; height: 16px; }
.btn-back-small:hover { background: #e4e7ed; color: #303133; }

.session-title { font-size: 20px; font-weight: 700; color: #303133; margin-bottom: 6px; }
.session-meta { display: flex; gap: 16px; }

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #909399;
}
.meta-item svg { width: 14px; height: 14px; }
.meta-item.answered { color: #409eff; }
.meta-item.correct { color: #67c23a; }

.header-right { display: flex; align-items: center; gap: 10px; }

/* 重置进度按钮 */
.btn-reset-progress {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: rgba(245, 108, 108, 0.06);
  color: #f56c6c;
  font-size: 13px;
  font-weight: 500;
  border: 1.5px solid rgba(245, 108, 108, 0.25);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
}
.btn-reset-progress svg { width: 14px; height: 14px; }
.btn-reset-progress:hover {
  background: rgba(245, 108, 108, 0.12);
  border-color: #f56c6c;
}

.btn-finish {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #fff;
  color: #f56c6c;
  font-size: 14px;
  font-weight: 500;
  border: 1.5px solid rgba(245, 108, 108, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
}
.btn-finish svg { width: 16px; height: 16px; }
.btn-finish:hover { background: rgba(245, 108, 108, 0.04); border-color: #f56c6c; }

/* 主内容区 */
.practice-main {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 24px;
  margin-bottom: 24px;
}

/* 题目区域 */
.question-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.08);
}

.question-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.meta-left { display: flex; align-items: center; gap: 14px; }

.q-number {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-size: 15px;
  font-weight: 600;
  color: #909399;
  background: #f5f7fa;
  padding: 6px 14px;
  border-radius: 10px;
}

.q-type-tag {
  font-size: 12px;
  font-weight: 600;
  padding: 5px 14px;
  border-radius: 20px;
}
.q-type-tag.single_choice { background: rgba(64, 158, 255, 0.1); color: #409eff; }
.q-type-tag.big_question { background: rgba(230, 162, 60, 0.1); color: #e6a23c; }

/* 已锁定标签 */
.q-locked-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
  background: rgba(245, 108, 108, 0.1);
  color: #f56c6c;
}
.q-locked-tag svg { width: 12px; height: 12px; }

.btn-favorite-q {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
}
.btn-favorite-q svg { width: 18px; height: 18px; color: #909399; }
.btn-favorite-q:hover { background: rgba(230, 162, 60, 0.1); }
.btn-favorite-q:hover svg { color: #e6a23c; }
.btn-favorite-q.favorited { background: linear-gradient(135deg, #fa709a, #fee140); }
.btn-favorite-q.favorited svg { color: #fff; }

/* 题干 */
.question-stem { margin-bottom: 28px; }
.stem-text { font-size: 16px; color: #303133; line-height: 1.9; white-space: pre-wrap; margin: 0; }
.stem-image { max-width: 100%; border-radius: 16px; margin-top: 16px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); }

/* 选项 */
.question-options { display: flex; flex-direction: column; gap: 12px; margin-bottom: 28px; }

.option-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px 20px;
  background: #f9fafb;
  border: 2px solid transparent;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.25s ease;
  position: relative;
}
.option-card:hover:not(.dimmed) { border-color: rgba(102, 126, 234, 0.3); background: rgba(102, 126, 234, 0.04); }
.option-card.selected { border-color: #667eea; background: rgba(102, 126, 234, 0.06); }
.option-card.correct { border-color: #67c23a; background: rgba(103, 194, 58, 0.08); }
.option-card.wrong { border-color: #f56c6c; background: rgba(245, 108, 108, 0.08); }
.option-card.dimmed { opacity: 0.5; cursor: default; }

.opt-key {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  color: #667eea;
  font-size: 15px;
  font-weight: 700;
  border-radius: 10px;
  flex-shrink: 0;
  transition: all 0.25s ease;
}
.option-card.selected .opt-key { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; }
.option-card.correct .opt-key { background: #67c23a; color: #fff; }
.option-card.wrong .opt-key { background: #f56c6c; color: #fff; }

.opt-content { flex: 1; }
.opt-text { font-size: 15px; color: #303133; line-height: 1.6; }
.opt-image { max-width: 200px; border-radius: 8px; margin-top: 8px; }

.opt-badge {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 12px;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 20px;
}
.correct-badge { background: #67c23a; color: #fff; }
.wrong-badge { background: #f56c6c; color: #fff; }

/* 大题提示 */
.big-question-tip {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 18px 20px;
  background: linear-gradient(135deg, rgba(230, 162, 60, 0.08), rgba(230, 162, 60, 0.04));
  border: 1px solid rgba(230, 162, 60, 0.2);
  border-radius: 16px;
  margin-bottom: 28px;
}
.big-question-tip svg { width: 20px; height: 20px; color: #e6a23c; flex-shrink: 0; }
.big-question-tip span { font-size: 14px; color: #925f0a; line-height: 1.5; }

/* 锁定题提示 */
.locked-tip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: rgba(245, 108, 108, 0.06);
  border: 1px solid rgba(245, 108, 108, 0.2);
  border-radius: 14px;
  margin-bottom: 20px;
}
.locked-tip svg { width: 16px; height: 16px; color: #f56c6c; flex-shrink: 0; }
.locked-tip span { font-size: 13px; color: #f56c6c; line-height: 1.5; }

/* 答案解析区域 */
.answer-feedback-section {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.06), rgba(118, 75, 162, 0.04));
  border: 1px solid rgba(102, 126, 234, 0.15);
  border-radius: 20px;
  padding: 24px;
  margin-top: 8px;
}

.feedback-header { margin-bottom: 20px; }

.feedback-result-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  padding: 10px 20px;
  border-radius: 12px;
}
.feedback-result-badge svg { width: 18px; height: 18px; }
.badge-correct { background: rgba(103, 194, 58, 0.15); color: #67c23a; }
.badge-wrong { background: rgba(245, 108, 108, 0.15); color: #f56c6c; }
.badge-neutral { background: rgba(230, 162, 60, 0.15); color: #e6a23c; }

.feedback-correct-answer {
  background: rgba(103, 194, 58, 0.08);
  border: 1.5px solid rgba(103, 194, 58, 0.2);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 16px;
}

.feedback-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #8a92b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}
.feedback-label svg { width: 16px; height: 16px; }

.correct-answer-value {
  font-size: 28px;
  font-weight: 800;
  color: #67c23a;
  letter-spacing: 4px;
}

.feedback-analysis {
  background: rgba(91, 108, 255, 0.05);
  border: 1.5px solid rgba(91, 108, 255, 0.12);
  border-radius: 14px;
  padding: 16px 20px;
}
.analysis-text { font-size: 14px; color: #4a517a; line-height: 1.9; white-space: pre-wrap; }
.analysis-image { max-width: 100%; border-radius: 10px; margin-top: 10px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); }

.feedback-no-analysis {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 24px;
  color: #b0b5d0;
  font-size: 14px;
}
.feedback-no-analysis svg { width: 20px; height: 20px; }

/* 右侧面板 */
.sidebar-area { display: flex; flex-direction: column; gap: 20px; }

.sidebar-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 4px 24px rgba(102, 126, 234, 0.08);
}

.sidebar-card-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}
.sidebar-card-title svg { width: 18px; height: 18px; color: #667eea; }

/* 答题卡 */
.answer-legend { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 14px; }

.legend-pill {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 500;
}
.legend-pill.current { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; }
.legend-pill.correct { background: rgba(103, 194, 58, 0.15); color: #67c23a; }
.legend-pill.wrong { background: rgba(245, 108, 108, 0.15); color: #f56c6c; }
.legend-pill.unanswered { background: #f5f7fa; color: #909399; }

.answer-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }

.answer-btn {
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
.answer-btn:hover { border-color: rgba(102, 126, 234, 0.3); color: #667eea; }
.answer-btn.current { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3); }
.answer-btn.correct { background: rgba(103, 194, 58, 0.15); color: #67c23a; }
.answer-btn.wrong { background: rgba(245, 108, 108, 0.15); color: #f56c6c; }
.answer-btn.unattempted { background: rgba(64, 158, 255, 0.06); color: #909399; }
.answer-btn.unattempted:hover { border-color: rgba(102, 126, 234, 0.3); color: #667eea; }

/* 计时器 */
.timer-card { text-align: center; }

.timer-display {
  font-size: 36px;
  font-weight: 700;
  font-family: 'SF Mono', 'Consolas', monospace;
  color: #303133;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.timer-controls { display: flex; gap: 8px; }

.timer-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  background: #f5f7fa;
  color: #606266;
  font-size: 13px;
  font-weight: 500;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.25s ease;
}
.timer-btn svg { width: 14px; height: 14px; }
.timer-btn:hover { background: rgba(102, 126, 234, 0.1); color: #667eea; }
.timer-btn.reset:hover { background: rgba(245, 108, 108, 0.1); color: #f56c6c; }

/* 底部操作栏 */
.practice-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: rgba(255, 255, 255, 0.98);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  box-shadow: 0 -4px 24px rgba(102, 126, 234, 0.06);
}

.btn-nav-footer {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
}
.btn-nav-footer svg { width: 18px; height: 18px; }
.btn-nav-footer.prev { background: #f5f7fa; color: #606266; border: none; }
.btn-nav-footer.prev:hover:not(:disabled) { background: #e4e7ed; color: #303133; }
.btn-nav-footer.next { background: #f5f7fa; color: #606266; border: none; }
.btn-nav-footer.next:hover { background: rgba(102, 126, 234, 0.1); color: #667eea; }
.btn-nav-footer:disabled { opacity: 0.4; cursor: not-allowed; }

.footer-center { flex: 1; display: flex; justify-content: center; padding: 0 20px; }

.progress-dots { display: flex; gap: 6px; flex-wrap: wrap; max-width: 400px; justify-content: center; }

.progress-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e4e7ed;
  transition: all 0.2s ease;
}
.progress-dot.current { background: linear-gradient(135deg, #667eea, #764ba2); transform: scale(1.4); box-shadow: 0 2px 6px rgba(102, 126, 234, 0.4); }
.progress-dot.correct { background: #67c23a; }
.progress-dot.wrong { background: #f56c6c; }

.btn-submit-answer {
  padding: 14px 32px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}
.btn-submit-answer:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); }
.btn-submit-answer:disabled { background: #c0c4cc; box-shadow: none; cursor: not-allowed; }

.btn-finish-practice {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #43e97b, #38f9d7);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(67, 233, 123, 0.3);
}
.btn-finish-practice svg { width: 18px; height: 18px; }
.btn-finish-practice:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(67, 233, 123, 0.4); }

/* 响应式 */
@media (max-width: 1024px) {
  .practice-main { grid-template-columns: 1fr; }
  .sidebar-area { display: grid; grid-template-columns: repeat(2, 1fr); }
  .answer-grid { grid-template-columns: repeat(8, 1fr); }
}

@media (max-width: 768px) {
  .practice-header { flex-direction: column; gap: 16px; align-items: flex-start; }
  .header-left { flex-direction: column; align-items: flex-start; gap: 12px; }
  .sidebar-area { grid-template-columns: 1fr; }
  .practice-footer { flex-wrap: wrap; gap: 12px; }
  .footer-center { order: -1; width: 100%; }
  .result-stats { grid-template-columns: 1fr; }
  .result-actions { flex-direction: column; }
}
</style>
