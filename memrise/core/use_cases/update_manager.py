from __future__ import annotations

from dataclasses import field, dataclass
from typing import List, TYPE_CHECKING

from memrise.core.domains.entities import DashboardEntity
from memrise.core.modules.selectors import CourseSelector, LevelSelector, WordSelector

if TYPE_CHECKING:
    from memrise.core.repositoris.repos import Repository
    from memrise.core.domains.entities import LevelEntity, CourseEntity, WordEntity


@dataclass
class DashboardLoader:
    repo: Repository
    dashboard: "DashboardEntity" = field(init=False)

    def __post_init__(self) -> None:
        self.dashboard = DashboardEntity()

    def load_assets(self) -> DashboardEntity:
        """Получение всех пользовательских учебных курсов отображаемых в dashboard"""
        course_entities = self.repo.get_courses()
        for course in course_entities:
            self.dashboard.add_course(course)

        self._load_levels()

        return self.dashboard

    def _load_levels(self) -> None:
        for course_entities in self.dashboard.courses:
            try:
                level_entities = self.repo.get_levels(course_entities)
                for level in level_entities:
                    course_entities.add_level(level)
            except ValueError:
                pass

    def get_courses(self) -> List[CourseEntity]:
        return self.dashboard.get_courses()

    def get_levels(self, course_entity: CourseEntity) -> List[LevelEntity]:
        level_entities = []
        for course in self.dashboard.courses:
            if course.id == course_entity.id:
                level_entities.extend(course.levels)

        return level_entities

    def get_words(self, level_entity: LevelEntity) -> List[WordEntity]:
        word_entities = []
        for course_entity in self.dashboard.courses:
            for level in course_entity.levels:
                if level.id == level_entity.id:
                    word_entities.extend(level.words)

        return word_entities


@dataclass
class UpdateManager:
    fresh_repo: Repository
    actual_repo: Repository
    loader: DashboardLoader = field(init=False)

    def __post_init__(self) -> None:
        """При инициализации класса, так же запускаем стягивание новых данных из memrise"""
        self.loader = DashboardLoader(repo=self.fresh_repo)
        self.loader.load_assets()

    def update(self) -> None:
        """Основной метод обновления данных"""
        self.update_courses()
        self.update_levels()
        self.update_words()

    def update_courses(self) -> None:
        fresh_course_entities = self.loader.get_courses()
        actual_course_entities = self.actual_repo.get_courses()
        courses_diff = CourseSelector.match(
            fresh_course_entities, actual_course_entities
        )
        self.actual_repo.save_courses(courses_diff)

    def update_levels(self) -> None:
        for course_entity in self.actual_repo.get_courses():
            actual_level_entities = self.actual_repo.get_levels(course_entity)
            fresh_level_entities = self.loader.get_levels(course_entity)
            level_diff = LevelSelector.match(
                fresh_level_entities, actual_level_entities
            )
            course_record = self.actual_repo.get_course_by_entity(course_entity)
            self.actual_repo.save_levels(level_diff, course_record)

    def update_words(self) -> None:
        for course_entity in self.actual_repo.get_courses():
            actual_level_entities = self.actual_repo.get_levels(course_entity)
            for level_entity in actual_level_entities:
                fresh_words_entities = self.loader.get_words(level_entity)
                actual_words_entities = level_entity.words
                words_diff = WordSelector.match(
                    fresh_words_entities, actual_words_entities
                )
                level_record = self.actual_repo.get_level_by_entity(level_entity)
                self.actual_repo.save_words(words_diff, level_record)
