"""
question_bank/urls.py
=====================
题库模块 URL 配置。
"""
from django.urls import path

from .views import (
    CourseListView,
    ChapterListByCourseView,
    SubChapterListByChapterView,
    QuestionListBySubChapterView,
    QuestionDetailView,
    get_sort_data,
)

urlpatterns = [
    # 题库浏览 API
    path("courses/", CourseListView.as_view(), name="course-list"),
    path("courses/<int:course_id>/chapters/", ChapterListByCourseView.as_view(), name="chapter-list"),
    path("chapters/<int:chapter_id>/subchapters/", SubChapterListByChapterView.as_view(), name="subchapter-list"),
    path("subchapters/<int:subchapter_id>/questions/", QuestionListBySubChapterView.as_view(), name="question-list"),
    path("questions/<int:question_id>/", QuestionDetailView.as_view(), name="question-detail"),

    # 拖动排序 API（由 admin.py 中的 sort_view 渲染模板，data/save API 放在这里）
    path("admin/sort/data/", get_sort_data, name="sort-data"),
]
