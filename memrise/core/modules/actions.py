from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, List

from memrise import logger
from memrise.core.domains.entities import WordEntity, LevelEntity, CourseEntity
from memrise.models import Course, Level, Word

EntityT = TypeVar("EntityT", WordEntity, LevelEntity, CourseEntity)


@dataclass
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


@dataclass
class CourseActions(Actions):
    def create(self, entities: List[CourseEntity]) -> None:
        logger.info(f"Добавление новых курсов[{len(entities)}]: {[x.id for x in entities]}")
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
        logger.info(f"Обновление курсов[{len(entities)}]: {[x.id for x in entities]}")
        for item in entities:
            Course.objects.filter(id=item.id).update(
                name=item.name,
                url=item.url,
                difficult=item.difficult,
                num_things=item.num_words,
                num_levels=item.num_levels,
                difficult_url=item.difficult_url,
            )

    def equal(self, entities: List[CourseEntity]) -> None:
        logger.info(f"Курсы без изменений[{len(entities)}]: {[x.id for x in entities]}")

    def delete(self, entities: List[CourseEntity]) -> None:
        logger.info(f"Удаление курсов[{len(entities)}]: {[x.id for x in entities]}")
        for item in entities:
            Course.objects.get(id=item.id).delete()


@dataclass
class LevelActions(Actions):
    parent_course: Course

    def create(self, entities: List[LevelEntity]) -> None:
        logger.info(
            f"Курс {self.parent_course.id} --> Добавление новых уровней[{len(entities)}]: {[x.id for x in entities]}"
        )
        for item in entities:
            Level.objects.create(
                id=item.id, name=item.name, number=item.number, course=self.parent_course
            )

    def update(self, entities: List[LevelEntity]) -> None:
        logger.info(
            f"Курс {self.parent_course.id} --> Обновление уровней[{len(entities)}]: {[x.id for x in entities]}"
        )
        for item in entities:
            Level.objects.filter(id=item.id, course=self.parent_course).update(
                name=item.name
            )

    def equal(self, entities: List[LevelEntity]) -> None:
        logger.info(
            f"Курс {self.parent_course.id} --> Уровни без изменений[{len(entities)}]: {[x.id for x in entities]}"
        )

    def delete(self, entities: List[LevelEntity]) -> None:
        logger.info(
            f"Курс {self.parent_course.id} --> Удаление уровней[{len(entities)}]: {[x.id for x in entities]}"
        )
        for item in entities:
            Level.objects.get(
                id=item.id, course=self.parent_course.id
            ).delete()


@dataclass
class WordActions(Actions):
    level_parent: Level

    def create(self, entities: List[WordEntity]) -> None:
        header = f"Курс {self.level_parent.course.id} --> Уровень {self.level_parent.number} -->"
        logger.info(f"{header} Добавление новых слов[{len(entities)}]: {[x.id for x in entities]}")
        for item in entities:
            Word.objects.create(
                id=item.id,
                level=self.level_parent,
                word_a=item.word_a,
                word_b=item.word_b,
            )

    def update(self, entities: List[WordEntity]) -> None:
        header = f"Курс {self.level_parent.course.id} --> Уровень {self.level_parent.number} -->"
        logger.info(f"{header} Обновление слов[{len(entities)}]: {[x.id for x in entities]}")
        for item in entities:
            Word.objects.filter(id=item.id).update(
                word_a=item.word_a,
                word_b=item.word_b,
            )

    def equal(self, entities: List[WordEntity]) -> None:
        header = f"Курс {self.level_parent.course.id} --> Уровень {self.level_parent.number} -->"
        logger.info(f"{header} Слова без изменений[{len(entities)}]: {[x.id for x in entities]}")

    def delete(self, entities: List[WordEntity]) -> None:
        header = f"Курс {self.level_parent.course.id} --> Уровень {self.level_parent.number} -->"
        logger.info(f"{header} Удаление слов[{len(entities)}]: {[x.id for x in entities]}")
        for item in entities:
            Word.objects.get(id=item.id).delete()
