<template>
  <div class="filter-card">
    <div class="filter-row">
      <select
        v-model="localCourse"
        @change="onCourseChange"
        class="filter-select"
      >
        <option value="">全部课程</option>
        <option v-for="c in courseOptions" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>

      <select
        v-model="localChapter"
        @change="onChapterChange"
        class="filter-select"
        :disabled="!localCourse"
      >
        <option value="">全部章节</option>
        <option v-for="ch in chapterOptions" :key="ch.id" :value="ch.id">{{ ch.name }}</option>
      </select>

      <select
        v-model="localSubchapter"
        @change="onSubchapterChange"
        class="filter-select"
        :disabled="!localChapter"
      >
        <option value="">全部子章节</option>
        <option v-for="sc in subchapterOptions" :key="sc.id" :value="sc.id">{{ sc.name }}</option>
      </select>

      <input
        v-model="localKeyword"
        @keyup.enter="onSearch"
        type="text"
        class="filter-input"
        placeholder="搜索题目编号或题干关键词..."
      />

      <button class="btn-filter" @click="onSearch">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/>
          <line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        筛选
      </button>

      <button
        v-if="hasActiveFilter"
        class="btn-reset-small"
        @click="onReset"
      >
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
        重置
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { getChaptersByCourse, getSubChaptersByChapter } from '@/api/questionBank'

const props = defineProps({
  courseOptions: { type: Array, default: () => [] },
  modelCourse: { type: [String, Number], default: '' },
  modelChapter: { type: [String, Number], default: '' },
  modelSubchapter: { type: [String, Number], default: '' },
  modelKeyword: { type: String, default: '' }
})

const emit = defineEmits([
  'update:modelCourse',
  'update:modelChapter',
  'update:modelSubchapter',
  'update:modelKeyword',
  'filter-change',
  'course-change',
  'chapter-change'
])

const localCourse = ref(props.modelCourse)
const localChapter = ref(props.modelChapter)
const localSubchapter = ref(props.modelSubchapter)
const localKeyword = ref(props.modelKeyword)
const chapterOptions = ref([])
const subchapterOptions = ref([])

watch(() => props.modelCourse, v => { localCourse.value = v })
watch(() => props.modelChapter, v => { localChapter.value = v })
watch(() => props.modelSubchapter, v => { localSubchapter.value = v })
watch(() => props.modelKeyword, v => { localKeyword.value = v })

const hasActiveFilter = computed(() =>
  localCourse.value || localChapter.value || localSubchapter.value || localKeyword.value
)

const onCourseChange = async () => {
  localChapter.value = ''
  localSubchapter.value = ''
  chapterOptions.value = []
  subchapterOptions.value = []
  emit('update:modelCourse', localCourse.value)
  if (localCourse.value) {
    try {
      const res = await getChaptersByCourse(localCourse.value)
      chapterOptions.value = res.data || []
    } catch (e) {
      console.error('加载章节列表失败', e)
    }
  }
  emit('course-change', localCourse.value)
}

const onChapterChange = async () => {
  localSubchapter.value = ''
  subchapterOptions.value = []
  emit('update:modelChapter', localChapter.value)
  if (localChapter.value) {
    try {
      const res = await getSubChaptersByChapter(localChapter.value)
      subchapterOptions.value = res.data || []
    } catch (e) {
      console.error('加载子章节列表失败', e)
    }
  }
  emit('chapter-change', localChapter.value)
}

const onSubchapterChange = () => {
  emit('update:modelSubchapter', localSubchapter.value)
  emit('filter-change')
}

const onSearch = () => {
  emit('update:modelKeyword', localKeyword.value)
  emit('filter-change')
}

const onReset = () => {
  localCourse.value = ''
  localChapter.value = ''
  localSubchapter.value = ''
  localKeyword.value = ''
  chapterOptions.value = []
  subchapterOptions.value = []
  emit('update:modelCourse', '')
  emit('update:modelChapter', '')
  emit('update:modelSubchapter', '')
  emit('update:modelKeyword', '')
  emit('filter-change')
}
</script>
