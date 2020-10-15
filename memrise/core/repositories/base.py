from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar, TYPE_CHECKING

from memrise.core.modules.actions.aggregator import Assembler
from memrise.core.modules.selectors import DiffContainer

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity, LevelEntity

RepositoryT = TypeVar("RepositoryT")


@dataclass
class Repository(Generic[RepositoryT], ABC):
    assembler: Assembler

    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    @abstractmethod
    def update_courses(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""

    @abstractmethod
    def update_levels(self, diff: DiffContainer) -> None:
        """Сохранение уровней в хранилище"""

    @abstractmethod
    def update_words(self, diff: DiffContainer) -> None:
        """Сохранение слов в хранилище"""
