<template>
  <div class="question-card" @click="$emit('click')">
    <!-- 左侧图标块 -->
    <div class="card-icon-block" :class="iconClass">
      <svg v-if="iconType === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <svg v-else-if="iconType === 'star'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
      </svg>
      <svg v-else-if="iconType === 'clock'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12,6 12,12 16,14"/>
      </svg>
    </div>

    <!-- 中间内容 -->
    <div class="card-body">
      <div class="card-meta-row">
        <span class="card-id">{{ item.business_id }}</span>
        <span class="tag" :class="typeTagClass">{{ typeLabel }}</span>
        <span v-if="item.wrong_count" class="tag tag-red">
          答错 {{ item.wrong_count }} 次
        </span>
        <span v-if="item.favorite_time" class="tag tag-purple">
          {{ formatTime(item.favorite_time) }}
        </span>
      </div>

      <div class="card-stem">{{ item.stem_text || '[图片题]' }}</div>

      <div class="card-path">
        {{ item.course_name }}
        <span class="separator">&gt;</span>
        {{ item.chapter_name }}
        <span class="separator">&gt;</span>
        {{ item.subchapter_name }}
      </div>

      <div v-if="item.last_wrong_time" class="card-time">
        上次错误：{{ formatDate(item.last_wrong_time) }}
      </div>
    </div>

    <!-- 右侧操作按钮 -->
    <div class="card-actions" @click.stop>
      <button class="btn-detail" @click.stop="$emit('click')">查看详情</button>
      <button class="btn-primary-action" @click.stop="$emit('action')">
        {{ actionLabel }}
      </button>
      <button class="btn-danger-action" @click.stop="$emit('remove')">
        {{ removeLabel }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  item: { type: Object, required: true },
  iconType: { type: String, default: 'error' },
  actionLabel: { type: String, default: '去重练' },
  removeLabel: { type: String, default: '移出错题本' }
})

defineEmits(['click', 'action', 'remove'])

const iconClass = computed(() => {
  if (props.iconType === 'error') return 'card-icon-purple'
  if (props.iconType === 'clock') return 'card-icon-blue'
  return 'card-icon-orange'
})

const typeLabel = computed(() =>
  props.item.question_type === 'single_choice' ? '单选题' : '大题'
)

const typeTagClass = computed(() =>
  props.item.question_type === 'single_choice' ? 'tag-green' : 'tag-orange'
)

const formatDate = (str) => {
  if (!str) return ''
  const d = new Date(str)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const formatTime = (str) => {
  if (!str) return ''
  const d = new Date(str)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
</script>

<style scoped>
.question-card {
  background: white;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.question-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  border-color: #e0e0e0;
}

.card-icon-block {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.card-icon-purple {
  background: #f3e8ff;
  color: #9333ea;
}

.card-icon-orange {
  background: #fff7ed;
  color: #ea580c;
}

.card-icon-blue {
  background: #eff6ff;
  color: #2563eb;
}

.card-icon-block svg {
  width: 22px;
  height: 22px;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-meta-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  flex-wrap: wrap;
}

.card-id {
  font-weight: 700;
  font-size: 13px;
  color: #333;
}

.tag {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}

.tag-green {
  background: #dcfce7;
  color: #16a34a;
}

.tag-orange {
  background: #ffedd5;
  color: #ea580c;
}

.tag-red {
  background: #fef2f2;
  color: #dc2626;
}

.tag-purple {
  background: #f3e8ff;
  color: #9333ea;
}

.card-stem {
  font-size: 14px;
  color: #333;
  line-height: 1.6;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 4px;
}

.card-path {
  font-size: 12px;
  color: #999;
}

.card-path .separator {
  margin: 0 3px;
}

.card-time {
  font-size: 12px;
  color: #ef4444;
  margin-top: 4px;
}

.card-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.btn-detail,
.btn-primary-action,
.btn-danger-action {
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  white-space: nowrap;
  transition: all 0.2s;
}

.btn-detail {
  background: #f5f5f5;
  color: #555;
}

.btn-detail:hover {
  background: #e8e8e8;
  color: #333;
}

.btn-primary-action {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-primary-action:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

.btn-danger-action {
  background: white;
  color: #ef4444;
  border: 1.5px solid #fecaca;
}

.btn-danger-action:hover {
  background: #fef2f2;
  border-color: #ef4444;
}
</style>
