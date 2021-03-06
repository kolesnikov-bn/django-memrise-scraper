"""
Dashboard - Агрегирующий класс контейнер для работы с репозиторизиями
=========================================================

Позволяет стягивать все данные из репозитория в контейнер и работать уже с кешированными данными
В первую очередь данный модуль служит для того чтобы сделать срез данных резозитория и работать
с этими кешированными данными как с единой сущностью.
Приложение обращается к репозиторию только один раз чтобы получить все данные.
Если это репозиторий memrise, то мы стягиваем все новые данные только один раз, что позволяет избежать множественных
тяжелых вызовов, которые занимают очень большое время.

HOW TO USE IT:
    dashboard = Dashboard(MemriseRep())
    dashboard.load_assets()
    ...
    courses = dashboard.get_courses()
    level_entities = dashboard.get_levels(CourseEntity)
    word_entities = dashboard.get_words(LevelEntity)
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from operator import attrgetter
from typing import List, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from memrise.core.repositories.base import Repository
    from memrise.core.domains.entities import (
        CourseEntity,
        LevelEntity,
        WordEntity,
    )


@dataclass
class DashboardCourseContainer:
    _courses: List[CourseEntity] = field(init=False, default_factory=list)

    @property
    def courses(self):
        return self._courses

    def add_course(self, course: CourseEntity) -> None:
        """Добавление курса в course_container"""
        self._courses.append(course)

    def add_courses(self, courses: List[CourseEntity]) -> None:
        """Массовое добавление курсов в course_container"""
        self._courses = courses

    def get_courses(self) -> List[CourseEntity]:
        """Получение отсортированного списока курсов"""
        return sorted(self._courses, key=attrgetter("id"))

    def purge(self) -> None:
        """Очищение course_container, удаление курсов"""
        self._courses = []


@dataclass
class Dashboard:
    origin_repo: "Repository"
    course_container: "DashboardCourseContainer"

    def load_assets(self) -> "DashboardCourseContainer":
        """Получение всех пользовательских учебных курсов отображаемых в course_container"""
        course_entities = self.origin_repo.get_courses()
        self.course_container.add_courses(course_entities)
        self._fetch_levels()

        return self.course_container

    def _fetch_levels(self) -> None:
        """Стягиваем уровни из репозитория и добавляем их в course_container,
        если уровни имееют слова, то они тоже будут там
        """
        level_entities = self.origin_repo.get_levels(self.course_container.courses)
        level_maps = self.group_levels_by_course(level_entities)

        for course_entities in self.course_container.courses:
            course_entities.add_levels(level_maps[course_entities.id])

    def group_levels_by_course(
        self, level_entities: List["LevelEntity"]
    ) -> Dict[int, List["LevelEntity"]]:
        """Группировка уровней по курсам"""
        level_maps = defaultdict(list)
        [level_maps[level.course_id].append(level) for level in level_entities]
        return level_maps

    def get_courses(self) -> List["CourseEntity"]:
        """Получение курсров из course_container"""
        return self.course_container.get_courses()

    def get_levels(self) -> List["LevelEntity"]:
        """Получение уровней из course_container"""
        level_entities = []
        for course_entity in self.course_container.courses:
            level_entities.extend(course_entity.levels)

        return level_entities

    def get_words(self) -> List["WordEntity"]:
        """Получение слов из course_container"""
        word_entities = []
        for course_entity in self.course_container.courses:
            for level_entity in course_entity.levels:
                word_entities.extend(level_entity.words)

        return word_entities

    def refresh_assets(self) -> None:
        """Очистка и обновление всех данных, может быть очень трудозатратная особенно при работс memrise.
        В этом случае оно идет в memrise и опять стягивает все данные.
        Использовать только в крайних случаях!!!
        """
        self.course_container.purge()
        self.load_assets()
