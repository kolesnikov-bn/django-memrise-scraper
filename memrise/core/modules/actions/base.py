from abc import ABC, abstractmethod
from typing import List, ClassVar, TypeVar

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity

EntityT = TypeVar("EntityT", WordEntity, LevelEntity, CourseEntity)


class Actions(ABC):
    prefix: ClassVar[str] = ""
    postfix: ClassVar[str] = "[$total]: $id_items"

    @abstractmethod
    def report(self, entities: List[EntityT], msg: str) -> None:
        """Логирование событий действий"""

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
