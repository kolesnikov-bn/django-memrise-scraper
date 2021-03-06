# type: ignore

import random

from django.test import TestCase

from memrise.core.domains.entities import (
    CourseEntity,
    LevelEntity,
    WordEntity,
)
from memrise.core.use_cases.dashboard import DashboardCourseContainer


class TestWordEntity(TestCase):
    def test_entity(self):
        word_id = 816
        level_id = 14
        main_word = "main word"
        translate_word = "second word"
        word_entity = WordEntity(
            id=word_id, level_id=level_id, word_a=main_word, word_b=translate_word
        )
        word_as_dict = word_entity.dict()
        expected = {
            "id": 816,
            "level_id": 14,
            "word_a": "main word",
            "word_b": "second word",
            "is_learned": False,
        }
        self.assertDictEqual(word_as_dict, expected)


class TestLevelEntity(TestCase):
    def test_entity(self):
        level_id = 1342
        number = 3
        course_id = 14543
        name = "TestLevel"
        words = []
        le = LevelEntity(
            id=level_id, number=number, course_id=course_id, name=name, words=words
        )
        level_as_dict = le.dict()
        expected = {
            "id": 1342,
            "number": 3,
            "course_id": 14543,
            "name": "TestLevel",
            "words": [],
        }
        self.assertDictEqual(level_as_dict, expected)

    def test_add_word(self):
        """Добавление по одной сущности слова WordEntity в объект черзе метод add_word"""
        le = LevelEntity(number=3, course_id=14543, name="TestLevel", id=1)
        self.assertListEqual(le.words, [])
        word_entity1 = WordEntity(
            id=1, word_a="essential", word_b="translate_word1", level_id=le.id
        )
        word_entity2 = WordEntity(
            id=2, word_a="appropriate", word_b="translate_word2", level_id=le.id
        )
        exptected = [word_entity1, word_entity2]
        for word in exptected:
            le.add_word(word)

        self.assertListEqual(le.words, exptected)

    def test_add_words(self):
        """Добавление множественных сущностей WordEntity в объект черзе метод add_words"""
        le = LevelEntity(number=3, course_id=14543, name="TestLevel", id=1)
        self.assertListEqual(le.words, [])
        word_entity1 = WordEntity(
            id=1, word_a="essential", word_b="translate_word1", level_id=le.id
        )
        word_entity2 = WordEntity(
            id=2, word_a="appropriate", word_b="translate_word2", level_id=le.id
        )
        words = [word_entity1, word_entity2]
        le.add_words(words)

        self.assertListEqual(le.words, words)


class TestCourseEntity(TestCase):
    def test_entity(self):
        id = 618
        name = "Course 1"
        url = "/path/to/course"
        difficult = 234
        num_things = 123
        num_levels = 2
        difficult_url = "/path/to/difficult/words"
        is_disable = True
        ce = CourseEntity(
            id=id,
            name=name,
            url=url,
            difficult=difficult,
            num_words=num_things,
            num_levels=num_levels,
            difficult_url=difficult_url,
            is_disable=is_disable,
        )
        course_as_dict = ce.dict()
        expected = {
            "id": 618,
            "name": "Course 1",
            "url": "/path/to/course",
            "difficult": 234,
            "num_words": 123,
            "num_levels": 2,
            "difficult_url": "/path/to/difficult/words",
            "levels_url": [],
            "levels": [],
            "is_disable": True,
        }
        self.assertDictEqual(course_as_dict, expected)

    def test_add_level(self):
        course_id = 1
        ce = CourseEntity(
            id=course_id,
            name="Course 1",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )
        level1 = LevelEntity(number=1, course_id=ce.id, name="TestLevel1", id=1)
        level2 = LevelEntity(number=2, course_id=ce.id, name="TestLevel2", id=2)
        expected = [level1, level2]
        for level in expected:
            ce.add_level(level)

        self.assertListEqual(ce.levels, expected)

    def test_add_levels(self):
        course_id = 1
        ce = CourseEntity(
            id=course_id,
            name="Course 1",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )
        level1 = LevelEntity(number=1, course_id=ce.id, name="TestLevel1", id=1)
        level2 = LevelEntity(number=2, course_id=ce.id, name="TestLevel2", id=2)
        levels = [level1, level2]
        ce.add_levels(levels)

        self.assertListEqual(ce.levels, levels)


class TestDashboardEntity(TestCase):
    def setUp(self) -> None:
        self.de = DashboardCourseContainer()

    def test_add_course(self):
        id = random.getrandbits(10)
        name = "Course 1"
        url = "/path/to/course"
        difficult = 234
        num_things = 123
        num_levels = 2
        difficult_url = "/path/to/difficult/words"
        ce = CourseEntity(
            id=id,
            name=name,
            url=url,
            difficult=difficult,
            num_words=num_things,
            num_levels=num_levels,
            difficult_url=difficult_url,
        )

        self.assertEqual(self.de.get_courses(), [])
        self.de.add_course(ce)
        courses = self.de.get_courses()
        self.assertEqual(len(courses), 1)
        for course in courses:
            self.assertEqual(course, ce)

    def test_add_courses(self):
        course_1 = CourseEntity(
            id=1,
            name="Course 1",
            url="/path/to/course",
            difficult=111,
            num_words=121,
            num_levels=11,
            difficult_url="/path/to/difficult/words",
        )
        course_2 = CourseEntity(
            id=2,
            name="Course 2",
            url="/path/to/course",
            difficult=222,
            num_words=122,
            num_levels=12,
            difficult_url="/path/to/difficult/words",
        )
        course_3 = CourseEntity(
            id=3,
            name="Course 3",
            url="/path/to/course",
            difficult=333,
            num_words=123,
            num_levels=13,
            difficult_url="/path/to/difficult/words",
        )
        courses = [course_1, course_2, course_3]
        self.assertEqual(self.de.get_courses(), [])
        self.de.add_courses(courses)
        stored_courses = self.de.get_courses()
        self.assertEqual(len(courses), 3)
        self.assertListEqual(stored_courses, courses)

    def test_get_courses(self):
        ce5 = CourseEntity(
            id=5,
            name="Course 5",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )
        ce1 = CourseEntity(
            id=1,
            name="Course 1",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )

        ce3 = CourseEntity(
            id=3,
            name="Course 3",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )

        ce8 = CourseEntity(
            id=8,
            name="Course 8",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )
        courses_entity = [ce5, ce3, ce1, ce8]
        for course_entity in courses_entity:
            self.de.add_course(course_entity)

        courses = self.de.get_courses()
        self.assertEqual(len(courses), 4)
        ids = [course.id for course in courses]
        expected = [1, 3, 5, 8]
        self.assertEqual(ids, expected)

    def test_purge(self):
        ce5 = CourseEntity(
            id=5,
            name="Course 5",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )
        ce1 = CourseEntity(
            id=1,
            name="Course 1",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )

        ce3 = CourseEntity(
            id=3,
            name="Course 3",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )

        ce8 = CourseEntity(
            id=8,
            name="Course 8",
            url="/path/to/course",
            difficult=234,
            num_words=123,
            num_levels=2,
            difficult_url="/path/to/difficult/words",
        )
        courses_entity = [ce5, ce3, ce1, ce8]
        for course_entity in courses_entity:
            self.de.add_course(course_entity)

        courses = self.de.get_courses()
        self.assertEqual(len(courses), 4)
        self.de.purge()
        self.assertEqual(self.de.get_courses(), [])
