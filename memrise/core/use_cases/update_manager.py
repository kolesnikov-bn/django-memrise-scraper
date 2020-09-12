from __future__ import annotations

from typing import List, TYPE_CHECKING

from pydantic.dataclasses import dataclass

from memrise.core.modules.selectors import CourseSelector, LevelSelector, WordSelector
from memrise.core.repositoris.repos import Repository

if TYPE_CHECKING:
    from memrise.core.domains.entities import LevelEntity


@dataclass
class UpdateManager:
    fresh_repo: Repository
    actual_repo: Repository

    def update(self) -> None:
        self.update_courses()
        self.update_levels()
        # self.update_words()

    def update_courses(self) -> None:
        fresh_course_entities = self.fresh_repo.get_courses()
        actual_course_entities = self.actual_repo.get_courses()
        courses_diff = CourseSelector.match(
            fresh_course_entities, actual_course_entities
        )
        self.actual_repo.save_courses(courses_diff)

    def update_levels(self) -> None:
        for course in self.actual_repo.get_courses():
            actual_level_entities = self.actual_repo.get_levels(course)
            fresh_level_entities = self.fresh_repo.get_levels(course)
            level_diff = LevelSelector.match(
                fresh_level_entities, actual_level_entities
            )
            course_record = self.actual_repo.get_course_by_entity(course)
            self.actual_repo.save_levels(level_diff, course_record)
            self.update_words(fresh_level_entities, self.actual_repo.get_levels(course))

    def update_words(
        self,
        fresh_level_entities: List[LevelEntity],
        actual_level_entities: List[LevelEntity],
    ) -> None:
        for fresh_level_entity, actual_level_entity in zip(
            fresh_level_entities, actual_level_entities
        ):
            fresh_words_entities = fresh_level_entity.words
            actual_words_entities = actual_level_entity.words
            words_diff = WordSelector.match(fresh_words_entities, actual_words_entities)
            level_record = self.actual_repo.get_level_by_entity(actual_level_entity)
            self.actual_repo.save_words(words_diff, level_record)
