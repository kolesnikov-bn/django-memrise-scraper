from __future__ import annotations

from typing import List, ClassVar, TYPE_CHECKING

from memrise.core.modules.actions.base import Actions
from memrise.models import Course, Level, Word

if TYPE_CHECKING:
    from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity


class DBCourseActions(Actions):
    def create(self, entities: List[CourseEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Добавление новых курсовself.postfix"
        )

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
        self.reporter.report(entities, f"{self.prefix}Обновление курсов{self.postfix}")

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
        self.reporter.report(
            entities, f"{self.prefix}Курсы без изменений{self.postfix}"
        )

    def delete(self, entities: List[CourseEntity]) -> None:
        # Курсы не удаляем, а отключаем, для того чтобы можно было бы вернуться к ним.
        self.reporter.report(entities, f"{self.prefix}Отключение курсов{self.postfix}")

        courses = []
        for item in entities:
            courses.append(Course(id=item.id, is_disable=True))

        Course.objects.bulk_update(
            courses, ["is_disable"],
        )

        # self.reporter.report(entities, f"{self.prefix}Удаление курсов{self.postfix}")

        # courses = []
        # for item in entities:
        #     courses.append(item.id)
        #
        # Course.objects.filter(id__in=courses).delete()


class DBLevelActions(Actions):
    prefix: ClassVar[str] = "Курс $course_id --> "

    def create(self, entities: List[LevelEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Добавление новых уровней{self.postfix}"
        )

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
        self.reporter.report(entities, f"{self.prefix}Обновление уровней{self.postfix}")

        levels = []
        for item in entities:
            levels.append(Level(id=item.id, course_id=item.course_id, name=item.name))

        Level.objects.bulk_update(levels, ["name"])

    def equal(self, entities: List[LevelEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Уровни без изменений{self.postfix}"
        )

    def delete(self, entities: List[LevelEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Удаление уровней{self.postfix}")

        levels = []
        for item in entities:
            levels.append(item.id)

        Level.objects.filter(id__in=levels).delete()


class DBWordActions(Actions):
    prefix: ClassVar[str] = "Уровень $level_id --> "

    def create(self, entities: List[WordEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Добавление новых слов{self.postfix}"
        )

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
        self.reporter.report(entities, f"{self.prefix}Обновление слов{self.postfix}")

        words = []
        for item in entities:
            words.append(Word(id=item.id, word_a=item.word_a, word_b=item.word_b))

        # TODO: сделать тесты, была не отловлена ошибка по обновлению данных!!!
        Word.objects.bulk_update(words, ["word_a", "word_b"])

    def equal(self, entities: List[WordEntity]) -> None:
        self.reporter.report(
            entities, f"{self.prefix}Слова без изменений{self.postfix}"
        )

    def delete(self, entities: List[WordEntity]) -> None:
        self.reporter.report(entities, f"{self.prefix}Удаление слов{self.postfix}")

        words = []
        for item in entities:
            words.append(item.id)

        Word.objects.filter(id__in=words).delete()
