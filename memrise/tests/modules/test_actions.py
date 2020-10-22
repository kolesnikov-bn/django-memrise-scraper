from django.test import TestCase

from memrise.core.domains.entities import CourseEntity, LevelEntity
from memrise.core.modules.actions.action_reporter import CourseReporter, LevelReporter
from memrise.core.modules.actions.db_actions import DBCourseActions, DBLevelActions
from memrise.models import Course, Level
from memrise.tests.data_for_test import fresh_course_entities, fresh_level_entities


class TestDBCourseActions(TestCase):
    fixtures = ["db"]

    def setUp(self):
        self.fresh_entities = [
            CourseEntity(
                id=1,
                name="course 1",
                url="/course/1",
                difficult=1,
                num_words=1,
                num_levels=1,
                difficult_url="/difficult/1",
            ),
            CourseEntity(
                id=2,
                name="course 2",
                url="/course/2",
                difficult=2,
                num_words=2,
                num_levels=2,
                difficult_url="/difficult/2",
            ),
            CourseEntity(
                id=3,
                name="course 3",
                url="/course/3",
                difficult=3,
                num_words=3,
                num_levels=3,
                difficult_url="/difficult/3",
            ),
            CourseEntity(
                id=4,
                name="course 4",
                url="/course/4",
                difficult=4,
                num_words=4,
                num_levels=4,
                difficult_url="/difficult/4",
            ),
            CourseEntity(
                id=5,
                name="course 5",
                url="/course/5",
                difficult=5,
                num_words=5,
                num_levels=5,
                difficult_url="/difficult/5",
            ),
        ]

    def test_create(self):
        before_courses = Course.objects.all()
        expected_before_num_courses = 5
        self.assertEqual(len(before_courses), expected_before_num_courses)
        dca = DBCourseActions(reporter=CourseReporter())
        dca.create(self.fresh_entities)

        after_courses = Course.objects.all()
        expected_after_num_courses = expected_before_num_courses + len(
            self.fresh_entities
        )
        self.assertEqual(len(after_courses), expected_after_num_courses)

    def test_update(self):
        before_courses = Course.objects.all()
        self.assertEqual(
            [x.name for x in before_courses],
            [
                "Adjective Complex",
                "Adverb Complex",
                "Noun Complex",
                "Verb Complex",
                "Animals",
            ],
        )
        dca = DBCourseActions(reporter=CourseReporter())
        dca.update(fresh_course_entities)

        after_courses = Course.objects.all()
        self.assertEqual(
            [x.name for x in after_courses],
            [
                "Adjective Complex",
                "Verbs New Name verb of clothes",
                "Noun Complex",
                "Verb Complex",
                "Animals",
            ],
        )

    def test_equal(self):
        before_courses = Course.objects.all()
        dca = DBCourseActions(reporter=CourseReporter())
        dca.equal(fresh_course_entities)
        after_courses = Course.objects.all()
        self.assertListEqual(list(before_courses), list(after_courses))

    def test_delete(self):
        before_courses = Course.objects.all()
        self.assertTrue(all(x.is_disable is False for x in before_courses))
        dca = DBCourseActions(reporter=CourseReporter())
        dca.delete(fresh_course_entities)
        after_courses = Course.objects.all()
        self.assertFalse(all(x.is_disable is False for x in after_courses))
        self.assertEqual(
            [x.is_disable for x in after_courses], [True, True, False, False, True]
        )


class TestDBLevelActions(TestCase):
    fixtures = ["db"]

    def setUp(self):
        self.fresh_entities = [
            LevelEntity(id=11, number=1, course_id=1987730, name="test 1"),
            LevelEntity(id=21, number=2, course_id=1987730, name="test 2"),
            LevelEntity(id=31, number=3, course_id=1987730, name="test 3"),
            LevelEntity(id=41, number=4, course_id=1987730, name="test 4"),
            LevelEntity(id=51, number=5, course_id=1987730, name="test 5"),
        ]

    def test_create(self):
        before_levels = Level.objects.all()
        expected_before_num_levels = 29
        self.assertEqual(len(before_levels), expected_before_num_levels)
        dca = DBLevelActions(reporter=LevelReporter())
        dca.create(self.fresh_entities)

        after_levels = Level.objects.all()
        expected_after_num_levels = expected_before_num_levels + len(
            self.fresh_entities
        )
        self.assertEqual(len(after_levels), expected_after_num_levels)

    def test_update(self):
        update_ids = [x.id for x in fresh_level_entities]
        before_levels = Level.objects.all().filter(id__in=update_ids)
        self.assertEqual(
            [f"{x.id} -- {x.name}" for x in before_levels],
            [
                "1 -- New level",
                "2 -- New level",
                "3 -- New level",
                "52 -- 1 - 20",
                "137 -- Safari and Exotic Animals",
                "138 -- About Animals",
            ],
        )
        dca = DBLevelActions(reporter=LevelReporter())
        dca.update(fresh_level_entities)

        after_levels = Level.objects.all().filter(id__in=update_ids)
        self.assertEqual(
            [f"{x.id} -- {x.name}" for x in after_levels],
            [
                "1 -- New level",
                "2 -- New level",
                "3 -- New level",
                "52 -- New level",
                "137 -- Level 123-346",
                "138 -- New level",
            ],
        )

    def test_equal(self):
        before_levels = Level.objects.all()
        dca = DBLevelActions(reporter=LevelReporter())
        dca.equal(fresh_level_entities)
        after_levels = Level.objects.all()
        self.assertListEqual(list(before_levels), list(after_levels))

    def test_delete(self):
        before_levels = Level.objects.all()
        self.assertEqual(len(before_levels), 29)
        dca = DBLevelActions(reporter=LevelReporter())
        dca.delete(fresh_level_entities)
        after_levels = Level.objects.all()
        self.assertEqual(len(after_levels), 23)
