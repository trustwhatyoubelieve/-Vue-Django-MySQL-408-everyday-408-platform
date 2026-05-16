"""
practice/models.py
===================
在线练习数据模型。
"""
from django.db import models
from django.contrib.auth import get_user_model
from apps.question_bank.models import SubChapter, Question, QuestionType

User = get_user_model()


class SessionStatus(models.TextChoices):
    """练习会话状态枚举"""
    IN_PROGRESS = "in_progress", "进行中"
    FINISHED = "finished", "已完成"


class AnswerMode(models.TextChoices):
    """作答方式枚举（保留扩展性）"""
    SINGLE_CHOICE = "single_choice", "单选题作答"
    BIG_QUESTION_VIEWED = "big_question_viewed", "大题已查看"


class ProgressStatus(models.TextChoices):
    """子章节刷题进度状态枚举"""
    UNATTEMPTED = "unattempted", "未作答"
    CORRECT = "correct", "正确"
    WRONG = "wrong", "错误"


class SubchapterPracticeProgress(models.Model):
    """
    子章节刷题进度模型（固定进度表）

    以「用户 + 子章节 + 题目」为粒度，长期保存每道题目的首次作答结果。
    用于：
    - 右侧题号颜色显示（绿 / 红 / 灰）
    - 判断哪些题还能继续做（仅灰色题可提交）
    - 支持用户中断后下次继续练习
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="practice_progresses",
        verbose_name="用户"
    )
    subchapter = models.ForeignKey(
        SubChapter,
        on_delete=models.CASCADE,
        related_name="practice_progresses",
        verbose_name="所属子章节"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="practice_progresses",
        verbose_name="题目"
    )
    status = models.CharField(
        max_length=20,
        choices=ProgressStatus.choices,
        default=ProgressStatus.UNATTEMPTED,
        verbose_name="状态"
    )
    first_answer = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="首次答案"
    )
    is_locked = models.BooleanField(
        default=False,
        verbose_name="是否锁定（锁定后不允许再覆盖）"
    )
    first_answered_at = models.DateTimeField(null=True, blank=True, verbose_name="首次作答时间")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subchapter_practice_progress"
        verbose_name = "子章节刷题进度"
        verbose_name_plural = "子章节刷题进度"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subchapter", "question"],
                name="unique_user_subchapter_question_progress"
            ),
        ]
        indexes = [
            models.Index(fields=["user", "subchapter"]),
            models.Index(fields=["user", "subchapter", "status"]),
        ]

    def __str__(self):
        return f"{self.user.username} / {self.subchapter.name} / Q{self.question.id} -> {self.status}"


class PracticeSession(models.Model):
    """
    练习会话模型
    表示用户针对某个子章节开始的一次练习会话。
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="practice_sessions",
        verbose_name="用户"
    )
    subchapter = models.ForeignKey(
        SubChapter,
        on_delete=models.CASCADE,
        related_name="practice_sessions",
        verbose_name="所属子章节"
    )
    total_count = models.PositiveIntegerField(default=0, verbose_name="题目总数")
    answered_count = models.PositiveIntegerField(default=0, verbose_name="已答数量")
    correct_count = models.PositiveIntegerField(default=0, verbose_name="正确数量")
    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.IN_PROGRESS,
        verbose_name="会话状态"
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="开始时间")
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name="完成时间")

    class Meta:
        db_table = "practice_session"
        verbose_name = "练习会话"
        verbose_name_plural = "练习会话"
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "subchapter"]),
        ]

    def __str__(self):
        return f"练习会话 {self.id} - {self.user.username} / {self.subchapter.name}"

    @property
    def accuracy(self):
        """正确率，已答数量为0时返回None"""
        if self.answered_count == 0:
            return None
        return round(self.correct_count / self.answered_count, 4)

    def get_question_ids(self):
        """获取该会话对应的子章节下所有启用题目的ID列表（按顺序）"""
        return list(
            self.subchapter.questions.filter(is_active=True)
            .order_by("order_no", "id")
            .values_list("id", flat=True)
        )

    def update_statistics(self):
        """根据关联的作答记录重新计算会话统计"""
        records = self.records.filter(is_answered=True)
        self.answered_count = records.count()
        self.correct_count = records.filter(is_correct=True).count()
        self.save(update_fields=["answered_count", "correct_count"])


class PracticeRecord(models.Model):
    """
    练习记录模型
    表示某次练习会话中用户对某道题的作答记录。
    """
    session = models.ForeignKey(
        PracticeSession,
        on_delete=models.CASCADE,
        related_name="records",
        verbose_name="所属练习会话"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="practice_records",
        verbose_name="用户"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="practice_records",
        verbose_name="题目"
    )
    user_answer = models.CharField(
        max_length=1,
        blank=True,
        null=True,
        verbose_name="用户答案"
    )
    is_correct = models.BooleanField(
        blank=True,
        null=True,
        verbose_name="是否正确"
    )
    is_answered = models.BooleanField(default=False, verbose_name="是否已作答")
    answer_mode = models.CharField(
        max_length=30,
        choices=AnswerMode.choices,
        default=AnswerMode.SINGLE_CHOICE,
        verbose_name="作答方式"
    )
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="作答时间")

    class Meta:
        db_table = "practice_record"
        verbose_name = "练习记录"
        verbose_name_plural = "练习记录"
        ordering = ["session", "question__order_no"]
        indexes = [
            models.Index(fields=["user", "question"]),
            models.Index(fields=["session", "question"]),
        ]
        constraints = [
            # 同一会话内同一道题只允许一条记录
            models.UniqueConstraint(
                fields=["session", "question"],
                name="unique_session_question_record"
            ),
        ]

    def __str__(self):
        status = "正确" if self.is_correct else ("错误" if self.is_answered else "未答")
        return f"{self.user.username} - {self.question.business_id} - {status}"
