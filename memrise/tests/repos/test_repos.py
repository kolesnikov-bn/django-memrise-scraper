import json
from typing import Dict
from unittest import skip

from django.conf import settings
from django.test import TestCase

from memrise.core.domains.entities import WordEntity
from memrise.core.modules.actions.aggregator import DBAggregator, JsonAggregator
from memrise.core.modules.factories.factories import factory_mapper
from memrise.core.modules.selectors import (
    CourseSelector,
    LevelSelector,
    WordSelector,
    DiffContainer,
)
from memrise.core.repositories.repos import JsonRep, DBRep
from memrise.core.responses.course_response import CoursesResponse
from memrise.di import UpdateMemriseContainer
from memrise.models import Course, Level, Word
from memrise.shares.contants import DASHBOARD_FIXTURE
from memrise.tests.data_for_test import (
    fresh_course_entities,
    fresh_level_entities,
    fresh_word_entities,
)

LEVEL_TEXT_FIXTURE = settings.RESOURSES / "fixtures/level_text_response.html"


class ResponseCourseMock:
    status_code = 200

    def json(self) -> Dict:
        with DASHBOARD_FIXTURE.open() as f:
            dashboard_fixtures = json.loads(f.read())

        return dashboard_fixtures


def test_text_response() -> str:
    with LEVEL_TEXT_FIXTURE.open() as f:
        dashboard_fixtures = f.read()

    return dashboard_fixtures


class ResponseLevelMock:
    status_code = 200
    text = test_text_response()


class TestJsonRep(TestCase):
    def setUp(self) -> None:
        self.repo = JsonRep(JsonAggregator())

    def test_get_courses(self) -> None:
        courses = self.repo.get_courses()
        self.assertEqual(len(courses), 5)
        excepted = [1987730, 2147115, 5605650, 2014031, 2014042]
        self.assertEqual([x.id for x in courses], excepted)

    def test_get_levels(self) -> None:
        with DASHBOARD_FIXTURE.open() as f:
            dashboard_fixtures_response = json.loads(f.read())

        courses_response = CoursesResponse(**dashboard_fixtures_response)
        courses_entities = factory_mapper.seek(courses_response.courses)
        level_entities = self.repo.get_levels(courses_entities)
        self.assertEqual(len(level_entities), 9)
        expected_contain_levels = [1, 2, 3, 4, 5, 6, 1, 2, 3]
        self.assertEqual([x.number for x in level_entities], expected_contain_levels)

    def test_save_courses(self):
        diff = DiffContainer()
        self.assertIsNone(self.repo.update_courses(diff))

    def test_save_levels(self):
        diff = DiffContainer()
        self.assertIsNone(self.repo.update_levels(diff))

    def test_save_words(self):
        diff = DiffContainer()
        self.assertIsNone(self.repo.update_words(diff))


class TestDBRep(TestCase):
    fixtures = ["db"]

    def setUp(self) -> None:
        self.repo = DBRep(DBAggregator())

    def test_get_courses(self) -> None:
        courses = self.repo.get_courses()
        self.assertEqual(len(courses), 5)
        expected = [1987730, 2147115, 2147124, 2147132, 5605650]
        self.assertEqual([x.id for x in courses], expected)

    def test_fetch_levels(self) -> None:
        courses = self.repo.get_courses()
        level_entities = self.repo.get_levels(courses)
        self.assertEqual(len(level_entities), 29)
        # Проверяем что полученный список отсортировн по id.
        self.assertTrue(
            all(
                level_entities[i].id <= level_entities[i + 1].id
                for i in range(len(level_entities) - 1)
            )
        )

        # fmt: off
        expected = [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1, 2, 3]
        self.assertEqual([x.number for x in level_entities], expected)
        expected_num_words = [4, 3, 4, 2, 2, 2, 2, 3, 3, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 4, 2, 3, 3]
        self.assertEqual([len(x.words) for x in level_entities], expected_num_words)
        # fmt: on

    def test__get_word_entities(self):
        level_record = Level.objects.all().first()
        word_entities = self.repo._get_word_entities(level_record)
        expected = [
            WordEntity(
                id=204850790, level_id=1, word_a="fair", word_b="справедливый, честный"
            ),
            WordEntity(
                id=204850795,
                level_id=1,
                word_a="nasty",
                word_b="мерзкий, противный, неприятный",
            ),
            WordEntity(id=204850798, level_id=1, word_a="rough", word_b="грубый"),
            WordEntity(
                id=204850807, level_id=1, word_a="vital", word_b="жизненно важный"
            ),
        ]
        self.assertEqual(word_entities, expected)

    def test__get_word_if_word_record_is_none(self):
        level_record = Level.objects.all().first()
        level_record.words.all().delete()
        word_entities = self.repo._get_word_entities(level_record)
        self.assertListEqual(word_entities, [])

    def test_save_course(self) -> None:
        actual_course_entities = self.repo.get_courses()
        # Check before.
        expect_before = [1987730, 2147115, 2147124, 2147132, 5605650]
        self.assertEqual([x.id for x in actual_course_entities], expect_before)

        # Make diff.
        diff = CourseSelector.match(fresh_course_entities, actual_course_entities)
        self.repo.update_courses(diff)
        self.assertEqual(len(diff.create), 1)
        self.assertEqual(len(diff.update), 1)
        self.assertEqual(len(diff.equal), 2)
        self.assertEqual(len(diff.delete), 2)

        # Check after.
        actual_course_entities_after = self.repo.get_courses()
        expect_id_course_after = [1234, 1987730, 2147115, 5605650]
        self.assertEqual(
            [course.id for course in actual_course_entities_after],
            expect_id_course_after,
        )

    def test_save_level(self) -> None:
        course_records = Course.objects.all()

        # Check before.
        levels_before = Level.objects.filter(course_id__in=course_records)
        self.assertEqual(len(levels_before), 29)

        # Save.
        course_entity = factory_mapper.seek(course_records)
        actual_level_entities = self.repo.get_levels(course_entity)
        diff = LevelSelector.match(fresh_level_entities, actual_level_entities)
        self.repo.update_levels(diff)

        # Check after.
        levels_after = Level.objects.filter(course_id__in=course_records)
        self.assertEqual(len(levels_after), 8)

    def test_save_words(self) -> None:
        level = Level.objects.first()
        words = Word.objects.filter(level=level).all()

        # Check before.
        self.assertEqual(len(words), 4)
        self.assertEqual(
            [x.id for x in words], [204850790, 204850795, 204850798, 204850807]
        )

        # Save.
        actual_word_entities = factory_mapper.seek(words)
        fresh_word_entities20 = fresh_word_entities[:20]
        diff = WordSelector.match(fresh_word_entities20, actual_word_entities)
        self.assertEqual(len(diff.create), 20)
        self.assertEqual(len(diff.update), 0)
        self.assertEqual(len(diff.equal), 0)
        self.assertEqual(len(diff.delete), 4)
        self.repo.update_words(diff)

        # Check after.
        words_after = Word.objects.filter(level=level).all()
        self.assertEqual(len(words_after), 20)
        self.assertEqual([x.id for x in words_after], [x for x in range(1, 21)])


class TestMemriseRep(TestCase):
    def setUp(self) -> None:
        self.repo = UpdateMemriseContainer.original_repo

    @skip("Вернуться позже, сделать ассинхронные тесты")
    def test_get_courses(self, mock_get) -> None:
        pass

    @skip("Вернуться позже, сделать ассинхронные тесты")
    def test_fetch_levels(self) -> None:
        pass

    def test_save_courses(self):
        diff = DiffContainer()
        self.assertIsNone(self.repo.update_courses(diff,))

    def test_save_levels(self):
        diff = DiffContainer()
        self.assertIsNone(self.repo.update_levels(diff,))

    def test_save_words(self):
        diff = DiffContainer()
        self.assertIsNone(self.repo.update_words(diff,))
