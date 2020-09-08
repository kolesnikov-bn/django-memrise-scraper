# type: ignore

from django.test import TestCase

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity
from memrise.core.modules.factory import CoursesMaker
from memrise.core.use_cases.selectors import CourseSelector
from memrise.models import Course

fresh_course_entities = [
    CourseEntity(
        id=1987730,
        name="Adjective Complex",
        url="/course/1987730/adjective-complex/",
        difficult=46,
        num_words=581,
        num_levels=36,
        difficult_url="/course/1987730/adjective-complex/difficult-items/",
    ),
    CourseEntity(
        id=2000641,
        name="Verbs New Name verb of clothes",
        url='/course/2000641/verbs-of-wear-clothes/',
        difficult=5,
        num_words=19,
        num_levels=2,
        difficult_url='/course/2000641/verbs-of-wear-clothes/difficult-items/',
    ),
    CourseEntity(
        id=1234,
        name="New Course",
        url='/course/1234/new-courses/',
        difficult=5,
        num_words=3,
        num_levels=2,
        difficult_url='/course/1234/new-courses/difficult-items/',
    ),
    CourseEntity(
        id=2014022,
        name='Food',
        url='/course/2014022/food/',
        difficult=9,
        num_words=70,
        num_levels=4,
        difficult_url='/course/2014022/food/difficult-items/',
    ),
]


class TestSelectors(TestCase):
    fixtures = ["db"]

    def test_course_sequencer(self):
        actual_course_entities = CoursesMaker().make(Course.objects.all())
        cs = CourseSelector()
        result = cs.match(fresh_course_entities, actual_course_entities)
        self.assertEqual(len(result.create), 1)
        self.assertEqual(len(result.delete), 8)
        self.assertEqual(len(result.equal), 2)
        self.assertEqual(len(result.update), 1)
