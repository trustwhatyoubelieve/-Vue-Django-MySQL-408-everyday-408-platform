"""
question_bank/serializers.py
============================
题库浏览 API 序列化器。
"""
from rest_framework import serializers

from .models import Course, Chapter, SubChapter, Question


class CourseListSerializer(serializers.ModelSerializer):
    """课程列表序列化器"""
    chapter_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "order_no", "chapter_count"]


class ChapterListSerializer(serializers.ModelSerializer):
    """章节列表序列化器"""
    course_id = serializers.IntegerField(source="course_id", read_only=True)
    subchapter_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chapter
        fields = ["id", "name", "order_no", "course_id", "subchapter_count"]


class SubChapterListSerializer(serializers.ModelSerializer):
    """子章节列表序列化器"""
    chapter_id = serializers.IntegerField(source="chapter_id", read_only=True)
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = SubChapter
        fields = ["id", "name", "order_no", "chapter_id", "question_count"]


class QuestionListSerializer(serializers.ModelSerializer):
    """题目列表序列化器（浏览用）"""
    business_id = serializers.CharField(read_only=True)
    subchapter_id = serializers.IntegerField(source="subchapter_id", read_only=True)
    stem_preview = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id", "business_id", "subchapter_id", "order_no",
            "question_type", "stem_preview", "stem_image"
        ]

    def get_stem_preview(self, obj):
        text = obj.stem_text or ""
        return text[:80] + "…" if len(text) > 80 else text


class QuestionDetailSerializer(serializers.ModelSerializer):
    """题目详情序列化器（完整内容）"""
    business_id = serializers.CharField(read_only=True)
    subchapter_id = serializers.IntegerField(source="subchapter_id", read_only=True)

    # 所属层级信息（用于显示路径）
    course_name = serializers.CharField(source="course.name", read_only=True)
    chapter_name = serializers.CharField(source="chapter.name", read_only=True)
    subchapter_name = serializers.CharField(source="subchapter.name", read_only=True)

    class Meta:
        model = Question
        fields = [
            "id", "business_id", "subchapter_id", "order_no",
            "question_type",
            "stem_text", "stem_image",
            "option_a_text", "option_a_image",
            "option_b_text", "option_b_image",
            "option_c_text", "option_c_image",
            "option_d_text", "option_d_image",
            "correct_answer",
            "analysis_text", "analysis_image",
            "course_name", "chapter_name", "subchapter_name",
        ]
