from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar, TYPE_CHECKING

from memrise.core.repositories.setters.setters import RepositorySetter

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity, LevelEntity

RepositoryT = TypeVar("RepositoryT")


@dataclass
class Repository(Generic[RepositoryT], ABC):
    setter: RepositorySetter

    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        """Стягивание уровней курса"""
