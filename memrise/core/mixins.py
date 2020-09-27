from abc import ABC

from dataclasses import dataclass, asdict
from typing import Set, Dict


@dataclass
class Mixin(ABC):
    pass


@dataclass
class AsDictMixin(Mixin):
    def as_dict(self, exclude: Set["str"]) -> Dict:
        entity_dict = asdict(self)

        for key in exclude:
            del entity_dict[key]

        return entity_dict
