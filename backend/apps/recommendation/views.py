"""
recommendation/views.py
=====================
错题复习推荐 API 视图。

接口设计：
    GET  /api/recommendations/wrong-questions/
        → 获取当前用户所有待复习的错题（is_mastered=False 且 next_review_time <= now）
        → 按 next_review_time 升序排列

    POST /api/recommendations/wrong-questions/<id>/review/
        → 提交复习结果
        → 请求体: { "is_correct": true/false }
        → 返回: 更新后的复习状态
"""
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.question_bank.models import Question
from apps.practice.models import PracticeRecord
from .models import WrongQuestionReview
from .serializers import (
    ReviewRecordSerializer,
    ReviewRecordListSerializer,
    ReviewResultSerializer,
    HighWrongRateQuestionSerializer,
)


def build_response(code=0, message="", data=None):
    """统一响应格式"""
    return Response({
        "code": code,
        "message": message,
        "data": data
    })


class WrongQuestionRecommendListView(APIView):
    """
    GET /api/recommendations/wrong-questions/
    获取当前用户需要复习的错题推荐列表。

    查询条件：
        - user = 当前登录用户
        - is_mastered = False（未掌握）
        - next_review_time <= 当前时间（已到复习时间）
        - is_removed = False（未被移除）

    返回：按 next_review_time 升序排列
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()

        # 查询待复习的错题
        review_list = WrongQuestionReview.objects.filter(
            user=request.user,
            is_mastered=False,
            is_removed=False,
            next_review_time__lte=now,
        ).select_related(
            'question__subchapter__chapter__course'
        ).order_by('next_review_time')

        serializer = ReviewRecordSerializer(review_list, many=True)

        return build_response(
            code=0,
            message="获取推荐错题成功",
            data={
                "count": review_list.count(),
                "results": serializer.data,
            }
        )


class WrongQuestionReviewSubmitView(APIView):
    """
    POST /api/recommendations/wrong-questions/<id>/review/
    提交错题复习结果。

    请求体：
        { "is_correct": true/false }

    复习规则（简化版艾宾浩斯遗忘曲线）：
        答对：
            review_count + 1
            next_review_time 根据新的 review_count 确定：
                review_count=0 → 1天后
                review_count=1 → 2天后
                review_count=2 → 4天后
                review_count=3 → 7天后
                review_count>=4 → 15天后
            若 review_count >= 5，is_mastered = True

        答错：
            review_count = 0
            next_review_time = 明天（1天后）
            is_mastered = False
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = ReviewResultSerializer(data=request.data)
        if not serializer.is_valid():
            return build_response(code=1, message="参数错误", data=serializer.errors)

        is_correct = serializer.validated_data['is_correct']

        try:
            review_record = WrongQuestionReview.objects.select_related(
                'question__subchapter__chapter__course'
            ).get(id=pk, user=request.user)
        except WrongQuestionReview.DoesNotExist:
            return build_response(code=1, message="复习记录不存在或无权访问")

        # 调用模型方法更新复习状态
        review_record.update_after_review(is_correct=is_correct)

        # 刷新获取最新状态
        review_record.refresh_from_db()

        message = "复习完成，该题已掌握！" if review_record.is_mastered else "复习记录已更新"
        return build_response(
            code=0,
            message=message,
            data={
                "review_count": review_record.review_count,
                "next_review_time": review_record.next_review_time,
                "is_mastered": review_record.is_mastered,
            }
        )


class WrongQuestionAllListView(APIView):
    """
    GET /api/recommendations/wrong-questions/all/
    获取当前用户所有的复习记录（包含已掌握的），用于展示复习历史。
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        review_list = WrongQuestionReview.objects.filter(
            user=request.user,
            is_removed=False,
        ).select_related(
            'question__subchapter__chapter__course'
        ).order_by('-updated_at')

        serializer = ReviewRecordListSerializer(review_list, many=True)

        return build_response(
            code=0,
            message="获取复习记录成功",
            data={
                "count": review_list.count(),
                "results": serializer.data,
            }
        )


class WrongQuestionRemoveView(APIView):
    """
    POST /api/recommendations/wrong-questions/<id>/remove/
    将某道题的复习记录从复习计划中移除（软删除）。
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            review_record = WrongQuestionReview.objects.get(id=pk, user=request.user)
        except WrongQuestionReview.DoesNotExist:
            return build_response(code=1, message="复习记录不存在或无权访问")

        review_record.is_removed = True
        review_record.save(update_fields=['is_removed', 'updated_at'])

        return build_response(code=0, message="已从复习计划中移除")


# =============================================================================
# 高频错题推荐
# =============================================================================

class HighWrongRateRecommendationView(APIView):
    """
    GET /api/recommendations/high-wrong-rate/
    基于全站用户答题行为统计，推荐错误率高、练习次数多的重点题目。

    统计逻辑：
        - 统计每道题的全站 total_attempts（总作答次数）和 wrong_attempts（错误次数）
        - 过滤 total_attempts < 3 的题目（避免样本过小）
        - 计算错误率 wrong_rate = wrong_attempts / total_attempts
        - 计算推荐分数 score = wrong_rate * 0.7 + normalized_total_attempts * 0.3
            - wrong_rate: 题目历史错误率
            - normalized_total_attempts: 题目练习次数归一化热度（相对于当前结果集最大值）
        - 按 score 降序排列，取前 10 道题

    用户标记：
        - user_has_done: 当前用户是否做过该题
        - user_has_wrong: 当前用户是否做错过该题

    推荐理由：
        - 根据错误率和热度综合判断，生成友好推荐理由
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ① 统计全站每道题的作答数据
        # 使用 Django ORM 聚合查询，统计每道题的作答记录
        from django.db.models import Count, Q

        stats = (
            PracticeRecord.objects
            .filter(is_answered=True)  # 只统计已作答的记录
            .values('question_id')
            .annotate(
                total_attempts=Count('id'),
                wrong_attempts=Count('id', filter=Q(is_correct=False)),
            )
        )

        # 转为 dict，key 为 question_id
        stats_dict = {s['question_id']: s for s in stats}

        # ② 过滤出 total_attempts >= 3 的题目
        filtered_stats = [s for s in stats_dict.values() if s['total_attempts'] >= 3]

        if not filtered_stats:
            # 数据不足，返回空列表
            return build_response(
                code=0,
                message="当前暂无高频错题推荐，请继续积累练习数据。",
                data={"count": 0, "results": []}
            )

        # ③ 计算归一化热度（基于当前结果集的最大 total_attempts）
        max_attempts = max(s['total_attempts'] for s in filtered_stats)
        for s in filtered_stats:
            s['wrong_rate'] = round(s['wrong_attempts'] / s['total_attempts'], 4)
            s['normalized_attempts'] = s['total_attempts'] / max_attempts if max_attempts > 0 else 0
            # 推荐分数 = 错误率 * 0.7 + 归一化热度 * 0.3
            s['score'] = round(s['wrong_rate'] * 0.7 + s['normalized_attempts'] * 0.3, 4)

        # ④ 按 score 降序排列，取前 10
        sorted_stats = sorted(filtered_stats, key=lambda x: x['score'], reverse=True)[:10]

        # ⑤ 获取当前用户对该10道题的作答记录（是否有做、是否做错）
        question_ids = [s['question_id'] for s in sorted_stats]
        user_records = PracticeRecord.objects.filter(
            user=request.user,
            question_id__in=question_ids,
            is_answered=True,
        ).values('question_id', 'is_correct')

        user_done_set = set(r['question_id'] for r in user_records)
        user_wrong_set = set(r['question_id'] for r in user_records if r['is_correct'] is False)

        # ⑥ 查询题目详情（预加载位置信息）
        questions = Question.objects.filter(
            id__in=question_ids,
            is_active=True,
        ).select_related('subchapter__chapter__course')

        question_map = {q.id: q for q in questions}

        # ⑦ 组装返回数据
        results = []
        for s in sorted_stats:
            q = question_map.get(s['question_id'])
            if not q:
                continue

            # 生成推荐理由
            reason = _generate_reason(s['wrong_rate'], s['total_attempts'])

            results.append({
                'question_id': q.id,
                'business_id': q.business_id,
                'question_type': q.question_type,
                'stem_text': q.stem_text or '',
                'stem_image': q.stem_image.url if q.stem_image else None,
                'option_a_text': q.option_a_text or '',
                'option_b_text': q.option_b_text or '',
                'option_c_text': q.option_c_text or '',
                'option_d_text': q.option_d_text or '',
                'option_a_image': q.option_a_image.url if q.option_a_image else None,
                'option_b_image': q.option_b_image.url if q.option_b_image else None,
                'option_c_image': q.option_c_image.url if q.option_c_image else None,
                'option_d_image': q.option_d_image.url if q.option_d_image else None,
                'correct_answer': q.correct_answer,
                'analysis_text': q.analysis_text or '',
                'analysis_image': q.analysis_image.url if q.analysis_image else None,
                'course_name': q.subchapter.chapter.course.name,
                'chapter_name': q.subchapter.chapter.name,
                'subchapter_name': q.subchapter.name,
                'total_attempts': s['total_attempts'],
                'wrong_attempts': s['wrong_attempts'],
                'wrong_rate': s['wrong_rate'],
                'score': s['score'],
                'user_has_done': s['question_id'] in user_done_set,
                'user_has_wrong': s['question_id'] in user_wrong_set,
                'reason': reason,
            })

        return build_response(
            code=0,
            message="获取高频错题推荐成功",
            data={
                "count": len(results),
                "results": results,
            }
        )


def _generate_reason(wrong_rate, total_attempts):
    """
    根据错误率和练习次数生成推荐理由。
    """
    rate_percent = int(wrong_rate * 100)
    if wrong_rate >= 0.7:
        return f"该题历史错误率高达 {rate_percent}%，属于高频易错题，建议重点练习。"
    elif wrong_rate >= 0.5:
        return f"该题历史错误率为 {rate_percent}%，错误率较高，建议加强练习。"
    elif wrong_rate >= 0.3:
        return f"该题历史错误率为 {rate_percent}%，结合练习次数 {total_attempts} 次，是值得关注的易错题。"
    else:
        return f"该题历史错误率为 {rate_percent}%，练习次数 {total_attempts} 次，是全站重点练习题。"
