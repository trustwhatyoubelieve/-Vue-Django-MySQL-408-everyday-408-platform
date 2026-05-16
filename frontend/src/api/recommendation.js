/**
 * 智能推荐 API — 错题复习推荐
 */
import request from './request'

/**
 * 获取当前用户需要复习的错题列表
 * GET /api/recommendations/wrong-questions/
 * @returns {Promise<{count: number, results: Array}>}
 */
export const getRecommendWrongQuestions = () =>
  request.get('/recommendations/wrong-questions/')

/**
 * 提交错题复习结果
 * POST /api/recommendations/wrong-questions/{id}/review/
 * @param {number} reviewId - 复习记录 ID
 * @param {boolean} isCorrect - 本次是否答对
 * @returns {Promise<{review_count: number, next_review_time: string, is_mastered: boolean}>}
 */
export const submitReviewResult = (reviewId, isCorrect) =>
  request.post(`/recommendations/wrong-questions/${reviewId}/review/`, { is_correct: isCorrect })

/**
 * 获取当前用户所有复习记录（含已掌握）
 * GET /api/recommendations/wrong-questions/all/
 * @returns {Promise<{count: number, results: Array}>}
 */
export const getAllReviewRecords = () =>
  request.get('/recommendations/wrong-questions/all/')

/**
 * 将复习记录从复习计划中移除
 * POST /api/recommendations/wrong-questions/{id}/remove/
 * @param {number} reviewId - 复习记录 ID
 * @returns {Promise}
 */
export const removeReviewRecord = (reviewId) =>
  request.post(`/recommendations/wrong-questions/${reviewId}/remove/`)

/**
 * 获取高频错题推荐
 * GET /api/recommendations/high-wrong-rate/
 * @returns {Promise<{count: number, results: Array}>}
 */
export const getHighWrongRateQuestions = () =>
  request.get('/recommendations/high-wrong-rate/')
