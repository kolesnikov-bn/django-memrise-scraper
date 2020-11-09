from abc import ABC
from typing import List
from urllib.parse import urljoin

from pydantic import BaseModel, Field

from memrise.core.mixins import AsDictMixin
from memrise.shares.types import URL


class Entity(BaseModel, ABC):
    pass


class WordEntity(Entity, AsDictMixin):
    id: int
    level_id: int
    word_a: str
    word_b: str
    is_learned: bool = False


class LevelEntity(Entity, AsDictMixin):
    id: int
    number: int
    course_id: int
    name: str
    words: List[WordEntity] = Field(default_factory=list)

    def add_word(self, word: WordEntity) -> None:
        """Добавление слова в уровень"""
        self.words.append(word)

    def add_words(self, words: List[WordEntity]) -> None:
        """Массовое добавление слов в уровень"""
        self.words = words


class CourseEntity(Entity, AsDictMixin):
    id: int
    name: str
    url: str
    difficult: int
    num_words: int
    num_levels: int
    difficult_url: str
    levels_url: List[URL] = Field(default_factory=list)
    levels: List[LevelEntity] = Field(default_factory=list)
    is_disable: bool = Field(default=False)

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
