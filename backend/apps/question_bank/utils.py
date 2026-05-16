"""
question_bank/utils.py
=====================
业务编号生成工具函数。
"""


def generate_business_id(course_order, chapter_order, subchapter_order, question_order):
    """
    生成 10 位业务编号。
    格式：CC(2) + HH(2) + SS(2) + QQQQ(4) = 10 位
    例如：01 02 03 0001 -> 0102030001

    参数：
        course_order      : int，课程 order_no
        chapter_order     : int，章节 order_no
        subchapter_order  : int，子章节 order_no
        question_order    : int，题目 order_no
    返回：str，10 位固定宽度编号
    """
    return (
        f"{course_order:02d}"
        f"{chapter_order:02d}"
        f"{subchapter_order:02d}"
        f"{question_order:04d}"
    )


def generate_question_display(question):
    """
    给定 Question 实例，生成其 10 位业务编号。
    依赖 question.subchapter.chapter.course 的 order_no 链路。
    若任意环节缺失则返回 "??????????"
    """
    try:
        course_order = question.subchapter.chapter.course.order_no
        chapter_order = question.subchapter.chapter.order_no
        subchapter_order = question.subchapter.order_no
        question_order = question.order_no
        return generate_business_id(
            course_order, chapter_order, subchapter_order, question_order
        )
    except Exception:
        return "??????????"
