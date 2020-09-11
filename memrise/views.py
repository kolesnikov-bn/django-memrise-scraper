from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from memrise import logger
from memrise.core.use_cases.update_manager import UpdateManager


@require_http_methods(["GET"])
def update(request: HttpRequest) -> HttpResponse:
    logger.info("Начало обновления курсов")
    um = UpdateManager()
    um.update()

    return HttpResponse("OK")
