"""
Репозитории проекта
===================

"""
import json
from abc import abstractmethod, ABC
from typing import Generic, List, Generator

from pydantic import FilePath
from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import (
    RepositoryT,
    CourseEntity,
    LevelEntity, WordEntity,
)
from memrise.core.modules.factory import CoursesMaker, WordMaker
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.use_cases.selectors import DiffContainer
from memrise.models import Course, Word
from memrise.shares.contants import DASHBOARD_FIXTURE, LEVELS_FIXTURE


@dataclass
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def fetch_levels(self, course: CourseEntity) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    @abstractmethod
    def save_course(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""


class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    dashboard_fixture: FilePath = DASHBOARD_FIXTURE
    levels_fixture: FilePath = LEVELS_FIXTURE

    def fetch_levels(self, course: CourseEntity) -> List[LevelEntity]:
        levels = []
        with self.levels_fixture.open() as f:
            levels_map = json.loads(f.read())

        level_entities = {
            item["id"]: item["levels"] for item in levels_map if item["id"] == course.id
        }
        if level_entities:
            levels = []
            for item in level_entities[course.id]:
                item["course_id"] = course.id
                levels.append(LevelEntity(**item))

        return levels

    def get_courses(self) -> List[CourseEntity]:
        with self.dashboard_fixture.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        course_maker = CoursesMaker()
        course_maker.make(courses_response.iterator())

        return course_maker.courses

    def save_course(self, diff: DiffContainer) -> None:
        pass


class DBRep(Repository):
    """Работа с данными в БД"""

    def get_courses(self) -> List[CourseEntity]:
        course_maker = CoursesMaker()
        courses = course_maker.make(Course.objects.iterator())
        return courses

    def fetch_levels(self, course: CourseEntity) -> Generator[LevelEntity, None, None]:
        try:
            level_entries = Course.objects.get(id=course.id).level_set.all()
        except Course.DoesNotExist:
            raise ValueError(f"Курс {course.id} не найден в БД")

        for level in level_entries:
            words = self._fetch_words(level.word_set.iterator())
            yield LevelEntity(number=level.number, course_id=course.id, name=level.name, words=words)

    def _fetch_words(self, words: Generator[Word, None, None]) -> Generator[WordEntity, None, None]:
        wm = WordMaker()
        yield from wm.make(words)

    def save_course(self, diff: DiffContainer) -> None:
        pass
