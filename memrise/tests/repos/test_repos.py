import json
from collections import defaultdict, Counter
from typing import Dict
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase

from memrise.core.modules.factories.factories import factory_mapper
from memrise.core.modules.selectors import CourseSelector, LevelSelector, WordSelector
from memrise.core.repositoris.repos import JsonRep, DBRep, MemriseRep
from memrise.core.responses.course_response import CoursesResponse
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
        self.repo = JsonRep()

    def test_fetch_levels(self) -> None:
        with DASHBOARD_FIXTURE.open() as f:
            dashboard_fixtures = json.loads(f.read())

        courses_response = CoursesResponse(**dashboard_fixtures)
        courses = factory_mapper.seek(courses_response.courses)
        expected_len_levels = [6, 3]
        for course, extected in zip(courses, expected_len_levels):
            levels = self.repo.get_levels(course)
            self.assertEqual(len(levels), extected)
            if levels:
                expected_contain_levels = [x for x in range(1, len(levels) + 1)]
                self.assertEqual([x.number for x in levels], expected_contain_levels)

    def test_get_courses(self) -> None:
        courses = self.repo.get_courses()
        self.assertEqual(len(courses), 5)
        excepted = [1987730, 2147115, 5605650, 2014031, 2014042]
        self.assertEqual([x.id for x in courses], excepted)


class TestDBRep(TestCase):
    fixtures = ["db"]

    def setUp(self) -> None:
        self.repo = DBRep()

    def test_get_courses(self) -> None:
        courses = self.repo.get_courses()
        self.assertEqual(len(courses), 5)
        expected = [1987730, 2147115, 2147124, 2147132, 5605650]
        self.assertEqual([x.id for x in courses], expected)

    def test_fetch_levels(self) -> None:
        courses = self.repo.get_courses()
        result = self.repo.get_levels(courses[0])
        levels = list(result)
        self.assertEqual(len(levels), 7)
        expected = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual([x.number for x in levels], expected)
        expected_num_words = [4, 3, 4, 2, 2, 2, 2]
        self.assertEqual([len(x.words) for x in levels], expected_num_words)

    def test_save_course(self) -> None:
        actual_course_entities = self.repo.get_courses()
        expect_before = [1987730, 2147115, 2147124, 2147132, 5605650]
        self.assertEqual([x.id for x in actual_course_entities], expect_before)
        diff = CourseSelector.match(fresh_course_entities, actual_course_entities)
        self.repo.save_courses(diff)
        actual_course_entities_after = self.repo.get_courses()
        expect_after = [1234, 1987730, 2147115, 5605650]
        self.assertEqual([x.id for x in actual_course_entities_after], expect_after)
        diff_after = CourseSelector.match(
            fresh_course_entities, actual_course_entities_after
        )
        self.assertEqual(len(diff_after.create), 0)
        self.assertEqual(len(diff_after.update), 0)
        self.assertEqual(len(diff_after.equal), 4)
        self.assertEqual(len(diff_after.delete), 0)

    def test_save_level(self) -> None:
        courses = defaultdict(list)
        [courses[x.course_id].append(x) for x in fresh_level_entities]

        for course_id, fresh_levels in courses.items():
            course_object = Course.objects.get(id=course_id)
            course_entity = factory_mapper.seek([course_object])[0]
            actual_level_entities = self.repo.get_levels(course_entity)
            diff = LevelSelector.match(fresh_levels, actual_level_entities)
            self.repo.save_levels(diff, Course.objects.get(id=course_entity.id))

        levels_after = Level.objects.filter(course_id__in=courses)
        self.assertEqual(len(levels_after), 8)
        self.assertEqual(
            Counter([x.course_id for x in levels_after]),
            {1987730: 3, 5605650: 3, 2147115: 2},
        )

    def test_save_words(self) -> None:
        level = Level.objects.first()
        words = Word.objects.filter(level=level).all()
        self.assertEqual(len(words), 4)
        self.assertEqual(
            [x.id for x in words], [204850790, 204850795, 204850798, 204850807]
        )
        actual_word_entities = factory_mapper.seek(words)
        fresh_word_entities20 = fresh_word_entities[:20]
        diff = WordSelector.match(fresh_word_entities20, actual_word_entities)
        self.assertEqual(len(diff.create), 20)
        self.assertEqual(len(diff.update), 0)
        self.assertEqual(len(diff.equal), 0)
        self.assertEqual(len(diff.delete), 4)
        self.repo.save_words(diff, level)
        words_after = Word.objects.filter(level=level).all()
        self.assertEqual(len(words_after), 20)
        self.assertEqual([x.id for x in words_after], [x for x in range(1, 21)])


class TestMemriseRep(TestCase):
    def setUp(self) -> None:
        self.repo = MemriseRep()

    @patch(
        "memrise.core.modules.api.base.api._session.request",
        lambda *_, **__: ResponseLevelMock(),
    )
    def test_fetch_levels(self) -> None:
        with DASHBOARD_FIXTURE.open() as f:
            dashboard_fixtures = json.loads(f.read())

        courses_response = CoursesResponse(**dashboard_fixtures)
        courses = factory_mapper.seek(courses_response.courses)
        extected_levels_num = [36]
        for course, expected in zip(courses, extected_levels_num):
            result = self.repo.get_levels(course)
            self.assertEqual(len(result), expected)

    @patch(
        "memrise.core.modules.api.base.api._session.request",
        lambda *_, **__: ResponseCourseMock(),
    )
    def test_get_courses(self) -> None:
        courses = self.repo.get_courses()
        self.assertEqual(len(courses), 5)
        expected = [1987730, 2014031, 2014042, 2147115, 5605650]
        self.assertEqual([x.id for x in courses], expected)
