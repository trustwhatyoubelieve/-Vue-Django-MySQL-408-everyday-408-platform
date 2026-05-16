from django.db import models
from django.conf import settings
from apps.question_bank.models import Question


class WrongQuestion(models.Model):
    """
    错题本：记录用户做错的题目。
    同一用户对同一题只有一条记录。
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wrong_questions'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='wrong_records'
    )
    wrong_count = models.PositiveIntegerField(
        default=1,
        verbose_name="累计错误次数"
    )
    last_wrong_at = models.DateTimeField(
        auto_now=True,
        verbose_name="最近一次答错时间"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="是否保留在错题本中"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'wrong_questions'
        verbose_name = '错题记录'
        verbose_name_plural = '错题记录'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'question'],
                name='unique_user_wrong_question'
            )
        ]
        ordering = ['-last_wrong_at']

    def __str__(self):
        return f"{self.user.username} - {self.question.business_id}"


class FavoriteQuestion(models.Model):
    """
    收藏夹：用户收藏的题目。
    同一用户对同一题只能收藏一次。
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_questions'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='favorite_records'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite_questions'
        verbose_name = '收藏记录'
        verbose_name_plural = '收藏记录'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'question'],
                name='unique_user_favorite_question'
            )
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.question.business_id}"
