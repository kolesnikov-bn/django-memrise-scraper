from dataclasses import field

from pydantic.dataclasses import dataclass

from memrise.core.modules.selectors import CourseSelector, LevelSelector
from memrise.core.repositoris.repos import MemriseRep, Repository, DBRep


@dataclass
class UpdateManager:
    memrise_repo: Repository = field(default_factory=MemriseRep)
    db_repo: Repository = field(default_factory=DBRep)

    def update(self) -> None:
        self.update_courses()
        self.update_levels()
        self.update_words()

    def update_courses(self) -> None:
        fresh_courses = self.memrise_repo.get_courses()
        actual_courses = self.db_repo.get_courses()
        courses_diff = CourseSelector.match(fresh_courses, actual_courses)
        self.db_repo.save_courses(courses_diff)

    def update_levels(self) -> None:
        for course in self.db_repo.get_courses():
            actual_levels = self.db_repo.get_levels(course)
            fresh_levels = self.memrise_repo.get_levels(course)
            level_diff = LevelSelector.match(fresh_levels, actual_levels)
            course_entry = self.db_repo.get_course_by_entity(course)
            self.db_repo.save_levels(level_diff, course_entry)

    def update_words(self) -> None:
        pass
