from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from memrise.core.modules.actions.action_reporter import (
    CourseReporter,
    LevelReporter,
    WordReporter,
)
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


@dataclass
class ActionsBatch(ABC):
    course: ClassVar[Actions]
    level: ClassVar[Actions]
    word: ClassVar[Actions]

    def __post_init__(self):
        self.init()

    @abstractmethod
    def init(self):
        """Инициализация действий и привязка их к аттрибутам моделей"""


@dataclass
class DBActionsBatch(ActionsBatch):
    def init(self):
        self.course = DBCourseActions(reporter=CourseReporter())
        self.level = DBLevelActions(reporter=LevelReporter())
        self.word = DBWordActions(reporter=WordReporter())


@dataclass
class JsonActionsBatch(ActionsBatch):
    def init(self):
        self.course = EmptyCourseActions(reporter=CourseReporter())
        self.level = EmptyLevelActions(reporter=LevelReporter())
        self.word = EmptyWordActions(reporter=WordReporter())


@dataclass
class MemriseActionsBatch(ActionsBatch):
    def init(self):
        self.course = EmptyCourseActions(reporter=CourseReporter())
        self.level = EmptyLevelActions(reporter=LevelReporter())
        self.word = EmptyWordActions(reporter=WordReporter())
