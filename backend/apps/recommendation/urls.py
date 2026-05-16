"""
recommendation/urls.py
===================
错题复习推荐的 URL 路由配置。
"""
from django.urls import path
from .views import (
    WrongQuestionRecommendListView,
    WrongQuestionReviewSubmitView,
    WrongQuestionAllListView,
    WrongQuestionRemoveView,
    HighWrongRateRecommendationView,
)

app_name = 'recommendation'

urlpatterns = [
    # 获取待复习错题列表
    path('wrong-questions/', WrongQuestionRecommendListView.as_view(), name='wrong-questions'),
    # 提交复习结果
    path('wrong-questions/<int:pk>/review/', WrongQuestionReviewSubmitView.as_view(), name='wrong-questions-review'),
    # 获取所有复习记录（含已掌握）
    path('wrong-questions/all/', WrongQuestionAllListView.as_view(), name='wrong-questions-all'),
    # 移出复习计划
    path('wrong-questions/<int:pk>/remove/', WrongQuestionRemoveView.as_view(), name='wrong-questions-remove'),
    # 高频错题推荐
    path('high-wrong-rate/', HighWrongRateRecommendationView.as_view(), name='high-wrong-rate'),
]
