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

from stories import Result, Success, story

from memrise.core.modules.selectors import CourseSelector, LevelSelector, WordSelector
from memrise.core.use_cases.dashboard import Dashboard

if TYPE_CHECKING:
    from memrise.core.repositories.base import Repository


@dataclass
class UpdateManager:
    actual_repo: Repository
    dashboard: Dashboard

    @story
    def update(I) -> None:
        """Основной метод обновления всех данных данных"""
        # It's stories methods without call and we shall use noqa comments.
        I.load_assets  # noqa
        I.update_courses  # noqa
        I.update_levels  # noqa
        I.update_words  # noqa

    def load_assets(self, ctx) -> Success:
        self.dashboard.load_assets()
        ctx.fresh_course_entities = self.dashboard.get_courses()
        ctx.fresh_level_entities = self.dashboard.get_levels()
        ctx.fresh_word_entities = self.dashboard.get_words()
        return Success()

    def update_courses(self, ctx) -> Success:
        """Обновление курсов"""

        actual_course_entities = self.actual_repo.get_courses()
        diff = CourseSelector.match(ctx.fresh_course_entities, actual_course_entities)
        self.actual_repo.update_courses(diff)
        return Success()

    def update_levels(self, ctx) -> Success:
        """Обновление уровней"""

        actual_level_entities = self.actual_repo.get_levels(ctx.fresh_course_entities)
        diff = LevelSelector.match(ctx.fresh_level_entities, actual_level_entities)
        self.actual_repo.update_levels(diff)
        return Success()

    def update_words(self, ctx) -> Result:
        """Обновление слов"""

        actual_word_entities = [
            word
            for actual_level_entity in ctx.fresh_level_entities
            for word in actual_level_entity.words
        ]

        diff = WordSelector.match(ctx.fresh_word_entities, actual_word_entities)
        self.actual_repo.update_words(diff)
        return Result(ctx)
