from abc import ABC, abstractmethod
from typing import List, ClassVar, TypeVar

from pydantic import BaseModel

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity
from memrise.core.modules.actions.action_reporter import Reporter

EntityT = TypeVar("EntityT", WordEntity, LevelEntity, CourseEntity)


class Actions(BaseModel, ABC):
    reporter: Reporter
    prefix: ClassVar[str] = ""
    postfix: ClassVar[str] = "[$total]: $id_items"

    @abstractmethod
    def create(self, entities: List[EntityT]) -> None:
        """Добавление новых записей в хранилище"""

    @abstractmethod
    def update(self, entities: List[EntityT]) -> None:
        """Обновление записей в хранилище"""

    @abstractmethod
    def equal(self, entities: List[EntityT]) -> None:
        """Данные одинаковые с источником, выводим отладочную информацию"""

    @abstractmethod
    def delete(self, entities: List[EntityT]) -> None:
        """Удаление записей из хранилища, в источнике данных больше нет"""
