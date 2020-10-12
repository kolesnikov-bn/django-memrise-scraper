from collections import defaultdict
from string import Template
from typing import List

from memrise import logger
from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity


class ActionReporter:
    @classmethod
    def course_report(cls, entities: List[CourseEntity], msg: str) -> None:
        total = len(entities)
        id_items = [item_entity.id for item_entity in entities]
        logger_msg = Template(msg).substitute(total=total, id_items=id_items)
        logger.info(logger_msg)

    @classmethod
    def level_report(cls, entities: List[LevelEntity], msg: str) -> None:
        container = defaultdict(list)
        [container[entity.course_id].append(entity) for entity in entities]

        for course_id, items in container.items():
            total = len(items)
            id_items = [item_entity.id for item_entity in items]
            logger_msg = Template(msg).substitute(
                course_id=course_id, total=total, id_items=id_items
            )
            logger.info(logger_msg)

    @classmethod
    def word_report(cls, entities: List[WordEntity], msg: str) -> None:
        container = defaultdict(list)
        [container[entity.level_id].append(entity) for entity in entities]

        for level_id, items in container.items():
            total = len(items)
            id_items = [item_entity.id for item_entity in items]
            logger_msg = Template(msg).substitute(
                level_id=level_id, total=total, id_items=id_items
            )
            logger.info(logger_msg)