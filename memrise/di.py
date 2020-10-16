from _dependencies.injector import Injector

from memrise.core.modules.actions.actions_batch import DBActionsBatch
from memrise.core.modules.counter import MemriseRequestCounter
from memrise.core.modules.parsing.regular_lxml import RegularLXML
from memrise.core.repositories.repos import DBRep, MemriseRep
from memrise.core.use_cases.dashboard import (
    Dashboard,
    DashboardCourseContainer,
)
from memrise.core.use_cases.update_manager import UpdateManager


class UpdateMemriseContainer(Injector):
    manager = UpdateManager
    actual_repo = DBRep
    dashboard = Dashboard
    origin_repo = MemriseRep
    parser = RegularLXML
    counter = MemriseRequestCounter
    course_container = DashboardCourseContainer
    batch = DBActionsBatch
