/**
 * API 接口统一导出
 */
import request from './request'

// 健康检查接口
export const healthAPI = {
  check: () => request.get('/health/')
}

// 用户接口
export const userAPI = {
  register: (data) => request.post('/users/users/register/', data),
  login: (data) => request.post('/users/users/login/', data),
  getMe: () => request.get('/users/users/me/'),
  refreshToken: (data) => request.post('/users/users/token/refresh/', data)
}

// 题库浏览接口
export * from './questionBank'

// 在线练习接口
export * from './practice'

// 学习记录接口（错题本/收藏夹）
export * from './records'

// 学习统计接口
export * from './stats'

// 智能推荐接口
export * from './recommendation'
