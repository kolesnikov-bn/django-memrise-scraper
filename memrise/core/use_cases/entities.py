from __future__ import annotations

from dataclasses import dataclass, field
from operator import attrgetter
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity


@dataclass
class Dashboard:
    _courses: List[CourseEntity] = field(init=False, default_factory=list)

    @property
    def courses(self):
        return self._courses

    def add_course(self, course: CourseEntity) -> None:
        """Добавление курса в dashboard"""
        self._courses.append(course)

    def add_courses(self, courses: List[CourseEntity]) -> None:
        """Массовое добавление курсов в dashboard"""
        self._courses = courses

    def get_courses(self) -> List[CourseEntity]:
        """Получение отсортированного списока курсов"""
        return sorted(self._courses, key=attrgetter("id"))

    def purge(self) -> None:
        """Очищение dashboard, удаление курсов"""
        self._courses = []
