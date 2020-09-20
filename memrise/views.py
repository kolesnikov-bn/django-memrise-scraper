from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from memrise import logger
from memrise.core.repositoris.repos import MemriseRep, DBRep
from memrise.core.use_cases.update_manager import UpdateManager
from memrise.models import Course, Level, Word
from memrise.serializers import (
    CourseSerializer,
    LevelSerializer,
    WordSerializer,
)


@require_http_methods(["GET"])
def update(request: HttpRequest) -> HttpResponse:
    logger.info("Начало обновления курсов")
    memrise_repo = MemriseRep()
    db_repo = DBRep()

    um = UpdateManager(fresh_repo=memrise_repo, actual_repo=db_repo)
    um.update()
    logger.info("Обновление закончено успешно")
    return HttpResponse("OK")


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer


class LevelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Level.objects.all().order_by("course_id", "number")
    serializer_class = LevelSerializer


class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Word.objects.all().order_by("level", "id")
    serializer_class = WordSerializer
