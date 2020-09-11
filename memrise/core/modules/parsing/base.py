"""
Базовый модуль парсинга данных со страницы курса или курсов используемый при построении обхода курсов через стратегии
===========================================================

Описание и назначение:
----------------------

При начале обхода вытягивания слов с учебного курса, можно будет выстроить список стратегий, которые при обходе
будут вытягивать данные.
Можно будет создать как отдельные стратегии с испольванием различных библиотек, например: lxml, beautifulSoup, scrapy
Или же различные стратегии для получения основных слов курса, так и слова `difficult`, которые имееют отличное дерево
формирования html в отличнии от `regular`

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from memrise.core.domains.entities import LevelEntity

if TYPE_CHECKING:
    pass


@dataclass  # type: ignore
class Parser(ABC):
    level: LevelEntity = field(init=False)

    @abstractmethod
    def parse(self, response: str, level_num: int) -> LevelEntity:
        """Парсинг слов в учебном курсе"""
