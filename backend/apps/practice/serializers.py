"""
practice/serializers.py
========================
练习相关序列化器。
"""
from rest_framework import serializers
from .models import PracticeSession, PracticeRecord
from apps.question_bank.models import Question, SubChapter


class PracticeSessionStartSerializer(serializers.Serializer):
    """开始练习请求序列化器"""
    subchapter_id = serializers.IntegerField(required=True)


class SubChapterBriefSerializer(serializers.ModelSerializer):
    """子章节简要信息序列化器"""
    class Meta:
        model = SubChapter
        fields = ["id", "name"]


class PracticeSessionSerializer(serializers.ModelSerializer):
    """练习会话序列化器"""
    subchapter = SubChapterBriefSerializer(read_only=True)
    accuracy = serializers.FloatField(read_only=True)

    class Meta:
        model = PracticeSession
        fields = [
            "id", "subchapter", "total_count",
            "answered_count", "correct_count",
            "accuracy", "status", "started_at", "finished_at"
        ]


class PracticeSessionDetailSerializer(serializers.ModelSerializer):
    """练习会话详情序列化器（含题目列表和固定进度）"""
    subchapter = SubChapterBriefSerializer(read_only=True)
    accuracy = serializers.FloatField(read_only=True)
    question_ids = serializers.SerializerMethodField()
    progress_map = serializers.SerializerMethodField()

    class Meta:
        model = PracticeSession
        fields = [
            "id", "subchapter", "total_count",
            "answered_count", "correct_count",
            "accuracy", "status", "started_at", "finished_at",
            "question_ids", "progress_map"
        ]

    def get_question_ids(self, obj):
        return obj.get_question_ids()

    def get_progress_map(self, obj):
        from .views import get_subchapter_progress_map
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return get_subchapter_progress_map(request.user, obj.subchapter)
        return {}


class PracticeQuestionSerializer(serializers.ModelSerializer):
    """练习题目序列化器（练习模式，不暴露正确答案）"""
    course_id = serializers.IntegerField(source="subchapter.chapter.course.id", read_only=True)
    course_name = serializers.CharField(source="subchapter.chapter.course.name", read_only=True)
    course_mindmap_url = serializers.SerializerMethodField()
    chapter_name = serializers.CharField(source="subchapter.chapter.name", read_only=True)
    subchapter_name = serializers.CharField(source="subchapter.name", read_only=True)
    stem_image = serializers.SerializerMethodField()
    option_a_image = serializers.SerializerMethodField()
    option_b_image = serializers.SerializerMethodField()
    option_c_image = serializers.SerializerMethodField()
    option_d_image = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            "id", "business_id", "question_type",
            "stem_text", "stem_image",
            "option_a_text", "option_a_image",
            "option_b_text", "option_b_image",
            "option_c_text", "option_c_image",
            "option_d_text", "option_d_image",
            "order_no",
            "course_id", "course_name", "course_mindmap_url",
            "chapter_name", "subchapter_name",
        ]

    def get_course_mindmap_url(self, obj):
        """获取课程思维导图 PDF URL"""
        from apps.question_bank.views import build_media_url
        request = self.context.get("request")
        course = obj.subchapter.chapter.course
        if course.mindmap_pdf and request:
            return build_media_url(request, course.mindmap_pdf.name)
        return None

    def get_stem_image(self, obj):
        from apps.question_bank.views import build_media_url
        request = self.context.get("request")
        if obj.stem_image and request:
            return build_media_url(request, obj.stem_image.name)
        return None

    def get_option_a_image(self, obj):
        from apps.question_bank.views import build_media_url
        request = self.context.get("request")
        if obj.option_a_image and request:
            return build_media_url(request, obj.option_a_image.name)
        return None

    def get_option_b_image(self, obj):
        from apps.question_bank.views import build_media_url
        request = self.context.get("request")
        if obj.option_b_image and request:
            return build_media_url(request, obj.option_b_image.name)
        return None

    def get_option_c_image(self, obj):
        from apps.question_bank.views import build_media_url
        request = self.context.get("request")
        if obj.option_c_image and request:
            return build_media_url(request, obj.option_c_image.name)
        return None

    def get_option_d_image(self, obj):
        from apps.question_bank.views import build_media_url
        request = self.context.get("request")
        if obj.option_d_image and request:
            return build_media_url(request, obj.option_d_image.name)
        return None


class SubmitAnswerSerializer(serializers.Serializer):
    """提交答案请求序列化器"""
    question_id = serializers.IntegerField(required=True)
    user_answer = serializers.CharField(max_length=1, required=False, allow_blank=True, allow_null=True)


class SubmitAnswerResponseSerializer(serializers.Serializer):
    """提交答案响应序列化器"""
    question_id = serializers.IntegerField()
    practice_status = serializers.CharField()
    user_answer = serializers.CharField(allow_blank=True, allow_null=True)
    is_correct = serializers.BooleanField(allow_null=True)
    correct_answer = serializers.CharField(allow_blank=True, allow_null=True)
    course_mindmap_url = serializers.CharField(allow_null=True, allow_blank=True)
    course_name = serializers.CharField(allow_null=True, allow_blank=True)
    is_locked = serializers.BooleanField()


class PracticeRecordSerializer(serializers.ModelSerializer):
    """练习记录序列化器"""
    question_id = serializers.IntegerField(source="question.id", read_only=True)
    business_id = serializers.CharField(source="question.business_id", read_only=True)
    question_type = serializers.CharField(source="question.question_type", read_only=True)
    stem_text = serializers.CharField(source="question.stem_text", read_only=True)

    class Meta:
        model = PracticeRecord
        fields = [
            "id", "question_id", "business_id", "question_type",
            "stem_text", "user_answer", "is_correct",
            "is_answered", "answer_mode", "answered_at"
        ]
