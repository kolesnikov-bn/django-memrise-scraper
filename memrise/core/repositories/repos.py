"""
Репозитории проекта
===================

"""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from operator import attrgetter
from pathlib import Path
from typing import List, TYPE_CHECKING

from memrise.core.modules.actions.base import Actions
from memrise.core.modules.api import async_api, api
from memrise.core.modules.factories.factories import factory_mapper
from memrise.core.modules.selectors import DiffContainer
from memrise.core.repositories.base import Repository
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Level
from memrise.shares.contants import DASHBOARD_FIXTURE, LEVELS_FIXTURE

if TYPE_CHECKING:
    from memrise.core.modules.counter import MemriseRequestCounter
    from memrise.core.modules.parsing.base import Parser
    from memrise.shares.types import URL
    from memrise.core.domains.entities import CourseEntity, WordEntity, LevelEntity


@dataclass
class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    def get_courses(self) -> List[CourseEntity]:
        with DASHBOARD_FIXTURE.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        return factory_mapper.seek(courses_response.courses)

    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        with LEVELS_FIXTURE.open() as f:
            response = json.loads(f.read())

        level_structs = [LevelStruct(**level) for level in response]
        return factory_mapper.seek(level_structs)

    def update_courses(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.course, diff)

    def update_levels(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.level, diff)

    def update_words(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.word, diff)

    def _apply_diff(self, actions: Actions, diff: DiffContainer) -> None:
        """Применение конкретных команд к расхождениям данных"""
        actions.create(diff.create)
        actions.update(diff.update)
        actions.delete(diff.delete)
        actions.equal(diff.equal)


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

    def update_courses(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.course, diff)

    def update_levels(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.level, diff)

    def update_words(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.word, diff)

    def _apply_diff(self, actions: Actions, diff: DiffContainer) -> None:
        """Применение конкретных команд к расхождениям данных"""
        actions.create(diff.create)
        actions.update(diff.update)
        actions.delete(diff.delete)
        actions.equal(diff.equal)


@dataclass
class MemriseRep(Repository):
    """Получение данных из Memrise по API"""

    parser: Parser
    counter: MemriseRequestCounter

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

    def update_courses(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.course, diff)

    def update_levels(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.level, diff)

    def update_words(self, diff: DiffContainer) -> None:
        self._apply_diff(self.assembler.word, diff)

    def _apply_diff(self, actions: Actions, diff: DiffContainer) -> None:
        """Применение конкретных команд к расхождениям данных"""
        actions.create(diff.create)
        actions.update(diff.update)
        actions.delete(diff.delete)
        actions.equal(diff.equal)
