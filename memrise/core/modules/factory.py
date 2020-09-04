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
    data: List[CourseEntity] = field(default_factory=list)

    def make(self, courses: Generator[CoursesMakerT, None, None]) -> List[CourseEntity]:
        for course in courses:
            attrs = {
                "id": course.id,
                "name": course.name,
                "url": course.url,
                "difficult": course.difficult,
                "num_words": course.num_things,
                "num_levels": course.num_levels,
                "difficult_url": urljoin(course.url, DIFFICULT_ITEM_URL),
            }
            ce = CourseEntity(**attrs)
            ce.generate_levels_url()

            self._append(ce)

        return self.data

    def _append(self, item):
        self.data.append(item)
