<template>
  <div class="empty-card">
    <div class="empty-icon-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path v-if="type === 'success'" d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline v-if="type === 'success'" points="22,4 12,14.01 9,11.01"/>

        <path v-else-if="type === 'star'" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>

        <circle v-else-if="type === 'error'" cx="12" cy="12" r="10"/>
        <line v-if="type === 'error'" x1="12" y1="8" x2="12" y2="12"/>
        <line v-if="type === 'error'" x1="12" y1="16" x2="12.01" y2="16"/>

        <rect v-else x="3" y="3" width="18" height="18" rx="2" ry="2"/>
        <line v-if="type === 'search'" x1="9" y1="9" x2="15" y2="15"/>
        <line v-if="type === 'search'" x1="15" y1="9" x2="9" y2="15"/>
      </svg>
    </div>
    <div class="empty-title">{{ title }}</div>
    <p class="empty-desc">{{ description }}</p>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  type: { type: String, default: 'star' },
  title: { type: String, default: '暂无数据' },
  description: { type: String, default: '' }
})
</script>
