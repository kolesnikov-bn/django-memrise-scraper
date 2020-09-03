from __future__ import annotations

from abc import abstractmethod
from dataclasses import field
from operator import attrgetter
from typing import Dict, List
from typing import Generic, TypeVar
from urllib.parse import urljoin

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from memrise.core.modules.helpers import DashboardCounter
from memrise.shares.types import URL

RepositoryT = TypeVar("RepositoryT")


class WordEntity(BaseModel):
    id: int
    word: str
    translate: str


class LevelEntity(BaseModel):
    number: int
    name: str = ""
    words: List[WordEntity] = Field(default_factory=list)

    def add(self, word: WordEntity) -> None:
        """Добавление слов уровня оригинальное слово и его перевод"""
        self.words.append(word)


class CourseEntity(BaseModel):
    id: int
    name: str
    url: str
    difficult: int
    num_things: int
    num_levels: int
    difficult_url: str
    levels_url: List[URL] = Field(default_factory=list)
    levels: List[LevelEntity] = Field(default_factory=list)

    def make_urls(self) -> None:
        for idx in range(1, self.num_levels + 1):
            url = URL(urljoin(self.url, str(idx)))
            self.levels_url.append(url)

    def add_level(self, level: LevelEntity) -> None:
        self.levels.append(level)


@dataclass  # type: ignore
class Repository(Generic[RepositoryT]):
    @abstractmethod
    def get_courses(self, dashboard: DashboardEntity) -> List[CourseEntity]:
        """ Получение всех пользовательских курстов на домашней странице

        :param dashboard: фильтры для итерационного запроса получения курсов
        """
        raise NotImplementedError(
            "The `get_courses` method must be implemented in derived class"
        )

    @abstractmethod
    def fetch_levels(self, course: CourseEntity) -> List[LevelEntity]:
        """Получение """
        raise NotImplementedError(
            "The `fetch_levels` method must be implemented in derived class"
        )


@dataclass(repr=False)
class DashboardEntity:
    courses: List[CourseEntity] = field(default_factory=list)
    counter: DashboardCounter = field(default_factory=DashboardCounter)

    def offset(self) -> Dict:
        return self.counter.next()

    def add_course(self, course: CourseEntity) -> None:
        """Добавление курса в dashboard"""
        self.courses.append(course)

    def get_courses(self) -> List[CourseEntity]:
        """Получаем отсортированный список курсов"""
        return sorted(self.courses, key=attrgetter("id"))

    def purge(self) -> None:
        """Очищаем dashboard"""
        self.courses = []
