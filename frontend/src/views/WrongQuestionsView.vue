<template>
  <div class="page-container">
    <!-- 页面英雄区 -->
    <div class="page-hero">
      <div class="page-hero-title">我的错题本</div>
      <div class="page-hero-subtitle">汇总所有做错的题目，针对性复习，高效提升</div>
    </div>

    <!-- 统计卡片 -->
    <PageHeaderStats :stats="statsData" />

    <!-- 列表/详情切换 -->
    <div v-if="!currentDetail">
      <!-- 筛选工具条 -->
      <FilterToolbar
        :courseOptions="courseOptions"
        v-model:modelCourse="filterCourse"
        v-model:modelChapter="filterChapter"
        v-model:modelSubchapter="filterSubchapter"
        v-model:modelKeyword="filterKeyword"
        @filter-change="loadList"
        @course-change="loadList"
      />

      <!-- 列表标题栏 -->
      <div class="list-header">
        <div class="list-count">共 <span>{{ wrongQuestions.length }}</span> 题</div>
        <div class="list-sort">
          <span>排序：</span>
          <select v-model="sortOrder" class="sort-select" @change="loadList">
            <option value="recent">最近错误</option>
            <option value="times">错误次数</option>
            <option value="course">按课程</option>
          </select>
        </div>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="loading-wrapper">
        <div class="loading-spinner"></div>
        <div class="loading-text">正在加载错题数据...</div>
      </div>

      <!-- 空状态 -->
      <EmptyStateCard
        v-else-if="wrongQuestions.length === 0"
        type="success"
        title="暂无错题"
        description="太棒了！你没有需要复习的错题，继续保持这份学习状态吧！"
      />

      <!-- 错题列表 -->
      <template v-else>
        <QuestionCard
          v-for="item in paginatedQuestions"
          :key="item.id"
          :item="item"
          iconType="error"
          actionLabel="去重练"
          removeLabel="移出错题本"
          @click="showDetail(item)"
          @action="onRePractice(item)"
          @remove="onRemove(item)"
        />

        <!-- 分页 -->
        <PaginationBar
          :currentPage="currentPage"
          :totalPages="totalPages"
          :total="wrongQuestions.length"
          @page-change="onPageChange"
        />
      </template>
    </div>

    <!-- 详情页 -->
    <div v-else>
      <!-- 顶部操作栏 -->
      <div class="detail-topbar">
        <div class="detail-topbar-left">
          <button class="btn-back-new" @click="currentDetail = null">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15,18 9,12 15,6"/>
            </svg>
            返回列表
          </button>
        </div>
        <div class="detail-topbar-right">
          <button class="btn-danger-action" @click="onRemoveFromDetail">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3,6 5,6 21,6"/>
              <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
              <path d="M10 11v6M14 11v6"/>
            </svg>
            移出错题本
          </button>
          <button class="btn-primary-action" @click="onRePracticeFromDetail">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23,4 23,10 17,10"/>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
            </svg>
            去重练
          </button>
        </div>
      </div>

      <!-- 详情卡片 -->
      <div class="detail-card">
        <div class="detail-meta-row">
          <span class="detail-id">{{ currentDetail.business_id }}</span>
          <span class="tag tag-green">{{ typeLabel(currentDetail.question_type) }}</span>
          <span class="tag tag-red">累计答错 {{ currentDetail.wrong_count }} 次</span>
        </div>
        <div class="detail-path">
          {{ currentDetail.course_name }}
          <span class="sep">&gt;</span>
          {{ currentDetail.chapter_name }}
          <span class="sep">&gt;</span>
          {{ currentDetail.subchapter_name }}
        </div>

        <!-- 题干 -->
        <div class="detail-section">
          <div class="detail-label">题干</div>
          <div v-if="currentDetail.stem_text" class="detail-text">{{ currentDetail.stem_text }}</div>
          <img v-if="currentDetail.stem_image" :src="currentDetail.stem_image" class="detail-img" />
        </div>

        <!-- 选项 -->
        <div v-if="currentDetail.question_type === 'single_choice'" class="detail-section">
          <div class="detail-label">选项</div>
          <div
            v-for="opt in detailOptions"
            :key="opt.key"
            class="option-item"
            :class="{ correct: opt.key === currentDetail.correct_answer }"
          >
            <span class="option-key">{{ opt.key }}.</span>
            <span v-if="opt.text" class="option-text">{{ opt.text }}</span>
            <img v-if="opt.image" :src="opt.image" class="option-img" />
          </div>
        </div>

        <!-- 正确答案 -->
        <div class="detail-section">
          <div class="detail-label">正确答案</div>
          <div class="correct-answer-display">{{ currentDetail.correct_answer }}</div>
        </div>

        <!-- 解析 -->
        <div v-if="currentDetail.analysis_text || currentDetail.analysis_image" class="detail-section">
          <div class="detail-label">解析</div>
          <div v-if="currentDetail.analysis_text" class="detail-text">{{ currentDetail.analysis_text }}</div>
          <img v-if="currentDetail.analysis_image" :src="currentDetail.analysis_image" class="detail-img" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getWrongQuestions, getWrongQuestionDetail, removeWrongQuestion } from '@/api/records'
import { getCourses } from '@/api/questionBank'
import PageHeaderStats from '@/components/common/PageHeaderStats.vue'
import FilterToolbar from '@/components/common/FilterToolbar.vue'
import QuestionCard from '@/components/common/QuestionCard.vue'
import EmptyStateCard from '@/components/common/EmptyStateCard.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'

const router = useRouter()

const loading = ref(false)
const wrongQuestions = ref([])
const currentDetail = ref(null)
const courseOptions = ref([])
const filterCourse = ref('')
const filterChapter = ref('')
const filterSubchapter = ref('')
const filterKeyword = ref('')
const sortOrder = ref('recent')
const currentPage = ref(1)
const pageSize = ref(10)

const totalPages = computed(() => Math.max(1, Math.ceil(wrongQuestions.value.length / pageSize.value)))

const paginatedQuestions = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return wrongQuestions.value.slice(start, start + pageSize.value)
})

const statsData = computed(() => {
  const total = wrongQuestions.value.length
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const todayAdded = wrongQuestions.value.filter(item => {
    if (!item.created_at) return false
    const d = new Date(item.created_at)
    d.setHours(0, 0, 0, 0)
    return d.getTime() === today.getTime()
  }).length
  const mastered = 0
  return [
    {
      icon: 'error',
      iconBg: 'linear-gradient(135deg, rgba(245,108,108,0.15), rgba(245,108,108,0.08))',
      value: total,
      label: '累计错题数'
    },
    {
      icon: 'add',
      iconBg: 'linear-gradient(135deg, rgba(230,162,60,0.15), rgba(230,162,60,0.08))',
      value: todayAdded,
      label: '今日新增'
    },
    {
      icon: 'review',
      iconBg: 'linear-gradient(135deg, rgba(91,108,255,0.15), rgba(107,95,214,0.08))',
      value: total,
      label: '待复习'
    },
    {
      icon: 'done',
      iconBg: 'linear-gradient(135deg, rgba(103,194,58,0.15), rgba(103,194,58,0.08))',
      value: mastered,
      label: '已掌握'
    }
  ]
})

const loadList = async () => {
  loading.value = true
  currentPage.value = 1
  try {
    const params = {}
    if (filterCourse.value) params.course_id = filterCourse.value
    if (filterChapter.value) params.chapter_id = filterChapter.value
    if (filterSubchapter.value) params.subchapter_id = filterSubchapter.value
    const res = await getWrongQuestions(params)
    let data = res.data || []

    if (filterKeyword.value) {
      const kw = filterKeyword.value.toLowerCase()
      data = data.filter(item =>
        (item.business_id || '').toLowerCase().includes(kw) ||
        (item.stem_text || '').toLowerCase().includes(kw)
      )
    }

    if (sortOrder.value === 'times') {
      data = [...data].sort((a, b) => (b.wrong_count || 0) - (a.wrong_count || 0))
    }

    wrongQuestions.value = data
  } catch (e) {
    console.error('加载错题本失败', e)
    wrongQuestions.value = []
  } finally {
    loading.value = false
  }
}

const loadCourses = async () => {
  try {
    const res = await getCourses()
    courseOptions.value = res.data || []
  } catch (e) {
    console.error('加载课程列表失败', e)
  }
}

const showDetail = async (item) => {
  currentDetail.value = null
  try {
    const res = await getWrongQuestionDetail(item.id)
    currentDetail.value = res.data
  } catch (e) {
    console.error('加载错题详情失败', e)
  }
}

const onRemove = async (item) => {
  if (!confirm('确定要将此题移出错题本吗？')) return
  try {
    await removeWrongQuestion(item.id)
    wrongQuestions.value = wrongQuestions.value.filter(q => q.id !== item.id)
    alert('已移出错题本')
  } catch (e) {
    console.error('移除失败', e)
  }
}

const onRemoveFromDetail = async () => {
  if (!currentDetail.value) return
  if (!confirm('确定要将此题移出错题本吗？')) return
  try {
    await removeWrongQuestion(currentDetail.value.id)
    wrongQuestions.value = wrongQuestions.value.filter(q => q.id !== currentDetail.value.id)
    currentDetail.value = null
    alert('已移出错题本')
  } catch (e) {
    console.error('移除失败', e)
  }
}

const onRePractice = (item) => {
  router.push(`/practice/${item.subchapter_id}`)
}

const onRePracticeFromDetail = () => {
  if (!currentDetail.value) return
  router.push(`/practice/${currentDetail.value.subchapter_id}`)
}

const onPageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const typeLabel = (type) => type === 'single_choice' ? '单选题' : '大题'

const detailOptions = computed(() => {
  if (!currentDetail.value) return []
  return ['A', 'B', 'C', 'D'].map(key => ({
    key,
    text: currentDetail.value[`option_${key.toLowerCase()}_text`],
    image: currentDetail.value[`option_${key.toLowerCase()}_image`]
  })).filter(opt => opt.text || opt.image)
})

onMounted(() => {
  loadCourses()
  loadList()
})
</script>
