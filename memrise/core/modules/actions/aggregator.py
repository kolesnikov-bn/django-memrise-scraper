from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

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


# TODO: Нужно подумать над более продуманными названиями для агрегаторов, да, они собирают разные действия,
#  но возможно что будет найдено более лучшее и осмысленное название.


@dataclass
class ActionAggregator(ABC):
    course: ClassVar[Actions]
    level: ClassVar[Actions]
    word: ClassVar[Actions]

    def __post_init__(self):
        self.init()

    @abstractmethod
    def init(self):
        """Инициализация действий и привязка их к аттрибутам моделей"""


@dataclass
class DBAggregator(ActionAggregator):
    def init(self):
        self.course = DBCourseActions()
        self.level = DBLevelActions()
        self.word = DBWordActions()


@dataclass
class JsonAggregator(ActionAggregator):
    def init(self):
        self.course = JsonCourseActions()
        self.level = JsonLevelActions()
        self.word = JsonWordActions()


@dataclass
class MemriseAggregator(ActionAggregator):
    def init(self):
        self.course = MemriseCourseActions()
        self.level = MemriseLevelActions()
        self.word = MemriseWordActions()
