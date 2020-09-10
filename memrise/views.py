from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods

from memrise import logger
from memrise.core.modules.api.base import api


@require_http_methods(["GET"])
def checkout(request: HttpRequest) -> HttpResponse:
    logger.info("Начало обновления курсов")
    params = dict(
        courses_filter="learning",
        offset=0,
        limit=4,
        get_review_count="true",
        category_id=6,
    )
    result = api.load_dashboard_courses(params)

    return HttpResponse("OK")
