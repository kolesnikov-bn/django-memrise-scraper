from abc import ABC
from dataclasses import dataclass, field
from operator import attrgetter
from typing import List
from urllib.parse import urljoin

from memrise.core.mixins import AsDictMixin
from memrise.shares.types import URL


@dataclass
class Entity(ABC):
    pass


@dataclass
class WordEntity(Entity, AsDictMixin):
    id: int
    level_id: int
    word_a: str
    word_b: str


@dataclass
class LevelEntity(Entity, AsDictMixin):
    id: int
    number: int
    course_id: int
    name: str
    words: List[WordEntity] = field(default_factory=list)

    def add_word(self, word: WordEntity) -> None:
        """Добавление слова в уровень"""
        self.words.append(word)

    def add_words(self, words: List[WordEntity]) -> None:
        """Массовое добавление слов в уровень"""
        self.words = words


@dataclass
class CourseEntity(Entity, AsDictMixin):
    id: int
    name: str
    url: str
    difficult: int
    num_words: int
    num_levels: int
    difficult_url: str
    levels_url: List[URL] = field(default_factory=list)
    levels: List[LevelEntity] = field(default_factory=list)

    def generate_levels_url(self) -> None:
        """Создание списка URL уровней"""
        for idx in range(1, self.num_levels + 1):
            url = URL(urljoin(self.url, str(idx)))
            self.levels_url.append(url)

    def add_level(self, level: LevelEntity) -> None:
        """Добавление уровней в курс"""
        self.levels.append(level)

    def add_levels(self, levels: List[LevelEntity]) -> None:
        """Массовое добавление уровней в курс"""
        self.levels = levels


@dataclass
class DashboardEntity:
    courses: List[CourseEntity] = field(default_factory=list)

    def add_course(self, course: CourseEntity) -> None:
        """Добавление курса в dashboard"""
        self.courses.append(course)

    def add_courses(self, courses: List[CourseEntity]) -> None:
        """Массовое добавление курсов в dashboard"""
        self.courses = courses

    def get_courses(self) -> List[CourseEntity]:
        """Получение отсортированного списока курсов"""
        return sorted(self.courses, key=attrgetter("id"))

    def purge(self) -> None:
        """Очищение dashboard, удаление курсов"""
        self.courses = []
