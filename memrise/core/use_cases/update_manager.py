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
from memrise.core.use_cases.loader import DashboardLoader

if TYPE_CHECKING:
    from memrise.core.repositoris.repos import Repository


@dataclass
class UpdateManager:
    actual_repo: Repository
    loader: DashboardLoader

    def __post_init__(self) -> None:
        """При инициализации класса, так же запускаем стягивание новых данных из memrise"""
        self.loader.load_assets()

    def update(self) -> None:
        """Основной метод обновления всех данных данных"""
        self.update_courses()
        self.update_levels()
        self.update_words()

    def update_courses(self) -> None:
        """Обновление курсов"""
        fresh_course_entities = self.loader.get_courses()
        actual_course_entities = self.actual_repo.get_courses()
        diff = CourseSelector.match(fresh_course_entities, actual_course_entities)
        self.actual_repo.save_courses(diff)

    def update_levels(self) -> None:
        """Обновление уровней"""
        for course_entity in self.actual_repo.get_courses():
            actual_level_entities = self.actual_repo.get_levels(course_entity)
            fresh_level_entities = self.loader.get_levels(course_entity)
            diff = LevelSelector.match(fresh_level_entities, actual_level_entities)
            course_record = self.actual_repo.get_course_by_entity(course_entity)
            self.actual_repo.save_levels(diff, course_record)

    def update_words(self) -> None:
        """Обновление слов"""
        for course_entity in self.actual_repo.get_courses():
            actual_level_entities = self.actual_repo.get_levels(course_entity)
            for level_entity in actual_level_entities:
                fresh_word_entities = self.loader.get_words(level_entity)
                actual_word_entities = level_entity.words
                diff = WordSelector.match(fresh_word_entities, actual_word_entities)
                level_record = self.actual_repo.get_level_by_entity(level_entity)
                self.actual_repo.save_words(diff, level_record)
