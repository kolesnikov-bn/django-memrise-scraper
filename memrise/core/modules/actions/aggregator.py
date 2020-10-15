from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from memrise.core.modules.actions.base import Actions
from memrise.core.modules.actions.db_actions import (
    DBCourseActions,
    DBLevelActions,
    DBWordActions,
)
from memrise.core.modules.actions.empty_actions import (
    EmptyCourseActions,
    EmptyLevelActions,
    EmptyWordActions,
)


# TODO: Нужно подумать над более продуманными названиями для агрегаторов, да, они собирают разные действия,
#  но возможно что будет найдено более лучшее и осмысленное название.


@dataclass
class Assembler(ABC):
    course: ClassVar[Actions]
    level: ClassVar[Actions]
    word: ClassVar[Actions]

    def __post_init__(self):
        self.init()

    @abstractmethod
    def init(self):
        """Инициализация действий и привязка их к аттрибутам моделей"""


@dataclass
class DBAssembler(Assembler):
    def init(self):
        self.course = DBCourseActions()
        self.level = DBLevelActions()
        self.word = DBWordActions()


@dataclass
class JsonAssembler(Assembler):
    def init(self):
        self.course = EmptyCourseActions()
        self.level = EmptyLevelActions()
        self.word = EmptyWordActions()


@dataclass
class MemriseAssembler(Assembler):
    def init(self):
        self.course = EmptyCourseActions()
        self.level = EmptyLevelActions()
        self.word = EmptyWordActions()
