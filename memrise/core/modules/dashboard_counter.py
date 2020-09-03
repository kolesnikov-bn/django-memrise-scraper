from itertools import count
from typing import Callable, Dict

from pydantic import BaseModel

LIMIT = 4
STEP = LIMIT + 1
START_OFFSET = 0


def counter(step: int) -> Callable[[], int]:
    return count(start=0, step=step).__next__


class DashboardCounter(BaseModel):
    courses_filter: str = "learning"
    offset: int = START_OFFSET
    limit: int = LIMIT
    get_review_count: str = "true"
    category_id: int = 6
    counter: Callable[[], int] = counter(STEP)

    def next(self) -> Dict:
        self.offset = self.counter()  # type: ignore
        return self.dict(exclude={"counter"})
