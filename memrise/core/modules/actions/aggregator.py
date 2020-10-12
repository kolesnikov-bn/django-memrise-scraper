from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from memrise.core.modules.actions.base import Actions
from memrise.core.modules.actions.db_actions import (
    DBCourseActions,
    DBLevelActions,
    DBWordActions,
)
from memrise.core.modules.actions.json_actions import (
    JsonCourseActions,
    JsonLevelActions,
    JsonWordActions,
)
from memrise.core.modules.actions.memrise_actions import (
    MemriseCourseActions,
    MemriseLevelActions,
    MemriseWordActions,
)


@dataclass
class ActionsAggregator(ABC):
    course: Actions = field(init=False)
    level: Actions = field(init=False)
    word: Actions = field(init=False)

    def __post_init__(self):
        self.init()

    @abstractmethod
    def init(self):
        """Инициализация действий и привязка их к аттрибутам моделей"""


@dataclass
class DBAggregator(ActionsAggregator):
    def init(self):
        self.course = DBCourseActions()
        self.level = DBLevelActions()
        self.word = DBWordActions()


@dataclass
class JsonAggregator(ActionsAggregator):
    def init(self):
        self.course = JsonCourseActions()
        self.level = JsonLevelActions()
        self.word = JsonWordActions()


@dataclass
class MemriseAggregator(ActionsAggregator):
    def init(self):
        self.course = MemriseCourseActions()
        self.level = MemriseLevelActions()
        self.word = MemriseWordActions()
