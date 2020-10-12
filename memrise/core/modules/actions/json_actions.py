from __future__ import annotations

from typing import List, ClassVar, TYPE_CHECKING

from memrise.core.modules.actions.action_reporter import ActionReporter as reporter
from memrise.core.modules.actions.base import Actions

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity


class JsonCourseActions(Actions):
    def report(self, entities: List[CourseEntity], msg: str) -> None:
        reporter.course_report(entities, f"{self.prefix}{msg}{self.postfix}")

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
        reporter.level_report(entities, f"{self.prefix}{msg}{self.postfix}")

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
        reporter.word_report(entities, f"{self.prefix}{msg}{self.postfix}")

    def create(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Добавление новых слов")

    def update(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Обновление слов")

    def equal(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Слова без изменений")

    def delete(self, entities: List[WordEntity]) -> None:
        self.report(entities, "Удаление слов")
