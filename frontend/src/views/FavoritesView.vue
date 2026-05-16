<template>
  <div class="page-container">
    <!-- 页面英雄区 -->
    <div class="page-hero">
      <div class="page-hero-title">我的收藏夹</div>
      <div class="page-hero-subtitle">您收藏的题目会在这里展示，方便随时复习与练习</div>
    </div>

    <!-- 统计卡片 -->
    <PageHeaderStats :stats="statsData" />

    <!-- 列表/详情切换 -->
    <div v-if="!currentFavorite">
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
        <div class="list-count">共 <span>{{ favorites.length }}</span> 题</div>
        <div class="list-sort">
          <span>排序：</span>
          <select v-model="sortOrder" class="sort-select" @change="loadList">
            <option value="recent">最近收藏</option>
            <option value="time">收藏时间</option>
            <option value="course">按课程</option>
          </select>
        </div>
      </div>

      <!-- 加载中 -->
      <div v-if="loading" class="loading-wrapper">
        <div class="loading-spinner"></div>
        <div class="loading-text">正在加载收藏数据...</div>
      </div>

      <!-- 空状态 -->
      <EmptyStateCard
        v-else-if="favorites.length === 0"
        type="star"
        title="暂无收藏"
        description="在题库中点击收藏按钮，将喜欢的题目加入收藏夹，方便随时复习与练习。"
      />

      <!-- 收藏列表 -->
      <template v-else>
        <QuestionCard
          v-for="item in paginatedFavorites"
          :key="item.id"
          :item="item"
          iconType="star"
          actionLabel="开始练习"
          removeLabel="取消收藏"
          @click="showDetail(item)"
          @action="onPractice(item)"
          @remove="onRemove(item)"
        />

        <!-- 分页 -->
        <PaginationBar
          :currentPage="currentPage"
          :totalPages="totalPages"
          :total="favorites.length"
          @page-change="onPageChange"
        />
      </template>
    </div>

    <!-- 详情页 -->
    <div v-else>
      <!-- 顶部操作栏 -->
      <div class="detail-topbar">
        <div class="detail-topbar-left">
          <button class="btn-back-new" @click="currentFavorite = null">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15,18 9,12 15,6"/>
            </svg>
            返回列表
          </button>
        </div>
        <div class="detail-topbar-right">
          <button class="btn-danger-action" @click="onRemoveFromDetail">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>
            </svg>
            取消收藏
          </button>
          <button class="btn-primary-action" @click="onPracticeFromDetail">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23,4 23,10 17,10"/>
              <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/>
            </svg>
            开始练习
          </button>
        </div>
      </div>

      <!-- 详情卡片 -->
      <div class="detail-card">
        <div class="detail-meta-row">
          <span class="detail-id">{{ currentFavorite.business_id }}</span>
          <span class="tag tag-green">{{ typeLabel(currentFavorite.question_type) }}</span>
          <span v-if="currentFavorite.favorite_time" class="tag tag-purple">
            收藏于 {{ formatDate(currentFavorite.favorite_time) }}
          </span>
        </div>
        <div class="detail-path">
          {{ currentFavorite.course_name }}
          <span class="sep">&gt;</span>
          {{ currentFavorite.chapter_name }}
          <span class="sep">&gt;</span>
          {{ currentFavorite.subchapter_name }}
        </div>

        <!-- 题干 -->
        <div class="detail-section">
          <div class="detail-label">题干</div>
          <div v-if="currentFavorite.stem_text" class="detail-text">{{ currentFavorite.stem_text }}</div>
          <img v-if="currentFavorite.stem_image" :src="currentFavorite.stem_image" class="detail-img" />
        </div>

        <!-- 选项 -->
        <div v-if="currentFavorite.question_type === 'single_choice'" class="detail-section">
          <div class="detail-label">选项</div>
          <div
            v-for="opt in detailOptions"
            :key="opt.key"
            class="option-item"
            :class="{ correct: opt.key === currentFavorite.correct_answer }"
          >
            <span class="option-key">{{ opt.key }}.</span>
            <span v-if="opt.text" class="option-text">{{ opt.text }}</span>
            <img v-if="opt.image" :src="opt.image" class="option-img" />
          </div>
        </div>

        <!-- 正确答案 -->
        <div class="detail-section">
          <div class="detail-label">正确答案</div>
          <div class="correct-answer-display">{{ currentFavorite.correct_answer }}</div>
        </div>

        <!-- 解析 -->
        <div v-if="currentFavorite.analysis_text || currentFavorite.analysis_image" class="detail-section">
          <div class="detail-label">解析</div>
          <div v-if="currentFavorite.analysis_text" class="detail-text">{{ currentFavorite.analysis_text }}</div>
          <img v-if="currentFavorite.analysis_image" :src="currentFavorite.analysis_image" class="detail-img" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getFavorites, removeFavorite } from '@/api/records'
import { getQuestionDetail, getCourses } from '@/api/questionBank'
import PageHeaderStats from '@/components/common/PageHeaderStats.vue'
import FilterToolbar from '@/components/common/FilterToolbar.vue'
import QuestionCard from '@/components/common/QuestionCard.vue'
import EmptyStateCard from '@/components/common/EmptyStateCard.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'

const router = useRouter()

const loading = ref(false)
const favorites = ref([])
const currentFavorite = ref(null)
const courseOptions = ref([])
const filterCourse = ref('')
const filterChapter = ref('')
const filterSubchapter = ref('')
const filterKeyword = ref('')
const sortOrder = ref('recent')
const currentPage = ref(1)
const pageSize = ref(10)

const totalPages = computed(() => Math.max(1, Math.ceil(favorites.value.length / pageSize.value)))

const paginatedFavorites = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return favorites.value.slice(start, start + pageSize.value)
})

const statsData = computed(() => {
  const total = favorites.value.length
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const thisWeek = new Date(today)
  thisWeek.setDate(thisWeek.getDate() - 7)

  let recentAdded = 0
  let weekAdded = 0

  favorites.value.forEach(item => {
    if (!item.created_at) return
    const d = new Date(item.created_at)
    d.setHours(0, 0, 0, 0)
    if (d.getTime() === today.getTime()) recentAdded++
    if (d >= thisWeek) weekAdded++
  })

  return [
    {
      icon: 'star',
      iconBg: 'linear-gradient(135deg, rgba(230,162,60,0.15), rgba(230,162,60,0.08))',
      value: total,
      label: '收藏总数'
    },
    {
      icon: 'target',
      iconBg: 'linear-gradient(135deg, rgba(91,108,255,0.15), rgba(107,95,214,0.08))',
      value: Math.floor(total * 0.3),
      label: '重点题目'
    },
    {
      icon: 'add',
      iconBg: 'linear-gradient(135deg, rgba(103,194,58,0.15), rgba(103,194,58,0.08))',
      value: recentAdded,
      label: '今日新增'
    },
    {
      icon: 'clock',
      iconBg: 'linear-gradient(135deg, rgba(107,95,214,0.15), rgba(91,108,255,0.08))',
      value: weekAdded,
      label: '本周新增'
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
    const res = await getFavorites(params)
    let data = res.data || []

    if (filterKeyword.value) {
      const kw = filterKeyword.value.toLowerCase()
      data = data.filter(item =>
        (item.business_id || '').toLowerCase().includes(kw) ||
        (item.stem_text || '').toLowerCase().includes(kw)
      )
    }

    favorites.value = data
  } catch (e) {
    console.error('加载收藏夹失败', e)
    favorites.value = []
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
  currentFavorite.value = null
  try {
    const res = await getQuestionDetail(item.question_id)
    currentFavorite.value = { ...res.data, favorite_id: item.id, favorite_time: item.created_at }
  } catch (e) {
    console.error('加载收藏详情失败', e)
  }
}

const onRemove = async (item) => {
  if (!confirm('确定要取消收藏吗？')) return
  try {
    await removeFavorite(item.id)
    favorites.value = favorites.value.filter(f => f.id !== item.id)
    alert('已取消收藏')
  } catch (e) {
    console.error('取消收藏失败', e)
  }
}

const onRemoveFromDetail = async () => {
  if (!currentFavorite.value) return
  if (!confirm('确定要取消收藏吗？')) return
  try {
    await removeFavorite(currentFavorite.value.favorite_id)
    favorites.value = favorites.value.filter(f => f.id !== currentFavorite.value.favorite_id)
    currentFavorite.value = null
    alert('已取消收藏')
  } catch (e) {
    console.error('取消收藏失败', e)
  }
}

const onPractice = (item) => {
  router.push(`/practice/${item.subchapter_id}`)
}

const onPracticeFromDetail = () => {
  if (!currentFavorite.value) return
  router.push(`/practice/${currentFavorite.value.subchapter_id}`)
}

const onPageChange = (page) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const typeLabel = (type) => type === 'single_choice' ? '单选题' : '大题'

const formatDate = (str) => {
  if (!str) return ''
  const d = new Date(str)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const detailOptions = computed(() => {
  if (!currentFavorite.value) return []
  return ['A', 'B', 'C', 'D'].map(key => ({
    key,
    text: currentFavorite.value[`option_${key.toLowerCase()}_text`],
    image: currentFavorite.value[`option_${key.toLowerCase()}_image`]
  })).filter(opt => opt.text || opt.image)
})

onMounted(() => {
  loadCourses()
  loadList()
})
</script>
