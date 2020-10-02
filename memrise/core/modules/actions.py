from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from string import Template
from typing import TypeVar, List

from memrise import logger
from memrise.core.domains.entities import WordEntity, LevelEntity, CourseEntity
from memrise.models import Course, Level, Word

EntityT = TypeVar("EntityT", WordEntity, LevelEntity, CourseEntity)


@dataclass
class Actions(ABC):
    @abstractmethod
    def report(self, entities: List[CourseEntity], msg: str) -> None:
        """Логирование события в действии"""

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
    def report(self, entities: List[CourseEntity], msg: str) -> None:
        item_count = len(entities)
        item_ids = [item_entity.id for item_entity in entities]
        logger_msg = Template(msg).substitute(item_count=item_count, item_ids=item_ids)
        logger.info(logger_msg)

    def create(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Добавление новых курсов")
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
        self.report(entities, "Обновление курсов")
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
        self.report(entities, "Курсы без изменений[")

    def delete(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Удаление курсов[")
        for item in entities:
            Course.objects.get(id=item.id).delete()


@dataclass
class LevelActions(Actions):
    def report(self, entities: List[LevelEntity], msg: str) -> None:
        maps = defaultdict(list)
        [maps[entity.course_id].append(entity) for entity in entities]

        for course_id, item_entities in maps.items():
            item_count = len(item_entities)
            item_ids = [item_entity.id for item_entity in item_entities]
            logger_msg = Template(msg).substitute(
                course_id=course_id, item_count=item_count, item_ids=item_ids
            )
            logger.info(logger_msg)

    def create(self, entities: List[LevelEntity]) -> None:
        msg = "Курс $course_id --> Добавление новых уровней[$item_count]: $item_ids"
        self.report(entities, msg)

        for item in entities:
            Level.objects.create(
                id=item.id,
                name=item.name,
                number=item.number,
                course_id=item.course_id,
            )

    def update(self, entities: List[LevelEntity]) -> None:
        msg = "Курс $course_id --> Обновление уровней[$item_count]: $item_ids"
        self.report(entities, msg)

        for item in entities:
            Level.objects.filter(id=item.id, course_id=item.course_id).update(
                name=item.name
            )

    def equal(self, entities: List[LevelEntity]) -> None:
        msg = "Курс $course_id --> Уровни без изменений[$item_count]: $item_ids"
        self.report(entities, msg)

    def delete(self, entities: List[LevelEntity]) -> None:
        msg = "Курс $course_id -->  Удаление уровней[$item_count]: $item_ids"
        self.report(entities, msg)
        for item in entities:
            Level.objects.get(id=item.id, course_id=item.course_id).delete()


@dataclass
class WordActions(Actions):
    def report(self, entities: List[WordEntity], msg: str) -> None:
        maps = defaultdict(list)
        [maps[entity.level_id].append(entity) for entity in entities]

        for level_id, item_entities in maps.items():
            item_count = len(item_entities)
            item_ids = [item_entity.id for item_entity in item_entities]
            logger_msg = Template(msg).substitute(
                level_id=level_id, item_count=item_count, item_ids=item_ids
            )
            logger.info(logger_msg)

    def create(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Добавление новых слов[$item_count]: $item_ids"
        self.report(entities, msg)

        for item in entities:
            Word.objects.create(
                id=item.id,
                level_id=item.level_id,
                word_a=item.word_a,
                word_b=item.word_b,
            )

    def update(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Обновление слов[$item_count]: $item_ids"
        self.report(entities, msg)

        for item in entities:
            Word.objects.filter(id=item.id).update(
                word_a=item.word_a, word_b=item.word_b,
            )

    def equal(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Слова без изменений[$item_count]: $item_ids"
        self.report(entities, msg)

    def delete(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Удаление слов[$item_count]: $item_ids"
        self.report(entities, msg)

        for item in entities:
            Word.objects.get(id=item.id).delete()
