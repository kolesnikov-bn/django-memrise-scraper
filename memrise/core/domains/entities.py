from __future__ import annotations

from dataclasses import field
from operator import attrgetter
from typing import List
from urllib.parse import urljoin

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from memrise.shares.types import URL


class WordEntity(BaseModel):
    id: int
    word_a: str
    word_b: str


class LevelEntity(BaseModel):
    level_id: int
    number: int
    course_id: int
    name: str
    words: List[WordEntity] = Field(default_factory=list)

    def add_word(self, word: WordEntity) -> None:
        """Добавление слова в уровень"""
        self.words.append(word)


class CourseEntity(BaseModel):
    id: int
    name: str
    url: str
    difficult: int
    num_words: int
    num_levels: int
    difficult_url: str
    levels_url: List[URL] = Field(default_factory=list)
    levels: List[LevelEntity] = Field(default_factory=list)

    def generate_levels_url(self) -> None:
        """Создание списка URL уровней"""
        for idx in range(1, self.num_levels + 1):
            url = URL(urljoin(self.url, str(idx)))
            self.levels_url.append(url)

    def add_level(self, level: LevelEntity) -> None:
        """Добавление уровня в курс"""
        self.levels.append(level)


@dataclass(repr=False)
class DashboardEntity:
    courses: List[CourseEntity] = field(default_factory=list)

    def add_course(self, course: CourseEntity) -> None:
        """Добавление курса в dashboard"""
        self.courses.append(course)

    def get_courses(self) -> List[CourseEntity]:
        """Получение отсортированного списока курсов"""
        return sorted(self.courses, key=attrgetter("id"))

    def purge(self) -> None:
        """Очищение dashboard, удаление курсов"""
        self.courses = []
