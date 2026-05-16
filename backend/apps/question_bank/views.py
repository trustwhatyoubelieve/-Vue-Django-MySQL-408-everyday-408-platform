"""
question_bank/views.py
=====================
题库浏览 API 视图。
"""
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Chapter, SubChapter, Question
from apps.practice.models import SubchapterPracticeProgress


def build_media_url(request, path):
    """构建媒体文件的完整 URL"""
    if not path:
        return None
    # 开发环境：拼接 MEDIA_URL（注意 MEDIA_URL 以 / 开头）
    # 例如：/media/questions/stem/xxx.jpg
    media_url = settings.MEDIA_URL + path
    # 构建绝对 URL
    return request.build_absolute_uri(media_url)


# --------------------------------------------------------------------------
# 课程相关
# --------------------------------------------------------------------------

class CourseListView(APIView):
    """
    GET /api/question-bank/courses/
    获取课程列表（仅启用状态）
    """
    permission_classes = [AllowAny]

    def get(self, request):
        courses = Course.objects.filter(is_active=True).order_by("order_no", "id")
        result = []
        for c in courses:
            mindmap_url = None
            if c.mindmap_pdf:
                mindmap_url = build_media_url(request, c.mindmap_pdf.name)
            result.append({
                "id": c.id,
                "name": c.name,
                "order_no": c.order_no,
                "chapter_count": c.chapters.filter(is_active=True).count(),
                "question_count": Question.objects.filter(
                    is_active=True, subchapter__chapter__course=c
                ).count(),
                "has_mindmap": bool(c.mindmap_pdf),
                "mindmap_pdf_url": mindmap_url,
            })
        return Response({"code": 0, "message": "获取课程列表成功", "data": result})


# --------------------------------------------------------------------------
# 章节相关
# --------------------------------------------------------------------------

class ChapterListByCourseView(APIView):
    """
    GET /api/question-bank/courses/<course_id>/chapters/
    获取指定课程下的章节列表（仅启用状态）
    """
    permission_classes = [AllowAny]

    def get(self, request, course_id):
        chapters = Chapter.objects.filter(
            course_id=course_id, is_active=True
        ).order_by("order_no", "id")
        result = []
        for ch in chapters:
            result.append({
                "id": ch.id,
                "name": ch.name,
                "order_no": ch.order_no,
                "course_id": ch.course_id,
                "subchapter_count": ch.subchapters.filter(is_active=True).count(),
            })
        return Response({"code": 0, "message": "获取章节列表成功", "data": result})


# --------------------------------------------------------------------------
# 子章节相关
# --------------------------------------------------------------------------

class SubChapterListByChapterView(APIView):
    """
    GET /api/question-bank/chapters/<chapter_id>/subchapters/
    获取指定章节下的子章节列表（仅启用状态）
    """
    permission_classes = [AllowAny]

    def get(self, request, chapter_id):
        subchapters = SubChapter.objects.filter(
            chapter_id=chapter_id, is_active=True
        ).order_by("order_no", "id")
        result = []
        for sc in subchapters:
            result.append({
                "id": sc.id,
                "name": sc.name,
                "order_no": sc.order_no,
                "chapter_id": sc.chapter_id,
                "question_count": sc.questions.filter(is_active=True).count(),
            })
        return Response({"code": 0, "message": "获取子章节列表成功", "data": result})


# --------------------------------------------------------------------------
# 题目相关
# --------------------------------------------------------------------------

class QuestionListBySubChapterView(APIView):
    """
    GET /api/question-bank/subchapters/<subchapter_id>/questions/
    获取指定子章节下的题目列表（仅启用状态）。
    支持登录用户返回每题的 practice_status：
      unattempted：未做过
      correct：做过且最近一次正确
      wrong：做过且最近一次错误
    """
    permission_classes = [AllowAny]

    def get(self, request, subchapter_id):
        questions = Question.objects.filter(
            subchapter_id=subchapter_id, is_active=True
        ).order_by("order_no", "id")

        # 判断登录用户（可选，题库可浏览）
        user = getattr(request, 'user', None)
        if user and not user.is_authenticated:
            user = None

        # 固定进度表：直接从 SubchapterPracticeProgress 获取状态
        status_map = {}  # {question_id: 'unattempted'|'correct'|'wrong'}

        if user:
            progress_qs = SubchapterPracticeProgress.objects.filter(
                user=user,
                subchapter_id=subchapter_id
            )
            for p in progress_qs:
                status_map[p.question_id] = p.status

        result = []
        for q in questions:
            stem_preview = (q.stem_text or "")[:80]
            if len(q.stem_text or "") > 80:
                stem_preview += "…"
            result.append({
                "id": q.id,
                "business_id": q.business_id,
                "subchapter_id": q.subchapter_id,
                "order_no": q.order_no,
                "question_type": q.question_type,
                "stem_preview": stem_preview,
                "stem_image": build_media_url(request, q.stem_image.name) if q.stem_image else None,
                "practice_status": status_map.get(q.id, 'unattempted'),
            })
        return Response({"code": 0, "message": "获取题目列表成功", "data": result})


class QuestionDetailView(APIView):
    """
    GET /api/question-bank/questions/<question_id>/
    获取单个题目详情
    """
    permission_classes = [AllowAny]

    def get(self, request, question_id):
        try:
            question = (
                Question.objects
                .select_related("subchapter__chapter__course")
                .get(id=question_id, is_active=True)
            )
        except Question.DoesNotExist:
            return Response({"code": 1, "message": "题目不存在或未启用"})

        course = question.subchapter.chapter.course
        mindmap_url = None
        if course.mindmap_pdf:
            mindmap_url = build_media_url(request, course.mindmap_pdf.name)

        return Response({"code": 0, "message": "获取题目详情成功", "data": {
            "id": question.id,
            "business_id": question.business_id,
            "subchapter_id": question.subchapter_id,
            "order_no": question.order_no,
            "question_type": question.question_type,
            "stem_text": question.stem_text,
            "stem_image": build_media_url(request, question.stem_image.name) if question.stem_image else None,
            "option_a_text": question.option_a_text,
            "option_a_image": build_media_url(request, question.option_a_image.name) if question.option_a_image else None,
            "option_b_text": question.option_b_text,
            "option_b_image": build_media_url(request, question.option_b_image.name) if question.option_b_image else None,
            "option_c_text": question.option_c_text,
            "option_c_image": build_media_url(request, question.option_c_image.name) if question.option_c_image else None,
            "option_d_text": question.option_d_text,
            "option_d_image": build_media_url(request, question.option_d_image.name) if question.option_d_image else None,
            "correct_answer": question.correct_answer,
            "analysis_text": question.analysis_text,
            "analysis_image": build_media_url(request, question.analysis_image.name) if question.analysis_image else None,
            "course_name": course.name,
            "course_id": course.id,
            "course_mindmap_url": mindmap_url,
            "chapter_name": question.subchapter.chapter.name,
            "subchapter_name": question.subchapter.name,
            }
        },
        )


# =============================================================================
# 辅助视图：获取排序数据（供前端调用）
# =============================================================================

@staff_member_required
def get_sort_data(request):
    """
    获取指定类型的排序数据
    GET 参数：
        type: course | chapter | subchapter | question
        id: 对应类型的父级 ID（chapter 需要 course_id，subchapter 需要 chapter_id，question 需要 subchapter_id）
    """
    sort_type = request.GET.get("type")
    item_id = request.GET.get("id")

    if sort_type == "course":
        courses = Course.objects.filter(is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "items": [
                    {"id": c.id, "name": c.name, "order_no": c.order_no}
                    for c in courses
                ]
            }
        })
    elif sort_type == "chapter":
        course_id = request.GET.get("course_id")
        if not course_id:
            return JsonResponse({"code": 1, "message": "缺少 course_id"}, status=400)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({"code": 1, "message": "课程不存在"}, status=404)
        chapters = Chapter.objects.filter(course=course, is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "parent": {"id": course.id, "name": course.name},
                "items": [
                    {"id": ch.id, "name": ch.name, "order_no": ch.order_no}
                    for ch in chapters
                ]
            }
        })
    elif sort_type == "subchapter":
        chapter_id = request.GET.get("chapter_id")
        if not chapter_id:
            return JsonResponse({"code": 1, "message": "缺少 chapter_id"}, status=400)
        try:
            chapter = Chapter.objects.select_related("course").get(id=chapter_id)
        except Chapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "章节不存在"}, status=404)
        subchapters = SubChapter.objects.filter(chapter=chapter, is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "parent": {"id": chapter.id, "name": chapter.name, "course_id": chapter.course.id, "course_name": chapter.course.name},
                "items": [
                    {"id": sc.id, "name": sc.name, "order_no": sc.order_no}
                    for sc in subchapters
                ]
            }
        })
    elif sort_type == "question":
        subchapter_id = request.GET.get("subchapter_id")
        if not subchapter_id:
            return JsonResponse({"code": 1, "message": "缺少 subchapter_id"}, status=400)
        try:
            subchapter = SubChapter.objects.select_related("chapter__course").get(id=subchapter_id)
        except SubChapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "子章节不存在"}, status=404)
        questions = Question.objects.filter(subchapter=subchapter, is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "parent": {
                    "id": subchapter.id,
                    "name": subchapter.name,
                    "chapter_id": subchapter.chapter.id,
                    "chapter_name": subchapter.chapter.name,
                    "course_id": subchapter.chapter.course.id,
                    "course_name": subchapter.chapter.course.name,
                },
                "items": [
                    {
                        "id": q.id,
                        "business_id": q.business_id,
                        "stem_preview": (q.stem_text or "")[:50],
                        "order_no": q.order_no,
                    }
                    for q in questions
                ]
            }
        })
    else:
        return JsonResponse({"code": 1, "message": "未知类型"}, status=400)
