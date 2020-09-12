from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from memrise import logger
from memrise.core.repositoris.repos import MemriseRep, DBRep
from memrise.core.use_cases.update_manager import UpdateManager


@require_http_methods(["GET"])
def update(request: HttpRequest) -> HttpResponse:
    logger.info("Начало обновления курсов")
    memrise_repo = MemriseRep()
    db_repo = DBRep()

    um = UpdateManager(fresh_repo=memrise_repo, actual_repo=db_repo)
    um.update()

    return HttpResponse("OK")
