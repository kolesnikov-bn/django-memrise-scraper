# type: ignore

from django.test import TestCase

from memrise.core.modules.factories.factories import factory_mapper
from memrise.core.modules.selectors import CourseSelector, LevelSelector, WordSelector
from memrise.models import Course, Level, Word
from memrise.tests.data_for_test import (
    fresh_course_entities,
    fresh_level_entities,
    fresh_word_entities,
)


class TestSelectors(TestCase):
    fixtures = ["db"]

    def test_course_selector(self):
        actual_course_entities = factory_mapper.seek(Course.objects.all())
        result = CourseSelector.match(fresh_course_entities, actual_course_entities)
        self.assertEqual(len(result.create), 1)
        self.assertEqual(len(result.delete), 2)
        self.assertEqual(len(result.equal), 2)
        self.assertEqual(len(result.update), 1)

    def test_level_selector(self):
        actual_level_entities = factory_mapper.seek(Level.objects.all())
        result = LevelSelector.match(fresh_level_entities, actual_level_entities)
        self.assertEqual(len(result.create), 2)
        self.assertEqual(len(result.delete), 23)
        self.assertEqual(len(result.equal), 3)
        self.assertEqual(len(result.update), 3)

    def test_word_selector(self):
        actual_word_entities = factory_mapper.seek(Word.objects.all())
        result = WordSelector.match(fresh_word_entities, actual_word_entities)
        self.assertEqual(len(result.create), 20)
        self.assertEqual(len(result.update), 3)
        self.assertEqual(len(result.equal), 7)
        self.assertEqual(len(result.delete), 60)
