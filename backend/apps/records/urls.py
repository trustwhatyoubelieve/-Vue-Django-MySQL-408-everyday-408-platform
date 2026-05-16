from django.urls import path
from .views import (
    WrongQuestionListView,
    WrongQuestionDetailView,
    WrongQuestionRemoveView,
    FavoriteListView,
    FavoriteCreateView,
    FavoriteRemoveView,
    FavoriteCheckView,
    OverviewStatsView,
    CourseStatsView,
    ChapterStatsView,
    SubChapterStatsView,
    RecentSessionsView,
    RecentWrongQuestionsView,
    RecentFavoritesView,
    DailyPracticeStatsView,
)

urlpatterns = [
    # 错题本
    path('wrong-questions/', WrongQuestionListView.as_view(), name='wrong-question-list'),
    path('wrong-questions/<int:pk>/', WrongQuestionDetailView.as_view(), name='wrong-question-detail'),
    path('wrong-questions/<int:pk>/remove/', WrongQuestionRemoveView.as_view(), name='wrong-question-remove'),

    # 收藏夹
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('favorites/add/', FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/<int:pk>/remove/', FavoriteRemoveView.as_view(), name='favorite-remove'),
    path('favorites/check/', FavoriteCheckView.as_view(), name='favorite-check'),

    # 学习统计
    path('stats/overview/', OverviewStatsView.as_view(), name='stats-overview'),
    path('stats/courses/', CourseStatsView.as_view(), name='stats-courses'),
    path('stats/chapters/', ChapterStatsView.as_view(), name='stats-chapters'),
    path('stats/subchapters/', SubChapterStatsView.as_view(), name='stats-subchapters'),
    path('stats/recent-sessions/', RecentSessionsView.as_view(), name='stats-recent-sessions'),
    path('stats/recent-wrong-questions/', RecentWrongQuestionsView.as_view(), name='stats-recent-wrong'),
    path('stats/recent-favorites/', RecentFavoritesView.as_view(), name='stats-recent-favorites'),
    path('stats/daily-practice/', DailyPracticeStatsView.as_view(), name='stats-daily-practice'),
]
