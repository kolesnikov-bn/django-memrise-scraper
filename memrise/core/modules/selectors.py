"""
Модуль импорта и сравнения сущностей с новыми данными и сохранненными
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar, Generator

from pydantic import BaseModel, Field

from memrise.core.domains.entities import CourseEntity, LevelEntity, WordEntity

DomainEntity = TypeVar("DomainEntity", CourseEntity, LevelEntity, WordEntity)


class DiffContainer(BaseModel, Generic[DomainEntity]):
    create: List[DomainEntity] = Field(default_factory=list)
    update: List[DomainEntity] = Field(default_factory=list)
    equal: List[DomainEntity] = Field(default_factory=list)
    delete: List[DomainEntity] = Field(default_factory=list)

    def __iter__(self) -> "Generator":
        yield from self.__dict__.items()


class Selector(ABC, Generic[DomainEntity]):
    @classmethod
    @abstractmethod
    def match(
        cls, fresh_entities: List[DomainEntity], actual_entities: List[DomainEntity]
    ) -> DiffContainer[DomainEntity]:
        """Сравнение новых данных и сохраненных, а также возвращение контейнера с дельтой между ними"""


class CourseSelector(Selector):
    @classmethod
    def match(
        cls, fresh_entities: List[CourseEntity], actual_entities: List[CourseEntity]
    ) -> DiffContainer[CourseEntity]:

        diff: DiffContainer[CourseEntity] = DiffContainer()
        exists_actual_items = {
            actual_entity.id: actual_entity for actual_entity in actual_entities
        }
        # Убираем ключи которые не будут участвовать в сравнении. Эти ключи будут сравниваться в отдельном отборщике.
        excluded = {"levels", "levels_url"}

        for entity in fresh_entities:
            entity_id = entity.id

            if entity_id not in exists_actual_items:
                diff.create.append(entity)
            elif exists_actual_items[entity_id].dict(exclude=excluded) != entity.dict(
                exclude=excluded
            ):
                diff.update.append(entity)
                del exists_actual_items[entity_id]
            else:
                diff.equal.append(entity)
                del exists_actual_items[entity_id]

        for actual_item in exists_actual_items:
            diff.delete.append(exists_actual_items[actual_item])

        return diff


class LevelSelector(Selector):
    @classmethod
    def match(
        cls, fresh_entities: List[LevelEntity], actual_entities: List[LevelEntity]
    ) -> DiffContainer[LevelEntity]:
        diff = DiffContainer()
        exists_actual_items = {
            actual_entity.id: actual_entity for actual_entity in actual_entities
        }
        # Убираем ключи которые не будут участвовать в сравнении. Эти ключи будут сравниваться в отдельном отборщике.
        excluded = {"words"}

        for entity in fresh_entities:
            entity_id = entity.id

            if entity_id not in exists_actual_items:
                diff.create.append(entity)
            elif exists_actual_items[entity_id].dict(exclude=excluded) != entity.dict(
                exclude=excluded
            ):
                diff.update.append(entity)
                del exists_actual_items[entity_id]
            else:
                diff.equal.append(entity)
                del exists_actual_items[entity_id]

        for actual_item in exists_actual_items:
            diff.delete.append(exists_actual_items[actual_item])

        return diff


class WordSelector(Selector):
    @classmethod
    def match(
        cls, fresh_entities: List[WordEntity], actual_entities: List[WordEntity]
    ) -> DiffContainer[WordEntity]:
        diff = DiffContainer()
        exists_actual_items = {
            actual_entity.id: actual_entity for actual_entity in actual_entities
        }

        for entity in fresh_entities:
            entity_id = entity.id
            if entity_id not in exists_actual_items:
                diff.create.append(entity)
            elif exists_actual_items[entity_id] != entity:
                diff.update.append(entity)
                del exists_actual_items[entity_id]
            else:
                diff.equal.append(entity)
                del exists_actual_items[entity_id]

        for actual_item in exists_actual_items:
            diff.delete.append(exists_actual_items[actual_item])

        return diff
