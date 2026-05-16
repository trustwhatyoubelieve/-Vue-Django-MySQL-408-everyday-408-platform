"""
practice/urls.py
================
练习模块 URL 配置。
"""
from django.urls import path
from .views import (
    StartPracticeView,
    SessionDetailView,
    SessionQuestionView,
    SubmitAnswerView,
    FinishPracticeView,
    ResetProgressView,
)

urlpatterns = [
    # 开始练习
    path("sessions/start/", StartPracticeView.as_view(), name="practice-start"),
    # 获取会话详情
    path("sessions/<int:session_id>/", SessionDetailView.as_view(), name="practice-session-detail"),
    # 获取练习题目详情
    path("sessions/<int:session_id>/questions/<int:question_id>/", SessionQuestionView.as_view(), name="practice-question"),
    # 提交答案
    path("sessions/<int:session_id>/submit/", SubmitAnswerView.as_view(), name="practice-submit"),
    # 完成练习
    path("sessions/<int:session_id>/finish/", FinishPracticeView.as_view(), name="practice-finish"),
    # 重置子章节进度
    path("subchapters/<int:subchapter_id>/reset-progress/", ResetProgressView.as_view(), name="practice-reset-progress"),
]
