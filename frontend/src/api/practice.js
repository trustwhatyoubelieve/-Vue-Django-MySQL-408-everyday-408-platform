/**
 * 在线练习 API
 */
import request from './request'

/**
 * 开始练习
 * @param {number} subchapterId - 子章节 ID
 * @returns {Promise<{session_id, subchapter, total_count, answered_count, correct_count, progress_map}>}
 */
export const startPractice = (subchapterId) =>
  request.post('/practice/sessions/start/', { subchapter_id: subchapterId })

/**
 * 获取练习会话详情
 * @param {number} sessionId - 会话 ID
 * @returns {Promise<{id, subchapter, total_count, answered_count, correct_count, accuracy, status, question_ids, progress_map}>}
 */
export const getPracticeSession = (sessionId) =>
  request.get(`/practice/sessions/${sessionId}/`)

/**
 * 获取练习题目详情（练习模式，不暴露答案）
 * @param {number} sessionId - 会话 ID
 * @param {number} questionId - 题目 ID
 * @returns {Promise<{id, business_id, question_type, stem_text, stem_image, options, order_no, practice_status, is_locked, ...}>}
 */
export const getPracticeQuestion = (sessionId, questionId) =>
  request.get(`/practice/sessions/${sessionId}/questions/${questionId}/`)

/**
 * 提交答案
 * @param {number} sessionId - 会话 ID
 * @param {object} payload - { question_id, user_answer }
 * @returns {Promise<{question_id, practice_status, user_answer, is_correct, correct_answer, analysis_text, analysis_image, is_locked}>}
 */
export const submitPracticeAnswer = (sessionId, payload) =>
  request.post(`/practice/sessions/${sessionId}/submit/`, payload)

/**
 * 完成练习
 * @param {number} sessionId - 会话 ID
 * @returns {Promise<{session_id, total_count, answered_count, correct_count, accuracy}>}
 */
export const finishPractice = (sessionId) =>
  request.post(`/practice/sessions/${sessionId}/finish/`)

/**
 * 重置子章节刷题进度
 * @param {number} subchapterId - 子章节 ID
 * @returns {Promise<{subchapter_id, subchapter_name, deleted_count}>}
 */
export const resetSubchapterProgress = (subchapterId) =>
  request.post(`/practice/subchapters/${subchapterId}/reset-progress/`)
