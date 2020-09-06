import json

from django.test import TestCase

from memrise.core.modules.factory import CoursesMaker
from memrise.core.repositoris.repos import JsonRep
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
