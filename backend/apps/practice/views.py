"""
practice/views.py
=================
在线练习 API 视图。

核心变更：
- 所有作答状态不再依赖 PracticeRecord 的「最近一次记录」
- 改为依赖 SubchapterPracticeProgress 固定进度表
- 绿色/红色题锁定，不可再覆盖
- 只有灰色题允许提交
"""
from django.db import transaction
from django.utils import timezone
from django.conf import settings

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.question_bank.models import SubChapter, Question, QuestionType
from .models import (
    PracticeSession, PracticeRecord, SessionStatus, AnswerMode,
    SubchapterPracticeProgress, ProgressStatus
)
from .serializers import (
    PracticeSessionSerializer,
    PracticeSessionDetailSerializer,
    PracticeQuestionSerializer,
    SubmitAnswerSerializer,
)


def build_response(code=0, message="", data=None):
    """统一响应格式"""
    return Response({
        "code": code,
        "message": message,
        "data": data
    })


def build_media_url(request, path):
    """构建媒体文件的完整 URL"""
    if not path:
        return None
    media_url = settings.MEDIA_URL + path
    return request.build_absolute_uri(media_url)


# --------------------------------------------------------------------------
# 辅助函数：获取子章节所有题目的固定进度
# --------------------------------------------------------------------------

def get_subchapter_progress_map(user, subchapter):
    """
    获取指定用户在某子章节下所有题目的固定进度。
    返回 {question_id: 'unattempted'|'correct'|'wrong'}
    """
    progress_qs = SubchapterPracticeProgress.objects.filter(
        user=user,
        subchapter=subchapter
    )
    result = {}
    for p in progress_qs:
        result[p.question_id] = p.status
    return result


# --------------------------------------------------------------------------
# 练习会话接口
# --------------------------------------------------------------------------


class StartPracticeView(APIView):
    """
    POST /api/practice/sessions/start/
    开始练习：创建练习会话，返回会话信息和所有题目的固定进度。
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subchapter_id = request.data.get("subchapter_id")
        if not subchapter_id:
            return build_response(code=1, message="subchapter_id 为必填参数")

        try:
            subchapter = SubChapter.objects.select_related(
                "chapter__course"
            ).get(id=subchapter_id, is_active=True)
        except SubChapter.DoesNotExist:
            return build_response(code=1, message="子章节不存在或未启用")

        total_count = subchapter.questions.filter(is_active=True).count()
        if total_count == 0:
            return build_response(code=1, message="该子章节暂无题目可练习")

        # 获取当前用户在该子章节下的固定进度
        progress_map = get_subchapter_progress_map(request.user, subchapter)

        # 统计已作答数（绿 + 红）
        answered_count = sum(1 for v in progress_map.values() if v != ProgressStatus.UNATTEMPTED)
        correct_count = sum(1 for v in progress_map.values() if v == ProgressStatus.CORRECT)

        # 创建练习会话
        session = PracticeSession.objects.create(
            user=request.user,
            subchapter=subchapter,
            total_count=total_count,
            answered_count=answered_count,
            correct_count=correct_count,
            status=SessionStatus.IN_PROGRESS,
        )

        return build_response(
            code=0,
            message="开始练习成功",
            data={
                "session_id": session.id,
                "subchapter": {
                    "id": subchapter.id,
                    "name": subchapter.name,
                },
                "total_count": total_count,
                "answered_count": answered_count,
                "correct_count": correct_count,
                "progress_map": progress_map,
            }
        )


class SessionDetailView(APIView):
    """
    GET /api/practice/sessions/<session_id>/
    获取练习会话详情（包含题目 ID 列表和固定进度）。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = PracticeSession.objects.select_related(
                "subchapter__chapter__course"
            ).get(id=session_id)
        except PracticeSession.DoesNotExist:
            return build_response(code=1, message="练习会话不存在")

        if session.user_id != request.user.id:
            return build_response(code=1, message="无权访问此练习会话")

        progress_map = get_subchapter_progress_map(request.user, session.subchapter)
        data = {
            "id": session.id,
            "subchapter": {
                "id": session.subchapter.id,
                "name": session.subchapter.name,
            },
            "total_count": session.total_count,
            "answered_count": session.answered_count,
            "correct_count": session.correct_count,
            "accuracy": session.accuracy,
            "status": session.status,
            "started_at": session.started_at,
            "finished_at": session.finished_at,
            "question_ids": session.get_question_ids(),
            "progress_map": progress_map,
        }
        return build_response(code=0, message="获取成功", data=data)


class SessionQuestionView(APIView):
    """
    GET /api/practice/sessions/<session_id>/questions/<question_id>/
    获取练习题目详情（练习模式，不暴露正确答案）。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id, question_id):
        try:
            session = PracticeSession.objects.select_related(
                "subchapter"
            ).get(id=session_id)
        except PracticeSession.DoesNotExist:
            return build_response(code=1, message="练习会话不存在")

        if session.user_id != request.user.id:
            return build_response(code=1, message="无权访问此练习会话")

        try:
            question = Question.objects.select_related(
                "subchapter__chapter__course"
            ).get(id=question_id, subchapter=session.subchapter, is_active=True)
        except Question.DoesNotExist:
            return build_response(code=1, message="题目不存在或不属于当前练习")

        serializer = PracticeQuestionSerializer(question, context={"request": request})
        data = serializer.data

        # 查固定进度表
        progress = SubchapterPracticeProgress.objects.filter(
            user=request.user,
            subchapter=session.subchapter,
            question=question
        ).first()

        if progress and progress.status != ProgressStatus.UNATTEMPTED:
            # 已锁定：返回状态，但不允许再次提交
            data["practice_status"] = progress.status
            data["first_answer"] = progress.first_answer
            data["is_locked"] = progress.is_locked
            data["is_answered"] = True
            data["user_answer"] = progress.first_answer
            data["is_correct"] = (progress.status == ProgressStatus.CORRECT)
        else:
            # 未作答或无进度
            data["practice_status"] = ProgressStatus.UNATTEMPTED
            data["first_answer"] = None
            data["is_locked"] = False
            data["is_answered"] = False
            data["user_answer"] = None
            data["is_correct"] = None

        return build_response(code=0, message="获取成功", data=data)


class SubmitAnswerView(APIView):
    """
    POST /api/practice/sessions/<session_id>/submit/
    提交答案。

    核心规则：
    - 先检查固定进度表，如果该题已经是 correct/wrong（已锁定），返回错误
    - 只有 unattempted 状态的题才允许提交
    - 提交成功后写入固定进度表并锁定，同时写入 PracticeRecord
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        serializer = SubmitAnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return build_response(code=1, message="参数错误", data=serializer.errors)

        question_id = serializer.validated_data["question_id"]
        user_answer = serializer.validated_data.get("user_answer")

        try:
            session = PracticeSession.objects.select_related("subchapter").get(id=session_id)
        except PracticeSession.DoesNotExist:
            return build_response(code=1, message="练习会话不存在")

        if session.user_id != request.user.id:
            return build_response(code=1, message="无权访问此练习会话")

        if session.status == SessionStatus.FINISHED:
            return build_response(code=1, message="练习会话已结束，无法继续作答")

        try:
            question = Question.objects.get(
                id=question_id,
                subchapter=session.subchapter,
                is_active=True
            )
        except Question.DoesNotExist:
            return build_response(code=1, message="题目不存在或不属于当前练习")

        if question.question_type == QuestionType.SINGLE_CHOICE:
            return self._handle_single_choice(request, session, question, user_answer)
        elif question.question_type == QuestionType.BIG_QUESTION:
            return self._handle_big_question(request, session, question)
        else:
            return build_response(code=1, message="不支持的题目类型")

    def _handle_single_choice(self, request, session, question, user_answer):
        """处理单选题"""
        if not user_answer:
            return build_response(code=1, message="单选题必须提交答案")

        # ---- 核心检查：固定进度表是否已锁定 ----
        existing_progress = SubchapterPracticeProgress.objects.filter(
            user=request.user,
            subchapter=session.subchapter,
            question=question
        ).first()

        if existing_progress and existing_progress.is_locked:
            return build_response(
                code=1,
                message="该题已作答，如需重做请先重置本子章节进度"
            )

        # 判定正误
        is_correct = (user_answer.upper() == question.correct_answer.upper())
        new_status = ProgressStatus.CORRECT if is_correct else ProgressStatus.WRONG

        # ---- 写入固定进度表 ----
        with transaction.atomic():
            progress, _ = SubchapterPracticeProgress.objects.update_or_create(
                user=request.user,
                subchapter=session.subchapter,
                question=question,
                defaults={
                    "status": new_status,
                    "first_answer": user_answer.upper(),
                    "is_locked": True,
                    "first_answered_at": timezone.now(),
                }
            )

            # 写入练习历史记录
            record, created = PracticeRecord.objects.update_or_create(
                session=session,
                question=question,
                defaults={
                    "user": request.user,
                    "user_answer": user_answer.upper(),
                    "is_correct": is_correct,
                    "is_answered": True,
                    "answer_mode": AnswerMode.SINGLE_CHOICE,
                }
            )

            # 更新会话统计（基于固定进度表）
            self._update_session_stats(session)

            # 错题本逻辑
            if not is_correct:
                from apps.records.models import WrongQuestion
                record, created = WrongQuestion.objects.get_or_create(
                    user=request.user,
                    question=question,
                    defaults={'wrong_count': 1, 'is_active': True}
                )
                if not created:
                    record.wrong_count += 1
                    record.is_active = True
                    record.save(update_fields=['wrong_count', 'is_active', 'updated_at'])

                # 错题复习推荐逻辑：创建或更新复习计划
                from apps.recommendation.models import WrongQuestionReview
                from datetime import timedelta

                review, review_created = WrongQuestionReview.objects.get_or_create(
                    user=request.user,
                    question=question,
                    defaults={
                        'next_review_time': timezone.now() + timedelta(days=1),
                        'review_count': 0,
                        'is_mastered': False,
                        'is_removed': False,
                    }
                )
                # 如果记录已存在且不是新创建的，则不重复创建
                # （下次复习时 review_count 和 next_review_time 已在 update_after_review 中更新）

        # 获取课程思维导图
        course = question.subchapter.chapter.course
        mindmap_url = None
        if course.mindmap_pdf:
            mindmap_url = build_media_url(request, course.mindmap_pdf.name)

        return build_response(
            code=0,
            message="提交成功",
            data={
                "question_id": question.id,
                "practice_status": new_status,
                "user_answer": user_answer.upper(),
                "is_correct": is_correct,
                "correct_answer": question.correct_answer,
                "course_mindmap_url": mindmap_url,
                "course_name": course.name,
                "is_locked": True,
            }
        )

    def _handle_big_question(self, request, session, question):
        """处理大题（查看即为作答，不自动判分）"""
        existing_progress = SubchapterPracticeProgress.objects.filter(
            user=request.user,
            subchapter=session.subchapter,
            question=question
        ).first()

        if existing_progress and existing_progress.is_locked:
            return build_response(
                code=1,
                message="该题已作答，如需重做请先重置本子章节进度"
            )

        with transaction.atomic():
            progress, _ = SubchapterPracticeProgress.objects.update_or_create(
                user=request.user,
                subchapter=session.subchapter,
                question=question,
                defaults={
                    "status": ProgressStatus.CORRECT,
                    "first_answer": None,
                    "is_locked": True,
                    "first_answered_at": timezone.now(),
                }
            )

            record, created = PracticeRecord.objects.update_or_create(
                session=session,
                question=question,
                defaults={
                    "user": session.user,
                    "user_answer": None,
                    "is_correct": None,
                    "is_answered": True,
                    "answer_mode": AnswerMode.BIG_QUESTION_VIEWED,
                }
            )

            self._update_session_stats(session)

        course = question.subchapter.chapter.course
        mindmap_url = None
        if course.mindmap_pdf:
            mindmap_url = build_media_url(request, course.mindmap_pdf.name)

        return build_response(
            code=0,
            message="已标记为已学习",
            data={
                "question_id": question.id,
                "practice_status": ProgressStatus.CORRECT,
                "user_answer": None,
                "is_correct": None,
                "correct_answer": None,
                "course_mindmap_url": mindmap_url,
                "course_name": course.name,
                "is_locked": True,
            }
        )

    def _update_session_stats(self, session):
        """根据固定进度表重新计算会话统计"""
        progress_qs = SubchapterPracticeProgress.objects.filter(
            user=session.user,
            subchapter=session.subchapter
        )
        total = progress_qs.count()
        correct = progress_qs.filter(status=ProgressStatus.CORRECT).count()
        answered = total - progress_qs.filter(status=ProgressStatus.UNATTEMPTED).count()
        session.answered_count = answered
        session.correct_count = correct
        session.total_count = session.subchapter.questions.filter(is_active=True).count()
        session.save(update_fields=["answered_count", "correct_count", "total_count"])


class FinishPracticeView(APIView):
    """
    POST /api/practice/sessions/<session_id>/finish/
    完成练习。
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        try:
            session = PracticeSession.objects.get(id=session_id)
        except PracticeSession.DoesNotExist:
            return build_response(code=1, message="练习会话不存在")

        if session.user_id != request.user.id:
            return build_response(code=1, message="无权访问此练习会话")

        if session.status == SessionStatus.FINISHED:
            return build_response(code=1, message="练习会话已经结束")

        session.status = SessionStatus.FINISHED
        session.finished_at = timezone.now()
        session.save(update_fields=["status", "finished_at"])

        return build_response(
            code=0,
            message="练习完成",
            data={
                "session_id": session.id,
                "total_count": session.total_count,
                "answered_count": session.answered_count,
                "correct_count": session.correct_count,
                "accuracy": session.accuracy,
            }
        )


class ResetProgressView(APIView):
    """
    POST /api/practice/subchapters/<subchapter_id>/reset-progress/
    重置指定子章节的刷题进度（仅影响当前用户）。
    不删除历史 PracticeRecord。
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, subchapter_id):
        try:
            subchapter = SubChapter.objects.get(id=subchapter_id, is_active=True)
        except SubChapter.DoesNotExist:
            return build_response(code=1, message="子章节不存在或未启用")

        # 删除该用户在该子章节下的所有固定进度记录
        deleted_count, _ = SubchapterPracticeProgress.objects.filter(
            user=request.user,
            subchapter=subchapter
        ).delete()

        return build_response(
            code=0,
            message="进度已重置",
            data={
                "subchapter_id": subchapter_id,
                "subchapter_name": subchapter.name,
                "deleted_count": deleted_count,
            }
        )
