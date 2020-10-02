"""
Репозитории проекта
===================

"""
from __future__ import annotations

import asyncio
import json
from abc import abstractmethod, ABC
from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path
from typing import Generic, List, TYPE_CHECKING, TypeVar

from memrise.core.modules.actions import CourseActions, LevelActions, WordActions
from memrise.core.modules.api.async_api import async_api
from memrise.core.modules.api.base import api
from memrise.core.modules.dashboard_counter import DashboardCounter
from memrise.core.modules.factories.factories import factory_mapper
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Level
from memrise.shares.contants import DASHBOARD_FIXTURE, LEVELS_FIXTURE

if TYPE_CHECKING:
    from memrise.core.modules.selectors import DiffContainer
    from memrise.core.modules.parsing.base import Parser
    from memrise.shares.types import URL
    from memrise.core.domains.entities import CourseEntity, WordEntity, LevelEntity
    from memrise.core.modules.actions import Actions


RepositoryT = TypeVar("RepositoryT")


@dataclass  # type: ignore
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def get_levels(self, course_entity: CourseEntity) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    @abstractmethod
    def save_courses(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""

    @abstractmethod
    def save_levels(self, diff: DiffContainer, parent_course_record: Course) -> None:
        """Сохранение уровней в хранилище"""

    @abstractmethod
    def save_words(self, diff: DiffContainer, parent_level_record: Level) -> None:
        """Сохранение слов в хранилище"""

    @abstractmethod
    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        """Получение курса записи по сущности курса `CourseEntity`"""

    @abstractmethod
    def get_level_by_entity(self, level_entity: LevelEntity) -> Level:
        """Получение уровня записи по сущности уровня `LevelEntity`"""


@dataclass
class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    dashboard_fixture: Path = DASHBOARD_FIXTURE
    levels_fixture: Path = LEVELS_FIXTURE

    def get_courses(self) -> List[CourseEntity]:
        with self.dashboard_fixture.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        return factory_mapper.seek(courses_response.courses)

    def get_levels(self, course_entity: CourseEntity) -> List[LevelEntity]:
        with self.levels_fixture.open() as f:
            levels_map = json.loads(f.read())

        level_structs = [LevelStruct(**level) for level in levels_map]
        level_entities = factory_mapper.seek(level_structs)
        filtered_level_entities = [
            level for level in level_entities if level.course_id == course_entity.id
        ]

        return filtered_level_entities

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer, parent_course_record: Course) -> None:
        pass

    def save_words(self, diff: DiffContainer, parent_level_record: Level) -> None:
        pass

    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        pass

    def get_level_by_entity(self, level_entity: LevelEntity) -> Level:
        pass


@dataclass
class DBRep(Repository):
    """Работа с данными в БД"""

    def get_courses(self) -> List[CourseEntity]:
        course_entities = factory_mapper.seek(Course.objects.all())
        return sorted(course_entities, key=attrgetter("id"))

    def get_levels(self, course_entity: CourseEntity) -> List[LevelEntity]:
        try:
            level_records = Course.objects.get(
                id=course_entity.id
            ).levels.prefetch_related("words")
        except Course.DoesNotExist:
            raise ValueError(f"Курс {course_entity.id} не найден в БД")

        level_records_with_words = []
        for level in level_records:
            level.entity_words = self._get_entity_words(level)
            level_records_with_words.append(level)

        if level_records_with_words:
            level_entities = factory_mapper.seek(level_records_with_words)
            return sorted(level_entities, key=attrgetter("id"))
        else:
            return []

    def _get_entity_words(self, level_record: Level) -> List[WordEntity]:
        if word_records := level_record.words.all():
            return factory_mapper.seek(word_records)
        else:
            return []

    def save_courses(self, diff: DiffContainer) -> None:
        actions = CourseActions()
        self._apply_diff(actions, diff)

    def save_levels(self, diff: DiffContainer, parent_course_record: Course) -> None:
        actions = LevelActions(parent_course_record=parent_course_record)
        self._apply_diff(actions, diff)

    def save_words(self, diff: DiffContainer, parent_level_record: Level) -> None:
        actions = WordActions(parent_level_record=parent_level_record)
        self._apply_diff(actions, diff)

    def _apply_diff(self, actions: Actions, diff: DiffContainer) -> None:
        """Применение действий по различиям"""
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)

    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        return Course.objects.get(id=course_entity.id)

    def get_level_by_entity(self, level_entity: LevelEntity) -> Level:
        return Level.objects.get(id=level_entity.id)


@dataclass
class MemriseRep(Repository):
    """Получение данных из Memrise по API"""

    parser: Parser

    def get_courses(self) -> List[CourseEntity]:
        counter = DashboardCounter()
        course_entities = []
        while True:
            response = api.load_dashboard_courses(counter.next())
            courses_response = CoursesResponse(**response)
            course_entities.extend(factory_mapper.seek(courses_response.courses))

            if courses_response.has_more_courses is False:
                break

        return sorted(course_entities, key=attrgetter("id"))

    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        urls = [url for course_entity in courses for url in course_entity.levels_url]
        level_entities = asyncio.run(self._bulk_crawl(urls))
        return sorted(level_entities, key=attrgetter("id"))

    async def _bulk_crawl(self, urls: List[URL]) -> None:
        tasks = [self._fetch_level_and_parse(url=url) for url in urls]
        return await asyncio.gather(*tasks)

    async def _fetch_level_and_parse(self, url: URL) -> LevelEntity:
        html = await async_api.get_level(url)
        level_number = int(Path(url).stem)
        return self.parser.parse(html, level_number)

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer, parent_course_record: Course) -> None:
        pass

    def save_words(self, diff: DiffContainer, parent_level_record: Level) -> None:
        pass

    def get_course_by_entity(self, course_entity: CourseEntity) -> Course:
        pass

    def get_level_by_entity(self, level_entity: LevelEntity) -> Level:
        pass
