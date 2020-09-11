"""
Фабрики по созданию базовых объектов
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import field
from typing import Generator, TypeVar, List, Generic
from urllib.parse import urljoin

from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity
from memrise.core.responses.course_response import CourseItemResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Level, Word
from memrise.shares.contants import DIFFICULT_ITEMS_URL

DomainEntityT = TypeVar("DomainEntityT", CourseEntity, LevelEntity, WordEntity)
CoursesMakerT = TypeVar("CoursesMakerT", CourseItemResponse, Course)
LevelMakerT = TypeVar("LevelMakerT", LevelStruct, Level)
WordMakerT = TypeVar("WordMakerT", Word, Word)


@dataclass
class EntityMaker(Generic[DomainEntityT], ABC):
    data: List[DomainEntityT] = field(default_factory=list)

    @abstractmethod
    def make(self, items: Generator[DomainEntityT, None, None]) -> List[DomainEntityT]:
        pass

    @abstractmethod
    def _append(self, item: DomainEntityT) -> None:
        pass


class CourseEntityMaker(EntityMaker):
    data: List[CourseEntity] = field(default_factory=list)

    def make(self, items: Generator[CoursesMakerT, None, None]) -> List[CourseEntity]:
        for item in items:
            attrs = {
                "id": item.id,
                "name": item.name,
                "url": item.url,
                "difficult": item.difficult,
                "num_words": item.num_things,
                "num_levels": item.num_levels,
                "difficult_url": urljoin(item.url, DIFFICULT_ITEMS_URL),
            }
            ce = CourseEntity(**attrs)
            ce.generate_levels_url()

            self._append(ce)

        return self.data

    def _append(self, item: CourseEntity) -> None:
        self.data.append(item)


class LevelEntityMaker(EntityMaker):
    data: List[LevelEntity] = field(default_factory=list)

    def make(self, items: Generator[LevelMakerT, None, None]) -> List[LevelEntity]:
        for item in items:
            attrs = {
                "id": item.id,
                "number": item.number,
                "course_id": item.course_id,
                "name": item.name,
                "words": [],
            }

            try:
                # Отработает если пришел LevelStruct.
                attrs["words"] = item.words
            except AttributeError:
                pass

            le = LevelEntity(**attrs)
            self._append(le)

        return self.data

    def _append(self, item: LevelEntity) -> None:
        self.data.append(item)


class WordEntityMaker(EntityMaker):
    data: List[WordEntity] = field(default_factory=list)

    def make(self, items: Generator[WordMakerT, None, None]) -> List[WordEntity]:
        for item in items:
            attrs = {
                "id": item.id,
                "word_a": item.word_a,
                "word_b": item.word_b,
            }
            le = WordEntity(**attrs)

            self._append(le)

        return self.data

    def _append(self, item: WordEntity) -> None:
        self.data.append(item)
