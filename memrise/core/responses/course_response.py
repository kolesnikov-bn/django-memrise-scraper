from dataclasses import dataclass
from typing import Generator, List, Optional
from uuid import UUID


@dataclass
class Category:
    name: str
    photo: str


@dataclass
class Goal:
    course_id: int
    goal: int
    points: int
    streak: int


@dataclass
class SelectorClass:
    session_type: str
    is_enabled: bool
    counter: int
    is_pro: bool
    url: Optional[str] = None


@dataclass
class NextSession:
    recommendation_id: UUID
    next_session: SelectorClass
    selector: List[SelectorClass]
    is_unlocked: bool

    def __post_init__(self) -> None:
        # На входе для всех пользовательских типов входят словари, по этому преобразуем их в типы.
        self.next_session = SelectorClass(**self.next_session)
        self.selector = [SelectorClass(**item) for item in self.selector]


@dataclass
class Source:
    id: int
    slug: str
    name: str
    photo: str
    parent_id: int
    index: int
    language_code: str


@dataclass
class CourseItemResponse:
    id: int
    name: str
    slug: str
    url: str
    description: str
    photo: str
    photo_small: str
    photo_large: str
    num_things: int
    num_levels: int
    num_learners: int
    source: Source
    target: Source
    learned: int
    review: int
    ignored: int
    ltm: int
    difficult: int
    category: Category
    next_session: NextSession
    percent_complete: int
    goal: Optional[Goal] = None

    def __post_init__(self) -> None:
        # На входе для всех пользовательских типов входят словари, по этому преобразуем их в типы.
        self.category = Category(**self.category)
        self.next_session = NextSession(**self.next_session)
        self.source = Source(**self.source)
        self.target = Source(**self.target)
        if self.goal:
            self.goal = Goal(**self.goal)


@dataclass
class CoursesResponse:
    courses: List[CourseItemResponse]
    to_review_total: Optional[int]
    has_more_courses: Optional[bool] = False

    def __post_init__(self) -> None:
        # На входе для всех пользовательских типов входят словари, по этому преобразуем их в типы.
        self.courses = [CourseItemResponse(**course) for course in self.courses]

    def iterator(self) -> Generator[CourseItemResponse, None, None]:
        yield from self.courses
