from abc import ABC, abstractmethod
from collections import defaultdict
from string import Template
from typing import TypeVar, List, ClassVar

from memrise import logger
from memrise.core.domains.entities import WordEntity, LevelEntity, CourseEntity
from memrise.models import Course, Level, Word

EntityT = TypeVar("EntityT", WordEntity, LevelEntity, CourseEntity)
# TODO: пересмотреть механизм работы с действиями и даными.
# TODO: а еще при появлении новых действий например для MemriseAPI будет усложняться и увеличиваться логика


class Reporter:
    @classmethod
    def course_report(cls, entities: List[CourseEntity], msg: str) -> None:
        total = len(entities)
        id_items = [item_entity.id for item_entity in entities]
        logger_msg = Template(msg).substitute(total=total, id_items=id_items)
        logger.info(logger_msg)

    @classmethod
    def level_report(cls, entities: List[LevelEntity], msg: str) -> None:
        container = defaultdict(list)
        [container[entity.course_id].append(entity) for entity in entities]

        for course_id, items in container.items():
            total = len(items)
            id_items = [item_entity.id for item_entity in items]
            logger_msg = Template(msg).substitute(
                course_id=course_id, total=total, id_items=id_items
            )
            logger.info(logger_msg)

    @classmethod
    def word_report(cls, entities: List[WordEntity], msg: str) -> None:
        container = defaultdict(list)
        [container[entity.level_id].append(entity) for entity in entities]

        for level_id, items in container.items():
            total = len(items)
            id_items = [item_entity.id for item_entity in items]
            logger_msg = Template(msg).substitute(
                level_id=level_id, total=total, id_items=id_items
            )
            logger.info(logger_msg)


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


# <editor-fold desc="DB actions">
class DBCourseActions(Actions):
    def report(self, entities: List[CourseEntity], msg: str) -> None:
        Reporter.course_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Добавление новых курсов")

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
        self.report(entities, "Обновление курсов")

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
        self.report(entities, "Курсы без изменений")

    def delete(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Удаление курсов")

        courses = []
        for item in entities:
            courses.append(item.id)

        Course.objects.filter(id__in=courses).delete()


class DBLevelActions(Actions):
    prefix: ClassVar[str] = "Курс $course_id --> "

    def report(self, entities: List[LevelEntity], msg: str) -> None:
        Reporter.level_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Добавление новых уровней")

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
        self.report(entities, "Обновление уровней")

        levels = []
        for item in entities:
            levels.append(Level(id=item.id, course_id=item.course_id, name=item.name))

        Level.objects.bulk_update(levels, ["name"])

    def equal(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Уровни без изменений")

    def delete(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Удаление уровней")

        levels = []
        for item in entities:
            levels.append(item.id)

        Level.objects.filter(id__in=levels).delete()


class DBWordActions(Actions):
    prefix: ClassVar[str] = "Уровень $level_id --> "

    def report(self, entities: List[WordEntity], msg: str) -> None:
        Reporter.word_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Добавление новых слов")

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
        self.report(entities, "Обновление слов")

        words = []
        for item in entities:
            words.append(Word(id=item.id))

        Word.objects.bulk_update(words, ["word_a", "word_b"])

    def equal(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Слова без изменений")

    def delete(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Удаление слов")

        words = []
        for item in entities:
            words.append(item.id)

        Word.objects.filter(id__in=words).delete()


# </editor-fold>


# <editor-fold desc="Json actions">
class JsonCourseActions(Actions):
    def report(self, entities: List[CourseEntity], msg: str) -> None:
        Reporter.course_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Добавление новых курсов")

    def update(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Обновление курсов")

    def equal(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Курсы без изменений")

    def delete(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Удаление курсов")


class JsonLevelActions(Actions):
    prefix: ClassVar[str] = "Курс $course_id --> "

    def report(self, entities: List[LevelEntity], msg: str) -> None:
        Reporter.level_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Добавление новых уровней")

    def update(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Обновление уровней")

    def equal(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Уровни без изменений")

    def delete(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Удаление уровней")


class JsonWordActions(Actions):
    prefix: ClassVar[str] = "Уровень $level_id --> "

    def report(self, entities: List[WordEntity], msg: str) -> None:
        Reporter.word_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Добавление новых слов")

    def update(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Обновление слов")

    def equal(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Слова без изменений")

    def delete(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Удаление слов")


# </editor-fold>


# <editor-fold desc="MemriseAPI actions">
class MemriseCourseActions(Actions):
    def report(self, entities: List[CourseEntity], msg: str) -> None:
        Reporter.course_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Добавление новых курсов")

    def update(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Обновление курсов")

    def equal(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Курсы без изменений")

    def delete(self, entities: List[CourseEntity]) -> None:
        self.report(entities, "Удаление курсов")


class MemriseLevelActions(Actions):
    prefix: ClassVar[str] = "Курс $course_id --> "

    def report(self, entities: List[LevelEntity], msg: str) -> None:
        Reporter.level_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Добавление новых уровней")

    def update(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Обновление уровней")

    def equal(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Уровни без изменений")

    def delete(self, entities: List[LevelEntity]) -> None:
        self.report(entities, "Удаление уровней")


class MemriseWordActions(Actions):
    prefix: ClassVar[str] = "Уровень $level_id --> "

    def report(self, entities: List[WordEntity], msg: str) -> None:
        Reporter.word_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Добавление новых слов")

    def update(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Обновление слов")

    def equal(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Слова без изменений")

    def delete(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Удаление слов")


# </editor-fold>
