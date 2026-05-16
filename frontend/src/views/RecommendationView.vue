<template>
  <div class="page-container">

    <!-- ========== 页面英雄区 ========== -->
    <div class="page-hero">
      <div class="page-hero-title">智能推荐</div>
      <div class="page-hero-subtitle">基于艾宾浩斯遗忘曲线与全站答题数据，智能推荐个性化复习内容</div>
    </div>

    <!-- ========== Tab 切换 ========== -->
    <div class="recommendation-tabs">
      <div
        class="tab-item"
        :class="{ active: activeTab === 'ebbinghaus' }"
        @click="switchTab('ebbinghaus')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <polyline points="12,6 12,12 16,14"/>
        </svg>
        错题复习推荐
      </div>
      <div
        class="tab-item"
        :class="{ active: activeTab === 'high-wrong' }"
        @click="switchTab('high-wrong')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
        </svg>
        高频错题推荐
      </div>
    </div>

    <!-- ========== Tab 1: 错题复习推荐 ========== -->
    <div v-show="activeTab === 'ebbinghaus'">
      <!-- 艾宾浩斯复习进度说明 -->
      <div class="review-guide-card">
        <div class="guide-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="16" x2="12" y2="12"/>
            <line x1="12" y1="8" x2="12.01" y2="8"/>
          </svg>
          艾宾浩斯复习间隔
          <button class="guide-help-btn" @click="showGuideModal = true" title="什么是艾宾浩斯复习间隔？">?</button>
        </div>
        <div class="guide-steps">
          <div class="guide-step">
            <div class="step-num">1</div>
            <div class="step-label">第1次复习</div>
            <div class="step-interval">错后 1 天</div>
          </div>
          <div class="guide-arrow">→</div>
          <div class="guide-step">
            <div class="step-num">2</div>
            <div class="step-label">第2次复习</div>
            <div class="step-interval">再隔 2 天</div>
          </div>
          <div class="guide-arrow">→</div>
          <div class="guide-step">
            <div class="step-num">3</div>
            <div class="step-label">第3次复习</div>
            <div class="step-interval">再隔 4 天</div>
          </div>
          <div class="guide-arrow">→</div>
          <div class="guide-step">
            <div class="step-num">4</div>
            <div class="step-label">第4次复习</div>
            <div class="step-interval">再隔 7 天</div>
          </div>
          <div class="guide-arrow">→</div>
          <div class="guide-step mastered">
            <div class="step-num">5+</div>
            <div class="step-label">已掌握</div>
            <div class="step-interval">再隔 15 天</div>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="ebbinghausLoading" class="loading-wrapper">
        <div class="loading-spinner"></div>
        <div class="loading-text">正在加载复习推荐...</div>
      </div>

      <!-- 空状态 -->
      <EmptyStateCard
        v-else-if="recommendList.length === 0"
        type="success"
        title="当前暂无需要复习的错题"
        description="保持当前的学习节奏，继续加油！当你做错新题目时，系统会自动将它们加入复习计划。"
      />

      <!-- 推荐复习列表 -->
      <template v-else>
        <div class="review-stats-bar">
          <div class="stats-info">
            当前共有 <span class="highlight-num">{{ recommendList.length }}</span> 道错题等待复习
          </div>
        </div>

        <!-- 列表模式 -->
        <div v-if="!currentReviewQuestion" class="review-list-area">
          <QuestionCard
            v-for="item in paginatedList"
            :key="item.id"
            :item="item"
            iconType="clock"
            actionLabel="开始复习"
            removeLabel="移出计划"
            @click="startReview(item)"
            @action="startReview(item)"
            @remove="onRemoveFromPlan(item)"
          />
          <PaginationBar
            :currentPage="currentPage"
            :totalPages="totalPages"
            :total="recommendList.length"
            @page-change="onPageChange"
          />
        </div>

        <!-- 复习作答模式 -->
        <div v-else class="review-practice-area">
          <div class="review-topbar">
            <div class="topbar-left">
              <button class="btn-back-new" @click="exitReview">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15,18 9,12 15,6"/>
                </svg>
                返回列表
              </button>
            </div>
            <div class="topbar-center">
              <span class="review-progress-badge">
                第 {{ reviewIndex + 1 }} / {{ reviewTotal }} 题
              </span>
              <span class="review-count-badge">
                本轮第 {{ currentReviewQuestion.review_count + 1 }} 次复习
              </span>
            </div>
            <div class="topbar-right"></div>
          </div>

          <!-- 题目卡片 -->
          <div class="review-question-card">
            <div class="rq-meta">
              <div class="rq-meta-left">
                <span class="q-number">{{ currentReviewQuestion.business_id }}</span>
                <span class="q-type-tag">{{ typeLabel(currentReviewQuestion.question_type) }}</span>
              </div>
              <div class="rq-path">
                {{ currentReviewQuestion.course_name }} /
                {{ currentReviewQuestion.chapter_name }} /
                {{ currentReviewQuestion.subchapter_name }}
              </div>
            </div>

            <div class="rq-stem">
              <p v-if="currentReviewQuestion.stem_text" v-html="currentReviewQuestion.stem_text"></p>
              <img v-if="currentReviewQuestion.stem_image" :src="buildImageUrl(currentReviewQuestion.stem_image)" class="stem-image" />
            </div>

            <div class="rq-options" v-if="currentReviewQuestion.question_type === 'single_choice'">
              <div
                v-for="opt in buildOptionList(currentReviewQuestion)"
                :key="opt.key"
                class="rq-option"
                :class="{
                  'selected': selectedAnswer === opt.key,
                  'correct': showResult && opt.key === currentReviewQuestion.correct_answer,
                  'wrong': showResult && selectedAnswer === opt.key && opt.key !== currentReviewQuestion.correct_answer
                }"
                @click="!showResult && selectAnswer(opt.key)"
              >
                <div class="opt-letter">{{ opt.key }}</div>
                <div class="opt-text">{{ opt.text }}</div>
              </div>
            </div>

            <!-- 作答后结果展示 -->
            <div v-if="showResult" class="rq-result">
              <div class="result-banner" :class="isCurrentCorrect ? 'correct-banner' : 'wrong-banner'">
                <span>{{ isCurrentCorrect ? '回答正确' : '回答错误' }}</span>
                <span v-if="isCurrentCorrect" class="result-sub">继续保持，记忆更深刻！</span>
                <span v-else class="result-sub">别灰心，答错后会重新安排复习~</span>
              </div>

              <div class="result-analysis">
                <div class="analysis-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="16" x2="12" y2="12"/>
                    <line x1="12" y1="8" x2="12.01" y2="8"/>
                  </svg>
                  解析
                </div>
                <p v-if="currentReviewQuestion.analysis_text" v-html="currentReviewQuestion.analysis_text"></p>
                <p v-else class="no-analysis">暂无解析</p>
              </div>

              <div class="next-review-tip">
                <template v-if="reviewResult">
                  <div class="tip-item">
                    <span class="tip-label">复习次数：</span>
                    <span class="tip-value">{{ reviewResult.review_count }} 次</span>
                  </div>
                  <div class="tip-item" v-if="reviewResult.is_mastered">
                    <span class="tip-value mastered-badge">已掌握</span>
                    <span class="tip-sub">该错题已从复习计划中移除</span>
                  </div>
                  <div class="tip-item" v-else>
                    <span class="tip-label">下次复习：</span>
                    <span class="tip-value">{{ formatNextReviewTime(reviewResult.next_review_time) }}</span>
                  </div>
                </template>
              </div>

              <div class="review-actions">
                <button v-if="!reviewResult" class="btn-submit-review" @click="submitReview">
                  提交答案
                </button>
                <button v-else class="btn-next-review" @click="nextReview">
                  {{ hasNextQuestion ? '下一题' : '查看结果' }}
                </button>
              </div>
            </div>

            <div v-else class="answer-submit-bar">
              <button class="btn-submit-review" :disabled="!selectedAnswer" @click="submitReview">
                提交答案
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- ========== Tab 2: 高频错题推荐 ========== -->
    <div v-show="activeTab === 'high-wrong'">
      <!-- 高频错题推荐算法说明 -->
      <div class="high-wrong-guide-card">
        <div class="guide-title">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
          </svg>
          高频错题推荐算法
          <button class="guide-help-btn" @click="showHighWrongGuideModal = true" title="什么是高频错题推荐算法？">?</button>
        </div>
        <div class="guide-formula">
          <div class="formula-label">推荐分数公式</div>
          <div class="formula-expression">
            <span class="formula-item wrong-rate">错误率</span>
            <span class="formula-op">× 0.7</span>
            <span class="formula-plus">+</span>
            <span class="formula-item heat">归一化热度</span>
            <span class="formula-op">× 0.3</span>
          </div>
        </div>
        <div class="guide-steps-high-wrong">
          <div class="guide-step-high">
            <div class="step-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
            </div>
            <div class="step-text">统计全站答题记录</div>
          </div>
          <div class="guide-arrow-sm">→</div>
          <div class="guide-step-high">
            <div class="step-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="20" x2="18" y2="10"/>
                <line x1="12" y1="20" x2="12" y2="4"/>
                <line x1="6" y1="20" x2="6" y2="14"/>
              </svg>
            </div>
            <div class="step-text">计算错误率与热度</div>
          </div>
          <div class="guide-arrow-sm">→</div>
          <div class="guide-step-high">
            <div class="step-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
              </svg>
            </div>
            <div class="step-text">综合评分取 Top 10</div>
          </div>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="highWrongLoading" class="loading-wrapper">
        <div class="loading-spinner"></div>
        <div class="loading-text">正在加载高频错题...</div>
      </div>

      <!-- 错误状态 -->
      <EmptyStateCard
        v-else-if="highWrongError"
        type="error"
        title="推荐数据加载失败"
        description="请稍后重试，或检查网络连接。"
      />

      <!-- 空状态 -->
      <EmptyStateCard
        v-else-if="highWrongList.length === 0"
        type="info"
        title="当前暂无高频错题推荐"
        description="请继续积累练习数据，随着更多用户参与练习，系统将逐渐识别高频易错题并为你推荐。"
      />

      <!-- 高频错题卡片列表 -->
      <template v-else>
        <div class="review-stats-bar">
          <div class="stats-info">
            基于全站 <span class="highlight-num">{{ highWrongList.length }}</span> 道高频易错题推荐
          </div>
        </div>

        <!-- 逐题作答模式 -->
        <div v-if="!currentHighWrongQuestion" class="high-wrong-list-area">
          <div
            v-for="(item, index) in highWrongPaginatedList"
            :key="item.question_id"
            class="high-wrong-card"
          >
            <!-- 卡片顶部信息 -->
            <div class="hwc-topbar">
              <div class="hwc-badges">
                <span class="hwc-rank">#{{ (highWrongPage - 1) * highWrongPerPage + index + 1 }}</span>
                <span class="hwc-type-tag">{{ typeLabel(item.question_type) }}</span>
                <span v-if="item.user_has_wrong" class="hwc-personal-tag personal-wrong">
                  你曾做错
                </span>
                <span v-else-if="item.user_has_done" class="hwc-personal-tag personal-done">
                  已做过
                </span>
              </div>
              <div class="hwc-stats">
                <span class="hwc-stat-item">
                  <span class="hwc-stat-label">错误率</span>
                  <span class="hwc-stat-value wrong-rate-high">{{ Math.round(item.wrong_rate * 100) }}%</span>
                </span>
                <span class="hwc-stat-item">
                  <span class="hwc-stat-label">练习</span>
                  <span class="hwc-stat-value">{{ item.total_attempts }}次</span>
                </span>
              </div>
            </div>

            <!-- 题干 -->
            <div class="hwc-stem">
              <span class="hwc-business-id">{{ item.business_id }}</span>
              <span v-if="item.stem_text" v-html="item.stem_text"></span>
              <img v-if="item.stem_image" :src="buildImageUrl(item.stem_image)" class="stem-image" />
            </div>

            <!-- 推荐理由 -->
            <div class="hwc-reason">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              {{ item.reason }}
            </div>

            <!-- 路径信息 -->
            <div class="hwc-path">
              {{ item.course_name }} / {{ item.chapter_name }} / {{ item.subchapter_name }}
            </div>

            <!-- 操作按钮 -->
            <div class="hwc-actions">
              <button class="btn-hw-start" @click="startHighWrongPractice(item)">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polygon points="5,3 19,12 5,21"/>
                </svg>
                开始练习
              </button>
            </div>
          </div>

          <PaginationBar
            :currentPage="highWrongPage"
            :totalPages="highWrongTotalPages"
            :total="highWrongList.length"
            @page-change="onHighWrongPageChange"
          />
        </div>

        <!-- 高频错题作答模式 -->
        <div v-else class="review-practice-area">
          <div class="review-topbar">
            <div class="topbar-left">
              <button class="btn-back-new" @click="exitHighWrongPractice">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="15,18 9,12 15,6"/>
                </svg>
                返回列表
              </button>
            </div>
            <div class="topbar-center">
              <span class="review-progress-badge">
                高频易错题
              </span>
              <span class="hw-wrong-rate-badge">
                全站错误率 {{ Math.round(currentHighWrongQuestion.wrong_rate * 100) }}%
              </span>
            </div>
            <div class="topbar-right"></div>
          </div>

          <div class="review-question-card">
            <div class="rq-meta">
              <div class="rq-meta-left">
                <span class="q-number">{{ currentHighWrongQuestion.business_id }}</span>
                <span class="q-type-tag">{{ typeLabel(currentHighWrongQuestion.question_type) }}</span>
                <span v-if="currentHighWrongQuestion.user_has_wrong" class="q-personal-tag personal-wrong">
                  你曾做错
                </span>
                <span v-else-if="currentHighWrongQuestion.user_has_done" class="q-personal-tag personal-done">
                  已做过
                </span>
              </div>
              <div class="rq-path">
                {{ currentHighWrongQuestion.course_name }} /
                {{ currentHighWrongQuestion.chapter_name }} /
                {{ currentHighWrongQuestion.subchapter_name }}
              </div>
            </div>

            <!-- 推荐理由小标签 -->
            <div class="hw-inline-reason">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
              {{ currentHighWrongQuestion.reason }}
            </div>

            <div class="rq-stem">
              <p v-if="currentHighWrongQuestion.stem_text" v-html="currentHighWrongQuestion.stem_text"></p>
              <img v-if="currentHighWrongQuestion.stem_image" :src="buildImageUrl(currentHighWrongQuestion.stem_image)" class="stem-image" />
            </div>

            <!-- 选项 -->
            <div class="rq-options" v-if="currentHighWrongQuestion.question_type === 'single_choice'">
              <div
                v-for="opt in buildHighWrongOptionList(currentHighWrongQuestion)"
                :key="opt.key"
                class="rq-option"
                :class="{
                  'selected': highWrongSelectedAnswer === opt.key,
                  'correct': highWrongShowResult && opt.key === currentHighWrongQuestion.correct_answer,
                  'wrong': highWrongShowResult && highWrongSelectedAnswer === opt.key && opt.key !== currentHighWrongQuestion.correct_answer
                }"
                @click="!highWrongShowResult && (highWrongSelectedAnswer = opt.key)"
              >
                <div class="opt-letter">{{ opt.key }}</div>
                <div class="opt-text">{{ opt.text }}</div>
              </div>
            </div>

            <!-- 结果展示 -->
            <div v-if="highWrongShowResult" class="rq-result">
              <div class="result-banner" :class="isHighWrongCorrect ? 'correct-banner' : 'wrong-banner'">
                <span>{{ isHighWrongCorrect ? '回答正确！' : '回答错误' }}</span>
                <span class="result-sub">
                  {{ isHighWrongCorrect ? '恭喜你掌握了本题！' : `正确答案是 ${currentHighWrongQuestion.correct_answer}，注意查看解析哦~` }}
                </span>
              </div>

              <!-- 全站统计信息 -->
              <div class="hw-stats-panel">
                <div class="hw-stats-title">全站答题统计</div>
                <div class="hw-stats-row">
                  <div class="hw-stat-box">
                    <div class="hw-stat-num">{{ currentHighWrongQuestion.total_attempts }}</div>
                    <div class="hw-stat-desc">总练习次数</div>
                  </div>
                  <div class="hw-stat-box">
                    <div class="hw-stat-num wrong">{{ currentHighWrongQuestion.wrong_attempts }}</div>
                    <div class="hw-stat-desc">错误次数</div>
                  </div>
                  <div class="hw-stat-box">
                    <div class="hw-stat-num">{{ Math.round(currentHighWrongQuestion.wrong_rate * 100) }}%</div>
                    <div class="hw-stat-desc">全站错误率</div>
                  </div>
                </div>
              </div>

              <div class="result-analysis">
                <div class="analysis-label">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="16" x2="12" y2="12"/>
                    <line x1="12" y1="8" x2="12.01" y2="8"/>
                  </svg>
                  解析
                </div>
                <p v-if="currentHighWrongQuestion.analysis_text" v-html="currentHighWrongQuestion.analysis_text"></p>
                <p v-else class="no-analysis">暂无解析</p>
              </div>

              <div class="review-actions">
                <button v-if="highWrongHasNext" class="btn-next-review" @click="nextHighWrongQuestion">
                  下一题
                </button>
                <button v-else class="btn-finish-review" @click="exitHighWrongPractice">
                  返回列表
                </button>
              </div>
            </div>

            <div v-else class="answer-submit-bar">
              <button class="btn-submit-review" :disabled="!highWrongSelectedAnswer" @click="checkHighWrongAnswer">
                提交答案
              </button>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- ========== 艾宾浩斯说明弹窗 ========== -->
    <Teleport to="body">
      <div v-if="showGuideModal" class="guide-modal-overlay" @click.self="showGuideModal = false">
        <div class="guide-modal-card">
          <div class="guide-modal-header">
            <div class="guide-modal-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              什么是艾宾浩斯遗忘曲线复习法？
            </div>
            <button class="guide-modal-close" @click="showGuideModal = false">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <div class="guide-modal-body">
            <p class="modal-intro">
              德国心理学家 <strong>艾宾浩斯</strong> 的研究表明：人类遗忘的速度是<strong>先快后慢</strong>——刚学完的知识在短时间内遗忘最快，之后遗忘速度逐渐放缓。
            </p>
            <p class="modal-intro">
              因此，在遗忘即将发生的关键时间点及时复习，能够将短期记忆高效转化为长期记忆。本系统的复习策略正是基于这一原理：
            </p>
            <div class="modal-rule-list">
              <div class="modal-rule-item">
                <span class="modal-rule-dot">1</span>
                <div>做错题目时，系统自动将其加入<strong>错题复习计划</strong>，安排第一次复习</div>
              </div>
              <div class="modal-rule-item">
                <span class="modal-rule-dot">2</span>
                <div>到达复习时间后，系统<strong>主动推荐</strong>该错题供你复习</div>
              </div>
              <div class="modal-rule-item">
                <span class="modal-rule-dot">3</span>
                <div>复习时答对 → 按 <strong>1→2→4→7→15 天</strong> 的间隔递增安排下次复习</div>
              </div>
              <div class="modal-rule-item">
                <span class="modal-rule-dot">4</span>
                <div>复习时答错 → 间隔<strong>重置为1天</strong>，从头开始间隔递增</div>
              </div>
              <div class="modal-rule-item">
                <span class="modal-rule-dot">5</span>
                <div>连续正确复习 <strong>5 次</strong> 后，标记为"已掌握"，从复习计划中移除</div>
              </div>
            </div>
            <div class="modal-example">
              <div class="modal-example-title">示例</div>
              <div class="modal-example-row">
                <span>4月1日做错</span>
                <span>→</span>
                <span>4月2日（第1次）</span>
                <span>→</span>
                <span>4月4日（第2次）</span>
                <span>→</span>
                <span>…</span>
                <span>→</span>
                <span>已掌握</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ========== 高频错题算法说明弹窗 ========== -->
    <Teleport to="body">
      <div v-if="showHighWrongGuideModal" class="guide-modal-overlay" @click.self="showHighWrongGuideModal = false">
        <div class="guide-modal-card">
          <div class="guide-modal-header hw-modal-header">
            <div class="guide-modal-title">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
              </svg>
              什么是高频错题推荐算法？
            </div>
            <button class="guide-modal-close" @click="showHighWrongGuideModal = false">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          <div class="guide-modal-body">
            <p class="modal-intro">
              高频错题推荐基于<strong>全站所有用户的答题数据</strong>，通过统计分析找出真正具有参考价值的易错题，帮助你针对性地加强练习。
            </p>

            <!-- 核心公式详解 -->
            <div class="hw-modal-formula-section">
              <div class="hw-modal-section-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"/>
                </svg>
                核心公式
              </div>
              <div class="hw-modal-formula-box">
                <span class="formula-item wrong-rate">错误率</span>
                <span class="formula-op">× 0.7</span>
                <span class="formula-plus">+</span>
                <span class="formula-item heat">归一化热度</span>
                <span class="formula-op">× 0.3</span>
              </div>
            </div>

            <!-- 指标解释 -->
            <div class="hw-modal-indicators">
              <div class="hw-modal-indicator">
                <div class="indicator-header">
                  <span class="indicator-dot wrong-rate-dot"></span>
                  <span class="indicator-name">错误率（权重 70%）</span>
                </div>
                <p class="indicator-desc">该题被做错的总次数 ÷ 该题被练习的总次数。错误率越高，说明这道题越容易出错，值得重点关注。</p>
                <div class="indicator-formula">错误率 = 错误次数 / 总练习次数</div>
              </div>
              <div class="hw-modal-indicator">
                <div class="indicator-header">
                  <span class="indicator-dot heat-dot"></span>
                  <span class="indicator-name">归一化热度（权重 30%）</span>
                </div>
                <p class="indicator-desc">热度指该题被全站用户练习的总次数。由于不同题目热度差异大，需要归一化到 0~1 范围后再参与计算。</p>
                <div class="indicator-formula">归一化热度 = 练习次数 / 结果集中最大练习次数</div>
              </div>
            </div>

            <!-- 为什么这样设计 -->
            <div class="hw-modal-why">
              <div class="hw-modal-section-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="12" cy="12" r="10"/>
                  <line x1="12" y1="16" x2="12" y2="12"/>
                  <line x1="12" y1="8" x2="12.01" y2="8"/>
                </svg>
                为什么这样设计？
              </div>
              <div class="why-item">
                <span class="why-dot">1</span>
                <p>错误率权重更高（70%），因为<strong>容易被做错</strong>才是推荐的核心依据，一道只有少量人做错的题参考价值不大。</p>
              </div>
              <div class="why-item">
                <span class="why-dot">2</span>
                <p>热度权重次之（30%），练习人数多的题更具<strong>普遍性</strong>，说明它是该知识点的典型考题。</p>
              </div>
              <div class="why-item">
                <span class="why-dot">3</span>
                <p>过滤练习次数 &lt; 3 次的题，避免因样本太少导致错误率失真。</p>
              </div>
            </div>

            <!-- 与艾宾浩斯的区别 -->
            <div class="hw-modal-vs">
              <div class="hw-modal-section-title">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="18" y1="20" x2="18" y2="10"/>
                  <line x1="12" y1="20" x2="12" y2="4"/>
                  <line x1="6" y1="20" x2="6" y2="14"/>
                </svg>
                与「错题复习推荐」的区别
              </div>
              <div class="vs-table">
                <div class="vs-row vs-header">
                  <span>对比维度</span>
                  <span>错题复习推荐</span>
                  <span>高频错题推荐</span>
                </div>
                <div class="vs-row">
                  <span>数据来源</span>
                  <span>仅你的错题</span>
                  <span>全站所有用户</span>
                </div>
                <div class="vs-row">
                  <span>推荐逻辑</span>
                  <span>基于遗忘曲线定时推送</span>
                  <span>基于错误率与热度评分</span>
                </div>
                <div class="vs-row">
                  <span>目的</span>
                  <span>巩固个人薄弱点</span>
                  <span>了解全站公认的难题</span>
                </div>
                <div class="vs-row">
                  <span>触发方式</span>
                  <span>到复习时间自动出现</span>
                  <span>随时可查看推荐列表</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  getRecommendWrongQuestions,
  submitReviewResult,
  removeReviewRecord,
  getHighWrongRateQuestions,
} from '@/api/recommendation'
import QuestionCard from '@/components/common/QuestionCard.vue'
import EmptyStateCard from '@/components/common/EmptyStateCard.vue'
import PaginationBar from '@/components/common/PaginationBar.vue'

// =============================================================================
// Tab 切换状态
// =============================================================================
const activeTab = ref('ebbinghaus')

function switchTab(tab) {
  if (activeTab.value === tab) return
  activeTab.value = tab
  if (tab === 'ebbinghaus') {
    if (recommendList.value.length === 0 && !ebbinghausLoading.value) {
      loadRecommendList()
    }
  } else {
    if (highWrongList.value.length === 0 && !highWrongLoading.value) {
      loadHighWrongList()
    }
  }
}

// =============================================================================
// Tab 1: 错题复习推荐（艾宾浩斯）— 状态
// =============================================================================
const ebbinghausLoading = ref(true)
const recommendList = ref([])
const currentPage = ref(1)
const perPage = 10
const showGuideModal = ref(false)

// 复习模式
const currentReviewQuestion = ref(null)
const reviewIndex = ref(0)
const reviewTotal = ref(0)
const reviewQueue = ref([])
const selectedAnswer = ref(null)
const showResult = ref(false)
const isCurrentCorrect = ref(false)
const reviewResult = ref(null)

// =============================================================================
// Tab 1: 计算属性
// =============================================================================
const paginatedList = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return recommendList.value.slice(start, start + perPage)
})

const totalPages = computed(() => Math.ceil(recommendList.value.length / perPage) || 1)

const hasNextQuestion = computed(() => {
  return reviewIndex.value < reviewQueue.value.length - 1
})

// =============================================================================
// Tab 1: 加载推荐列表
// =============================================================================
async function loadRecommendList() {
  ebbinghausLoading.value = true
  try {
    const res = await getRecommendWrongQuestions()
    recommendList.value = res.data?.results || []
    reviewQueue.value = [...recommendList.value]
    reviewTotal.value = reviewQueue.value.length
  } catch (e) {
    console.error('加载推荐列表失败', e)
    recommendList.value = []
  } finally {
    ebbinghausLoading.value = false
  }
}

// =============================================================================
// Tab 1: 移出复习计划
// =============================================================================
async function onRemoveFromPlan(item) {
  if (!confirm('确定要将该题从复习计划中移除吗？移除后不会影响错题本记录。')) return
  try {
    await removeReviewRecord(item.id)
    await loadRecommendList()
  } catch (e) {
    console.error('移除失败', e)
  }
}

// =============================================================================
// Tab 1: 复习流程
// =============================================================================
function startReview(item) {
  reviewQueue.value = [...recommendList.value]
  reviewTotal.value = reviewQueue.value.length
  reviewIndex.value = reviewQueue.value.findIndex(q => q.id === item.id)
  currentReviewQuestion.value = { ...item }
  selectedAnswer.value = null
  showResult.value = false
  isCurrentCorrect.value = false
  reviewResult.value = null
}

function exitReview() {
  currentReviewQuestion.value = null
  reviewIndex.value = 0
  selectedAnswer.value = null
  showResult.value = false
  isCurrentCorrect.value = false
  reviewResult.value = null
  loadRecommendList()
}

function selectAnswer(key) {
  selectedAnswer.value = key
}

async function submitReview() {
  if (!selectedAnswer.value) return
  if (!currentReviewQuestion.value) return

  isCurrentCorrect.value = selectedAnswer.value.toUpperCase() === currentReviewQuestion.value.correct_answer?.toUpperCase()
  showResult.value = true

  try {
    const res = await submitReviewResult(currentReviewQuestion.value.id, isCurrentCorrect.value)
    reviewResult.value = res.data
    const idx = reviewQueue.value.findIndex(q => q.id === currentReviewQuestion.value.id)
    if (idx !== -1) {
      reviewQueue.value[idx] = {
        ...reviewQueue.value[idx],
        review_count: res.data.review_count,
        is_mastered: res.data.is_mastered,
        next_review_time: res.data.next_review_time
      }
    }
  } catch (e) {
    console.error('提交复习结果失败', e)
    reviewResult.value = null
  }
}

function nextReview() {
  if (hasNextQuestion.value) {
    reviewIndex.value++
    currentReviewQuestion.value = { ...reviewQueue.value[reviewIndex.value] }
    selectedAnswer.value = null
    showResult.value = false
    isCurrentCorrect.value = false
    reviewResult.value = null
  } else {
    currentReviewQuestion.value = null
    loadRecommendList()
  }
}

function onPageChange(page) {
  currentPage.value = page
}

// =============================================================================
// Tab 2: 高频错题推荐 — 状态
// =============================================================================
const highWrongLoading = ref(false)
const highWrongError = ref(false)
const highWrongList = ref([])
const highWrongPage = ref(1)
const highWrongPerPage = 5
const showHighWrongGuideModal = ref(false)

// 高频错题作答模式
const currentHighWrongQuestion = ref(null)
const highWrongIndex = ref(0)
const highWrongSelectedAnswer = ref(null)
const highWrongShowResult = ref(false)
const isHighWrongCorrect = ref(false)

const highWrongHasNext = computed(() => {
  return highWrongIndex.value < highWrongList.value.length - 1
})

// =============================================================================
// Tab 2: 计算属性
// =============================================================================
const highWrongPaginatedList = computed(() => {
  const start = (highWrongPage.value - 1) * highWrongPerPage
  return highWrongList.value.slice(start, start + highWrongPerPage)
})

const highWrongTotalPages = computed(() => Math.ceil(highWrongList.value.length / highWrongPerPage) || 1)

// =============================================================================
// Tab 2: 加载高频错题列表
// =============================================================================
async function loadHighWrongList() {
  highWrongLoading.value = true
  highWrongError.value = false
  try {
    const res = await getHighWrongRateQuestions()
    highWrongList.value = res.data?.results || []
  } catch (e) {
    console.error('加载高频错题失败', e)
    highWrongError.value = true
    highWrongList.value = []
  } finally {
    highWrongLoading.value = false
  }
}

function onHighWrongPageChange(page) {
  highWrongPage.value = page
}

// =============================================================================
// Tab 2: 高频错题练习流程
// =============================================================================
function startHighWrongPractice(item) {
  highWrongIndex.value = highWrongList.value.findIndex(q => q.question_id === item.question_id)
  currentHighWrongQuestion.value = { ...item }
  highWrongSelectedAnswer.value = null
  highWrongShowResult.value = false
  isHighWrongCorrect.value = false
}

function exitHighWrongPractice() {
  currentHighWrongQuestion.value = null
  highWrongSelectedAnswer.value = null
  highWrongShowResult.value = false
  isHighWrongCorrect.value = false
  // 不重新加载列表，保留滚动位置
}

function checkHighWrongAnswer() {
  if (!highWrongSelectedAnswer.value || !currentHighWrongQuestion.value) return
  isHighWrongCorrect.value = highWrongSelectedAnswer.value.toUpperCase() === currentHighWrongQuestion.value.correct_answer?.toUpperCase()
  highWrongShowResult.value = true
}

function nextHighWrongQuestion() {
  if (highWrongHasNext.value) {
    highWrongIndex.value++
    currentHighWrongQuestion.value = { ...highWrongList.value[highWrongIndex.value] }
    highWrongSelectedAnswer.value = null
    highWrongShowResult.value = false
    isHighWrongCorrect.value = false
  } else {
    exitHighWrongPractice()
  }
}

// =============================================================================
// 辅助函数
// =============================================================================
function typeLabel(type) {
  const map = {
    'single_choice': '单选题',
    'big_question': '大题'
  }
  return map[type] || type
}

function buildOptionList(q) {
  const list = []
  if (q.option_a_text) list.push({ key: 'A', text: q.option_a_text })
  if (q.option_b_text) list.push({ key: 'B', text: q.option_b_text })
  if (q.option_c_text) list.push({ key: 'C', text: q.option_c_text })
  if (q.option_d_text) list.push({ key: 'D', text: q.option_d_text })
  return list
}

function buildHighWrongOptionList(q) {
  const list = []
  if (q.option_a_text) list.push({ key: 'A', text: q.option_a_text })
  if (q.option_b_text) list.push({ key: 'B', text: q.option_b_text })
  if (q.option_c_text) list.push({ key: 'C', text: q.option_c_text })
  if (q.option_d_text) list.push({ key: 'D', text: q.option_d_text })
  return list
}

function buildImageUrl(path) {
  if (!path) return null
  if (path.startsWith('http')) return path
  return `http://127.0.0.1:8000/media/${path}`
}

function formatNextReviewTime(timeStr) {
  if (!timeStr) return '—'
  const d = new Date(timeStr)
  const now = new Date()
  const diff = Math.ceil((d - now) / (1000 * 60 * 60 * 24))
  if (diff <= 0) return '已到期'
  if (diff === 1) return '明天'
  return `${diff} 天后`
}

// =============================================================================
// 初始化
// =============================================================================
onMounted(() => {
  loadRecommendList()
})
</script>

<style scoped>
/* ========== Tab 切换 ========== */
.recommendation-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  background: white;
  border-radius: 14px;
  padding: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
}

.tab-item {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  color: #666;
  transition: all 0.25s ease;
  border: 2px solid transparent;
}

.tab-item svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.tab-item.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
}

.tab-item:not(.active):hover {
  background: #f5f5f5;
  color: #333;
}

/* ========== 复习进度说明卡片 ========== */
.review-guide-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 24px 28px;
  margin-bottom: 28px;
  color: white;
}

.guide-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 18px;
  opacity: 0.9;
}

.guide-title svg {
  width: 18px;
  height: 18px;
}

.guide-help-btn {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(255,255,255,0.25);
  border: 1.5px solid rgba(255,255,255,0.5);
  color: white;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  margin-left: 4px;
}

.guide-help-btn:hover {
  background: rgba(255,255,255,0.4);
  transform: scale(1.1);
}

.guide-steps {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  flex-wrap: wrap;
}

.guide-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 80px;
}

.step-num {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.guide-step.mastered .step-num {
  background: rgba(255,255,255,0.4);
}

.step-label {
  font-size: 12px;
  opacity: 0.85;
}

.step-interval {
  font-size: 13px;
  font-weight: 600;
}

.guide-arrow {
  color: rgba(255,255,255,0.5);
  font-size: 18px;
  padding: 0 8px;
  margin-bottom: 16px;
}

/* ========== 统计栏 ========== */
.review-stats-bar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 16px;
  font-size: 14px;
  color: #666;
}

.highlight-num {
  color: #764ba2;
  font-weight: 700;
  font-size: 16px;
}

/* ========== 复习顶部操作栏 ========== */
.review-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  margin-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.btn-back-new {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-back-new:hover {
  background: #f5f5f5;
  border-color: #ccc;
}

.topbar-center {
  display: flex;
  align-items: center;
  gap: 12px;
}

.review-progress-badge {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

.review-count-badge {
  background: #fff3e0;
  color: #e65100;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

/* 高频错题专属徽章 */
.hw-wrong-rate-badge {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}

/* ========== 题目卡片 ========== */
.review-question-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  padding: 28px;
}

.rq-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.rq-meta-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.q-number {
  font-weight: 700;
  color: #333;
  font-size: 15px;
}

.q-type-tag {
  background: #ede9fe;
  color: #7c3aed;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.q-personal-tag {
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.personal-wrong {
  background: #fef2f2;
  color: #dc2626;
}

.personal-done {
  background: #eff6ff;
  color: #2563eb;
}

.rq-path {
  font-size: 12px;
  color: #999;
}

.rq-stem {
  font-size: 16px;
  line-height: 1.8;
  color: #222;
  margin-bottom: 24px;
}

.rq-stem p {
  margin: 0;
}

.stem-image {
  max-width: 100%;
  border-radius: 8px;
  margin-top: 8px;
}

/* ========== 选项 ========== */
.rq-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.rq-option {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 18px;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  background: white;
}

.rq-option:hover {
  border-color: #667eea;
  background: #f8f7ff;
}

.rq-option.selected {
  border-color: #667eea;
  background: #ede9fe;
}

.rq-option.correct {
  border-color: #22c55e;
  background: #f0fdf4;
}

.rq-option.wrong {
  border-color: #ef4444;
  background: #fef2f2;
}

.opt-letter {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  color: #555;
  flex-shrink: 0;
}

.rq-option.selected .opt-letter {
  background: #667eea;
  color: white;
}

.rq-option.correct .opt-letter {
  background: #22c55e;
  color: white;
}

.rq-option.wrong .opt-letter {
  background: #ef4444;
  color: white;
}

.opt-text {
  font-size: 15px;
  line-height: 1.7;
  color: #333;
}

/* ========== 结果展示 ========== */
.rq-result {
  margin-top: 8px;
}

.result-banner {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  font-size: 17px;
  font-weight: 700;
}

.correct-banner {
  background: #f0fdf4;
  color: #16a34a;
}

.wrong-banner {
  background: #fef2f2;
  color: #dc2626;
}

.result-sub {
  font-size: 13px;
  font-weight: 400;
  opacity: 0.8;
  margin-top: 4px;
}

/* 高频错题内联推荐理由 */
.hw-inline-reason {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f7ff;
  border: 1px solid #ede9fe;
  border-radius: 8px;
  padding: 8px 14px;
  margin-bottom: 20px;
  font-size: 13px;
  color: #7c3aed;
  line-height: 1.5;
}

.hw-inline-reason svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: #667eea;
}

/* 高频错题统计面板 */
.hw-stats-panel {
  background: #f8f7ff;
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 20px;
  border: 1px solid #ede9fe;
}

.hw-stats-title {
  font-size: 13px;
  font-weight: 700;
  color: #7c3aed;
  margin-bottom: 12px;
}

.hw-stats-row {
  display: flex;
  gap: 16px;
}

.hw-stat-box {
  flex: 1;
  text-align: center;
  padding: 10px;
  background: white;
  border-radius: 8px;
}

.hw-stat-num {
  font-size: 22px;
  font-weight: 800;
  color: #7c3aed;
  line-height: 1;
  margin-bottom: 4px;
}

.hw-stat-num.wrong {
  color: #764ba2;
}

.hw-stat-desc {
  font-size: 11px;
  color: #999;
}

/* ========== 解析 ========== */
.result-analysis {
  background: #fffbeb;
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 20px;
}

.analysis-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 700;
  color: #92400e;
  margin-bottom: 10px;
}

.analysis-label svg {
  width: 16px;
  height: 16px;
}

.result-analysis p {
  font-size: 14px;
  line-height: 1.8;
  color: #444;
  margin: 0;
}

.no-analysis {
  color: #999;
  font-style: italic;
}

/* ========== 下次复习提示 ========== */
.next-review-tip {
  background: #f8f7ff;
  border-radius: 10px;
  padding: 14px 18px;
  margin-bottom: 20px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #555;
}

.tip-label {
  color: #666;
}

.tip-value {
  font-weight: 700;
  color: #333;
}

.mastered-badge {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 12px;
}

.tip-sub {
  font-size: 12px;
  color: #999;
  margin-left: 4px;
}

/* ========== 操作按钮 ========== */
.answer-submit-bar {
  display: flex;
  justify-content: center;
  padding-top: 8px;
}

.btn-submit-review {
  padding: 12px 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-submit-review:hover:not(:disabled) {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit-review:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.review-actions {
  display: flex;
  justify-content: center;
}

.btn-next-review {
  padding: 12px 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-next-review:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-finish-review {
  padding: 12px 48px;
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-finish-review:hover {
  background: #f8f7ff;
}

/* ========== 高频错题卡片列表 ========== */
.high-wrong-list-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.high-wrong-card {
  background: white;
  border-radius: 16px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid #f0f0f0;
  transition: all 0.2s;
}

.high-wrong-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  border-color: #e0e0e0;
}

.hwc-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.hwc-badges {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hwc-rank {
  font-size: 13px;
  font-weight: 700;
  color: #764ba2;
  background: #f3e8ff;
  padding: 2px 10px;
  border-radius: 20px;
}

.hwc-type-tag {
  background: #ede9fe;
  color: #7c3aed;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.hwc-personal-tag {
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.hwc-stats {
  display: flex;
  gap: 12px;
}

.hwc-stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.hwc-stat-label {
  color: #999;
}

.hwc-stat-value {
  font-weight: 700;
  color: #333;
}

.wrong-rate-high {
  color: #764ba2;
}

.hwc-stem {
  font-size: 15px;
  line-height: 1.7;
  color: #222;
  margin-bottom: 12px;
}

.hwc-business-id {
  font-weight: 700;
  color: #764ba2;
  margin-right: 6px;
}

.hwc-reason {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  background: #f8f7ff;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
  color: #7c3aed;
  line-height: 1.6;
  margin-bottom: 12px;
}

.hwc-reason svg {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  margin-top: 2px;
  color: #667eea;
}

.hwc-path {
  font-size: 12px;
  color: #999;
  margin-bottom: 14px;
}

.hwc-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-hw-start {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-hw-start svg {
  width: 14px;
  height: 14px;
}

.btn-hw-start:hover {
  opacity: 0.9;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35);
}

/* ========== 高频错题推荐算法说明卡片 ========== */
.high-wrong-guide-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 24px 28px;
  margin-bottom: 28px;
  color: white;
}

.high-wrong-guide-card .guide-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 18px;
  opacity: 0.95;
}

.high-wrong-guide-card .guide-title svg {
  width: 20px;
  height: 20px;
}

/* 公式区域 */
.guide-formula {
  background: rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 18px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.formula-label {
  font-size: 12px;
  opacity: 0.8;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.formula-expression {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 15px;
  font-weight: 700;
}

.formula-item {
  padding: 6px 14px;
  border-radius: 8px;
}

.formula-item.wrong-rate {
  background: rgba(255, 255, 255, 0.25);
}

.formula-item.heat {
  background: rgba(254, 215, 170, 0.3);
  color: #fed7aa;
}

.formula-op {
  opacity: 0.8;
  font-weight: 400;
}

.formula-plus {
  font-size: 18px;
  opacity: 0.6;
}

/* 步骤区域 */
.guide-steps-high-wrong {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  flex-wrap: wrap;
}

.guide-step-high {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 100px;
}

.step-icon {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-icon svg {
  width: 20px;
  height: 20px;
}

.step-text {
  font-size: 13px;
  opacity: 0.9;
  text-align: center;
  line-height: 1.4;
}

.guide-arrow-sm {
  color: rgba(255, 255, 255, 0.4);
  font-size: 16px;
  padding: 0 8px;
}

/* 高频错题弹窗特有 header */
.hw-modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 弹窗内容样式 */
.hw-modal-formula-section {
  background: #f8f7ff;
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 20px;
  border: 1px solid #ede9fe;
}

.hw-modal-section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: #7c3aed;
  margin-bottom: 14px;
}

.hw-modal-section-title svg {
  width: 18px;
  height: 18px;
}

.hw-modal-formula-box {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  font-size: 16px;
  font-weight: 700;
}

.hw-modal-formula-box .formula-item {
  padding: 6px 14px;
  border-radius: 8px;
}

.hw-modal-formula-box .formula-item.wrong-rate {
  background: rgba(102, 126, 234, 0.15);
  color: #667eea;
}

.hw-modal-formula-box .formula-item.heat {
  background: rgba(118, 75, 162, 0.15);
  color: #764ba2;
}

.hw-modal-formula-box .formula-op {
  color: #666;
  font-weight: 400;
}

.hw-modal-formula-box .formula-plus {
  color: #999;
  font-size: 18px;
}

/* 指标解释 */
.hw-modal-indicators {
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 20px;
}

.hw-modal-indicator {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 16px 18px;
}

.indicator-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.indicator-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.wrong-rate-dot {
  background: #667eea;
}

.heat-dot {
  background: #764ba2;
}

.indicator-name {
  font-size: 14px;
  font-weight: 700;
  color: #333;
}

.indicator-desc {
  font-size: 13px;
  line-height: 1.7;
  color: #555;
  margin: 0 0 10px;
}

.indicator-formula {
  font-family: 'SF Mono', 'Consolas', monospace;
  font-size: 12px;
  background: #f9fafb;
  color: #6b7280;
  padding: 6px 12px;
  border-radius: 6px;
  display: inline-block;
}

/* 为什么这样设计 */
.hw-modal-why {
  background: #f8f7ff;
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 20px;
  border: 1px solid #ede9fe;
}

.hw-modal-why .hw-modal-section-title {
  color: #7c3aed;
  margin-bottom: 14px;
}

.why-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 12px;
  font-size: 13px;
  line-height: 1.7;
  color: #374151;
}

.why-item:last-child {
  margin-bottom: 0;
}

.why-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.why-item p {
  margin: 0;
}

/* 对比表格 */
.hw-modal-vs {
  background: #f8fafc;
  border-radius: 12px;
  padding: 18px 20px;
  border: 1px solid #e2e8f0;
}

.hw-modal-vs .hw-modal-section-title {
  color: #475569;
  margin-bottom: 14px;
}

.vs-table {
  font-size: 13px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.vs-row {
  display: grid;
  grid-template-columns: 1fr 1.2fr 1.2fr;
  border-bottom: 1px solid #e2e8f0;
}

.vs-row:last-child {
  border-bottom: none;
}

.vs-row span {
  padding: 10px 12px;
  border-right: 1px solid #e2e8f0;
  line-height: 1.5;
}

.vs-row span:last-child {
  border-right: none;
}

.vs-row span:first-child {
  background: #f1f5f9;
  font-weight: 600;
  color: #475569;
}

.vs-header span {
  background: #f1f5f9;
  font-weight: 700;
  color: #334155;
}

/* ========== 弹窗样式 ========== */
.guide-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(2px);
}

.guide-modal-card {
  background: white;
  border-radius: 20px;
  width: 90%;
  max-width: 560px;
  max-height: 85vh;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.2);
}

.guide-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.guide-modal-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 700;
}

.guide-modal-title svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}

.guide-modal-close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.guide-modal-close:hover {
  background: rgba(255,255,255,0.35);
}

.guide-modal-close svg {
  width: 14px;
  height: 14px;
  color: white;
}

.guide-modal-body {
  padding: 24px 28px 28px;
  overflow-y: auto;
  max-height: calc(85vh - 76px);
}

.modal-intro {
  font-size: 14px;
  line-height: 1.8;
  color: #444;
  margin: 0 0 14px;
}

.modal-intro:last-of-type {
  margin-bottom: 20px;
}

.modal-rule-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.modal-rule-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 14px;
  line-height: 1.7;
  color: #333;
}

.modal-rule-dot {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.modal-example {
  background: #f8f7ff;
  border-radius: 12px;
  padding: 16px 18px;
  border: 1px solid #ede9fe;
}

.modal-example-title {
  font-size: 13px;
  font-weight: 700;
  color: #7c3aed;
  margin-bottom: 10px;
}

.modal-example-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #555;
  flex-wrap: wrap;
}
</style>
