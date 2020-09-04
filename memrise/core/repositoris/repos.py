"""
Репозитории проекта
===================

"""
from abc import abstractmethod, ABC
from typing import Generic, List

from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import RepositoryT, DashboardEntity, CourseEntity, LevelEntity


@dataclass  # type: ignore
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self, dashboard: DashboardEntity) -> List[CourseEntity]:
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
