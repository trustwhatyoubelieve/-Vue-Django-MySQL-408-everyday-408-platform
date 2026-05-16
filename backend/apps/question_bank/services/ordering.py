"""
question_bank/services/ordering.py
===============================
顺序号管理服务，负责 order_no 的自动分配、插入、顺移、补位等原子操作。

所有方法均在 transaction.atomic 内执行，保证数据一致性。

核心策略：使用临时负值避免唯一约束冲突
"""

from django.db import transaction
from django.db.models import F


def get_next_order_no(model_class, scope_filter=None):
    """获取同级下一个 order_no（最大值 +1）"""
    qs = model_class.objects.all()
    if scope_filter:
        qs = qs.filter(**scope_filter)
    max_order = qs.order_by("-order_no").values_list("order_no", flat=True).first()
    return (max_order or 0) + 1


def _safe_increment(qs):
    """安全地将 queryset 中所有记录的 order_no 加 1"""
    qs.update(order_no=F("order_no") * -1)
    qs.update(order_no=-F("order_no") + 1)


def _safe_decrement(qs):
    """安全地将 queryset 中所有记录的 order_no 减 1"""
    qs.update(order_no=F("order_no") * -1)
    qs.update(order_no=-F("order_no") - 1)


def insert_order_at(model_class, scope_filter, target_order_no, exclude_id=None):
    """将目标位置之后（包括自身）的所有记录的 order_no +1"""
    qs = model_class.objects.filter(**scope_filter, order_no__gte=target_order_no)
    if exclude_id is not None:
        qs = qs.exclude(id=exclude_id)
    _safe_increment(qs)


def insert_at_end_or_position(model_class, scope_filter, target_order_no, exclude_id=None):
    """
    智能插入：如果 target_order_no 为空，追加到末尾；否则插入到指定位置。
    返回实际分配的 order_no。
    """
    if target_order_no is None or target_order_no == 0:
        # 追加到末尾：获取最大 order_no 并 +1
        last = model_class.objects.filter(**scope_filter).order_by('-order_no').first()
        return (last.order_no + 1) if last and last.order_no else 1
    else:
        # 插入到指定位置：将该位置及之后记录后移
        insert_order_at(model_class, scope_filter, target_order_no, exclude_id)
        return target_order_no


def close_order_gap(model_class, scope_filter, deleted_order, exclude_id=None):
    """删除后，将 > deleted_order 的记录 order_no -1 补位"""
    qs = model_class.objects.filter(**scope_filter, order_no__gt=deleted_order)
    if exclude_id is not None:
        qs = qs.exclude(id=exclude_id)
    _safe_decrement(qs)


def reorder_in_scope(model_class, scope_filter, obj_id, old_order_no, new_order_no):
    """在同一 scope 内重排单个对象的顺序号"""
    if old_order_no == new_order_no:
        return

    with transaction.atomic():
        if new_order_no < old_order_no:
            # 往前挪（例如 5→2）
            target = model_class.objects.get(id=obj_id)
            target.order_no = -target.order_no
            target.save(update_fields=["order_no"])
            qs = model_class.objects.filter(
                **scope_filter,
                order_no__gte=new_order_no,
                order_no__lt=old_order_no,
            )
            _safe_increment(qs)
            target.order_no = new_order_no
            target.save(update_fields=["order_no"])
        else:
            # 往后挪（例如 2→5）
            target = model_class.objects.get(id=obj_id)
            target.order_no = -target.order_no
            target.save(update_fields=["order_no"])
            qs = model_class.objects.filter(
                **scope_filter,
                order_no__gt=old_order_no,
                order_no__lte=new_order_no,
            )
            _safe_decrement(qs)
            target.order_no = new_order_no
            target.save(update_fields=["order_no"])


# ============================================================================
# 批量重排（用于拖动排序）
# ============================================================================

def batch_reorder(model_class, ordered_ids, scope_filter=None):
    """
    根据排序后的 ID 列表，批量更新所有对象的 order_no。
    使用临时偏移量法避免唯一约束冲突。
    """
    if not ordered_ids:
        return 0

    MAX_OFFSET = 10000

    with transaction.atomic():
        # 第1步：全部 order_no += MAX_OFFSET，腾出空间
        qs = model_class.objects.all()
        if scope_filter:
            qs = qs.filter(**scope_filter)
        qs.update(order_no=F('order_no') + MAX_OFFSET)

        # 第2步：按顺序分配新 order_no
        for idx, obj_id in enumerate(ordered_ids, start=1):
            model_class.objects.filter(id=obj_id).update(order_no=idx)

        return len(ordered_ids)


def batch_reorder_course(ordered_course_ids):
    """
    批量重排所有课程的顺序号（全局）。
    使用临时偏移量法避免唯一约束冲突。
    """
    from ..models import Course
    if not ordered_course_ids:
        return 0

    MAX_OFFSET = 10000

    with transaction.atomic():
        Course.objects.all().update(order_no=F('order_no') + MAX_OFFSET)
        for idx, obj_id in enumerate(ordered_course_ids, start=1):
            Course.objects.filter(id=obj_id).update(order_no=idx)
        return len(ordered_course_ids)


def batch_reorder_chapter(ordered_chapter_ids, course_id):
    """批量重排指定课程下的章节顺序号。"""
    from ..models import Chapter
    return batch_reorder(Chapter, ordered_chapter_ids, {"course_id": course_id})


def batch_reorder_subchapter(ordered_subchapter_ids, chapter_id):
    """批量重排指定章节下的子章节顺序号。"""
    from ..models import SubChapter
    return batch_reorder(SubChapter, ordered_subchapter_ids, {"chapter_id": chapter_id})


def batch_reorder_question(ordered_question_ids, subchapter_id):
    """批量重排指定子章节下的题目顺序号。"""
    from ..models import Question
    return batch_reorder(Question, ordered_question_ids, {"subchapter_id": subchapter_id})


# ============================================================================
# 级联更新 business_id
# ============================================================================

def update_business_ids_for_course(course):
    """更新课程下所有题目的 business_id"""
    from ..models import Question
    for ch in course.chapters.all():
        for sc in ch.subchapters.all():
            for q in sc.questions.all():
                q.business_id = generate_business_id(
                    course.order_no,
                    ch.order_no,
                    sc.order_no,
                    q.order_no
                )
                q.save(update_fields=["business_id"])


def update_business_ids_for_chapter(chapter):
    """更新章节下所有题目的 business_id"""
    from ..models import Question
    for sc in chapter.subchapters.all():
        for q in sc.questions.all():
            q.business_id = generate_business_id(
                chapter.course.order_no,
                chapter.order_no,
                sc.order_no,
                q.order_no
            )
            q.save(update_fields=["business_id"])


def update_business_ids_for_subchapter(subchapter):
    """更新子章节下所有题目的 business_id"""
    from ..models import Question
    for q in subchapter.questions.all():
        q.business_id = generate_business_id(
            subchapter.chapter.course.order_no,
            subchapter.chapter.order_no,
            subchapter.order_no,
            q.order_no
        )
        q.save(update_fields=["business_id"])


def generate_business_id(course_order, chapter_order, subchapter_order, question_order):
    """生成业务编号：CC HH SS QQQQ"""
    return f"{course_order:02d}{chapter_order:02d}{subchapter_order:02d}{question_order:04d}"
