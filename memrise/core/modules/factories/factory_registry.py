from abc import ABC
from dataclasses import dataclass, field
from typing import List, Set, Type, ClassVar

from memrise.core.modules.factories.base import Factory, ItemT
from memrise.core.modules.factories.entity_makers import DomainEntityT


@dataclass
class FactoryHandler(ABC):
    """
    Агрегирующий класс, позволяющий регистрировать у себя фабрики makers,
    производить поиск фабрик по критериям и создавать конкретный maker
    """

    _factories: List["Factory"] = field(init=False, default_factory=list)
    _registered: Set[str] = field(init=False, default_factory=set)
    strict: ClassVar[bool] = False

    def register(self, cls: Type[Factory]) -> Type[Factory]:
        """Регистрация фабрики maker

        :param cls: фабрика создания maker
        """
        if not issubclass(cls, Factory):
            raise TypeError("Можно зарегестрировато только подклассы от Factory")

        if cls.__name__ in self._registered:
            raise ValueError(f"`{cls.__name__}` класс уже зарегистрирован")

        self._factories.append(cls())
        self._registered.add(cls.__name__)
        return cls

    def seek(self, item: ItemT) -> List[DomainEntityT]:
        """Поиск конкретной фабрики по входящим параметам makers """
        matches: List[Factory] = [
            factory for factory in self._factories if factory.matches(item)
        ]

        if not matches:
            raise ValueError(f"Не найдено ни одиной фабрики по параметрам: `{item}`")

        if self.strict is True:
            if len(matches) > 1:
                raise ValueError("Найдено более одной фабрики!!!", matches, item)

        product = matches[0]
        return product.make_product(item)
