"""
recommendation/models.py
=======================
错题复习推荐模型 — 基于艾宾浩斯遗忘曲线的错题复习计划。

复习间隔规则（简化版艾宾浩斯遗忘曲线）：
    第 1 次复习：做错后 1 天
    第 2 次复习：上次复习后 2 天
    第 3 次复习：上次复习后 4 天
    第 4 次复习：上次复习后 7 天
    第 5 次及以后：上次复习后 15 天

说明：
    - review_count 表示"正确复习次数"（即复习时答对的次数）
    - 每次复习答错时，review_count 重置为 0，重新从间隔 1 天开始
    - 当 review_count >= 5 时，视为该错题已掌握（is_mastered=True）
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class WrongQuestionReview(models.Model):
    """
    错题复习记录表。

    记录用户某道错题的复习计划：
    - 用户首次做错时创建记录
    - 每次复习后根据答题结果更新状态和下次复习时间
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wrong_question_reviews',
        verbose_name='用户'
    )
    question = models.ForeignKey(
        'question_bank.Question',
        on_delete=models.CASCADE,
        related_name='review_records',
        verbose_name='题目'
    )
    # 第一次做错时间
    first_wrong_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='第一次做错时间'
    )
    # 最近一次复习时间（可能为空，初始创建时未进行过复习）
    last_review_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='最近一次复习时间'
    )
    # 已正确复习次数（每次复习答对 +1，答错重置为 0）
    review_count = models.PositiveIntegerField(
        default=0,
        verbose_name='已正确复习次数'
    )
    # 下次应复习时间
    next_review_time = models.DateTimeField(
        verbose_name='下次复习时间'
    )
    # 是否已掌握（当 review_count >= 5 时自动置为 True）
    is_mastered = models.BooleanField(
        default=False,
        verbose_name='是否已掌握'
    )
    # 是否从错题本移除（软删除）
    is_removed = models.BooleanField(
        default=False,
        verbose_name='是否从复习计划移除'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wrong_question_reviews'
        verbose_name = '错题复习记录'
        verbose_name_plural = '错题复习记录'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'question'],
                name='unique_user_question_review'
            )
        ]
        ordering = ['next_review_time']

    def __str__(self):
        return f"{self.user.username} - 题目{self.question.business_id} - 复习{self.review_count}次"

    def calculate_next_review_time(self):
        """
        根据当前复习次数计算下一次复习的间隔时间。

        复习间隔规则（天）：
            review_count = 0 → 第1次复习间隔 1 天
            review_count = 1 → 第2次复习间隔 2 天
            review_count = 2 → 第3次复习间隔 4 天
            review_count = 3 → 第4次复习间隔 7 天
            review_count >= 4 → 第5次及以后复习间隔 15 天
        """
        intervals = {
            0: 1,   # 第1次复习
            1: 2,   # 第2次复习
            2: 4,   # 第3次复习
            3: 7,   # 第4次复习
        }
        days = intervals.get(self.review_count, 15)
        return timezone.now() + timedelta(days=days)

    def update_after_review(self, is_correct: bool):
        """
        用户完成一次复习后更新复习记录。

        Args:
            is_correct: 本次复习是否答对

        规则：
            答对 → review_count + 1，重新计算 next_review_time
                    若 review_count >= 5，is_mastered = True
            答错 → review_count = 0，next_review_time = 明天（1天后）
                    is_mastered = False
        """
        now = timezone.now()
        self.last_review_time = now

        if is_correct:
            self.review_count += 1
            if self.review_count >= 5:
                self.is_mastered = True
            self.next_review_time = self.calculate_next_review_time()
        else:
            # 答错：重置复习次数，从头开始
            self.review_count = 0
            self.is_mastered = False
            self.next_review_time = now + timedelta(days=1)

        self.save(update_fields=[
            'last_review_time', 'review_count',
            'next_review_time', 'is_mastered', 'updated_at'
        ])
