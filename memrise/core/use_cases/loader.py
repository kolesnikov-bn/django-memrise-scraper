"""
DashboardLoader - Агрегирующий класс контейнер для работы с репозиторизиями
=========================================================

Позволяет стягивать все данные из репозитория в контейнер и работать уже с кешированными данными
В первую очередь данный модуль служит для того чтобы сделать срез данных резозитория и работать
с этими кешированными данными как с единой сущностью.
Приложение обращается к репозиторию только один раз чтобы получить все данные.
Если это репозиторий memrise, то мы стягиваем все новые данные только один раз, что позволяет избежать множественных
тяжелых вызовов, которые занимают очень большое время.

HOW TO USE IT:
    loader = DashboardLoader(MemriseRep())
    loader.load_assets()
    ...
    course_entities = loader.get_courses()
    level_entities = loader.get_levels(CourseEntity)
    word_entities = loader.get_words(LevelEntity)
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from memrise.core.domains.entities import DashboardEntity
    from memrise.core.repositoris.repos import Repository
    from memrise.core.domains.entities import (
        CourseEntity,
        LevelEntity,
        WordEntity,
    )


@dataclass
class DashboardLoader:
    repo: "Repository"
    dashboard: "DashboardEntity"

    def load_assets(self) -> "DashboardEntity":
        """Получение всех пользовательских учебных курсов отображаемых в dashboard"""
        course_entities = self.repo.get_courses()
        self.dashboard.add_courses(course_entities)
        self._fetch_levels()

        return self.dashboard

    def _fetch_levels(self) -> None:
        """Стягиваем уровни из репозитория и добавляем их в dashboard,
        если уровни имееют слова, то они тоже будут там
        """
        level_entities = self.repo.get_levels(self.dashboard.courses)
        level_maps = self.group_levels_by_course(level_entities)

        for course_entities in self.dashboard.courses:
            course_entities.add_levels(level_maps[course_entities.id])

    def group_levels_by_course(
        self, level_entities: List["LevelEntity"]
    ) -> Dict[int, List["LevelEntity"]]:
        """Группировка уровней по курсам"""
        level_maps = defaultdict(list)
        [level_maps[level.course_id].append(level) for level in level_entities]
        return level_maps

    def get_courses(self) -> List["CourseEntity"]:
        """Получение курсров из dashboard"""
        return self.dashboard.get_courses()

    def get_levels(self) -> List["LevelEntity"]:
        """Получение уровней из dashboard"""
        level_entities = []
        for course_entity in self.dashboard.courses:
            level_entities.extend(course_entity.levels)

        return level_entities

    def get_words(self) -> List["WordEntity"]:
        """Получение слов из dashboard"""
        word_entities = []
        for course_entity in self.dashboard.courses:
            for level_entity in course_entity.levels:
                word_entities.extend(level_entity.words)

        return word_entities

    def refresh_assets(self) -> None:
        """Очистка и обновление всех данных, может быть очень трудозатратная особенно при работс memrise.
        В этом случае оно идет в memrise и опять стягивает все данные.
        Использовать только в крайних случаях!!!
        """
        self.dashboard.purge()
        self.load_assets()
