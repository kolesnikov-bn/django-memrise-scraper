"""
Репозитории проекта
===================

"""
import json
from abc import abstractmethod, ABC
from typing import Generic, List

from pydantic import FilePath
from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import (
    RepositoryT,
    CourseEntity,
    LevelEntity,
)
from memrise.core.modules.factory import CoursesMaker
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.use_cases.selectors import DiffContainer
from memrise.shares.contants import DASHBOARD_FIXTURE, LEVELS_FIXTURE


@dataclass
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def fetch_levels(self, course: CourseEntity) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    @abstractmethod
    def save_course(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""


@dataclass
class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    dashboard_fixture: FilePath = DASHBOARD_FIXTURE
    levels_fixture: FilePath = LEVELS_FIXTURE

    def fetch_levels(self, course: CourseEntity) -> List[LevelEntity]:
        levels = []
        with self.levels_fixture.open() as f:
            levels_map = json.loads(f.read())

        level_entities = {
            item["id"]: item["levels"] for item in levels_map if item["id"] == course.id
        }
        if level_entities:
            levels = []
            for item in level_entities[course.id]:
                item["course_id"] = course.id
                levels.append(LevelEntity(**item))

        return levels

    def get_courses(self) -> List[CourseEntity]:
        with self.dashboard_fixture.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        course_maker = CoursesMaker()
        course_maker.make(courses_response.iterator())

        return course_maker.courses

    def save_course(self, diff: DiffContainer) -> None:
        pass
