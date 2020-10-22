from django.test import TestCase

from memrise.core.modules.actions.action_reporter import (
    CourseReporter,
    LevelReporter,
    WordReporter,
)
from memrise.tests.data_for_test import (
    fresh_course_entities,
    fresh_level_entities,
    fresh_word_entities,
)


class TestReporter(TestCase):
    def test_course_reporter(self):
        prefix = ""
        postfix = "[$total]: $id_items"
        cr = CourseReporter()
        cr.report(
            fresh_course_entities,
            f"{prefix}Тестирование визуализации добавления новых курсов{postfix}",
        )

    def test_level_reporter(self):
        prefix = "Курс $course_id --> "
        postfix = "[$total]: $id_items"
        lr = LevelReporter()
        lr.report(
            fresh_level_entities,
            f"{prefix}Тестирование визуализации добавления новых уровней{postfix}",
        )

    def test_word_reporter(self):
        prefix = "Уровень $level_id --> "
        postfix = "[$total]: $id_items"
        wr = WordReporter()
        wr.report(
            fresh_word_entities,
            f"{prefix}Тестирование визуализации добавления новых слов{postfix}",
        )
