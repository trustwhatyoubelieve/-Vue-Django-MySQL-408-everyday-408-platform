"""
records/views.py
================
错题本 & 收藏夹 & 学习统计 API 视图。
"""
from datetime import timedelta
from django.db.models import Count, Q
from django.db.models.functions import Cast
from django.db.models import DateField
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WrongQuestion, FavoriteQuestion
from .serializers import (
    WrongQuestionListSerializer,
    WrongQuestionDetailSerializer,
    FavoriteQuestionListSerializer,
    FavoriteQuestionCreateSerializer,
    FavoriteStatusSerializer,
    OverviewStatsSerializer,
    CourseStatsSerializer,
    ChapterStatsSerializer,
    RecentSessionSerializer,
    RecentWrongQuestionSerializer,
    RecentFavoriteSerializer,
)
from apps.practice.models import PracticeSession, PracticeRecord, SubchapterPracticeProgress


def build_response(code=0, message="", data=None):
    """统一响应格式"""
    return Response({
        "code": code,
        "message": message,
        "data": data
    })


# ========== 错题本 ==========

class WrongQuestionListView(APIView):
    """
    GET /api/records/wrong-questions/
    获取我的错题本列表（仅 is_active=True）。
    Query params:
      - course_id: 按课程筛选
      - chapter_id: 按章节筛选
      - subchapter_id: 按子章节筛选
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        course_id = request.query_params.get('course_id')
        chapter_id = request.query_params.get('chapter_id')
        subchapter_id = request.query_params.get('subchapter_id')

        qs = WrongQuestion.objects.filter(
            user=request.user,
            is_active=True
        ).select_related(
            'question',
            'question__subchapter',
            'question__subchapter__chapter',
            'question__subchapter__chapter__course'
        )

        if course_id:
            qs = qs.filter(question__subchapter__chapter__course_id=int(course_id))
        if chapter_id:
            qs = qs.filter(question__subchapter__chapter_id=int(chapter_id))
        if subchapter_id:
            qs = qs.filter(question__subchapter_id=int(subchapter_id))

        serializer = WrongQuestionListSerializer(
            qs.order_by('-last_wrong_at'),
            many=True,
            context={'request': request}
        )
        return build_response(
            code=0,
            message="获取错题本成功",
            data=serializer.data
        )


class WrongQuestionDetailView(APIView):
    """
    GET /api/records/wrong-questions/<wrong_question_id>/
    获取单个错题详情（仅限本人）。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            record = WrongQuestion.objects.select_related(
                'question',
                'question__subchapter',
                'question__subchapter__chapter',
                'question__subchapter__chapter__course'
            ).get(pk=pk, user=request.user, is_active=True)
        except WrongQuestion.DoesNotExist:
            return build_response(code=1, message="错题记录不存在")

        serializer = WrongQuestionDetailSerializer(record, context={'request': request})
        return build_response(
            code=0,
            message="获取错题详情成功",
            data=serializer.data
        )


class WrongQuestionRemoveView(APIView):
    """
    POST /api/records/wrong-questions/<wrong_question_id>/remove/
    将错题移出错题本（软删除，将 is_active 设为 False）。
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            record = WrongQuestion.objects.get(pk=pk, user=request.user, is_active=True)
        except WrongQuestion.DoesNotExist:
            return build_response(code=1, message="错题记录不存在")

        record.is_active = False
        record.save(update_fields=['is_active'])
        return build_response(code=0, message="已移出错题本")


# ========== 收藏夹 ==========

class FavoriteListView(APIView):
    """
    GET /api/records/favorites/
    获取我的收藏列表。
    Query params:
      - course_id: 按课程筛选
      - chapter_id: 按章节筛选
      - subchapter_id: 按子章节筛选
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        course_id = request.query_params.get('course_id')
        chapter_id = request.query_params.get('chapter_id')
        subchapter_id = request.query_params.get('subchapter_id')

        qs = FavoriteQuestion.objects.filter(
            user=request.user
        ).select_related(
            'question',
            'question__subchapter',
            'question__subchapter__chapter',
            'question__subchapter__chapter__course'
        )

        if course_id:
            qs = qs.filter(question__subchapter__chapter__course_id=int(course_id))
        if chapter_id:
            qs = qs.filter(question__subchapter__chapter_id=int(chapter_id))
        if subchapter_id:
            qs = qs.filter(question__subchapter_id=int(subchapter_id))

        serializer = FavoriteQuestionListSerializer(
            qs.order_by('-created_at'),
            many=True,
            context={'request': request}
        )
        return build_response(
            code=0,
            message="获取收藏夹成功",
            data=serializer.data
        )


class FavoriteCreateView(APIView):
    """
    POST /api/records/favorites/
    添加收藏（幂等：已存在则直接返回成功）。
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FavoriteQuestionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return build_response(code=1, message="参数错误", data=serializer.errors)

        question_id = serializer.validated_data['question_id']

        record, created = FavoriteQuestion.objects.get_or_create(
            user=request.user,
            question_id=question_id
        )
        return build_response(
            code=0,
            message="收藏成功" if created else "已收藏",
            data={"favorite_id": record.id}
        )


class FavoriteRemoveView(APIView):
    """
    POST /api/records/favorites/<favorite_id>/remove/
    取消收藏（物理删除）。
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            record = FavoriteQuestion.objects.get(pk=pk, user=request.user)
        except FavoriteQuestion.DoesNotExist:
            return build_response(code=1, message="收藏记录不存在")

        record.delete()
        return build_response(code=0, message="已取消收藏")


class FavoriteCheckView(APIView):
    """
    GET /api/records/favorites/check/?question_id=101
    查询某题是否已被当前用户收藏。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = FavoriteStatusSerializer(data=request.query_params)
        if not serializer.is_valid():
            return build_response(code=1, message="参数错误")

        question_id = serializer.validated_data['question_id']
        record = FavoriteQuestion.objects.filter(
            user=request.user,
            question_id=question_id
        ).first()

        return build_response(
            code=0,
            message="获取成功",
            data={
                "is_favorited": record is not None,
                "favorite_id": record.id if record else None
            }
        )


# ========== 学习统计 ==========

def calc_accuracy(total, correct):
    """安全计算正确率，total 为 0 时返回 0"""
    if not total:
        return 0.0
    return round(correct / total, 4)


class OverviewStatsView(APIView):
    """
    GET /api/records/stats/overview/
    获取学习中心总览统计。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 从 PracticeRecord 聚合
        answered = PracticeRecord.objects.filter(
            user=user, is_answered=True
        )
        total_answered = answered.count()
        total_correct = answered.filter(is_correct=True).count()

        # 从 PracticeSession 聚合
        total_sessions = PracticeSession.objects.filter(user=user).count()

        # 从 WrongQuestion 聚合（只统计 is_active=True）
        wrong_question_count = WrongQuestion.objects.filter(
            user=user, is_active=True
        ).count()

        # 从 FavoriteQuestion 聚合
        favorite_count = FavoriteQuestion.objects.filter(user=user).count()

        return build_response(
            code=0,
            message="获取学习总览成功",
            data={
                "total_sessions": total_sessions,
                "total_answered_questions": total_answered,
                "total_correct_questions": total_correct,
                "overall_accuracy": calc_accuracy(total_answered, total_correct),
                "wrong_question_count": wrong_question_count,
                "favorite_count": favorite_count,
            }
        )


class CourseStatsView(APIView):
    """
    GET /api/records/stats/courses/
    获取课程维度统计。
    Query params:
      - has_data=1 (default): 仅返回有练习记录的课程
      - has_data=0: 返回所有课程（含零练习的课程）
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        has_data = request.query_params.get('has_data', '1') == '1'

        from apps.question_bank.models import Course

        # 先从 PracticeRecord 聚合出每个 course_id 的做题统计
        raw_stats = (
            PracticeRecord.objects
            .filter(user=user, is_answered=True)
            .values('question__subchapter__chapter__course_id')
            .annotate(
                answered_count=Count('id'),
                correct_count=Count('id', filter=Q(is_correct=True))
            )
        )

        stats_map = {}
        for item in raw_stats:
            cid = item['question__subchapter__chapter__course_id']
            stats_map[cid] = {
                'answered_count': item['answered_count'],
                'correct_count': item['correct_count'],
            }

        # 构建结果：所有课程都查出来，再做合并
        courses = Course.objects.filter(is_active=True).order_by('order_no')
        result = []
        for course in courses:
            stats = stats_map.get(course.id)
            if stats or not has_data:
                answered = stats['answered_count'] if stats else 0
                correct = stats['correct_count'] if stats else 0
                result.append({
                    "course_id": course.id,
                    "course_name": course.name,
                    "answered_count": answered,
                    "correct_count": correct,
                    "accuracy": calc_accuracy(answered, correct),
                })

        return build_response(
            code=0,
            message="获取课程统计成功",
            data=result
        )


class ChapterStatsView(APIView):
    """
    GET /api/records/stats/chapters/?course_id=1&has_data=1
    获取章节维度统计。
    Query params:
      - course_id: 必选，指定课程
      - has_data=1 (default): 仅返回有练习记录的章节
      - has_data=0: 返回所有章节（含零练习的章节）
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        course_id = request.query_params.get('course_id')
        has_data = request.query_params.get('has_data', '1') == '1'

        if not course_id:
            return build_response(code=1, message="course_id 为必填参数")

        from apps.question_bank.models import Chapter

        # 先在 PracticeRecord 上按 chapter_id 聚合
        raw_stats = (
            PracticeRecord.objects
            .filter(
                user=user,
                is_answered=True,
                question__subchapter__chapter__course_id=int(course_id)
            )
            .values('question__subchapter__chapter_id')
            .annotate(
                answered_count=Count('id'),
                correct_count=Count('id', filter=Q(is_correct=True))
            )
        )

        stats_map = {}
        for item in raw_stats:
            chid = item['question__subchapter__chapter_id']
            stats_map[chid] = {
                'answered_count': item['answered_count'],
                'correct_count': item['correct_count'],
            }

        # 查询该课程下所有章节并合并统计
        chapters = Chapter.objects.filter(
            is_active=True, course_id=int(course_id)
        ).order_by('order_no')

        result = []
        for ch in chapters:
            stats = stats_map.get(ch.id)
            if stats or not has_data:
                answered = stats['answered_count'] if stats else 0
                correct = stats['correct_count'] if stats else 0
                result.append({
                    "chapter_id": ch.id,
                    "chapter_name": ch.name,
                    "answered_count": answered,
                    "correct_count": correct,
                    "accuracy": calc_accuracy(answered, correct),
                })

        return build_response(
            code=0,
            message="获取章节统计成功",
            data=result
        )


class SubChapterStatsView(APIView):
    """
    GET /api/records/stats/subchapters/?chapter_id=1&has_data=1
    获取子章节维度统计。
    Query params:
      - chapter_id: 必选，指定章节
      - has_data=1 (default): 仅返回有练习记录的子章节
      - has_data=0: 返回所有子章节（含零练习的子章节）

    进度口径：查 SubchapterPracticeProgress 表，status != unattempted 即为已完成。
    该表有 (user, subchapter, question) 唯一约束，每题只有一条记录，不会重复。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        chapter_id = request.query_params.get('chapter_id')
        has_data = request.query_params.get('has_data', '1') == '1'

        if not chapter_id:
            return build_response(code=1, message="chapter_id 为必填参数")

        from apps.question_bank.models import SubChapter
        from apps.practice.models import ProgressStatus

        # 从固定进度表查已完成题目数（correct + wrong）
        raw_stats = (
            SubchapterPracticeProgress.objects
            .filter(
                user=user,
                subchapter__chapter_id=int(chapter_id)
            )
            .values('subchapter_id')
            .annotate(
                answered_count=Count('id', filter=~Q(status=ProgressStatus.UNATTEMPTED)),
                correct_count=Count('id', filter=Q(status=ProgressStatus.CORRECT))
            )
        )

        stats_map = {}
        for item in raw_stats:
            scid = item['subchapter_id']
            stats_map[scid] = {
                'answered_count': item['answered_count'],
                'correct_count': item['correct_count'],
            }

        # 查询该章节下所有子章节并合并统计
        subchapters = SubChapter.objects.filter(
            is_active=True, chapter_id=int(chapter_id)
        ).order_by('order_no')

        result = []
        for sc in subchapters:
            stats = stats_map.get(sc.id)
            if stats or not has_data:
                answered = stats['answered_count'] if stats else 0
                correct = stats['correct_count'] if stats else 0
                result.append({
                    "subchapter_id": sc.id,
                    "subchapter_name": sc.name,
                    "answered_count": answered,
                    "correct_count": correct,
                    "accuracy": calc_accuracy(answered, correct),
                })

        return build_response(
            code=0,
            message="获取子章节统计成功",
            data=result
        )


class RecentSessionsView(APIView):
    """
    GET /api/records/stats/recent-sessions/
    获取最近练习记录（最近 8 条）。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = (
            PracticeSession.objects
            .filter(user=request.user)
            .select_related('subchapter')
            .order_by('-started_at')[:8]
        )

        result = []
        for s in sessions:
            result.append({
                "session_id": s.id,
                "subchapter_name": s.subchapter.name,
                "total_count": s.total_count,
                "answered_count": s.answered_count,
                "correct_count": s.correct_count,
                "accuracy": calc_accuracy(s.answered_count, s.correct_count),
                "started_at": s.started_at,
                "finished_at": s.finished_at,
                "status": s.status,
            })

        return build_response(
            code=0,
            message="获取最近练习成功",
            data=result
        )


class RecentWrongQuestionsView(APIView):
    """
    GET /api/records/stats/recent-wrong-questions/
    获取最近错题（最近 5 条）。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = (
            WrongQuestion.objects
            .filter(user=request.user, is_active=True)
            .select_related('question')
            .order_by('-last_wrong_at')[:5]
        )

        result = []
        for r in records:
            result.append({
                "wrong_question_id": r.id,
                "question_id": r.question.id,
                "business_id": r.question.business_id,
                "question_type": r.question.question_type,
                "stem_text": r.question.stem_text or None,
                "wrong_count": r.wrong_count,
                "last_wrong_at": r.last_wrong_at,
            })

        return build_response(
            code=0,
            message="获取最近错题成功",
            data=result
        )


class RecentFavoritesView(APIView):
    """
    GET /api/records/stats/recent-favorites/
    获取最近收藏（最近 5 条）。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = (
            FavoriteQuestion.objects
            .filter(user=request.user)
            .select_related('question')
            .order_by('-created_at')[:5]
        )

        result = []
        for r in records:
            result.append({
                "favorite_id": r.id,
                "question_id": r.question.id,
                "business_id": r.question.business_id,
                "question_type": r.question.question_type,
                "stem_text": r.question.stem_text or None,
                "created_at": r.created_at,
            })

        return build_response(
            code=0,
            message="获取最近收藏成功",
            data=result
        )


def format_duration(seconds):
    """将秒数格式化为 HH:MM:SS"""
    if seconds is None or seconds < 0:
        return "—"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


class DailyPracticeStatsView(APIView):
    """
    GET /api/records/stats/daily-practice/?days=14
    获取每日刷题统计（按天聚合）。

    Query params:
      - days: 返回最近多少天的数据，默认 14

    返回字段说明：
      - answered_count: 当天已答题目数量（基于 PracticeRecord.is_answered=True）
      - correct_count: 当天答对题目数量
      - accuracy: 当天正确率 = correct_count / answered_count（分母为0时返回0）
      - study_duration_seconds: 当天已完成 session 的总时长（秒）
        统计口径：仅统计 finished_at 不为空的已完成 session，
        时长 = finished_at - started_at，按 started_at 所在日期归属
      - study_duration_text: study_duration_seconds 的人类可读格式
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            days = int(request.query_params.get('days', 14))
            days = min(max(days, 1), 90)  # 限制范围 1~90 天
        except (ValueError, TypeError):
            days = 14

        today = timezone.now().date()
        start_date = today - timedelta(days=days - 1)

        # ---- 1. 从 PracticeRecord 聚合每日作答数据 ----
        # 使用 Cast 将 answered_at 转换为 DATE，绕过 answered_at__date 过滤器在
        # MySQL + Asia/Shanghai 时区下对 timezone-aware 字段的错误日期范围比较
        daily_records = (
            PracticeRecord.objects
            .filter(user=user, is_answered=True)
            .annotate(answered_date=Cast('answered_at', DateField()))
            .filter(answered_date__gte=start_date, answered_date__lte=today)
            .values('answered_date')
            .annotate(
                answered_count=Count('id'),
                correct_count=Count('id', filter=Q(is_correct=True)),
            )
            .order_by('answered_date')
        )

        stats_map = {}
        for rec in daily_records:
            date_str = str(rec['answered_date'])
            stats_map[date_str] = {
                'answered_count': rec['answered_count'],
                'correct_count': rec['correct_count'],
            }

        # ---- 2. 从 PracticeSession 聚合每日学习时长 ----
        # 仅统计已完成的 session，按 started_at 所在日期归属
        # 使用 Cast 将 started_at/finished_at 转换为 DATE，绕过 date 过滤器的时区问题
        finished_sessions = (
            PracticeSession.objects
            .filter(user=user, status='finished', finished_at__isnull=False)
            .annotate(
                started_date=Cast('started_at', DateField()),
                finished_date=Cast('finished_at', DateField()),
            )
            .filter(started_date__gte=start_date, started_date__lte=today)
            .order_by('started_at')
        )

        session_duration_map = {}
        for s in finished_sessions:
            date_str = str(s.started_at.date())
            duration = (s.finished_at - s.started_at).total_seconds()
            if duration > 0:
                session_duration_map[date_str] = session_duration_map.get(date_str, 0) + duration

        # ---- 3. 补全所有日期（含无数据的日期） ----
        result = []
        current = start_date
        while current <= today:
            date_str = str(current)
            stats = stats_map.get(date_str, {'answered_count': 0, 'correct_count': 0})
            answered = stats.get('answered_count', 0)
            correct = stats.get('correct_count', 0)
            duration_seconds = int(session_duration_map.get(date_str, 0))

            accuracy = round(correct / answered, 4) if answered > 0 else 0.0

            result.append({
                "date": date_str,
                "answered_count": answered,
                "correct_count": correct,
                "accuracy": accuracy,
                "study_duration_seconds": duration_seconds,
                "study_duration_text": format_duration(duration_seconds),
            })
            current += timedelta(days=1)

        return build_response(
            code=0,
            message="获取每日刷题统计成功",
            data=result
        )
