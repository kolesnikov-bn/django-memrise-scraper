import json

from django.test import TestCase

from memrise.core.modules.factories import CourseEntityMaker
from memrise.core.repositoris.repos import JsonRep, DBRep
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.use_cases.selectors import CourseSelector
from memrise.shares.contants import DASHBOARD_FIXTURE
from memrise.tests.data_for_test import fresh_course_entities


class TestJsonRep(TestCase):
    def test_fetch_levels(self) -> None:
        with DASHBOARD_FIXTURE.open() as f:
            dashboard_fixtures = json.loads(f.read())

        courses_response = CoursesResponse(**dashboard_fixtures)
        course_maker = CourseEntityMaker()
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
    fixtures = ["db"]

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

    def test_save_course(self) -> None:
        dbp = DBRep()
        actual_course_entities = dbp.get_courses()
        expect_before = [1987730, 2147115, 2147124, 2147132, 5605650]
        self.assertEqual([x.id for x in actual_course_entities], expect_before)
        diff = CourseSelector.match(fresh_course_entities, actual_course_entities)
        dbp.save_course(diff)
        actual_course_entities_after = dbp.get_courses()
        expect_after = [1234, 1987730, 2147115, 5605650]
        self.assertEqual([x.id for x in actual_course_entities_after], expect_after)
        diff_after = CourseSelector.match(
            fresh_course_entities, actual_course_entities_after
        )
        self.assertEqual(len(diff_after.create), 0)
        self.assertEqual(len(diff_after.update), 0)
        self.assertEqual(len(diff_after.equal), 4)
        self.assertEqual(len(diff_after.delete), 0)
