from _dependencies.injector import Injector

from memrise.core.modules.dashboard_counter import DashboardCounter
from memrise.core.modules.parsing.regular_lxml import RegularLXML
from memrise.core.repositoris.repos import DBRep, MemriseRep
from memrise.core.use_cases.dashboard import Dashboard
from memrise.core.use_cases.entities import DashboardContainer
from memrise.core.use_cases.update_manager import UpdateManager


class UpdateContainer(Injector):
    manager = UpdateManager
    actual_repo = DBRep
    dashboard = Dashboard
    repo = MemriseRep
    parser = RegularLXML
    counter = DashboardCounter
    course_container = DashboardContainer
