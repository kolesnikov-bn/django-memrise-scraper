from django.test import TestCase

from memrise.core.domains.entities import WordEntity, LevelEntity, CourseEntity
from memrise.core.modules.selectors import (
    DiffContainer,
    CourseSelector,
    WordSelector,
    LevelSelector,
)


class TestDiffContainer(TestCase):
    def test_container(self):
        dc = DiffContainer()
        dc.create.append(
            WordEntity(id=1, level_id=1, word_a="test a 1", word_b="translate b 1")
        )
        dc.create.append(
            WordEntity(id=2, level_id=2, word_a="test a 2", word_b="translate b 2")
        )
        dc.update.append(
            WordEntity(id=3, level_id=3, word_a="test a 3", word_b="translate b 3")
        )
        dc.equal.append(
            WordEntity(id=4, level_id=4, word_a="test a 4", word_b="translate b 4")
        )

        self.assertEqual(len(dc.create), 2)
        self.assertEqual(len(dc.delete), 0)
        self.assertEqual(len(dc.equal), 1)
        self.assertEqual(len(dc.update), 1)


class TestSelectors(TestCase):
    def test_word_match(self):
        fresh_entities = [
            WordEntity(id=1, level_id=1, word_a="test a 1", word_b="translate b 1"),
            WordEntity(id=2, level_id=2, word_a="test a 2", word_b="translate b 2"),
            WordEntity(id=3, level_id=3, word_a="test a 3", word_b="translate b 3"),
            WordEntity(id=4, level_id=4, word_a="test a 4", word_b="translate b 4"),
            WordEntity(id=5, level_id=5, word_a="test a 5", word_b="translate b 5"),
        ]
        actual_entities = [
            WordEntity(id=1, level_id=1, word_a="test a 11", word_b="translate b 11"),
            WordEntity(id=2, level_id=2, word_a="test a 2", word_b="translate b 2"),
            WordEntity(id=20, level_id=20, word_a="test a 20", word_b="translate b 20"),
            WordEntity(id=5, level_id=5, word_a="test a 50", word_b="translate b 5"),
        ]
        diff = WordSelector().match(
            fresh_entities=fresh_entities, actual_entities=actual_entities
        )
        self.assertEqual(len(diff.create), 2)
        self.assertEqual(len(diff.delete), 1)
        self.assertEqual(len(diff.equal), 1)
        self.assertEqual(len(diff.update), 2)

    def test_level_match(self):
        fresh_entities = [
            LevelEntity(id=1, number=1, course_id=1, name="test 1"),
            LevelEntity(id=2, number=2, course_id=2, name="test 2"),
            LevelEntity(id=3, number=3, course_id=3, name="test 3"),
            LevelEntity(id=4, number=4, course_id=4, name="test 4"),
            LevelEntity(id=5, number=5, course_id=5, name="test 5"),
        ]
        actual_entities = [
            LevelEntity(id=1, number=1, course_id=1, name="test 1"),
            LevelEntity(id=2, number=2, course_id=2, name="test 2"),
            LevelEntity(id=20, number=20, course_id=20, name="test 20"),
            LevelEntity(id=5, number=5, course_id=5, name="test 50"),
        ]
        diff = LevelSelector().match(
            fresh_entities=fresh_entities, actual_entities=actual_entities
        )
        self.assertEqual(len(diff.create), 2)
        self.assertEqual(len(diff.delete), 1)
        self.assertEqual(len(diff.equal), 2)
        self.assertEqual(len(diff.update), 1)

    def test_course_match(self):
        fresh_entities = [
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
        actual_entities = [
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
                id=20,
                name="course 20",
                url="/course/20",
                difficult=20,
                num_words=20,
                num_levels=20,
                difficult_url="/difficult/20",
            ),
            CourseEntity(
                id=5,
                name="course 5",
                url="/course/5",
                difficult=5,
                num_words=5,
                num_levels=5,
                difficult_url="/difficult/50",
            ),
        ]
        diff = CourseSelector().match(
            fresh_entities=fresh_entities, actual_entities=actual_entities
        )
        self.assertEqual(len(diff.create), 2)
        self.assertEqual(len(diff.delete), 1)
        self.assertEqual(len(diff.equal), 2)
        self.assertEqual(len(diff.update), 1)
