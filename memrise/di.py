from _dependencies.injector import Injector

from memrise.core.modules.dashboard_counter import DashboardCounter
from memrise.core.modules.parsing.regular_lxml import RegularLXML
from memrise.core.repositoris.repos import DBRep, MemriseRep
from memrise.core.use_cases.entities import Dashboard
from memrise.core.use_cases.loader import DashboardLoader
from memrise.core.use_cases.update_manager import UpdateManager


class UpdateContainer(Injector):
    manager = UpdateManager
    actual_repo = DBRep
    loader = DashboardLoader
    repo = MemriseRep
    parser = RegularLXML
    counter = DashboardCounter
    dashboard = Dashboard
