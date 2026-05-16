/**
 * 题库浏览 API
 */
import request from './request'

// 获取课程列表
export const getCourses = () => request.get('/question-bank/courses/')

// 获取某课程下的章节列表
export const getChaptersByCourse = (courseId) =>
  request.get(`/question-bank/courses/${courseId}/chapters/`)

// 获取某章节下的子章节列表
export const getSubChaptersByChapter = (chapterId) =>
  request.get(`/question-bank/chapters/${chapterId}/subchapters/`)

// 获取某子章节下的题目列表
export const getQuestionsBySubChapter = (subchapterId) =>
  request.get(`/question-bank/subchapters/${subchapterId}/questions/`)

// 获取单个题目详情
export const getQuestionDetail = (questionId) =>
  request.get(`/question-bank/questions/${questionId}/`)