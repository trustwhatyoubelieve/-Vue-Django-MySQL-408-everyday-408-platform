from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.db.models import F

from .utils import generate_question_display, generate_business_id
from .services import (
    get_next_order_no,
    insert_order_at,
    close_order_gap,
    reorder_in_scope,
)


def course_mindmap_upload_to(instance, filename):
    """课程思维导图 PDF 上传路径"""
    import os
    ext = os.path.splitext(filename)[1].lower()
    import uuid
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return f"course_mindmaps/{instance.id}/{unique_name}"


class Course(models.Model):
    """
    课程模型
    例如：数据结构、操作系统、计算机网络、组成原理
    """
    order_no = models.PositiveIntegerField(default=0, verbose_name="顺序号", unique=True)
    name = models.CharField(max_length=100, verbose_name="课程名称")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    mindmap_pdf = models.FileField(
        upload_to=course_mindmap_upload_to,
        blank=True,
        null=True,
        verbose_name="思维导图 PDF",
        help_text="上传该课程的思维导图 PDF 文件"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "question_bank_course"
        verbose_name = "课程"
        verbose_name_plural = "课程"
        ordering = ["order_no", "id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            # 新增：自动分配 order_no
            with transaction.atomic():
                if self.order_no:
                    # 手动指定位置：检查是否冲突
                    conflict = Course.objects.filter(order_no=self.order_no).first()
                    if conflict:
                        insert_order_at(Course, {}, self.order_no)
                else:
                    # 未指定：追加到末尾
                    self.order_no = get_next_order_no(Course, {})
                super().save(*args, **kwargs)
        else:
            # 更新：检测 order_no 是否变化
            try:
                old = Course.objects.get(id=self.id)
                old_order = old.order_no
                if old_order != self.order_no:
                    with transaction.atomic():
                        reorder_in_scope(Course, {}, self.id, old_order, self.order_no)
                        # 级联更新该课程下所有题目的 business_id
                        update_business_ids_for_course(self)
            except Course.DoesNotExist:
                pass
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        deleted_order = self.order_no
        super().delete(*args, **kwargs)
        close_order_gap(Course, {}, deleted_order)


class Chapter(models.Model):
    """
    章节模型
    属于某个课程下的章节
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="chapters",
        verbose_name="所属课程"
    )
    order_no = models.PositiveIntegerField(default=0, verbose_name="顺序号")
    name = models.CharField(max_length=100, verbose_name="章节名称")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "question_bank_chapter"
        verbose_name = "章节"
        verbose_name_plural = "章节"
        ordering = ["order_no", "id"]
        constraints = [
            models.UniqueConstraint(fields=["course", "order_no"], name="unique_course_order_no"),
            models.UniqueConstraint(fields=["course", "name"], name="unique_course_chapter"),
        ]

    def __str__(self):
        return f"{self.course.name} / {self.name}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        # 构建 scope_filter：章节的 scope 是其所属课程
        scope_filter = {"course": self.course}

        if is_new:
            # 新增
            with transaction.atomic():
                if self.order_no:
                    # 手动指定位置：检查是否冲突
                    conflict = Chapter.objects.filter(**scope_filter, order_no=self.order_no).first()
                    if conflict:
                        insert_order_at(Chapter, scope_filter, self.order_no)
                else:
                    # 未指定：追加到末尾
                    self.order_no = get_next_order_no(Chapter, scope_filter)
                super().save(*args, **kwargs)
                # 级联更新该课程下所有题目的 business_id
                update_business_ids_for_course(self.course)
        else:
            # 更新：检测 course 是否变化，或 order_no 是否变化
            try:
                old = Chapter.objects.get(id=self.id)
                old_course = old.course
                old_order = old.order_no
                course_changed = (old_course.id != self.course.id)
                order_changed = (old_order != self.order_no)

                if course_changed or order_changed:
                    with transaction.atomic():
                        if course_changed:
                            # 跨课程移动：旧课程补位
                            close_order_gap(Chapter, {"course": old_course}, old_order)
                            # 新课程中插入（可能冲突）
                            if self.order_no:
                                conflict = Chapter.objects.filter(**scope_filter, order_no=self.order_no).first()
                                if conflict:
                                    insert_order_at(Chapter, scope_filter, self.order_no)
                            else:
                                self.order_no = get_next_order_no(Chapter, scope_filter)
                        else:
                            # 同课程内移动
                            reorder_in_scope(Chapter, scope_filter, self.id, old_order, self.order_no)
                        super().save(*args, **kwargs)
                        # 级联更新：两个课程都需要更新
                        update_business_ids_for_course(self.course)
                        if course_changed:
                            update_business_ids_for_course(old_course)
                else:
                    super().save(*args, **kwargs)
            except Chapter.DoesNotExist:
                pass

    def delete(self, *args, **kwargs):
        deleted_order = self.order_no
        course = self.course
        super().delete(*args, **kwargs)
        close_order_gap(Chapter, {"course": course}, deleted_order)


class SubChapter(models.Model):
    """
    子章节模型
    属于某个章节下的子章节
    """
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="subchapters",
        verbose_name="所属章节"
    )
    order_no = models.PositiveIntegerField(default=0, verbose_name="顺序号")
    name = models.CharField(max_length=100, verbose_name="子章节名称")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "question_bank_subchapter"
        verbose_name = "子章节"
        verbose_name_plural = "子章节"
        ordering = ["order_no", "id"]
        constraints = [
            models.UniqueConstraint(fields=["chapter", "order_no"], name="unique_chapter_order_no"),
            models.UniqueConstraint(fields=["chapter", "name"], name="unique_chapter_subchapter"),
        ]

    def __str__(self):
        return f"{self.chapter.course.name} / {self.chapter.name} / {self.name}"

    @property
    def course(self):
        return self.chapter.course

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        scope_filter = {"chapter": self.chapter}

        if is_new:
            # 新增
            with transaction.atomic():
                if self.order_no:
                    # 手动指定位置：检查是否冲突
                    conflict = SubChapter.objects.filter(**scope_filter, order_no=self.order_no).first()
                    if conflict:
                        insert_order_at(SubChapter, scope_filter, self.order_no)
                else:
                    # 未指定：追加到末尾
                    self.order_no = get_next_order_no(SubChapter, scope_filter)
                super().save(*args, **kwargs)
                # 级联更新该章节下所有题目的 business_id
                update_business_ids_for_chapter(self.chapter)
        else:
            # 更新：检测 chapter 是否变化，或 order_no 是否变化
            try:
                old = SubChapter.objects.get(id=self.id)
                old_chapter = old.chapter
                old_order = old.order_no
                chapter_changed = (old_chapter.id != self.chapter.id)
                order_changed = (old_order != self.order_no)

                if chapter_changed or order_changed:
                    with transaction.atomic():
                        if chapter_changed:
                            # 跨章节移动：旧章节补位
                            close_order_gap(SubChapter, {"chapter": old_chapter}, old_order)
                            # 新章节中插入（可能冲突）
                            if self.order_no:
                                conflict = SubChapter.objects.filter(**scope_filter, order_no=self.order_no).first()
                                if conflict:
                                    insert_order_at(SubChapter, scope_filter, self.order_no)
                            else:
                                self.order_no = get_next_order_no(SubChapter, scope_filter)
                        else:
                            # 同章节内���动
                            reorder_in_scope(SubChapter, scope_filter, self.id, old_order, self.order_no)
                        super().save(*args, **kwargs)
                        # 级联更新：两个章节都需要更新
                        update_business_ids_for_chapter(self.chapter)
                        if chapter_changed:
                            update_business_ids_for_chapter(old_chapter)
                else:
                    super().save(*args, **kwargs)
            except SubChapter.DoesNotExist:
                pass

    def delete(self, *args, **kwargs):
        deleted_order = self.order_no
        chapter = self.chapter
        super().delete(*args, **kwargs)
        close_order_gap(SubChapter, {"chapter": chapter}, deleted_order)


def _get_file_extension(filename):
    """获取文件扩展名"""
    import os
    return os.path.splitext(filename)[1].lower()


def question_stem_upload_to(instance, filename):
    """题干图片上传路径"""
    ext = _get_file_extension(filename)
    import uuid
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return f"questions/stem/{unique_name}"


def question_option_upload_to(instance, filename):
    """选项图片上传路径"""
    ext = _get_file_extension(filename)
    import uuid
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return f"questions/options/{unique_name}"


def question_analysis_upload_to(instance, filename):
    """解析图片上传路径"""
    ext = _get_file_extension(filename)
    import uuid
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return f"questions/analysis/{unique_name}"


class QuestionType(models.TextChoices):
    """题目类型枚举"""
    SINGLE_CHOICE = "single_choice", "单选题"
    BIG_QUESTION = "big_question", "大题"


class CorrectAnswer(models.TextChoices):
    """单选题正确答案枚举"""
    A = "A", "A"
    B = "B", "B"
    C = "C", "C"
    D = "D", "D"


def has_content(text, image):
    """
    判断是否有有效内容（排除纯空格和空值）
    """
    if text and text.strip():
        return True
    if image:
        return True
    return False


class Question(models.Model):
    """
    题目模型
    支持单选题和大题两种类型
    """
    subchapter = models.ForeignKey(
        SubChapter,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="所属子章节"
    )
    order_no = models.PositiveIntegerField(default=0, verbose_name="顺序号")

    # 业务编号：10位固定编号 CC HH SS QQQQ（持久化存储）
    business_id = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="业务编号",
        help_text="10位固定编号：课程(2)+章节(2)+子章节(2)+题目(4)"
    )

    question_type = models.CharField(
        max_length=20,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE_CHOICE,
        verbose_name="题目类型"
    )

    stem_text = models.TextField(blank=True, null=True, verbose_name="题干文本")
    stem_image = models.ImageField(
        upload_to=question_stem_upload_to,
        blank=True,
        null=True,
        verbose_name="题干图片"
    )

    option_a_text = models.TextField(blank=True, null=True, verbose_name="选项A文本")
    option_a_image = models.ImageField(
        upload_to=question_option_upload_to,
        blank=True,
        null=True,
        verbose_name="选项A图片"
    )
    option_b_text = models.TextField(blank=True, null=True, verbose_name="选项B文本")
    option_b_image = models.ImageField(
        upload_to=question_option_upload_to,
        blank=True,
        null=True,
        verbose_name="选项B图片"
    )
    option_c_text = models.TextField(blank=True, null=True, verbose_name="选项C文本")
    option_c_image = models.ImageField(
        upload_to=question_option_upload_to,
        blank=True,
        null=True,
        verbose_name="选项C图片"
    )
    option_d_text = models.TextField(blank=True, null=True, verbose_name="选项D文本")
    option_d_image = models.ImageField(
        upload_to=question_option_upload_to,
        blank=True,
        null=True,
        verbose_name="选项D图片"
    )

    correct_answer = models.CharField(
        max_length=1,
        choices=CorrectAnswer.choices,
        blank=True,
        null=True,
        verbose_name="正确答案"
    )

    analysis_text = models.TextField(blank=True, null=True, verbose_name="解析文本")
    analysis_image = models.ImageField(
        upload_to=question_analysis_upload_to,
        blank=True,
        null=True,
        verbose_name="解析图片"
    )

    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "question_bank_question"
        verbose_name = "题目"
        verbose_name_plural = "题目"
        ordering = ["subchapter", "order_no", "id"]
        constraints = [
            models.UniqueConstraint(fields=["subchapter", "order_no"], name="unique_subchapter_order_no"),
        ]

    def __str__(self):
        return f"[{self.business_id}] {self.subchapter} / {(self.stem_text or '')[:20]}"

    @property
    def chapter(self):
        """获取所属章节"""
        return self.subchapter.chapter

    @property
    def course(self):
        """获取所属课程"""
        return self.subchapter.chapter.course

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        scope_filter = {"subchapter": self.subchapter}

        if is_new:
            # 新增
            with transaction.atomic():
                if self.order_no:
                    # 手动指定位置：检查是否冲突
                    conflict = Question.objects.filter(**scope_filter, order_no=self.order_no).first()
                    if conflict:
                        insert_order_at(Question, scope_filter, self.order_no)
                else:
                    # 未指定：追加到末尾
                    self.order_no = get_next_order_no(Question, scope_filter)
                # 计算 business_id
                self.business_id = generate_business_id(
                    self.subchapter.chapter.course.order_no,
                    self.subchapter.chapter.order_no,
                    self.subchapter.order_no,
                    self.order_no
                )
                super().save(*args, **kwargs)
        else:
            # 更新：检测 subchapter 是否变化，或 order_no 是否变化
            try:
                old = Question.objects.get(id=self.id)
                old_subchapter = old.subchapter
                old_order = old.order_no
                subchapter_changed = (old_subchapter.id != self.subchapter.id)
                order_changed = (old_order != self.order_no)

                if subchapter_changed or order_changed:
                    with transaction.atomic():
                        if subchapter_changed:
                            # 跨子章节移动：旧子章节补位
                            old_scope = {"subchapter": old_subchapter}
                            close_order_gap(Question, old_scope, old_order)
                            # 新子章节中插入
                            if self.order_no:
                                conflict = Question.objects.filter(**scope_filter, order_no=self.order_no).first()
                                if conflict:
                                    insert_order_at(Question, scope_filter, self.order_no)
                            else:
                                self.order_no = get_next_order_no(Question, scope_filter)
                        else:
                            # 同子章节内移动
                            reorder_in_scope(Question, scope_filter, self.id, old_order, self.order_no)
                        # 重新计算 business_id
                        self.business_id = generate_business_id(
                            self.subchapter.chapter.course.order_no,
                            self.subchapter.chapter.order_no,
                            self.subchapter.order_no,
                            self.order_no
                        )
                        super().save(*args, **kwargs)
                        # 级联更新：两个子章节都需要更新
                        update_business_ids_for_subchapter(self.subchapter)
                        if subchapter_changed:
                            update_business_ids_for_subchapter(old_subchapter)
                else:
                    super().save(*args, **kwargs)
            except Question.DoesNotExist:
                pass

    def delete(self, *args, **kwargs):
        deleted_order = self.order_no
        subchapter = self.subchapter
        super().delete(*args, **kwargs)
        close_order_gap(Question, {"subchapter": subchapter}, deleted_order)

    def clean(self):
        """模型校验逻辑"""
        super().clean()

        if not has_content(self.stem_text, self.stem_image):
            raise ValidationError({
                "stem_text": "题干文本和题干图片至少要有一个。"
            })

        if self.question_type == QuestionType.SINGLE_CHOICE:
            options = [
                (self.option_a_text, self.option_a_image, "A"),
                (self.option_b_text, self.option_b_image, "B"),
                (self.option_c_text, self.option_c_image, "C"),
                (self.option_d_text, self.option_d_image, "D"),
            ]

            for text, image, label in options:
                if not has_content(text, image):
                    raise ValidationError({
                        f"option_{label.lower()}_text": f"选项{label}的文本和图片不能同时为空。"
                    })

            if not self.correct_answer:
                raise ValidationError({
                    "correct_answer": "单选题必须选择正确答案。"
                })

        elif self.question_type == QuestionType.BIG_QUESTION:
            option_fields = [
                "option_a_text", "option_a_image",
                "option_b_text", "option_b_image",
                "option_c_text", "option_c_image",
                "option_d_text", "option_d_image",
            ]

            for field in option_fields:
                if getattr(self, field):
                    raise ValidationError({
                        field: "大题不需要填写选项内容。"
                    })

            if self.correct_answer:
                raise ValidationError({
                    "correct_answer": "大题不需要填写正确答案。"
                })


# ============================================================================
# 级联更新函数：更新业务编号
# ============================================================================

def update_business_ids_for_course(instance):
    """
    更新某个课程下所有题目的 business_id（级联到章节、子章节和题目）。
    在 Course.save() 中调用。
    """
    from .utils import generate_business_id
    course = instance if isinstance(instance, Course) else Course.objects.get(id=instance.id)
    updates = []
    for chapter in course.chapters.all().prefetch_related('subchapters__questions'):
        for subchapter in chapter.subchapters.all():
            for question in subchapter.questions.all():
                question.business_id = generate_business_id(
                    course.order_no,
                    chapter.order_no,
                    subchapter.order_no,
                    question.order_no
                )
                updates.append(question)
    if updates:
        Question.objects.bulk_update(updates, ["business_id"])


def update_business_ids_for_chapter(instance):
    """
    更新某个章节下所有题目的 business_id（级联到子章节和题目）。
    在 Chapter.save() 中调用。
    """
    from .utils import generate_business_id
    chapter = instance if isinstance(instance, Chapter) else Chapter.objects.get(id=instance.id)
    updates = []
    for subchapter in chapter.subchapters.all().prefetch_related('questions'):
        for question in subchapter.questions.all():
            question.business_id = generate_business_id(
                chapter.course.order_no,
                chapter.order_no,
                subchapter.order_no,
                question.order_no
            )
            updates.append(question)
    if updates:
        Question.objects.bulk_update(updates, ["business_id"])


def update_business_ids_for_subchapter(instance):
    """
    更新某个子章节下所有题目的 business_id。
    在 SubChapter.save() 中调用。
    """
    from .utils import generate_business_id
    subchapter = instance if isinstance(instance, SubChapter) else SubChapter.objects.get(id=instance.id)
    updates = []
    for question in subchapter.questions.all():
        question.business_id = generate_business_id(
            subchapter.chapter.course.order_no,
            subchapter.chapter.order_no,
            subchapter.order_no,
            question.order_no
        )
        updates.append(question)
    if updates:
        Question.objects.bulk_update(updates, ["business_id"])
