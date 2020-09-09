"""
Репозитории проекта
===================

"""
import json
from abc import abstractmethod, ABC
from typing import Generic, List, Generator

from pydantic import FilePath
from pydantic.dataclasses import dataclass

from memrise.core.domains.entities import (
    RepositoryT,
    CourseEntity,
    LevelEntity, WordEntity,
)
from memrise.core.modules.factories import CourseEntityMaker, WordEntityMaker
from memrise.core.repositoris.actions import CourseActions, LevelActions
from memrise.core.responses.course_response import CoursesResponse
from memrise.core.use_cases.selectors import DiffContainer
from memrise.models import Course, Word
from memrise.shares.contants import DASHBOARD_FIXTURE, LEVELS_FIXTURE


@dataclass
class Repository(Generic[RepositoryT], ABC):
    @abstractmethod
    def get_courses(self) -> List[CourseEntity]:
        """ Получение всех пользовательских курсов на домашней странице """

    @abstractmethod
    def fetch_levels(self, course_id: int) -> List[LevelEntity]:
        """Стягивание уровней курса"""

    @abstractmethod
    def save_course(self, diff: DiffContainer) -> None:
        """Сохранение курса в хранилище"""


class JsonRep(Repository):
    """Получение данных о курсах из тестовых fixtures, в данном случае из json файла"""

    dashboard_fixture: FilePath = DASHBOARD_FIXTURE
    levels_fixture: FilePath = LEVELS_FIXTURE

    def fetch_levels(self, course_id: int) -> List[LevelEntity]:
        levels = []
        with self.levels_fixture.open() as f:
            levels_map = json.loads(f.read())

        level_entities = {
            item["id"]: item["levels"] for item in levels_map if item["id"] == course_id
        }
        if level_entities:
            levels = []
            for item in level_entities[course_id]:
                item["course_id"] = course_id
                levels.append(LevelEntity(**item))

        return levels

    def get_courses(self) -> List[CourseEntity]:
        with self.dashboard_fixture.open() as f:
            response = json.loads(f.read())

        courses_response = CoursesResponse(**response)
        course_maker = CourseEntityMaker()
        course_maker.make(courses_response.iterator())

        return course_maker.courses

    def save_course(self, diff: DiffContainer) -> None:
        pass


class DBRep(Repository):
    """Работа с данными в БД"""

    def get_courses(self) -> List[CourseEntity]:
        course_maker = CourseEntityMaker()
        courses = course_maker.make(Course.objects.iterator())
        return courses

    def fetch_levels(self, course_id: int) -> Generator[LevelEntity, None, None]:
        # TODO: fetch_levels_by_course
        try:
            level_entries = Course.objects.get(id=course_id).level_set.all()
        except Course.DoesNotExist:
            raise ValueError(f"Курс {course_id} не найден в БД")

        for level in level_entries:
            words = self._fetch_words(level.word_set.iterator())
            yield LevelEntity(number=level.number, course_id=course_id, name=level.name, words=words)

    def _fetch_words(self, words: Generator[Word, None, None]) -> Generator[WordEntity, None, None]:
        wm = WordEntityMaker()
        yield from wm.make(words)

    def save_course(self, diff: DiffContainer) -> None:
        # TODO: save_courses.
        actions = CourseActions()
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)

    def save_levels(self, diff: DiffContainer, course_object: Course) -> None:
        actions = LevelActions(parent_course=course_object)
        for action_field, entities in diff:
            action_method = getattr(actions, action_field)
            action_method(entities)
