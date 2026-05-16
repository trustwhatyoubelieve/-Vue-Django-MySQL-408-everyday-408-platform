"""
批量从 JSON 文件导入题目到数据库

使用方法：
    python manage.py import_questions <json_file_or_directory>
    python manage.py import_questions ./questions.json
    python manage.py import_questions ./questions_folder/

选项：
    --skip-existing  跳过已存在的题目（按课程+章节+子章节+题干文本匹配）
"""
import json
import os
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.question_bank.models import Course, Chapter, SubChapter, Question


class Command(BaseCommand):
    help = '从 JSON 文件批量导入题目到题库'

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            nargs='+',
            type=str,
            help='JSON 文件路径或包含 JSON 文件的目录路径'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='跳过已存在的题目（按课程+章节+子章节+题干文本匹配）'
        )

    def handle(self, *args, **options):
        paths = options['path']
        skip_existing = options['skip_existing']

        json_files = []
        for p in paths:
            p = Path(p)
            if p.is_dir():
                json_files.extend(p.glob('*.json'))
            elif p.is_file() and p.suffix == '.json':
                json_files.append(p)

        if not json_files:
            self.stderr.write(self.style.ERROR('未找到任何 JSON 文件'))
            return

        self.stdout.write(f'找到 {len(json_files)} 个 JSON 文件\n')

        total_courses = 0
        total_chapters = 0
        total_subchapters = 0
        total_questions = 0

        for json_file in json_files:
            self.stdout.write(f'处理文件: {json_file}')
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                counts = self._import_data(data, skip_existing)
                total_courses += counts['courses']
                total_chapters += counts['chapters']
                total_subchapters += counts['subchapters']
                total_questions += counts['questions']

                self.stdout.write(self.style.SUCCESS(
                    f'  [完成] 课程:{counts["courses"]} 章节:{counts["chapters"]} '
                    f'子章节:{counts["subchapters"]} 题目:{counts["questions"]}\n'
                ))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  [失败] {json_file} - {e}\n'))

        self.stdout.write(self.style.SUCCESS(
            f'========== 总计导入 ==========\n'
            f'课程: {total_courses}\n'
            f'章节: {total_chapters}\n'
            f'子章节: {total_subchapters}\n'
            f'题目: {total_questions}\n'
        ))

    @transaction.atomic
    def _import_data(self, data, skip_existing=False):
        counts = {'courses': 0, 'chapters': 0, 'subchapters': 0, 'questions': 0}

        courses_data = data.get('courses', [])

        for course_data in courses_data:
            course_name = course_data['name']

            # 创建或获取课程
            course, created = Course.objects.get_or_create(
                name=course_name,
                defaults={'is_active': True}
            )
            if created:
                counts['courses'] += 1
                self.stdout.write(f'    + 课程: {course_name}')

            # 处理章节
            chapters_data = course_data.get('chapters', [])
            for chapter_data in chapters_data:
                chapter_name = chapter_data['name']

                chapter, created = Chapter.objects.get_or_create(
                    course=course,
                    name=chapter_name,
                    defaults={'is_active': True}
                )
                if created:
                    counts['chapters'] += 1
                    self.stdout.write(f'      + 章节: {chapter_name}')

                # 处理子章节
                subchapters_data = chapter_data.get('subchapters', [])
                for subchapter_data in subchapters_data:
                    subchapter_name = subchapter_data['name']

                    subchapter, created = SubChapter.objects.get_or_create(
                        chapter=chapter,
                        name=subchapter_name,
                        defaults={'is_active': True}
                    )
                    if created:
                        counts['subchapters'] += 1
                        self.stdout.write(f'        + 子章节: {subchapter_name}')

                    # 处理题目
                    questions_data = subchapter_data.get('questions', [])
                    for q_data in questions_data:
                        stem_text = q_data.get('stem_text', '')

                        # 检查是否已存在（可选）
                        if skip_existing:
                            exists = Question.objects.filter(
                                subchapter=subchapter,
                                stem_text=stem_text
                            ).exists()
                            if exists:
                                self.stdout.write(f'          - 跳过: {stem_text[:30]}...')
                                continue

                        # 构建选项数据
                        options = q_data.get('options', {})

                        question = Question(
                            subchapter=subchapter,
                            question_type=q_data.get('question_type', 'single_choice'),
                            stem_text=stem_text,
                            option_a_text=options.get('A', ''),
                            option_b_text=options.get('B', ''),
                            option_c_text=options.get('C', ''),
                            option_d_text=options.get('D', ''),
                            correct_answer=q_data.get('correct_answer', ''),
                            analysis_text=q_data.get('analysis_text', ''),
                            is_active=True,
                        )
                        question.save()
                        counts['questions'] += 1
                        self.stdout.write(f'          + 题目: {stem_text[:30]}...')

        return counts
