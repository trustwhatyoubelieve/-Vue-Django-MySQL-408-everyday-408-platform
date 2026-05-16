/**
 * 错题本 & 收藏夹 API
 */
import request from './request'

// ========== 错题本 ==========

/**
 * 获取我的错题本列表
 * @param {Object} params - 筛选参数
 * @param {number} [params.course_id] - 按课程筛选
 * @param {number} [params.chapter_id] - 按章节筛选
 * @param {number} [params.subchapter_id] - 按子章节筛选
 * @returns {Promise<Array>}
 */
export const getWrongQuestions = (params = {}) =>
  request.get('/records/wrong-questions/', params)

/**
 * 获取单个错题详情
 * @param {number} wrongQuestionId - 错题记录 ID
 * @returns {Promise<Object>}
 */
export const getWrongQuestionDetail = (wrongQuestionId) =>
  request.get(`/records/wrong-questions/${wrongQuestionId}/`)

/**
 * 将错题移出错题本（标记已掌握）
 * @param {number} wrongQuestionId - 错题记录 ID
 * @returns {Promise}
 */
export const removeWrongQuestion = (wrongQuestionId) =>
  request.post(`/records/wrong-questions/${wrongQuestionId}/remove/`)

// ========== 收藏夹 ==========

/**
 * 获取我的收藏列表
 * @param {Object} params - 筛选参数
 * @param {number} [params.course_id] - 按课程筛选
 * @param {number} [params.chapter_id] - 按章节筛选
 * @param {number} [params.subchapter_id] - 按子章节筛选
 * @returns {Promise<Array>}
 */
export const getFavorites = (params = {}) =>
  request.get('/records/favorites/', params)

/**
 * 收藏一道题（幂等）
 * @param {number} questionId - 题目 ID
 * @returns {Promise<{favorite_id: number}>}
 */
export const addFavorite = (questionId) =>
  request.post('/records/favorites/add/', { question_id: questionId })

/**
 * 取消收藏
 * @param {number} favoriteId - 收藏记录 ID
 * @returns {Promise}
 */
export const removeFavorite = (favoriteId) =>
  request.post(`/records/favorites/${favoriteId}/remove/`)

/**
 * 检查某题是否已收藏
 * @param {number} questionId - 题目 ID
 * @returns {Promise<{is_favorited: boolean, favorite_id: number|null}>}
 */
export const checkFavorite = (questionId) =>
  request.get('/records/favorites/check/', { question_id: questionId })
