from abc import ABC, abstractmethod
from collections import defaultdict
from string import Template
from typing import List, TypeVar

from pydantic import BaseModel

from memrise import logger
from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity
from memrise.core.modules.web_socket_client import wss

EntityT = TypeVar("EntityT", CourseEntity, LevelEntity, WordEntity, contravariant=True)


class Reporter(ABC, BaseModel):
    @abstractmethod
    def report(self, entities: List[EntityT], msg: str, is_mute=False) -> None:
        raise NotImplementedError


class CourseReporter(Reporter):
    def report(self, entities: List[CourseEntity], msg: str, is_mute=False) -> None:
        total = len(entities)
        id_items = [item_entity.id for item_entity in entities]
        logger_msg = Template(msg).substitute(total=total, id_items=id_items)
        logger.info(logger_msg)
        wss.publish(logger_msg, is_mute=is_mute)


class LevelReporter(Reporter):
    def report(self, entities: List[LevelEntity], msg: str, is_mute=False) -> None:
        container = defaultdict(list)
        [container[entity.course_id].append(entity) for entity in entities]

        for course_id, items in container.items():
            total = len(items)
            id_items = [item_entity.id for item_entity in items]
            logger_msg = Template(msg).substitute(
                course_id=course_id, total=total, id_items=id_items
            )
            logger.info(logger_msg)
            wss.publish(logger_msg, is_mute=is_mute)


class WordReporter(Reporter):
    def report(self, entities: List[WordEntity], msg: str, is_mute=False) -> None:
        container = defaultdict(list)
        [container[entity.level_id].append(entity) for entity in entities]

        for level_id, items in container.items():
            total = len(items)
            id_items = [item_entity.id for item_entity in items]
            logger_msg = Template(msg).substitute(
                level_id=level_id, total=total, id_items=id_items
            )
            logger.info(logger_msg)
            wss.publish(logger_msg, is_mute=is_mute)
