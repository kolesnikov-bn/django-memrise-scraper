from abc import ABC, abstractmethod
from collections import defaultdict
from string import Template
from typing import TypeVar, List

from memrise import logger
from memrise.core.domains.entities import WordEntity, LevelEntity, CourseEntity
from memrise.models import Course, Level, Word

EntityT = TypeVar("EntityT", WordEntity, LevelEntity, CourseEntity)
# TODO: пересмотреть механизм работы с действиями и даными.
# TODO: а еще при появлении новых действий например для MemriseAPI будет усложняться и увеличиваться логика


class Reporter:
    def report(self):
        pass


class Actions(ABC):
    @abstractmethod
    def report(self, entities: List[EntityT], msg: str) -> None:
        """Логирование события в действии"""
        # TODO: report можно вынести от сюда в отдельный класс

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


class CourseDBActions(Actions):
    def report(self, entities: List[CourseEntity], msg: str) -> None:
        item_count = len(entities)
        item_ids = [item_entity.id for item_entity in entities]
        logger_msg = Template(msg).substitute(item_count=item_count, id_items=item_ids)
        logger.info(logger_msg)

    def create(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Добавление новых курсов[$item_count]: $id_items")

        courses = []
        for item in entities:
            courses.append(
                Course(
                    id=item.id,
                    name=item.name,
                    url=item.url,
                    difficult=item.difficult,
                    num_things=item.num_words,
                    num_levels=item.num_levels,
                    difficult_url=item.difficult_url,
                )
            )

        Course.objects.bulk_create(courses)

    def update(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Обновление курсов[$item_count]: $id_items")

        courses = []
        for item in entities:
            courses.append(
                Course(
                    id=item.id,
                    name=item.name,
                    url=item.url,
                    difficult=item.difficult,
                    num_things=item.num_words,
                    num_levels=item.num_levels,
                    difficult_url=item.difficult_url,
                )
            )

        Course.objects.bulk_update(
            courses,
            ["name", "url", "difficult", "num_things", "num_levels", "difficult_url"],
        )

    def equal(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Курсы без изменений[$item_count]: $id_items")

    def delete(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Удаление курсов[$item_count]: $id_items")

        courses = []
        for item in entities:
            courses.append(item.id)

        Course.objects.filter(id__in=courses).delete()


class LevelDBActions(Actions):
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

        levels = []
        for item in entities:
            levels.append(
                Level(
                    id=item.id,
                    name=item.name,
                    number=item.number,
                    course_id=item.course_id,
                )
            )

        Level.objects.bulk_create(levels)

    def update(self, entities: List[LevelEntity]) -> None:
        msg = "Курс $course_id --> Обновление уровней[$item_count]: $item_ids"
        self.report(entities, msg)

        levels = []
        for item in entities:
            levels.append(Level(id=item.id, course_id=item.course_id, name=item.name))

        Level.objects.bulk_update(levels, ["name"])

    def equal(self, entities: List[LevelEntity]) -> None:
        msg = "Курс $course_id --> Уровни без изменений[$item_count]: $item_ids"
        self.report(entities, msg)

    def delete(self, entities: List[LevelEntity]) -> None:
        msg = "Курс $course_id -->  Удаление уровней[$item_count]: $item_ids"
        self.report(entities, msg)

        levels = []
        for item in entities:
            levels.append(item.id)

        Level.objects.filter(id__in=levels).delete()


class WordDBActions(Actions):
    def report(self, entities: List[WordEntity], msg: str) -> None:
        maps = defaultdict(list)
        [maps[entity.level_id].append(entity) for entity in entities]

        for level_id, item_entities in maps.items():
            item_count = len(item_entities)
            id_items = [item_entity.id for item_entity in item_entities]
            logger_msg = Template(msg).substitute(
                level_id=level_id, item_count=item_count, id_items=id_items
            )
            logger.info(logger_msg)

    def create(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Добавление новых слов[$item_count]: $id_items"
        self.report(entities, msg)

        words = []
        for item in entities:
            words.append(
                Word(
                    id=item.id,
                    level_id=item.level_id,
                    word_a=item.word_a,
                    word_b=item.word_b,
                )
            )

        Word.objects.bulk_create(words)

    def update(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Обновление слов[$item_count]: $id_items"
        self.report(entities, msg)

        words = []
        for item in entities:
            words.append(Word(id=item.id))

        Word.objects.bulk_update(words, ["word_a", "word_b"])

    def equal(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Слова без изменений[$item_count]: $id_items"
        self.report(entities, msg)

    def delete(self, entities: List[WordEntity]) -> None:
        msg = "Уровень $level_id --> Удаление слов[$item_count]: $id_items"
        self.report(entities, msg)

        words = []
        for item in entities:
            words.append(item.id)

        Word.objects.filter(id__in=words).delete()
