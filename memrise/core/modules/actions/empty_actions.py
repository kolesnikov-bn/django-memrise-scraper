from __future__ import annotations

from typing import List, ClassVar, TYPE_CHECKING

from memrise.core.modules.actions.base import Actions

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity


class EmptyCourseActions(Actions):
    def create(self, entities: List[CourseEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Добавление новых курсов{self.postfix}"
        )

    def update(self, entities: List[CourseEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Обновление курсов{self.postfix}")

    def equal(self, entities: List[CourseEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Курсы без изменений{self.postfix}"
        )

    def delete(self, entities: List[CourseEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Удаление курсов{self.postfix}")


class EmptyLevelActions(Actions):
    prefix: ClassVar[str] = "Курс $course_id --> "

    def create(self, entities: List[LevelEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Добавление новых уровней{self.postfix}"
        )

    def update(self, entities: List[LevelEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Обновление уровней{self.postfix}")

    def equal(self, entities: List[LevelEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Уровни без изменений{self.postfix}"
        )

    def delete(self, entities: List[LevelEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Удаление уровней{self.postfix}")


class EmptyWordActions(Actions):
    prefix: ClassVar[str] = "Уровень $level_id --> "

    def create(self, entities: List[WordEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Добавление новых слов{self.postfix}"
        )

    def update(self, entities: List[WordEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Обновление слов{self.postfix}")

    def equal(self, entities: List[WordEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Слова без изменений{self.postfix}"
        )

    def delete(self, entities: List[WordEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Удаление слов{self.postfix}")
