# type: ignore

from django.test import TestCase

from memrise.core.domains.entities import CourseEntity
from memrise.core.modules.factory import CoursesMaker
from memrise.core.use_cases.selectors import CourseSelector
from memrise.models import Course

fresh_course_entities = [
    CourseEntity(
        id=1987730,
        name="Adjective Complex",
        url="/course/1987730/adjective-complex/",
        difficult=6,
        num_words=19,
        num_levels=7,
        difficult_url="/course/1987730/adjective-complex/difficult-items/",
    ),
    CourseEntity(
        id=2147115,
        name="Verbs New Name verb of clothes",
        url="/course/2147115/verbs-of-wear-clothes/",
        difficult=5,
        num_words=19,
        num_levels=2,
        difficult_url="/course/2147115/verbs-of-wear-clothes/difficult-items/",
    ),
    CourseEntity(
        id=1234,
        name="New Course",
        url="/course/1234/new-courses/",
        difficult=5,
        num_words=3,
        num_levels=2,
        difficult_url="/course/1234/new-courses/difficult-items/",
    ),
    CourseEntity(
        id=5605650,
        name="Animals",
        url="/course/5605650/animals/",
        difficult=1,
        num_words=8,
        num_levels=3,
        difficult_url="/course/5605650/animals/difficult-items/",
    ),
]


class TestSelectors(TestCase):
    fixtures = ["db"]

    def test_course_selector(self):
        actual_course_entities = CoursesMaker().make(Course.objects.all())
        cs = CourseSelector()
        result = cs.match(fresh_course_entities, actual_course_entities)
        self.assertEqual(len(result.create), 1)
        self.assertEqual(len(result.delete), 2)
        self.assertEqual(len(result.equal), 2)
        self.assertEqual(len(result.update), 1)
