# type: ignore

from django.test import TestCase

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity
from memrise.core.modules.factory import CoursesMaker, LevelMaker, WordMaker
from memrise.core.use_cases.selectors import CourseSelector, LevelSelector, WordSelector
from memrise.models import Course, Level, Word

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

fresh_level_entities = [
    LevelEntity(
        number=1,
        course_id=1987730,
        name="New level",
        words=[WordEntity(id=1, word_a="test", word_b="sdlfksjd")],
    ),
    LevelEntity(
        number=2,
        course_id=1987730,
        name="New level",
        words=[WordEntity(id=2, word_a="check", word_b="blah-blah")],
    ),
    LevelEntity(number=3, course_id=1987730, name="New level"),
    LevelEntity(number=1, course_id=2147115, name="New level"),
    LevelEntity(number=1, course_id=5605650, name="Level 123-346"),
    LevelEntity(number=2, course_id=5605650, name="New level"),
    LevelEntity(number=12, course_id=5605650, name="New level12"),
    LevelEntity(number=11, course_id=2147115, name="New level11"),
]

fresh_word_entities = [
    WordEntity(id=1, word_a="nasty", word_b="мерзкий, противный, неприятный"),
    WordEntity(id=2, word_a="rough", word_b="грубый"),
    WordEntity(id=3, word_a="tense", word_b="напряженный"),
    WordEntity(id=4, word_a="vital", word_b="жизненно важный"),
    WordEntity(
        id=5, word_a="deprecated", word_b="устаревший, исключенный, не рекомендуемый",
    ),
    WordEntity(id=6, word_a="joyful", word_b="радостный, ликующий"),
    WordEntity(id=7, word_a="startled", word_b="испуганный, пораженный, встревоженный"),
    WordEntity(id=8, word_a="humiliated", word_b="униженный"),
    WordEntity(id=9, word_a="remarkable", word_b="замечательный, выдающийся"),
    WordEntity(id=10, word_a="odd", word_b="странный, необычный"),
    WordEntity(
        id=11, word_a="awkward", word_b="неловкий, неуклюжий (момент, поведение)"
    ),
    WordEntity(id=12, word_a="mere", word_b="простой, всего лишь"),
    WordEntity(id=13, word_a="pleased", word_b="довольный"),
    WordEntity(id=14, word_a="familiar", word_b="привычный, знакомый"),
    WordEntity(id=15, word_a="certain", word_b="определенный, уверенный"),
    WordEntity(id=16, word_a="essential", word_b="существенный, обязательный (вещь)"),
    WordEntity(id=17, word_a="immediate", word_b="немедленный"),
    WordEntity(id=18, word_a="appropriate", word_b="соответствующий, подходящий"),
    WordEntity(id=19, word_a="irregular", word_b="неправильный, нестандартный"),
    WordEntity(id=20, word_a="to adjust", word_b="регулировать, приспосабливаться"),
    WordEntity(id=204850790, word_a="fair", word_b="справедливый, честный"),
    WordEntity(id=204850795, word_a="nasty", word_b="мерзкий, противный, неприятный"),
    WordEntity(id=204850798, word_a="rough", word_b="грубый"),
    WordEntity(id=204850807, word_a="vital", word_b="жизненно важный"),
    WordEntity(id=204850898, word_a="irregular", word_b="неправильный, нестандартный"),
    WordEntity(
        id=204850899, word_a="independent", word_b="независимый, самостоятельный"
    ),
    WordEntity(id=204850900, word_a="proper", word_b="надлежащий, правильный"),
    WordEntity(id=204857074, word_a="content", word_b="blah-blah"),
    WordEntity(id=204857075, word_a="calm", word_b="blah-blah"),
    WordEntity(id=204857126, word_a="terrified", word_b="blah-blah"),
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

    def test_level_selector(self):
        actual_level_entities = LevelMaker().make(Level.objects.all())
        ls = LevelSelector()
        result = ls.match(fresh_level_entities, actual_level_entities)
        self.assertEqual(len(result.create), 2)
        self.assertEqual(len(result.delete), 23)
        self.assertEqual(len(result.equal), 3)
        self.assertEqual(len(result.update), 3)

    def test_word_selector(self):
        actual_word_entities = WordMaker().make(Word.objects.all())
        ws = WordSelector()
        result = ws.match(fresh_word_entities, actual_word_entities)
        self.assertEqual(len(result.create), 20)
        self.assertEqual(len(result.update), 3)
        self.assertEqual(len(result.equal), 7)
        self.assertEqual(len(result.delete), 60)
