from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity, LevelEntity
    from memrise.core.modules.actions.aggregator import ActionsAggregator
    from memrise.core.modules.actions.base import Actions
    from memrise.core.modules.selectors import DiffContainer


RepositoryT = TypeVar("RepositoryT")


@dataclass
class Repository(Generic[RepositoryT], ABC):
    actions: ActionsAggregator

    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def get_levels(self, courses: List[CourseEntity]) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    def save_courses(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""
        self._apply_diff(self.actions.course, diff)

    def save_levels(self, diff: DiffContainer) -> None:
        """Сохранение уровней в хранилище"""
        self._apply_diff(self.actions.level, diff)

    def save_words(self, diff: DiffContainer) -> None:
        """Сохранение слов в хранилище"""
        self._apply_diff(self.actions.word, diff)

    def _apply_diff(self, actions: Actions, diff: DiffContainer) -> None:
        """Применение действий по различиям"""
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)
