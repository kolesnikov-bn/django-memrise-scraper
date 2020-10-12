from abc import ABC
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


@dataclass
class DBAggregator(ActionsAggregator):
    def __post_init__(self):
        self.course = DBCourseActions()
        self.level = DBLevelActions()
        self.word = DBWordActions()


@dataclass
class JsonAggregator(ActionsAggregator):
    def __post_init__(self):
        self.course = JsonCourseActions()
        self.level = JsonLevelActions()
        self.word = JsonWordActions()


@dataclass
class MemriseAggregator(ActionsAggregator):
    def __post_init__(self):
        self.course = MemriseCourseActions()
        self.level = MemriseLevelActions()
        self.word = MemriseWordActions()
