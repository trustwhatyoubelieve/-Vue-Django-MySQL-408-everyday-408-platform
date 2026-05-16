"""
question_bank/admin.py
======================
Django Admin 配置，包含联动 API、列表展示优化和拖动排序页面。
"""

import json
import logging
from functools import wraps

from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.html import format_html, mark_safe
from django.urls import path, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Chapter, SubChapter, Question
from .forms import (
    CourseAdminForm,
    ChapterAdminForm,
    SubChapterAdminForm,
    QuestionAdminForm,
)


# =============================================================================
# CourseAdmin（含拖动排序入口 + 思维导图管理）
# =============================================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["order_no", "id", "name", "is_active", "has_mindmap", "created_at", "sort_action"]
    list_editable = ["name", "is_active"]
    list_display_links = ["id"]
    search_fields = ["name"]
    list_filter = ["is_active"]
    ordering = ["order_no", "id"]
    form = CourseAdminForm

    fieldsets = (
        ("基本信息", {
            "fields": ("name", "is_active", "order_no")
        }),
        ("思维导图", {
            "fields": ("mindmap_pdf", "mindmap_status"),
            "classes": ("collapse",),
        }),
    )

    readonly_fields = ["mindmap_status"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'order_no' in form.base_fields:
            form.base_fields['order_no'].help_text = "留空则自动追加到末尾；指定数字可插入到任意位置（自动后移后续课程）"
        if 'mindmap_pdf' in form.base_fields:
            form.base_fields['mindmap_pdf'].help_text = "上传该课程的思维导图 PDF 文件，仅支持 .pdf 格式，大小不超过 50MB"
        return form

    def has_mindmap(self, obj):
        """检查课程是否已上传思维导图"""
        if obj.mindmap_pdf:
            return mark_safe(
                f'<span style="color: #67c23a; font-weight: bold;">✓ 已上传</span>'
            )
        return mark_safe(
            f'<span style="color: #909399;">✗ 未上传</span>'
        )
    has_mindmap.short_description = "思维导图"

    def mindmap_status(self, obj):
        """显示当前思维导图状态和下载链接"""
        if obj.mindmap_pdf:
            url = obj.mindmap_pdf.url
            filename = obj.mindmap_pdf.name.split('/')[-1]
            return mark_safe(
                f'<div style="padding: 10px; background: #f0f9eb; border-radius: 6px;">'
                f'<p style="margin: 0 0 8px 0; color: #67c23a;">'
                f'<strong>已上传文件：</strong>{filename}'
                f'</p>'
                f'<a href="{url}" target="_blank" style="color: #409eff; text-decoration: none;">'
                f'👁 查看 / 下载 PDF'
                f'</a>'
                f'</div>'
            )
        return mark_safe(
            f'<div style="padding: 10px; background: #f4f4f5; border-radius: 6px; color: #909399;">'
            f'暂无思维导图，请在下方上传 PDF 文件'
            f'</div>'
        )
    mindmap_status.short_description = "当前思维导图"

    def sort_action(self, obj):
        """拖动排序入口按钮"""
        url = reverse("admin:question_bank_course_sort")
        return mark_safe(
            f'<a class="btn btn-sm btn-secondary" href="{url}">'
            f'<span class="material-icons" style="font-size:14px;vertical-align:middle;">drag_indicator</span> 拖动排序</a>'
        )
    sort_action.short_description = "操作"
    sort_action.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("sort/", self.admin_site.admin_view(self.sort_view), name="question_bank_course_sort"),
            path("sort/data/", self.admin_site.admin_view(self.sort_data_view), name="question_bank_course_sort_data"),
            path("sort/save/", csrf_exempt(self.admin_site.admin_view(self.sort_save_view)), name="question_bank_course_sort_save"),
        ]
        return custom + urls

    def sort_view(self, request):
        """课程拖动排序页面"""
        from django.middleware.csrf import get_token
        courses = Course.objects.filter(is_active=True).order_by("order_no", "id")
        csrf_token = get_token(request)
        # 直接构造 API URL
        admin_index = request.build_absolute_uri('/admin/')
        data_url = admin_index + 'question_bank/course/sort/data/'
        save_url = admin_index + 'question_bank/course/sort/save/'
        context = {
            "title": "拖动排序 - 课程",
            "items": courses,
            "changelist_url": reverse("admin:question_bank_course_changelist"),
            "app_label": self.opts.app_label,
            "opts": self.opts,
            "sort_type": "course",
            "data_url": data_url,
            "save_url": save_url,
            "csrf_token": csrf_token,
        }
        return render(request, "admin/question_bank/sort_items.html", context)

    def sort_data_view(self, request):
        """返回课程排序数据"""
        courses = Course.objects.filter(is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "items": [
                    {"id": c.id, "name": c.name, "order_no": c.order_no}
                    for c in courses
                ]
            }
        })

    def sort_save_view(self, request):
        """保存课程排序"""
        logger = logging.getLogger(__name__)
        from django.http import JsonResponse
        from .services.ordering import batch_reorder_course, update_business_ids_for_course
        if request.method != "POST":
            return JsonResponse({"code": 1, "message": "仅支持 POST"}, status=405)
        try:
            data = json.loads(request.body)
            ordered_ids = data.get("ordered_ids", [])
            logger.info(f"[Sort Save] Course reorder: ordered_ids={ordered_ids}")
            if not ordered_ids:
                return JsonResponse({"code": 1, "message": "未提供排序数据"})
            batch_reorder_course(ordered_ids)
            for cid in ordered_ids:
                try:
                    update_business_ids_for_course(Course.objects.get(id=cid))
                except Course.DoesNotExist:
                    pass
            return JsonResponse({"code": 0, "message": "排序更新成功"})
        except json.JSONDecodeError as e:
            logger.error(f"[Sort Save] JSON decode error: {e}, body={request.body}")
            return JsonResponse({"code": 1, "message": f"请求格式错误: {e}"}, status=400)
        except Exception as e:
            logger.error(f"[Sort Save] Error: {e}", exc_info=True)
            return JsonResponse({"code": 1, "message": str(e)}, status=400)


# =============================================================================
# ChapterAdmin（含联动 API + 拖动排序入口）
# =============================================================================

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ["id", "order_no", "name", "course", "is_active", "created_at", "sort_action"]
    list_editable = ["name", "course", "is_active"]
    search_fields = ["name", "course__name"]
    list_filter = ["course", "is_active"]
    autocomplete_fields = ["course"]
    ordering = ["course", "order_no", "id"]
    form = ChapterAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'order_no' in form.base_fields:
            form.base_fields['order_no'].help_text = "留空则自动追加到该课程最后；指定数字可插入到任意位置（自动后移后续章节）"
        return form

    def sort_action(self, obj):
        """拖动排序入口按钮"""
        if not obj:
            return mark_safe('<span style="color:#999;">请先筛选课程</span>')
        url = reverse("admin:question_bank_chapter_sort", args=[obj.course.id])
        return mark_safe(
            f'<a class="btn btn-sm btn-secondary" href="{url}">'
            f'<span class="material-icons" style="font-size:14px;vertical-align:middle;">drag_indicator</span> 拖动排序</a>'
        )
    sort_action.short_description = "操作"
    sort_action.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "sort/<int:course_id>/",
                self.admin_site.admin_view(self.sort_view),
                name="question_bank_chapter_sort",
            ),
            path(
                "sort/<int:course_id>/data/",
                self.admin_site.admin_view(self.sort_data_view),
                name="question_bank_chapter_sort_data",
            ),
            path(
                "sort/<int:course_id>/save/",
                csrf_exempt(self.admin_site.admin_view(self.sort_save_view)),
                name="question_bank_chapter_sort_save",
            ),
            path(
                "by-course/<int:course_id>/",
                self.admin_site.admin_view(self.by_course_api),
                name="question_bank_chapter_by_course",
            ),
        ]
        return custom + urls

    def sort_view(self, request, course_id):
        """章节拖动排序页面"""
        from django.middleware.csrf import get_token
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({"code": 1, "message": "课程不存在"}, status=404)

        chapters = Chapter.objects.filter(course=course, is_active=True).order_by("order_no", "id")
        admin_index = request.build_absolute_uri('/admin/')
        data_url = admin_index + f'question_bank/chapter/sort/{course_id}/data/'
        save_url = admin_index + f'question_bank/chapter/sort/{course_id}/save/'
        context = {
            "title": f"拖动排序 - {course.name} / 章节",
            "items": chapters,
            "parent_name": course.name,
            "parent_url": reverse("admin:question_bank_chapter_changelist") + f"?course__id__exact={course_id}",
            "changelist_url": reverse("admin:question_bank_chapter_changelist") + f"?course__id__exact={course_id}",
            "grandparent_url": reverse("admin:question_bank_course_changelist"),
            "grandparent_name": course.name,
            "app_label": self.opts.app_label,
            "opts": self.opts,
            "sort_type": "chapter",
            "course_id": course_id,
            "data_url": data_url,
            "save_url": save_url,
            "csrf_token": get_token(request),
        }
        return render(request, "admin/question_bank/sort_items.html", context)

    def sort_data_view(self, request, course_id):
        """返回章节排序数据"""
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({"code": 1, "message": "课程不存在"}, status=404)
        chapters = Chapter.objects.filter(course=course, is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "parent": {"id": course.id, "name": course.name},
                "items": [
                    {"id": ch.id, "name": ch.name, "order_no": ch.order_no}
                    for ch in chapters
                ]
            }
        })

    def sort_save_view(self, request, course_id):
        """保存章节排序"""
        import logging
        logger = logging.getLogger(__name__)
        from django.http import JsonResponse
        from .services.ordering import batch_reorder_chapter, update_business_ids_for_course
        if request.method != "POST":
            return JsonResponse({"code": 1, "message": "仅支持 POST"}, status=405)
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return JsonResponse({"code": 1, "message": "课程不存在"}, status=404)
        try:
            data = json.loads(request.body)
            ordered_ids = data.get("ordered_ids", [])
            logger.info(f"[Sort Save] Chapter reorder course_id={course_id}: ordered_ids={ordered_ids}")
            if not ordered_ids:
                return JsonResponse({"code": 1, "message": "未提供排序数据"})
            batch_reorder_chapter(ordered_ids, course_id)
            update_business_ids_for_course(course)
            return JsonResponse({"code": 0, "message": "排序更新成功"})
        except json.JSONDecodeError as e:
            logger.error(f"[Sort Save] JSON decode error: {e}, body={request.body}")
            return JsonResponse({"code": 1, "message": f"请求格式错误: {e}"}, status=400)
        except Exception as e:
            logger.error(f"[Sort Save] Error: {e}", exc_info=True)
            return JsonResponse({"code": 1, "message": str(e)}, status=400)

    def by_course_api(self, request, course_id):
        """
        GET /admin/question_bank/chapter/by-course/<course_id>/
        返回该课程下所有章节的 id-name 列表，供前端联动下拉使用。
        """
        chapters = Chapter.objects.filter(course_id=course_id, is_active=True).order_by("order_no")
        data = {"chapters": [{"id": c.id, "name": str(c)} for c in chapters]}
        return JsonResponse(data)


# =============================================================================
# SubChapterAdmin（含联动 API + 拖动排序入口）
# =============================================================================

@admin.register(SubChapter)
class SubChapterAdmin(admin.ModelAdmin):
    list_display = ["id", "order_no", "name", "chapter", "is_active", "created_at", "sort_action"]
    list_editable = ["name", "chapter", "is_active"]
    search_fields = ["name", "chapter__name", "chapter__course__name"]
    list_filter = ["chapter__course", "chapter", "is_active"]
    autocomplete_fields = ["chapter"]
    form = SubChapterAdminForm
    ordering = ["chapter", "order_no", "id"]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'order_no' in form.base_fields:
            form.base_fields['order_no'].help_text = "留空则自动追加到该章节最后；指定数字可插入到任意位置（自动后移后续子章节）"
        return form

    def sort_action(self, obj):
        """拖动排序入口按钮"""
        if not obj:
            return mark_safe('<span style="color:#999;">请先筛选章节</span>')
        url = reverse("admin:question_bank_subchapter_sort", args=[obj.chapter.id])
        return mark_safe(
            f'<a class="btn btn-sm btn-secondary" href="{url}">'
            f'<span class="material-icons" style="font-size:14px;vertical-align:middle;">drag_indicator</span> 拖动排序</a>'
        )
    sort_action.short_description = "操作"
    sort_action.allow_tags = True

    class Media:
        js = ("question_bank/admin.js",)

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "sort/<int:chapter_id>/",
                self.admin_site.admin_view(self.sort_view),
                name="question_bank_subchapter_sort",
            ),
            path(
                "sort/<int:chapter_id>/data/",
                self.admin_site.admin_view(self.sort_data_view),
                name="question_bank_subchapter_sort_data",
            ),
            path(
                "sort/<int:chapter_id>/save/",
                csrf_exempt(self.admin_site.admin_view(self.sort_save_view)),
                name="question_bank_subchapter_sort_save",
            ),
            path(
                "by-chapter/<int:chapter_id>/",
                self.admin_site.admin_view(self.by_chapter_api),
                name="question_bank_subchapter_by_chapter",
            ),
        ]
        return custom + urls

    def sort_view(self, request, chapter_id):
        """子章节拖动排序页面"""
        from django.middleware.csrf import get_token
        try:
            chapter = Chapter.objects.select_related("course").get(id=chapter_id)
        except Chapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "章节不存在"}, status=404)

        subchapters = SubChapter.objects.filter(chapter=chapter, is_active=True).order_by("order_no", "id")
        admin_index = request.build_absolute_uri('/admin/')
        data_url = admin_index + f'question_bank/subchapter/sort/{chapter_id}/data/'
        save_url = admin_index + f'question_bank/subchapter/sort/{chapter_id}/save/'
        context = {
            "title": f"拖动排序 - {chapter.course.name} / {chapter.name} / 子章节",
            "items": subchapters,
            "parent_name": f"{chapter.course.name} / {chapter.name}",
            "grandparent_name": chapter.course.name,
            "parent_url": reverse("admin:question_bank_chapter_changelist") + f"?course__id__exact={chapter.course.id}",
            "grandparent_url": reverse("admin:question_bank_course_changelist"),
            "changelist_url": reverse("admin:question_bank_subchapter_changelist") + f"?chapter__id__exact={chapter_id}",
            "app_label": self.opts.app_label,
            "opts": self.opts,
            "sort_type": "subchapter",
            "chapter_id": chapter_id,
            "course_id": chapter.course.id,
            "data_url": data_url,
            "save_url": save_url,
            "csrf_token": get_token(request),
        }
        return render(request, "admin/question_bank/sort_items.html", context)

    def sort_data_view(self, request, chapter_id):
        """返回子章节排序数据"""
        try:
            chapter = Chapter.objects.select_related("course").get(id=chapter_id)
        except Chapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "章节不存在"}, status=404)
        subchapters = SubChapter.objects.filter(chapter=chapter, is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "chapter": {"id": chapter.id, "name": chapter.name},
                "course": {"id": chapter.course.id, "name": chapter.course.name},
                "items": [
                    {"id": sc.id, "name": sc.name, "order_no": sc.order_no}
                    for sc in subchapters
                ]
            }
        })

    def sort_save_view(self, request, chapter_id):
        """保存子章节排序"""
        import logging
        logger = logging.getLogger(__name__)
        from django.http import JsonResponse
        from .services.ordering import batch_reorder_subchapter, update_business_ids_for_chapter
        if request.method != "POST":
            return JsonResponse({"code": 1, "message": "仅支持 POST"}, status=405)
        try:
            chapter = Chapter.objects.get(id=chapter_id)
        except Chapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "章节不存在"}, status=404)
        try:
            data = json.loads(request.body)
            ordered_ids = data.get("ordered_ids", [])
            logger.info(f"[Sort Save] SubChapter reorder chapter_id={chapter_id}: ordered_ids={ordered_ids}")
            if not ordered_ids:
                return JsonResponse({"code": 1, "message": "未提供排序数据"})
            batch_reorder_subchapter(ordered_ids, chapter_id)
            update_business_ids_for_chapter(chapter)
            return JsonResponse({"code": 0, "message": "排序更新成功"})
        except json.JSONDecodeError as e:
            logger.error(f"[Sort Save] JSON decode error: {e}, body={request.body}")
            return JsonResponse({"code": 1, "message": f"请求格式错误: {e}"}, status=400)
        except Exception as e:
            logger.error(f"[Sort Save] Error: {e}", exc_info=True)
            return JsonResponse({"code": 1, "message": str(e)}, status=400)

    def by_chapter_api(self, request, chapter_id):
        """
        GET /admin/question_bank/subchapter/by-chapter/<chapter_id>/
        返回该章节下所有子章节的 id-name 列表。
        """
        subchapters = SubChapter.objects.filter(chapter_id=chapter_id, is_active=True).order_by("order_no")
        data = {"subchapters": [{"id": s.id, "name": str(s)} for s in subchapters]}
        return JsonResponse(data)


# =============================================================================
# QuestionAdmin（含联动 + 10位编号展示 + 拖动排序入口）
# =============================================================================

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "business_id_display",
        "question_type",
        "course_display",
        "chapter_display",
        "subchapter_display",
        "order_no",
        "stem_preview",
        "correct_answer",
        "is_active",
        "sort_action",
    ]
    list_filter = [
        "question_type",
        "is_active",
        "subchapter__chapter__course",
        "subchapter__chapter",
        "subchapter",
    ]
    search_fields = [
        "stem_text",
        "subchapter__name",
        "subchapter__chapter__name",
        "subchapter__chapter__course__name",
    ]
    autocomplete_fields = ["subchapter"]
    form = QuestionAdminForm
    ordering = ["subchapter", "order_no", "id"]
    list_select_related = [
        "subchapter",
        "subchapter__chapter",
        "subchapter__chapter__course",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
        "business_id_display",
        "course_display",
        "chapter_display",
        "subchapter_display",
    ]
    list_editable = ["is_active"]

    fieldsets = (
        ("基本信息", {
            "fields": (
                "course_filter",
                "chapter_filter",
                "subchapter",
                "order_no",
                "question_type",
                "is_active",
            ),
        }),
        ("题干", {
            "fields": ("stem_text", "stem_image"),
        }),
        ("单选题选项", {
            "fields": (
                ("option_a_text", "option_a_image"),
                ("option_b_text", "option_b_image"),
                ("option_c_text", "option_c_image"),
                ("option_d_text", "option_d_image"),
                "correct_answer",
            ),
            "classes": ("collapse",),
        }),
        ("解析", {
            "fields": ("analysis_text", "analysis_image"),
        }),
        ("只读信息", {
            "fields": (
                "business_id_display",
                "course_display",
                "chapter_display",
                "subchapter_display",
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    class Media:
        js = ("question_bank/admin.js",)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'order_no' in form.base_fields:
            form.base_fields['order_no'].help_text = "留空则自动追加到当前子章节最后；指定数字可插入到任意位置（自动后移后续题目）"
        return form

    def sort_action(self, obj):
        """拖动排序入口按钮"""
        if not obj:
            return mark_safe('<span style="color:#999;">请先筛选子章节</span>')
        url = reverse("admin:question_bank_question_sort", args=[obj.subchapter.id])
        return mark_safe(
            f'<a class="btn btn-sm btn-secondary" href="{url}">'
            f'<span class="material-icons" style="font-size:14px;vertical-align:middle;">drag_indicator</span> 拖动排序</a>'
        )
    sort_action.short_description = "操作"
    sort_action.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "sort/<int:subchapter_id>/",
                self.admin_site.admin_view(self.sort_view),
                name="question_bank_question_sort",
            ),
            path(
                "sort/<int:subchapter_id>/data/",
                self.admin_site.admin_view(self.sort_data_view),
                name="question_bank_question_sort_data",
            ),
            path(
                "sort/<int:subchapter_id>/save/",
                csrf_exempt(self.admin_site.admin_view(self.sort_save_view)),
                name="question_bank_question_sort_save",
            ),
        ]
        return custom + urls

    def sort_view(self, request, subchapter_id):
        """题目拖动排序页面"""
        from django.middleware.csrf import get_token
        try:
            subchapter = SubChapter.objects.select_related("chapter__course").get(id=subchapter_id)
        except SubChapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "子章节不存在"}, status=404)

        questions = Question.objects.filter(subchapter=subchapter, is_active=True).order_by("order_no", "id")
        admin_index = request.build_absolute_uri('/admin/')
        data_url = admin_index + f'question_bank/question/sort/{subchapter_id}/data/'
        save_url = admin_index + f'question_bank/question/sort/{subchapter_id}/save/'
        context = {
            "title": f"拖动排序 - {subchapter.chapter.course.name} / {subchapter.chapter.name} / {subchapter.name} / 题目",
            "items": questions,
            "parent_name": f"{subchapter.chapter.course.name} / {subchapter.chapter.name} / {subchapter.name}",
            "grandparent_name": f"{subchapter.chapter.course.name} / {subchapter.chapter.name}",
            "great_grandparent_name": subchapter.chapter.course.name,
            "parent_url": reverse("admin:question_bank_subchapter_changelist") + f"?chapter__id__exact={subchapter.chapter.id}",
            "grandparent_url": reverse("admin:question_bank_chapter_changelist") + f"?course__id__exact={subchapter.chapter.course.id}",
            "great_grandparent_url": reverse("admin:question_bank_course_changelist"),
            "changelist_url": reverse("admin:question_bank_question_changelist") + f"?subchapter__id__exact={subchapter_id}",
            "app_label": self.opts.app_label,
            "opts": self.opts,
            "sort_type": "question",
            "subchapter_id": subchapter_id,
            "chapter_id": subchapter.chapter.id,
            "course_id": subchapter.chapter.course.id,
            "data_url": data_url,
            "save_url": save_url,
            "csrf_token": get_token(request),
        }
        return render(request, "admin/question_bank/sort_items.html", context)

    def sort_data_view(self, request, subchapter_id):
        """返回题目排序数据"""
        try:
            subchapter = SubChapter.objects.select_related("chapter__course").get(id=subchapter_id)
        except SubChapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "子章节不存在"}, status=404)
        questions = Question.objects.filter(subchapter=subchapter, is_active=True).order_by("order_no", "id")
        return JsonResponse({
            "code": 0,
            "data": {
                "subchapter": {"id": subchapter.id, "name": subchapter.name},
                "chapter": {"id": subchapter.chapter.id, "name": subchapter.chapter.name},
                "course": {"id": subchapter.chapter.course.id, "name": subchapter.chapter.course.name},
                "items": [
                    {
                        "id": q.id,
                        "business_id": q.business_id,
                        "stem_preview": (q.stem_text or "")[:50],
                        "order_no": q.order_no,
                    }
                    for q in questions
                ]
            }
        })

    def sort_save_view(self, request, subchapter_id):
        """保存题目排序"""
        import logging
        logger = logging.getLogger(__name__)
        from django.http import JsonResponse
        from .services.ordering import batch_reorder_question, update_business_ids_for_subchapter
        if request.method != "POST":
            return JsonResponse({"code": 1, "message": "仅支持 POST"}, status=405)
        try:
            subchapter = SubChapter.objects.get(id=subchapter_id)
        except SubChapter.DoesNotExist:
            return JsonResponse({"code": 1, "message": "子章节不存在"}, status=404)
        try:
            data = json.loads(request.body)
            ordered_ids = data.get("ordered_ids", [])
            logger.info(f"[Sort Save] Question reorder subchapter_id={subchapter_id}: ordered_ids={ordered_ids}")
            if not ordered_ids:
                return JsonResponse({"code": 1, "message": "未提供排序数据"})
            batch_reorder_question(ordered_ids, subchapter_id)
            update_business_ids_for_subchapter(subchapter)
            return JsonResponse({"code": 0, "message": "排序更新成功"})
        except json.JSONDecodeError as e:
            logger.error(f"[Sort Save] JSON decode error: {e}, body={request.body}")
            return JsonResponse({"code": 1, "message": f"请求格式错误: {e}"}, status=400)
        except Exception as e:
            logger.error(f"[Sort Save] Error: {e}", exc_info=True)
            return JsonResponse({"code": 1, "message": str(e)}, status=400)

    # --------------------------------------------------------------------------
    # 只读展示方法
    # --------------------------------------------------------------------------

    def business_id_display(self, obj):
        """10位业务编号（列表列 + 只读字段）"""
        return mark_safe(
            f'<code style="font-size:1.1em; letter-spacing:1px;">{obj.business_id}</code>'
        )
    business_id_display.short_description = "业务编号"
    business_id_display.admin_order_field = "subchapter__chapter__course__order_no"

    def course_display(self, obj):
        try:
            return obj.course.name
        except Exception:
            return "-"
    course_display.short_description = "课程"
    course_display.admin_order_field = "subchapter__chapter__course__name"

    def chapter_display(self, obj):
        try:
            return obj.chapter.name
        except Exception:
            return "-"
    chapter_display.short_description = "章节"
    chapter_display.admin_order_field = "subchapter__chapter__order_no"

    def subchapter_display(self, obj):
        try:
            return obj.subchapter.name
        except Exception:
            return "-"
    subchapter_display.short_description = "子章节"
    subchapter_display.admin_order_field = "subchapter__order_no"

    def stem_preview(self, obj):
        """题干预览（列表列）"""
        if obj.stem_text:
            text = (obj.stem_text[:50] + "...") if len(obj.stem_text) > 50 else obj.stem_text
            return mark_safe(f'<span title="{obj.stem_text}">{text}</span>')
        elif obj.stem_image:
            return format_html(
                '<img src="{}" style="max-height:40px;max-width:80px;" title="题干图片"/>',
                obj.stem_image.url
            )
        return "-"
    stem_preview.short_description = "题干预览"
