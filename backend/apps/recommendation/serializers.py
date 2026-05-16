"""
recommendation/serializers.py
=============================
错题复习推荐的序列化器。
"""
from rest_framework import serializers
from django.conf import settings
from .models import WrongQuestionReview


class ReviewRecordSerializer(serializers.ModelSerializer):
    """复习记录的序列化器（完整信息）"""
    question_id = serializers.IntegerField(source='question.id', read_only=True)
    business_id = serializers.CharField(source='question.business_id', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    stem_text = serializers.CharField(source='question.stem_text', read_only=True)
    stem_image = serializers.ImageField(source='question.stem_image', read_only=True)
    option_a_text = serializers.CharField(source='question.option_a_text', read_only=True)
    option_b_text = serializers.CharField(source='question.option_b_text', read_only=True)
    option_c_text = serializers.CharField(source='question.option_c_text', read_only=True)
    option_d_text = serializers.CharField(source='question.option_d_text', read_only=True)
    option_a_image = serializers.ImageField(source='question.option_a_image', read_only=True)
    option_b_image = serializers.ImageField(source='question.option_b_image', read_only=True)
    option_c_image = serializers.ImageField(source='question.option_c_image', read_only=True)
    option_d_image = serializers.ImageField(source='question.option_d_image', read_only=True)
    correct_answer = serializers.CharField(source='question.correct_answer', read_only=True)
    analysis_text = serializers.CharField(source='question.analysis_text', read_only=True)
    analysis_image = serializers.ImageField(source='question.analysis_image', read_only=True)
    course_name = serializers.CharField(source='question.subchapter.chapter.course.name', read_only=True)
    chapter_name = serializers.CharField(source='question.subchapter.chapter.name', read_only=True)
    subchapter_name = serializers.CharField(source='question.subchapter.name', read_only=True)

    class Meta:
        model = WrongQuestionReview
        fields = [
            'id',
            'question_id',
            'business_id',
            'question_type',
            'stem_text',
            'stem_image',
            'option_a_text',
            'option_b_text',
            'option_c_text',
            'option_d_text',
            'option_a_image',
            'option_b_image',
            'option_c_image',
            'option_d_image',
            'correct_answer',
            'analysis_text',
            'analysis_image',
            'course_name',
            'chapter_name',
            'subchapter_name',
            'first_wrong_time',
            'last_review_time',
            'review_count',
            'next_review_time',
            'is_mastered',
        ]


class ReviewRecordListSerializer(serializers.ModelSerializer):
    """复习记录列表序列化器（精简信息，用于列表展示）"""
    question_id = serializers.IntegerField(source='question.id', read_only=True)
    business_id = serializers.CharField(source='question.business_id', read_only=True)
    stem_text = serializers.CharField(source='question.stem_text', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    course_name = serializers.CharField(source='question.subchapter.chapter.course.name', read_only=True)
    chapter_name = serializers.CharField(source='question.subchapter.chapter.name', read_only=True)
    subchapter_name = serializers.CharField(source='question.subchapter.name', read_only=True)

    class Meta:
        model = WrongQuestionReview
        fields = [
            'id',
            'question_id',
            'business_id',
            'stem_text',
            'question_type',
            'course_name',
            'chapter_name',
            'subchapter_name',
            'review_count',
            'next_review_time',
            'is_mastered',
            'first_wrong_time',
        ]


class ReviewResultSerializer(serializers.Serializer):
    """
    提交复习结果的请求序列化器。
    """
    is_correct = serializers.BooleanField(
        required=True,
        help_text='本次复习是否答对'
    )


class ReviewResultResponseSerializer(serializers.Serializer):
    """
    提交复习结果后的响应序列化器。
    """
    message = serializers.CharField()
    review_count = serializers.IntegerField()
    next_review_time = serializers.DateTimeField()
    is_mastered = serializers.BooleanField()


# =============================================================================
# 高频错题推荐序列化器
# =============================================================================

class HighWrongRateQuestionSerializer(serializers.Serializer):
    """
    高频错题推荐结果序列化器。

    包含题目基本信息 + 全站统计信息 + 当前用户个人标记。
    """
    # 题目基本信息
    question_id = serializers.IntegerField(read_only=True)
    business_id = serializers.CharField(read_only=True)
    question_type = serializers.CharField(read_only=True)
    stem_text = serializers.CharField(read_only=True)
    stem_image = serializers.ImageField(read_only=True, required=False)
    option_a_text = serializers.CharField(read_only=True, required=False)
    option_b_text = serializers.CharField(read_only=True, required=False)
    option_c_text = serializers.CharField(read_only=True, required=False)
    option_d_text = serializers.CharField(read_only=True, required=False)
    option_a_image = serializers.ImageField(read_only=True, required=False)
    option_b_image = serializers.ImageField(read_only=True, required=False)
    option_c_image = serializers.ImageField(read_only=True, required=False)
    option_d_image = serializers.ImageField(read_only=True, required=False)
    correct_answer = serializers.CharField(read_only=True)
    analysis_text = serializers.CharField(read_only=True, required=False)
    analysis_image = serializers.ImageField(read_only=True, required=False)

    # 位置信息
    course_name = serializers.CharField(read_only=True)
    chapter_name = serializers.CharField(read_only=True)
    subchapter_name = serializers.CharField(read_only=True)

    # 全站统计信息
    total_attempts = serializers.IntegerField(read_only=True)
    wrong_attempts = serializers.IntegerField(read_only=True)
    wrong_rate = serializers.FloatField(read_only=True)
    score = serializers.FloatField(read_only=True)

    # 当前用户标记
    user_has_done = serializers.BooleanField(read_only=True)
    user_has_wrong = serializers.BooleanField(read_only=True)

    # 推荐理由
    reason = serializers.CharField(read_only=True)
