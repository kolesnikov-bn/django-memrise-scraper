from __future__ import annotations

from operator import attrgetter
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity


class Dashboard:
    def __init__(self):
        self.courses: List[CourseEntity] = []

    def add_course(self, course: CourseEntity) -> None:
        """Добавление курса в dashboard"""
        self.courses.append(course)

    def add_courses(self, courses: List[CourseEntity]) -> None:
        """Массовое добавление курсов в dashboard"""
        self.courses = courses

    def get_courses(self) -> List[CourseEntity]:
        """Получение отсортированного списока курсов"""
        return sorted(self.courses, key=attrgetter("id"))

    def purge(self) -> None:
        """Очищение dashboard, удаление курсов"""
        self.courses = []
