"""
question_bank/forms.py
=====================
后台录入表单，提供课程→章节→子章节三级联动下拉体验。
"""

from django import forms
from django.db.models import Q

from .models import Course, Chapter, SubChapter, Question


# =============================================================================
# PDF 文件校验函数
# =============================================================================
def validate_pdf_file(file):
    """校验上传文件是否为 PDF 格式"""
    import os
    if file:
        ext = os.path.splitext(file.name)[1].lower()
        if ext != '.pdf':
            raise forms.ValidationError("只能上传 PDF 格式的文件")
        # 校验文件大小（最大 50MB）
        if file.size > 50 * 1024 * 1024:
            raise forms.ValidationError("文件大小不能超过 50MB")


# =============================================================================
# Course 表单
# =============================================================================

class CourseAdminForm(forms.ModelForm):
    """
    课程录入表单。

    新增字段：
        order_no (IntegerField): 允许手动指定顺序号，默认追加到末尾。
        mindmap_pdf (FileField): 允许上传课程思维导图 PDF。

    行为：
        - 新增时：order_no 留空则自动追加到末尾。
        - 编辑时：保留原 order_no，同时可手动调整。
    """

    order_no = forms.IntegerField(
        required=False,
        label="顺序号",
        min_value=1,
        initial=None,
        help_text="留空则自动追加到末尾；指定数字可插入到任意位置（自动后移后续课程）"
    )

    class Meta:
        model = Course
        fields = ["name", "is_active", "mindmap_pdf"]

    def clean_mindmap_pdf(self):
        """校验思维导图 PDF"""
        file = self.cleaned_data.get("mindmap_pdf")
        if file:
            validate_pdf_file(file)
        return file


# =============================================================================
# Chapter 表单
# =============================================================================

class ChapterAdminForm(forms.ModelForm):
    """
    章节录入表单。

    新增字段：
        order_no (IntegerField): 允许手动指定顺序号，默认追加到该课程末尾。

    行为：
        - 新增时：order_no 留空则自动追加到该课程末尾。
        - 编辑时：保留原 order_no，同时可手动调整。
    """

    order_no = forms.IntegerField(
        required=False,
        label="顺序号",
        min_value=1,
        initial=None,
        help_text="留空则自动追加到该课程末尾；指定数字可插入到任意位置（自动后移后续章节）"
    )

    class Meta:
        model = Chapter
        fields = ["course", "name", "is_active"]

    def clean_order_no(self):
        val = self.cleaned_data.get("order_no")
        return val or None


# =============================================================================
# SubChapter 表单
# =============================================================================

class SubChapterAdminForm(forms.ModelForm):
    """
    子章节录入表单。

    新增字段：
        course (CharField): 仅用于筛选章节，不存入数据库。
        order_no (IntegerField): 允许手动指定顺序号，默认追加到末尾。

    行为：
        - 新增时：默认 order_no 留空（自动追加到末尾）。
        - 编辑时：保留原 order_no，同时可手动调整。
        - course 初始为空；选课程后章节下拉才出现可选项。
    """

    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=False,
        label="所属课程（筛选）",
        widget=forms.Select(attrs={"class": "custom-select", "id": "id_course_filter"}),
    )
    order_no = forms.IntegerField(
        required=False,
        label="顺序号",
        min_value=1,
        initial=None,
        help_text="留空则自动追加到该课程最后；指定数字可插入到任意位置（自动后移后续课程）"
    )

    class Meta:
        model = SubChapter
        fields = ["chapter", "name", "is_active"]
        widgets = {
            "chapter": forms.Select(attrs={"class": "custom-select", "id": "id_chapter"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ── 回显：编辑已有 SubChapter 时 ──
        if self.instance.pk and self.instance.chapter_id:
            self.fields["course"].initial = self.instance.chapter.course
            self.fields["chapter"].queryset = Chapter.objects.filter(
                course=self.instance.chapter.course, is_active=True
            )
        else:
            # 新增时：不过滤 queryset，让 ModelChoiceField 能验证用户选择
            self.fields["chapter"].queryset = Chapter.objects.filter(is_active=True)

        # ── 编辑时回显 order_no ──
        if self.instance.pk:
            self.fields["order_no"].initial = self.instance.order_no

    def clean(self):
        cleaned = super().clean()
        course = cleaned.get("course")
        chapter = cleaned.get("chapter")
        if course and chapter and chapter.course_id != course.id:
            self.add_error("chapter", f"所选章节“{chapter.name}”不属于课程“{course.name}”。")
        return cleaned

    def clean_order_no(self):
        val = self.cleaned_data.get("order_no")
        return val or None

    def save(self, commit=True):
        # order_no 由模型的 save() 处理，这里不需要手动干预
        return super().save(commit=commit)


# ============================================================================
# Question 表单
# ============================================================================

class QuestionAdminForm(forms.ModelForm):
    """
    题目录入表单。

    新增字段（不入库，仅用于筛选）：
        course_filter  : 先选课程
        chapter_filter : 再选章节（受课程过滤）
        order_no       : 允许手动指定顺序号，默认追加到末尾

    行为：
        - 新增时：三个筛选字段从空开始，逐级联动。
        - 编辑时：自动回显当前所在的 course / chapter / subchapter。
        - 业务编号 business_id 由 Question.business_id property 动态生成，不入库。
    """

    course_filter = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=False,
        label="所属课程",
        widget=forms.Select(attrs={"class": "custom-select", "id": "id_course_filter"}),
    )
    chapter_filter = forms.ModelChoiceField(
        queryset=Chapter.objects.none(),
        required=False,
        label="所属章节",
        widget=forms.Select(attrs={"class": "custom-select", "id": "id_chapter_filter"}),
    )
    order_no = forms.IntegerField(
        required=False,
        label="顺序号",
        min_value=1,
        help_text="留空则自动追加到当前子章节最后；指定数字可插入到任意位置（自动后移后续题目）"
    )

    class Meta:
        model = Question
        fields = [
            "subchapter", "order_no", "question_type", "is_active",
            "stem_text", "stem_image",
            "option_a_text", "option_a_image",
            "option_b_text", "option_b_image",
            "option_c_text", "option_c_image",
            "option_d_text", "option_d_image",
            "correct_answer",
            "analysis_text", "analysis_image",
        ]
        widgets = {
            "subchapter": forms.Select(attrs={"class": "custom-select", "id": "id_subchapter"}),
            "question_type": forms.Select(attrs={"class": "custom-select"}),
            "is_active": forms.CheckboxInput(),
            "correct_answer": forms.Select(attrs={"class": "custom-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ── 编辑时回显 course_filter / chapter_filter ──
        if self.instance.pk and self.instance.subchapter_id:
            sc = self.instance.subchapter
            ch = sc.chapter
            co = ch.course
            self.fields["course_filter"].initial = co
            self.fields["chapter_filter"].initial = ch
            self.fields["chapter_filter"].queryset = Chapter.objects.filter(course=co, is_active=True)
            self.fields["subchapter"].queryset = SubChapter.objects.filter(chapter=ch, is_active=True)
            self.fields["order_no"].initial = self.instance.order_no
        else:
            # 新增时：预加载所有可用选项，JS 负责按课程→章节→子章节逐级过滤
            self.fields["chapter_filter"].queryset = Chapter.objects.filter(is_active=True)
            self.fields["subchapter"].queryset = SubChapter.objects.filter(is_active=True)

        # ── 编辑时回显 order_no ──
        if self.instance.pk:
            self.fields["order_no"].initial = self.instance.order_no

    def clean(self):
        cleaned = super().clean()
        course_filter = cleaned.get("course_filter")
        chapter_filter = cleaned.get("chapter_filter")
        subchapter = cleaned.get("subchapter")

        if chapter_filter and subchapter and subchapter.chapter_id != chapter_filter.id:
            self.add_error(
                "subchapter",
                f"所选子章节不属于章节“{chapter_filter.name}”。"
            )
        if course_filter and chapter_filter and chapter_filter.course_id != course_filter.id:
            self.add_error(
                "chapter_filter",
                f"所选章节不属于课程“{course_filter.name}”。"
            )
        return cleaned

    def clean_order_no(self):
        val = self.cleaned_data.get("order_no")
        return val or None
