from operator import attrgetter
from typing import List

from memrise.core.domains.entities import CourseEntity


class Dashboard:
    def __init__(self):
        self.course_entities: List[CourseEntity] = list()

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
