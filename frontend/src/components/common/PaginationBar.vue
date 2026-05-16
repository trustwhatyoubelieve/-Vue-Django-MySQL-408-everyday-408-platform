<template>
  <div v-if="totalPages > 0" class="pagination-bar">
    <button
      class="page-btn"
      :disabled="currentPage <= 1"
      @click="$emit('page-change', currentPage - 1)"
    >
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15,18 9,12 15,6"/>
      </svg>
    </button>

    <button
      v-if="startPage > 1"
      class="page-btn"
      @click="$emit('page-change', 1)"
    >1</button>

    <span v-if="startPage > 2" class="page-ellipsis">...</span>

    <button
      v-for="page in visiblePages"
      :key="page"
      class="page-btn"
      :class="{ active: page === currentPage }"
      @click="$emit('page-change', page)"
    >{{ page }}</button>

    <span v-if="endPage < totalPages - 1" class="page-ellipsis">...</span>

    <button
      v-if="endPage < totalPages"
      class="page-btn"
      @click="$emit('page-change', totalPages)"
    >{{ totalPages }}</button>

    <button
      class="page-btn"
      :disabled="currentPage >= totalPages"
      @click="$emit('page-change', currentPage + 1)"
    >
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9,18 15,12 9,6"/>
      </svg>
    </button>

    <span class="page-info">
      共 {{ total }} 条 / 第 {{ currentPage }} / {{ totalPages }} 页
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: { type: Number, default: 1 },
  totalPages: { type: Number, default: 1 },
  total: { type: Number, default: 0 }
})

defineEmits(['page-change'])

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, props.currentPage - 2)
  const end = Math.min(props.totalPages, props.currentPage + 2)
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})
</script>
