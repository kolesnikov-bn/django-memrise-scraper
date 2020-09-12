from pydantic.dataclasses import dataclass

from memrise.core.modules.selectors import CourseSelector, LevelSelector
from memrise.core.repositoris.repos import Repository


@dataclass
class UpdateManager:
    fresh_repo: Repository
    actual_repo: Repository

    def update(self) -> None:
        self.update_courses()
        self.update_levels()
        self.update_words()

    def update_courses(self) -> None:
        fresh_courses = self.fresh_repo.get_courses()
        actual_courses = self.actual_repo.get_courses()
        courses_diff = CourseSelector.match(fresh_courses, actual_courses)
        self.actual_repo.save_courses(courses_diff)

    def update_levels(self) -> None:
        for course in self.actual_repo.get_courses():
            actual_levels = self.actual_repo.get_levels(course)
            fresh_levels = self.fresh_repo.get_levels(course)
            level_diff = LevelSelector.match(fresh_levels, actual_levels)
            course_entry = self.actual_repo.get_course_by_entity(course)
            self.actual_repo.save_levels(level_diff, course_entry)

    def update_words(self) -> None:
        pass
