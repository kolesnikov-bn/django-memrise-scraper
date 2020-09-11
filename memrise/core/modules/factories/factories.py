from typing import List

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity
from memrise.core.modules.factories.base import Factory, ItemT
from memrise.core.modules.factories.entity_makers import (
    CourseEntityMaker,
    LevelEntityMaker,
    WordEntityMaker, )
from memrise.core.modules.factories.factory_registry import FactoryHandler
from memrise.core.responses.course_response import CourseItemResponse
from memrise.core.responses.structs import LevelStruct
from memrise.models import Course, Level, Word

factory_mapper = FactoryHandler()


@factory_mapper.register
class CourseFactory(Factory):
    def matches(self, item: ItemT) -> bool:
        if not item:
            return False

        return all(isinstance(x, (CourseItemResponse, Course)) for x in item)

    def make_product(self, item: ItemT) -> List[CourseEntity]:
        return CourseEntityMaker().make(item)


@factory_mapper.register
class LevelFactory(Factory):
    def matches(self, item: ItemT) -> bool:
        if not item:
            return False

        return all(isinstance(x, (LevelStruct, Level)) for x in item)

    def make_product(self, item: ItemT) -> List[LevelEntity]:
        return LevelEntityMaker().make(item)


@factory_mapper.register
class WordFactory(Factory):
    def matches(self, item: ItemT) -> bool:
        if not item:
            return False

        return all(isinstance(x, Word) for x in item)

    def make_product(self, item: ItemT) -> List[WordEntity]:
        return WordEntityMaker().make(item)
