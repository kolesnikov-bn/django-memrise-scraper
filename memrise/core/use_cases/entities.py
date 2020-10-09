from dataclasses import field
from operator import attrgetter
from typing import List

from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import CourseEntity


@dataclass
class Dashboard:
    course_entities: List[CourseEntity] = field(default_factory=list)

    def add_course(self, course: CourseEntity) -> None:
        """Добавление курса в dashboard"""
        self.course_entities.append(course)

    def add_courses(self, courses: List[CourseEntity]) -> None:
        """Массовое добавление курсов в dashboard"""
        self.course_entities = courses

    def get_courses(self) -> List[CourseEntity]:
        """Получение отсортированного списока курсов"""
        return sorted(self.course_entities, key=attrgetter("id"))

    def purge(self) -> None:
        """Очищение dashboard, удаление курсов"""
        self.course_entities = []
