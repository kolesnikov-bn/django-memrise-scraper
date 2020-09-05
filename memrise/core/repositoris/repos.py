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
from memrise.shares.contants import DASHBOARD_FIXTURE, LEVELS_FIXTURE


@dataclass  # type: ignore
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице

        :param dashboard: фильтры для итерационного запроса получения курсов
        """
        raise NotImplementedError(
            "The `get_courses` method must be implemented in derived class"
        )

    @abstractmethod
    def fetch_levels(self, course: CourseEntity) -> List[LevelEntity]:
        """Стягивание уровней курса"""
        raise NotImplementedError(
            "The `fetch_levels` method must be implemented in derived class"
        )

    @abstractmethod
    def save_course(self, course: CourseEntity) -> None:
        """Сохранение курса в хранилище"""
        raise NotImplementedError(
            "The `save_courses` method must be implemented in derived class"
        )


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
            levels = [LevelEntity(**x) for x in level_entities[course.id]]

        return levels

    def get_courses(self) -> List[CourseEntity]:
        course_maker = CoursesMaker()
        with self.dashboard_fixture.open() as f:
            dashboard_fixtures = json.loads(f.read())

        courses_response = CoursesResponse(**dashboard_fixtures)
        course_maker.make(courses_response.iterator())

        return course_maker.courses

    def save_course(self, course: CourseEntity) -> None:
        pass
