"""
Репозитории проекта
===================

"""
from __future__ import annotations

import json
from abc import abstractmethod, ABC
from dataclasses import field
from operator import attrgetter
from pathlib import Path
from typing import Generic, List, TYPE_CHECKING, TypeVar

from pydantic import FilePath
from pydantic.dataclasses import dataclass

from memrise.core.modules.actions import CourseActions, LevelActions, WordActions
from memrise.core.modules.api.base import api
from memrise.core.modules.dashboard_counter import DashboardCounter
from memrise.core.modules.factories.factories import factory_mapper
from memrise.core.modules.parsing.regular_lxml import RegularLXML
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Level
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
    def save_words(self, diff: DiffContainer, level: Level) -> None:
        """Сохранение слов в хранилище"""

    @abstractmethod
    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        """Получение курса по сущности курса"""


class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    dashboard_fixture: FilePath = DASHBOARD_FIXTURE
    levels_fixture: FilePath = LEVELS_FIXTURE

    def get_courses(self) -> List[CourseEntity]:
        with self.dashboard_fixture.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        return factory_mapper.seek(courses_response.courses)

    def get_levels(self, course: CourseEntity) -> List[LevelEntity]:
        with self.levels_fixture.open() as f:
            levels_map = json.loads(f.read())

        response = [LevelStruct(**level) for level in levels_map]
        levels = factory_mapper.seek(response)
        levels = [level for level in levels if level.course_id == course.id]

        return levels

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer, course: Course) -> None:
        pass

    def save_words(self, diff: DiffContainer, level: Level) -> None:
        pass

    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        pass


class DBRep(Repository):
    """Работа с данными в БД"""

    def get_courses(self) -> List[CourseEntity]:
        courses = factory_mapper.seek(Course.objects.all())
        return sorted(courses, key=attrgetter("id"))

    def get_levels(self, course: CourseEntity) -> List[LevelEntity]:
        try:
            levels = Course.objects.get(id=course.id).level_set.all()
        except Course.DoesNotExist:
            raise ValueError(f"Курс {course.id} не найден в БД")

        levels_with_words = []
        for level in levels:
            level.words = self._get_words(level)
            levels_with_words.append(level)

        if levels_with_words:
            levels_entity = factory_mapper.seek(levels_with_words)
            return sorted(levels_entity, key=attrgetter("id"))
        else:
            return []

    def _get_words(self, level: Level) -> List[WordEntity]:
        words = level.word_set.all()

        if words:
            return factory_mapper.seek(words)
        else:
            return []

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

    def save_words(self, diff: DiffContainer, level: Level) -> None:
        actions = WordActions(level_parent=level)
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)

    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        return Course.objects.get(id=course_entity.id)


class MemriseRep(Repository):
    """Получение данных из Memrise по API"""

    parser: Parser = field(init=False)

    def __post_init__(self) -> None:
        self.parser = RegularLXML()

    def get_courses(self) -> List[CourseEntity]:
        counter = DashboardCounter()
        data = []
        while True:
            response = api.load_dashboard_courses(counter.next())
            courses_response = CoursesResponse(**response)
            data.extend(factory_mapper.seek(courses_response.courses))

            if courses_response.has_more_courses is False:
                break

        return sorted(data, key=attrgetter("id"))

    def get_levels(self, course: CourseEntity) -> List[LevelEntity]:
        levels = []
        for url in course.levels_url:
            level_number = int(Path(url).stem)
            level = self._get_level(url, level_number)
            levels.append(level)

        return sorted(levels, key=attrgetter("id"))

    def _get_level(self, endpoint: URL, level_number: int) -> LevelEntity:
        response = api.get_level(endpoint)
        level = self.parser.parse(response, level_number)
        return level

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer, course: Course) -> None:
        pass

    def save_words(self, diff: DiffContainer, level: Level) -> None:
        pass

    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        pass
