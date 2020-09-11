"""
Фабрики по созданию базовых объектов
"""

from __future__ import annotations

from dataclasses import field
from typing import Generator, TypeVar, List
from urllib.parse import urljoin

from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity
from memrise.core.responses.course_response import CourseItemResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Level, Word
from memrise.shares.contants import DIFFICULT_ITEMS_URL

CoursesMakerT = TypeVar("CoursesMakerT", CourseItemResponse, Course)
LevelMakerT = TypeVar("LevelMakerT", LevelStruct, Level)


@dataclass
class CourseEntityMaker:
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

    def _append(self, item):
        self.data.append(item)


@dataclass
class LevelEntityMaker:
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

    def _append(self, item):
        self.data.append(item)


@dataclass
class WordEntityMaker:
    data: List[WordEntity] = field(default_factory=list)

    def make(self, items: Generator[Word, None, None]) -> List[WordEntity]:
        for item in items:
            attrs = {
                "id": item.id,
                "word_a": item.word_a,
                "word_b": item.word_b,
            }
            le = WordEntity(**attrs)

            self._append(le)

        return self.data

    def _append(self, item):
        self.data.append(item)
