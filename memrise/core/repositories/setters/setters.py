from abc import ABC, abstractmethod
from dataclasses import dataclass

from memrise.core.modules.actions.aggregator import ActionsAggregator
from memrise.core.modules.actions.base import Actions
from memrise.core.modules.selectors import DiffContainer


@dataclass
class RepositorySetter(ABC):
    actions: ActionsAggregator

    @abstractmethod
    def save_courses(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""

    @abstractmethod
    def save_levels(self, diff: DiffContainer) -> None:
        """Сохранение уровней в хранилище"""

    @abstractmethod
    def save_words(self, diff: DiffContainer) -> None:
        """Сохранение слов в хранилище"""


@dataclass
class DefaultSetter(RepositorySetter):
    def save_courses(self, diff: DiffContainer) -> None:
        self._apply_diff(self.actions.course, diff)

    def save_levels(self, diff: DiffContainer) -> None:
        self._apply_diff(self.actions.level, diff)

    def save_words(self, diff: DiffContainer) -> None:
        self._apply_diff(self.actions.word, diff)

    def _apply_diff(self, actions: Actions, diff: DiffContainer) -> None:
        """Применение действий по различиям"""
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)
