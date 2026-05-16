from rest_framework import serializers
from .models import WrongQuestion, FavoriteQuestion
from apps.question_bank.models import Question


class QuestionBaseSerializer(serializers.ModelSerializer):
    """题目基础序列化器，输出业务编号"""
    class Meta:
        model = Question
        fields = ['id', 'business_id', 'question_type', 'stem_text', 'stem_image']


class WrongQuestionListSerializer(serializers.ModelSerializer):
    """错题本列表序列化器"""
    question_id = serializers.IntegerField(source='question.id', read_only=True)
    business_id = serializers.CharField(source='question.business_id', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    stem_text = serializers.CharField(source='question.stem_text', read_only=True)
    stem_image = serializers.SerializerMethodField()
    course_name = serializers.CharField(
        source='question.subchapter.chapter.course.name', read_only=True
    )
    chapter_name = serializers.CharField(
        source='question.subchapter.chapter.name', read_only=True
    )
    subchapter_name = serializers.CharField(
        source='question.subchapter.name', read_only=True
    )
    subchapter_id = serializers.IntegerField(
        source='question.subchapter.id', read_only=True
    )

    class Meta:
        model = WrongQuestion
        fields = [
            'id',
            'question_id',
            'business_id',
            'question_type',
            'stem_text',
            'stem_image',
            'wrong_count',
            'last_wrong_at',
            'course_name',
            'chapter_name',
            'subchapter_name',
            'subchapter_id',
        ]

    def get_stem_image(self, obj):
        if obj.question.stem_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.question.stem_image.url)
            return obj.question.stem_image.url
        return None


class WrongQuestionDetailSerializer(serializers.ModelSerializer):
    """错题详情序列化器，完整输出题目信息"""
    question_id = serializers.IntegerField(source='question.id', read_only=True)
    business_id = serializers.CharField(source='question.business_id', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    stem_text = serializers.CharField(source='question.stem_text', read_only=True)
    stem_image = serializers.SerializerMethodField()
    option_a_text = serializers.CharField(source='question.option_a_text', read_only=True)
    option_a_image = serializers.SerializerMethodField()
    option_b_text = serializers.CharField(source='question.option_b_text', read_only=True)
    option_b_image = serializers.SerializerMethodField()
    option_c_text = serializers.CharField(source='question.option_c_text', read_only=True)
    option_c_image = serializers.SerializerMethodField()
    option_d_text = serializers.CharField(source='question.option_d_text', read_only=True)
    option_d_image = serializers.SerializerMethodField()
    correct_answer = serializers.CharField(source='question.correct_answer', read_only=True)
    analysis_text = serializers.CharField(source='question.analysis_text', read_only=True)
    analysis_image = serializers.SerializerMethodField()
    course_name = serializers.CharField(
        source='question.subchapter.chapter.course.name', read_only=True
    )
    chapter_name = serializers.CharField(
        source='question.subchapter.chapter.name', read_only=True
    )
    subchapter_name = serializers.CharField(
        source='question.subchapter.name', read_only=True
    )
    subchapter_id = serializers.IntegerField(
        source='question.subchapter.id', read_only=True
    )

    class Meta:
        model = WrongQuestion
        fields = [
            'id',
            'question_id',
            'business_id',
            'question_type',
            'stem_text',
            'stem_image',
            'option_a_text',
            'option_a_image',
            'option_b_text',
            'option_b_image',
            'option_c_text',
            'option_c_image',
            'option_d_text',
            'option_d_image',
            'correct_answer',
            'analysis_text',
            'analysis_image',
            'wrong_count',
            'last_wrong_at',
            'course_name',
            'chapter_name',
            'subchapter_name',
            'subchapter_id',
        ]

    def _build_image_url(self, image_field):
        if image_field:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(image_field.url)
            return image_field.url
        return None

    def get_stem_image(self, obj):
        return self._build_image_url(obj.question.stem_image)

    def get_option_a_image(self, obj):
        return self._build_image_url(obj.question.option_a_image)

    def get_option_b_image(self, obj):
        return self._build_image_url(obj.question.option_b_image)

    def get_option_c_image(self, obj):
        return self._build_image_url(obj.question.option_c_image)

    def get_option_d_image(self, obj):
        return self._build_image_url(obj.question.option_d_image)

    def get_analysis_image(self, obj):
        return self._build_image_url(obj.question.analysis_image)


class FavoriteQuestionListSerializer(serializers.ModelSerializer):
    """收藏夹列表序列化器"""
    question_id = serializers.IntegerField(source='question.id', read_only=True)
    business_id = serializers.CharField(source='question.business_id', read_only=True)
    question_type = serializers.CharField(source='question.question_type', read_only=True)
    stem_text = serializers.CharField(source='question.stem_text', read_only=True)
    stem_image = serializers.SerializerMethodField()
    course_name = serializers.CharField(
        source='question.subchapter.chapter.course.name', read_only=True
    )
    chapter_name = serializers.CharField(
        source='question.subchapter.chapter.name', read_only=True
    )
    subchapter_name = serializers.CharField(
        source='question.subchapter.name', read_only=True
    )
    subchapter_id = serializers.IntegerField(
        source='question.subchapter.id', read_only=True
    )

    class Meta:
        model = FavoriteQuestion
        fields = [
            'id',
            'question_id',
            'business_id',
            'question_type',
            'stem_text',
            'stem_image',
            'created_at',
            'course_name',
            'chapter_name',
            'subchapter_name',
            'subchapter_id',
        ]

    def get_stem_image(self, obj):
        if obj.question.stem_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.question.stem_image.url)
            return obj.question.stem_image.url
        return None


class FavoriteQuestionCreateSerializer(serializers.Serializer):
    """添加收藏请求序列化器"""
    question_id = serializers.IntegerField()

    def validate_question_id(self, value):
        if not Question.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("题目不存在或已下架")
        return value


class FavoriteStatusSerializer(serializers.Serializer):
    """收藏状态查询序列化器"""
    question_id = serializers.IntegerField()

    def validate_question_id(self, value):
        if not Question.objects.filter(id=value).exists():
            raise serializers.ValidationError("题目不存在")
        return value


# ========== 学习统计序列化器 ==========

class OverviewStatsSerializer(serializers.Serializer):
    """学习中心总览统计序列化器"""
    total_sessions = serializers.IntegerField()
    total_answered_questions = serializers.IntegerField()
    total_correct_questions = serializers.IntegerField()
    overall_accuracy = serializers.FloatField()
    wrong_question_count = serializers.IntegerField()
    favorite_count = serializers.IntegerField()


class CourseStatsSerializer(serializers.Serializer):
    """课程维度统计序列化器"""
    course_id = serializers.IntegerField()
    course_name = serializers.CharField()
    answered_count = serializers.IntegerField()
    correct_count = serializers.IntegerField()
    accuracy = serializers.FloatField()


class ChapterStatsSerializer(serializers.Serializer):
    """章节维度统计序列化器"""
    chapter_id = serializers.IntegerField()
    chapter_name = serializers.CharField()
    answered_count = serializers.IntegerField()
    correct_count = serializers.IntegerField()
    accuracy = serializers.FloatField()


class RecentSessionSerializer(serializers.Serializer):
    """最近练习会话序列化器"""
    session_id = serializers.IntegerField()
    subchapter_name = serializers.CharField()
    total_count = serializers.IntegerField()
    answered_count = serializers.IntegerField()
    correct_count = serializers.IntegerField()
    accuracy = serializers.FloatField(allow_null=True)
    started_at = serializers.DateTimeField()
    finished_at = serializers.DateTimeField(allow_null=True)
    status = serializers.CharField()


class RecentWrongQuestionSerializer(serializers.Serializer):
    """最近错题序列化器"""
    wrong_question_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    business_id = serializers.CharField()
    question_type = serializers.CharField()
    stem_text = serializers.CharField(allow_null=True)
    wrong_count = serializers.IntegerField()
    last_wrong_at = serializers.DateTimeField()


class RecentFavoriteSerializer(serializers.Serializer):
    """最近收藏序列化器"""
    favorite_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    business_id = serializers.CharField()
    question_type = serializers.CharField()
    stem_text = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()

