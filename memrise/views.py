from __future__ import annotations

from dependencies import Injector
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from memrise import logger
from memrise.core.domains.entities import DashboardEntity
from memrise.core.modules.dashboard_counter import DashboardCounter
from memrise.core.modules.parsing.regular_lxml import RegularLXML
from memrise.core.modules.web_socket_client import wss
from memrise.core.repositoris.repos import MemriseRep, DBRep
from memrise.core.use_cases.loader import DashboardLoader
from memrise.core.use_cases.update_manager import UpdateManager
from memrise.models import Course, Level, Word
from memrise.serializers import (
    CourseSerializer,
    LevelSerializer,
    WordSerializer,
)


@require_http_methods(["GET"])
def update(request: HttpRequest) -> HttpResponse:
    begin_msg = "Начало обновления курсов"
    logger.info(begin_msg)
    wss.publish(begin_msg)

    class Container(Injector):
        manager = UpdateManager
        actual_repo = DBRep
        loader = DashboardLoader
        repo = MemriseRep
        parser = RegularLXML
        counter = DashboardCounter
        dashboard = DashboardEntity

    manager = Container.manager
    manager.update()
    end_message = "Обновление закончено успешно"
    logger.info(end_message)
    wss.publish(end_message)
    wss.close()
    return HttpResponse("OK")


class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Course.objects.all().order_by("-num_things")
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

    queryset = (
        Word.objects.all()
        .prefetch_related("level")
        .prefetch_related("level__course")
        .order_by("level", "id")
    )
    serializer_class = WordSerializer
