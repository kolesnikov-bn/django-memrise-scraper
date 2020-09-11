"""
Репозитории проекта
===================

"""
from __future__ import annotations

import json
from abc import abstractmethod, ABC
from dataclasses import field
from pathlib import Path
from typing import Generic, List, Generator, TYPE_CHECKING, TypeVar

from pydantic import FilePath
from pydantic.dataclasses import dataclass

from memrise.core.modules.actions import CourseActions, LevelActions, WordActions
from memrise.core.modules.api.base import api
from memrise.core.modules.dashboard_counter import DashboardCounter
from memrise.core.modules.factories import (
    CourseEntityMaker,
    WordEntityMaker,
    LevelEntityMaker,
)
from memrise.core.modules.parsing.regular_lxml import RegularLXML
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Word, Level
from memrise.shares.contants import DASHBOARD_FIXTURE, LEVELS_FIXTURE

if TYPE_CHECKING:
    from memrise.core.modules.selectors import DiffContainer
    from memrise.core.modules.parsing.base import Parser
    from memrise.shares.types import URL
    from memrise.core.domains.entities import CourseEntity, WordEntity, LevelEntity


RepositoryT = TypeVar("RepositoryT")


@dataclass
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def get_levels(self, course: CourseEntity) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    @abstractmethod
    def save_courses(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""

    @abstractmethod
    def save_levels(self, diff: DiffContainer, course: Course) -> None:
        """Сохранение уровней в хранилище"""

    @abstractmethod
    def save_words(self, diff: DiffContainer, level: Level):
        """Сохранение слов в хранилище"""


class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    dashboard_fixture: FilePath = DASHBOARD_FIXTURE
    levels_fixture: FilePath = LEVELS_FIXTURE

    def get_courses(self) -> List[CourseEntity]:
        with self.dashboard_fixture.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        course_maker = CourseEntityMaker()
        course_maker.make(courses_response.iterator())

        return course_maker.data

    def get_levels(self, course: CourseEntity) -> List[LevelEntity]:
        with self.levels_fixture.open() as f:
            levels_map = json.loads(f.read())

        response = [LevelStruct(**level) for level in levels_map]
        maker = LevelEntityMaker()
        levels = maker.make(response)
        levels = [level for level in levels if level.course_id == course.id]

        return levels

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer, course: Course) -> None:
        pass

    def save_words(self, diff: DiffContainer, level: Level):
        pass


class DBRep(Repository):
    """Работа с данными в БД"""

    def get_courses(self) -> List[CourseEntity]:
        course_maker = CourseEntityMaker()
        courses = course_maker.make(Course.objects.iterator())
        return courses

    def get_levels(self, course: CourseEntity) -> Generator[LevelEntity, None, None]:
        try:
            levels = Course.objects.get(id=course.id).level_set.all()
        except Course.DoesNotExist:
            raise ValueError(f"Курс {course.id} не найден в БД")

        levels_with_words = []
        for level in levels:
            level.words = self._get_words(level.word_set.iterator())
            levels_with_words.append(level)

        maker = LevelEntityMaker()
        yield from maker.make(levels_with_words)

    def _get_words(
        self, words: Generator[Word, None, None]
    ) -> Generator[WordEntity, None, None]:
        wm = WordEntityMaker()
        yield from wm.make(words)

    def save_courses(self, diff: DiffContainer) -> None:
        actions = CourseActions()
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)

    def save_levels(self, diff: DiffContainer, course: Course) -> None:
        actions = LevelActions(parent_course=course)
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)

    def save_words(self, diff: DiffContainer, level: Level):
        actions = WordActions(level_parent=level)
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)


class MemriseRep(Repository):
    """Получение данных из Memrise по API"""

    parser: Parser = field(init=False)

    def __post_init__(self) -> None:
        self.parser = RegularLXML()

    def get_courses(self) -> List[CourseEntity]:
        course_maker = CourseEntityMaker()
        counter = DashboardCounter()
        while True:
            response = api.load_dashboard_courses(counter.next())
            courses_response = CoursesResponse(**response)
            course_maker.make(courses_response.iterator())

            if courses_response.has_more_courses is False:
                break

        return course_maker.data

    def get_levels(self, course: CourseEntity) -> List[LevelEntity]:
        levels = []
        for url in course.levels_url:
            level_number = int(Path(url).stem)
            level = self._get_level(url, level_number)
            levels.append(level)

        return levels

    def _get_level(self, endpoint: URL, level_number: int) -> LevelEntity:
        response = api.get_level(endpoint)
        level = self.parser.parse(response, level_number)
        return level

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer, course: Course) -> None:
        pass

    def save_words(self, diff: DiffContainer, level: Level):
        pass
