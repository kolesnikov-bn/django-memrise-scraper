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
from memrise.core.modules.api import async_api, api
from memrise.core.modules.factories.factories import factory_mapper
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Level

if TYPE_CHECKING:
    from memrise.core.modules.selectors import DiffContainer
    from memrise.core.modules.parsing.base import Parser
    from memrise.shares.types import URL
    from memrise.core.domains.entities import CourseEntity, WordEntity, LevelEntity
    from memrise.core.modules.actions import Actions
    from memrise.core.modules.dashboard_counter import DashboardCounter


RepositoryT = TypeVar("RepositoryT")


@dataclass  # type: ignore
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    @abstractmethod
    def save_courses(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""

    @abstractmethod
    def save_levels(self, diff: DiffContainer) -> None:
        """Сохранение уровней в хранилище"""

    @abstractmethod
    def save_words(self, diff: DiffContainer) -> None:
        """Сохранение слов в хранилище"""


@dataclass
class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    dashboard_fixture: Path
    levels_fixture: Path

    def get_courses(self) -> List[CourseEntity]:
        with self.dashboard_fixture.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        return factory_mapper.seek(courses_response.courses)

    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        with self.levels_fixture.open() as f:
            response = json.loads(f.read())

        level_structs = [LevelStruct(**level) for level in response]
        return factory_mapper.seek(level_structs)

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer) -> None:
        pass

    def save_words(self, diff: DiffContainer) -> None:
        pass


@dataclass
class DBRep(Repository):
    """Работа с данными в БД"""

    def get_courses(self) -> List[CourseEntity]:
        course_entities = factory_mapper.seek(Course.objects.all())
        return sorted(course_entities, key=attrgetter("id"))

    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        # TODO: пересмотреть логику получения слов и уровней.
        course_records = (
            Course.objects.all()
            .prefetch_related("levels")
            .prefetch_related("levels__words")
        )

        level_records_with_words = []
        for course in course_records:
            for level in course.levels.all():
                level.entity_words = self._get_word_entities(level)
                level_records_with_words.append(level)

        if level_records_with_words:
            level_entities = factory_mapper.seek(level_records_with_words)
            return sorted(level_entities, key=attrgetter("id"))
        else:
            return []

    def _get_word_entities(self, level_record: Level) -> List[WordEntity]:
        if word_records := level_record.words.all():
            return factory_mapper.seek(word_records)
        else:
            return []

    def save_courses(self, diff: DiffContainer) -> None:
        actions = CourseActions()
        self._apply_diff(actions, diff)

    def save_levels(self, diff: DiffContainer) -> None:
        actions = LevelActions()
        self._apply_diff(actions, diff)

    def save_words(self, diff: DiffContainer) -> None:
        actions = WordActions()
        self._apply_diff(actions, diff)

    def _apply_diff(self, actions: Actions, diff: DiffContainer) -> None:
        """Применение действий по различиям"""
        # TODO: пересмотреть систему selectors/actions Diff, и вызов действий.
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)


@dataclass
class MemriseRep(Repository):
    """Получение данных из Memrise по API"""

    parser: Parser
    counter: DashboardCounter

    def get_courses(self) -> List[CourseEntity]:
        self.counter.reset()
        course_entities = []
        while True:
            response = api.load_dashboard_courses(self.counter.next())
            courses_response = CoursesResponse(**response)
            course_entities.extend(factory_mapper.seek(courses_response.courses))

            if courses_response.has_more_courses is False:
                break

        return sorted(course_entities, key=attrgetter("id"))

    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        urls = [url for course_entity in courses for url in course_entity.levels_url]
        level_entities = asyncio.run(self._bulk_crawl(urls))
        return sorted(level_entities, key=attrgetter("id"))

    async def _bulk_crawl(self, urls: List[URL]) -> List[LevelEntity]:
        tasks = [self._fetch_level_and_parse(url=url) for url in urls]
        return await asyncio.gather(*tasks)

    async def _fetch_level_and_parse(self, url: URL) -> LevelEntity:
        html = await async_api.get_level(url)
        level_number = int(Path(url).stem)
        return self.parser.parse(html, level_number)

    def save_courses(self, diff: DiffContainer) -> None:
        pass

    def save_levels(self, diff: DiffContainer) -> None:
        pass

    def save_words(self, diff: DiffContainer) -> None:
        pass
