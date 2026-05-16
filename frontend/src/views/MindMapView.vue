<template>
  <div class="mindmap-page">
    <div class="page-header">
      <div class="header-content">
        <div class="header-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <circle cx="12" cy="12" r="3"/>
            <line x1="12" y1="2" x2="12" y2="5"/>
            <line x1="12" y1="19" x2="12" y2="22"/>
            <line x1="2" y1="12" x2="5" y2="12"/>
            <line x1="19" y1="12" x2="22" y2="12"/>
          </svg>
        </div>
        <div class="header-text">
          <h1>思维导图</h1>
          <p>选择课程，查看知识点思维导图</p>
        </div>
      </div>
    </div>

    <div class="mindmap-container">
      <!-- 左侧：课程选择 -->
      <div class="course-sidebar">
        <div class="sidebar-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
          选择课程
        </div>
        <div class="course-list">
          <button
            v-for="course in courses"
            :key="course.id"
            class="course-item"
            :class="{ active: selectedCourseId === course.id }"
            @click="selectCourse(course)"
          >
            <div class="course-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 10v6M2 10l10-5 10 5-10 5z"/>
                <path d="M6 12v5c0 2 2 3 6 3s6-1 6-3v-5"/>
              </svg>
            </div>
            <div class="course-info">
              <span class="course-name">{{ course.name }}</span>
              <span class="course-code">章节数：{{ course.chapter_count }}</span>
            </div>
            <div v-if="course.has_mindmap" class="has-mindmap-badge">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <polyline points="20,6 9,17 4,12"/>
              </svg>
            </div>
          </button>
        </div>
      </div>

      <!-- 右侧：思维导图预览 -->
      <div class="mindmap-preview-area">
        <div v-if="!selectedCourseId" class="empty-state">
          <div class="empty-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="10"/>
              <circle cx="12" cy="12" r="3"/>
              <line x1="12" y1="2" x2="12" y2="5"/>
              <line x1="12" y1="19" x2="12" y2="22"/>
              <line x1="2" y1="12" x2="5" y2="12"/>
              <line x1="19" y1="12" x2="22" y2="12"/>
            </svg>
          </div>
          <h3>请选择课程</h3>
          <p>从左侧列表选择一门课程，查看对应的知识点思维导图</p>
        </div>

        <div v-else-if="loading" class="loading-state">
          <div class="spinner"></div>
          <span>加载中...</span>
        </div>

        <div v-else-if="!currentCourse?.has_mindmap" class="no-mindmap-state">
          <div class="no-mindmap-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14,2 14,8 20,8"/>
              <line x1="12" y1="11" x2="12" y2="17"/>
              <line x1="9" y1="14" x2="15" y2="14"/>
            </svg>
          </div>
          <h3>暂无思维导图</h3>
          <p>当前课程「{{ currentCourse?.name }}」暂未上传思维导图</p>
          <span class="hint">请在后台管理系统上传该课程的思维导图 PDF 文件</span>
        </div>

        <div v-else class="mindmap-viewer">
          <div class="viewer-header">
            <div class="viewer-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
              </svg>
              {{ currentCourse?.name }} - 思维导图
            </div>
            <div class="viewer-actions">
              <a
                v-if="mindmapViewerUrl"
                :href="mindmapViewerUrl"
                target="_blank"
                class="action-btn preview"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                  <circle cx="12" cy="12" r="3"/>
                </svg>
                全屏预览
              </a>
              <a
                v-if="mindmapUrl"
                :href="mindmapUrl"
                download
                class="action-btn download"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="7,10 12,15 17,10"/>
                  <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                下载 PDF
              </a>
            </div>
          </div>
          <div class="pdf-container">
            <div v-if="pdfViewerLoading" class="pdf-loading">
              <div class="spinner"></div>
              <span>加载思维导图中...</span>
            </div>
            <iframe
              v-if="pdfBlobUrl && !pdfViewerLoadError"
              :src="pdfBlobUrl"
              class="pdf-iframe"
              frameborder="0"
              title="思维导图 PDF"
            ></iframe>
            <div v-if="pdfViewerLoadError" class="pdf-fallback">
              <div class="pdf-fallback-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                  <polyline points="14,2 14,8 20,8"/>
                </svg>
              </div>
              <h3>PDF 预览失败</h3>
              <p class="pdf-error-hint">PDF 无法预览，请点击下方按钮打开</p>
              <div class="pdf-fallback-actions">
                <a :href="mindmapUrl" target="_blank" class="fallback-btn primary">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
                    <polyline points="15,3 21,3 21,9"/>
                    <line x1="10" y1="14" x2="21" y2="3"/>
                  </svg>
                  新窗口打开
                </a>
                <a :href="mindmapUrl" download class="fallback-btn">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                  下载 PDF
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { getCourses } from '@/api/questionBank'

const route = useRoute()

const courses = ref([])
const selectedCourseId = ref(null)
const loading = ref(false)

const pdfBlobUrl = ref(null)
const pdfViewerLoading = ref(true)
const pdfViewerLoadError = ref(false)

const currentCourse = computed(() =>
  courses.value.find(c => c.id === selectedCourseId.value)
)

const mindmapUrl = computed(() => {
  if (!currentCourse.value?.mindmap_pdf_url) return null
  return currentCourse.value.mindmap_pdf_url
})

const selectCourse = (course) => {
  selectedCourseId.value = course.id
  resetPdfState()
}

const resetPdfState = () => {
  if (pdfBlobUrl.value) {
    URL.revokeObjectURL(pdfBlobUrl.value)
    pdfBlobUrl.value = null
  }
  pdfViewerLoading.value = true
  pdfViewerLoadError.value = false
}

// 通过 fetch + Blob URL 方式，iframe 可直接渲染，绕过 localhost 跨域和浏览器 PDF 渲染问题
const loadPdfBlob = async (url) => {
  if (!url) return
  resetPdfState()
  pdfViewerLoading.value = true

  try {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`HTTP ${response.status}`)
    const blob = await response.blob()
    pdfBlobUrl.value = URL.createObjectURL(blob)
    pdfViewerLoading.value = false
    pdfViewerLoadError.value = false
  } catch (e) {
    console.error('[PDF] 加载失败:', e)
    pdfViewerLoading.value = false
    pdfViewerLoadError.value = true
  }
}

watch(selectedCourseId, async (newId) => {
  if (newId && mindmapUrl.value) {
    await nextTick()
    loadPdfBlob(mindmapUrl.value)
  }
})

const fetchCourses = async () => {
  loading.value = true
  try {
    const res = await getCourses()
    courses.value = res.data || []

    const courseParam = route.query.course
    if (courseParam) {
      const course = courses.value.find(c => c.id === parseInt(courseParam))
      if (course) {
        selectedCourseId.value = course.id
      }
    }
  } catch (e) {
    console.error('获取课程列表失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchCourses()
  if (selectedCourseId.value && mindmapUrl.value) {
    await nextTick()
    loadPdfBlob(mindmapUrl.value)
  }
})
</script>

<style scoped>
.mindmap-page {
  min-height: calc(100vh - 120px);
  padding: 32px;
}

.page-header {
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 24px;
  padding: 40px;
  margin-bottom: 32px;
  color: #fff;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.header-icon {
  width: 72px;
  height: 72px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon svg {
  width: 36px;
  height: 36px;
}

.header-text h1 {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px;
}

.header-text p {
  font-size: 15px;
  opacity: 0.85;
  margin: 0;
}

.mindmap-container {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  min-height: calc(100vh - 280px);
}

/* 课程侧边栏 */
.course-sidebar {
  background: #fff;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  height: fit-content;
  position: sticky;
  top: 24px;
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ebeef5;
}

.sidebar-title svg {
  width: 18px;
  height: 18px;
  color: #667eea;
}

.course-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.course-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #f9fafb;
  border: 1.5px solid transparent;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.25s ease;
  text-align: left;
  width: 100%;
}

.course-item:hover {
  background: #f0f2f5;
  border-color: rgba(102, 126, 234, 0.2);
}

.course-item.active {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.08));
  border-color: #667eea;
}

.course-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.course-icon svg {
  width: 20px;
  height: 20px;
  color: #fff;
}

.course-info {
  flex: 1;
  min-width: 0;
}

.course-name {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 2px;
}

.course-code {
  display: block;
  font-size: 12px;
  color: #909399;
}

.has-mindmap-badge {
  width: 24px;
  height: 24px;
  background: rgba(103, 194, 58, 0.15);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.has-mindmap-badge svg {
  width: 14px;
  height: 14px;
  color: #67c23a;
}

/* 预览区域 */
.mindmap-preview-area {
  background: #fff;
  border-radius: 20px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
}

.empty-state,
.loading-state,
.no-mindmap-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 500px;
  text-align: center;
  color: #909399;
}

.empty-icon,
.no-mindmap-icon {
  width: 100px;
  height: 100px;
  background: #f5f7fa;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.empty-icon svg,
.no-mindmap-icon svg {
  width: 48px;
  height: 48px;
  color: #c0c4cc;
}

.no-mindmap-icon {
  background: #fef0f0;
}

.no-mindmap-icon svg {
  color: #f56c6c;
}

.empty-state h3,
.no-mindmap-state h3 {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px;
}

.empty-state p,
.no-mindmap-state p {
  font-size: 14px;
  margin: 0;
  color: #909399;
}

.no-mindmap-state .hint {
  margin-top: 16px;
  font-size: 13px;
  color: #c0c4cc;
}

.loading-state {
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #ebeef5;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 思维导图查看器 */
.mindmap-viewer {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.viewer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.viewer-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.viewer-title svg {
  width: 20px;
  height: 20px;
  color: #667eea;
}

.viewer-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.25s ease;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn.preview {
  background: #f5f7fa;
  color: #606266;
  border: 1.5px solid #e4e7ed;
}

.action-btn.preview:hover {
  background: #ebeef5;
  border-color: #d3d6db;
}

.action-btn.download {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.action-btn.download:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.pdf-loading {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  background: #f5f7fa;
}

.pdf-loading .spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #ebeef5;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.pdf-fallback {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 600px;
  padding: 48px;
  gap: 12px;
  text-align: center;
}

.pdf-fallback-icon {
  width: 80px;
  height: 80px;
  background: #fef0f0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.pdf-fallback-icon svg {
  width: 40px;
  height: 40px;
  color: #f56c6c;
}

.pdf-fallback h3 {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.pdf-fallback p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.pdf-fallback-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.fallback-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.25s ease;
}

.fallback-btn svg {
  width: 16px;
  height: 16px;
}

.fallback-btn.primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: #fff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.fallback-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.fallback-btn:not(.primary) {
  background: #f5f7fa;
  color: #606266;
  border: 1.5px solid #e4e7ed;
}

.fallback-btn:not(.primary):hover {
  background: #ebeef5;
  border-color: #d3d6db;
}

.pdf-container {
  flex: 1;
  background: #f5f7fa;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #ebeef5;
  min-height: 600px;
  position: relative;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  min-height: 600px;
  display: block;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  min-height: 600px;
}

@media (max-width: 900px) {
  .mindmap-container {
    grid-template-columns: 1fr;
  }

  .course-sidebar {
    position: static;
  }
}
</style>
