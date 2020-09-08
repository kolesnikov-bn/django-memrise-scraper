from abc import ABC, abstractmethod
from typing import TypeVar, List

from memrise import logger
from memrise.core.domains.entities import WordEntity, LevelEntity, CourseEntity
from memrise.models import Course

EntityT = TypeVar("EntityT", WordEntity, LevelEntity, CourseEntity)


class Actions(ABC):
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


class CourseActions(Actions):
    def create(self, entities: List[CourseEntity]) -> None:
        logger.info(f"Добавление новых курсов: {[x.id for x in entities]}")
        for item in entities:
            Course.objects.create(
                id=item.id,
                name=item.name,
                url=item.url,
                difficult=item.difficult,
                num_things=item.num_words,
                num_levels=item.num_levels,
                difficult_url=item.difficult_url,
            )

    def update(self, entities: List[CourseEntity]) -> None:
        logger.info(f"Обновление курсов: {[x.id for x in entities]}")
        for item in entities:
            Course.objects.update_or_create(
                id=item.id,
                defaults={
                    "name": item.name,
                    "url": item.url,
                    "difficult": item.difficult,
                    "num_things": item.num_words,
                    "num_levels": item.num_levels,
                    "difficult_url": item.difficult_url,
                },
            )

    def equal(self, entities: List[CourseEntity]) -> None:
        logger.info(f"Курсы без изменений: {[x.id for x in entities]}")

    def delete(self, entities: List[CourseEntity]) -> None:
        logger.info(f"Удаление курсов: {[x.id for x in entities]}")
        for item in entities:
            Course.objects.get(id=item.id).delete()
