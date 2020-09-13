# pragma: no cover
from abc import ABC, abstractmethod
from typing import List, TypeVar

from memrise.core.modules.factories.entity_makers import DomainEntityT

ItemT = TypeVar("ItemT")


class Factory(ABC):
    """
    Класс, который умеет узнавать, может ли он смаппить определённый EntityMaker в нужный
    формат и умеет создавать нужный maker с параметрами
    """

    @abstractmethod
    def matches(self, item: ItemT) -> bool:
        """Механизм соответствия входящих параметров с конкретным maker"""

    @abstractmethod
    def make_product(self, item: ItemT) -> List[DomainEntityT]:
        """Создание конкретного продукта"""
