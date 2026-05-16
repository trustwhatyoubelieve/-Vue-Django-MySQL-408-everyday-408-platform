/**
 * 学习统计 API
 */
import request from './request'

/**
 * 获取学习总览统计
 * @returns {Promise<{total_sessions, total_answered_questions, total_correct_questions, overall_accuracy, wrong_question_count, favorite_count}>}
 */
export const getOverviewStats = () => request.get('/records/stats/overview/')

/**
 * 获取课程维度统计
 * @param {boolean} includeZero - 是否包含零练习的课程，默认 false（仅返回有数据的）
 * @returns {Promise<Array<{course_id, course_name, answered_count, correct_count, accuracy}>>}
 */
export const getCourseStats = (includeZero = false) =>
  request.get('/records/stats/courses/', { has_data: includeZero ? '0' : '1' })

/**
 * 获取章节维度统计
 * @param {number} courseId - 课程 ID（必填）
 * @param {boolean} includeZero - 是否包含零练习的章节，默认 false
 * @returns {Promise<Array<{chapter_id, chapter_name, answered_count, correct_count, accuracy}>>}
 */
export const getChapterStats = (courseId, includeZero = false) =>
  request.get('/records/stats/chapters/', {
    course_id: courseId,
    has_data: includeZero ? '0' : '1'
  })

/**
 * 获取子章节维度统计
 * @param {number} chapterId - 章节 ID（必填）
 * @param {boolean} includeZero - 是否包含零练习的子章节，默认 false
 * @returns {Promise<Array<{subchapter_id, subchapter_name, answered_count, correct_count, accuracy}>>}
 */
export const getSubChapterStats = (chapterId, includeZero = false) =>
  request.get('/records/stats/subchapters/', {
    chapter_id: chapterId,
    has_data: includeZero ? '0' : '1'
  })

/**
 * 获取最近练习记录
 * @returns {Promise<Array>}
 */
export const getRecentSessions = () => request.get('/records/stats/recent-sessions/')

/**
 * 获取最近错题
 * @returns {Promise<Array>}
 */
export const getRecentWrongQuestions = () => request.get('/records/stats/recent-wrong-questions/')

/**
 * 获取最近收藏
 * @returns {Promise<Array>}
 */
export const getRecentFavorites = () => request.get('/records/stats/recent-favorites/')

/**
 * 获取每日刷题统计
 * @param {number} days - 返回最近多少天的数据，默认 6
 * @returns {Promise<Array<{date, answered_count, correct_count, accuracy, study_duration_seconds, study_duration_text}>>}
 */
export const getDailyPracticeStats = (days = 6) =>
  request.get('/records/stats/daily-practice/', { days })
