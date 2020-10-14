"""
Update Manager
==============


Агрегирующий модуль спопобный собирать у себя все компоненты сервиса для обновления данных
между memrise и локальным хранилищем.

В первую очередь создан для работы между memrise -> DB, но может так же работать в других связках:
    - Memrise -> DB
    - Json -> DB
    - DB -> DB

HOW TO USE IT:
    memrise_repo = MemriseRep()
    db_repo = DBRep()
    um = UpdateManager(fresh_repo=memrise_repo, actual_repo=db_repo)
    um.update()

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from memrise.core.modules.selectors import CourseSelector, LevelSelector, WordSelector
from memrise.core.use_cases.dashboard import Dashboard

if TYPE_CHECKING:
    from memrise.core.repositories.base import Repository


@dataclass
class UpdateManager:
    actual_repo: Repository
    dashboard: Dashboard

    def __post_init__(self) -> None:
        """При инициализации класса, так же запускаем стягивание новых данных из memrise"""
        self.dashboard.load_assets()

    def update(self) -> None:
        """Основной метод обновления всех данных данных"""
        update_methods = [self.update_courses, self.update_levels, self.update_words]
        [method() for method in update_methods]

    def update_courses(self) -> None:
        """Обновление курсов"""
        fresh_course_entities = self.dashboard.get_courses()
        actual_course_entities = self.actual_repo.get_courses()
        diff = CourseSelector.match(fresh_course_entities, actual_course_entities)
        self.actual_repo.setter.save_courses(diff)

    def update_levels(self) -> None:
        """Обновление уровней"""

        course_entities = self.actual_repo.get_courses()
        actual_level_entities = self.actual_repo.get_levels(course_entities)
        fresh_level_entities = self.dashboard.get_levels()
        diff = LevelSelector.match(fresh_level_entities, actual_level_entities)
        self.actual_repo.setter.save_levels(diff)

    def update_words(self) -> None:
        """Обновление слов"""

        course_entities = self.actual_repo.get_courses()
        actual_level_entities = self.actual_repo.get_levels(course_entities)
        fresh_word_entities = self.dashboard.get_words()
        actual_word_entities = [
            word
            for actual_level_entity in actual_level_entities
            for word in actual_level_entity.words
        ]

        diff = WordSelector.match(fresh_word_entities, actual_word_entities)
        self.actual_repo.setter.save_words(diff)
