# type: ignore

import random

from django.test import TestCase

from memrise.core.domains.entities import (
    CourseEntity,
    LevelEntity,
    WordEntity,
    DashboardEntity,
)


class TestWordEntity(TestCase):
    def test_entity(self):
        word_id = random.getrandbits(10)
        main_word = "main word"
        translate_word = "second word"
        word_entity = WordEntity(id=word_id, word_a=main_word, word_b=translate_word)
        self.assertEqual(word_entity.id, word_id)
        self.assertEqual(word_entity.word_a, main_word)
        self.assertEqual(word_entity.word_b, translate_word)


class TestLevelEntity(TestCase):
    def test_entity(self):
        number = 3
        name = "TestLevel"
        words = []
        le = LevelEntity(number=number, name=name, words=words)
        self.assertEqual(le.number, number)
        self.assertEqual(le.name, name)
        self.assertEqual(le.words, words)

    def test_add(self):
        le = LevelEntity(number=3, name="TestLevel")
        self.assertListEqual(le.words, [])
        word_entity1 = WordEntity(id=1, word_a="essential", word_b="translate_word1")
        word_entity2 = WordEntity(id=2, word_a="appropriate", word_b="translate_word2")
        exptected = [word_entity1, word_entity2]
        for word in exptected:
            le.add_word(word)

        self.assertListEqual(le.words, exptected)


class TestCourseEntity(TestCase):
    def test_entity(self):
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
        self.assertEqual(ce.id, id)
        self.assertEqual(ce.name, name)
        self.assertEqual(ce.url, url)
        self.assertEqual(ce.difficult, difficult)
        self.assertEqual(ce.num_words, num_things)
        self.assertEqual(ce.num_levels, num_levels)
        self.assertEqual(ce.difficult_url, difficult_url)

    def test_add_level(self):
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
        level1 = LevelEntity(number=1, name="TestLevel1")
        level2 = LevelEntity(number=2, name="TestLevel2")
        expected = [level1, level2]
        for level in expected:
            ce.add_level(level)

        self.assertListEqual(ce.levels, expected)


class TestDashboardEntity(TestCase):
    def setUp(self) -> None:
        self.de = DashboardEntity()

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

    def test_offset(self):
        result = self.de.offset()
        keys = ["courses_filter", "offset", "limit", "get_review_count", "category_id"]
        self.assertEqual(list(result.keys()), keys)
