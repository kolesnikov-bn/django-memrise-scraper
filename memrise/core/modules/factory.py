"""
Фабрики по созданию базовых объектов
"""

from __future__ import annotations

from dataclasses import field
from typing import Generator, TypeVar, List
from urllib.parse import urljoin

from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import CourseEntity
from memrise.core.responses.course_response import CourseItemResponse
from memrise.shares.contants import DIFFICULT_ITEM_URL

CoursesMakerT = TypeVar("CoursesMakerT", CourseItemResponse, CourseItemResponse)


@dataclass
class CoursesMaker:
    courses: List[CourseEntity] = field(default_factory=list)

    def make(self, items: Generator[CoursesMakerT, None, None]) -> List[CourseEntity]:
        for item in items:
            attrs = {
                "id": item.id,
                "name": item.name,
                "url": item.url,
                "difficult": item.difficult,
                "num_words": item.num_things,
                "num_levels": item.num_levels,
                "difficult_url": urljoin(item.url, DIFFICULT_ITEM_URL),
            }
            ce = CourseEntity(**attrs)
            ce.generate_levels_url()

            self._append(ce)

        return self.courses

    def _append(self, item):
        self.courses.append(item)
