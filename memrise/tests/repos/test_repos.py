import json

from django.test import TestCase

from memrise.core.modules.factory import CoursesMaker
from memrise.core.repositoris.repos import JsonRep, DBRep
from memrise.core.responses.course_response import CoursesResponse
from memrise.shares.contants import DASHBOARD_FIXTURE


class TestJsonRep(TestCase):
    def test_fetch_levels(self) -> None:
        with DASHBOARD_FIXTURE.open() as f:
            dashboard_fixtures = json.loads(f.read())

        courses_response = CoursesResponse(**dashboard_fixtures)
        course_maker = CoursesMaker()
        courses = course_maker.make(courses_response.iterator())
        jp = JsonRep()
        expected_len_levels = [36, 9]
        for course, extected in zip(courses, expected_len_levels):
            levels = jp.fetch_levels(course)
            self.assertEqual(len(levels), extected)
            if levels:
                expected_contain_levels = [x for x in range(1, len(levels) + 1)]
                self.assertEqual([x.number for x in levels], expected_contain_levels)

    def test_get_courses(self) -> None:
        jp = JsonRep()
        courses = jp.get_courses()
        self.assertEqual(len(courses), 5)
        excepted = [1987730, 2147115, 5605650, 2014031, 2014042]
        self.assertEqual([x.id for x in courses], excepted)


class TestDBRep(TestCase):
    fixtures = ['db']

    def test_get_courses(self) -> None:
        dbp = DBRep()
        courses = dbp.get_courses()
        self.assertEqual(len(courses), 5)
        expected = [1987730, 2147115, 2147124, 2147132, 5605650]
        self.assertEqual([x.id for x in courses], expected)

    def test_fetch_levels(self) -> None:
        dbp = DBRep()
        courses = dbp.get_courses()
        result = dbp.fetch_levels(courses[0])
        levels = list(result)
        self.assertEqual(len(levels), 7)
        expected = [1, 2, 3, 4, 5, 6, 7]
        self.assertEqual([x.number for x in levels], expected)
        expected_num_words = [4, 3, 4, 2, 2, 2, 2]
        self.assertEqual([len(x.words) for x in levels], expected_num_words)
