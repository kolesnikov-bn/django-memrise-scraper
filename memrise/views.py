from __future__ import annotations

from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets

from memrise import logger
from memrise.core.modules.web_socket_client import wss
from memrise.di import UpdateMemriseContainer
from memrise.models import Course, Level, Word
from memrise.serializers import (
    CourseSerializer,
    LevelSerializer,
    WordSerializer,
    DuplicateSerializer,
)


@require_http_methods(["GET"])
def update(request: HttpRequest) -> HttpResponse:
    begin_msg = "Начало обновления курсов"
    logger.info(begin_msg)
    wss.publish(begin_msg)
    manager = UpdateMemriseContainer.manager
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


class DuplicateViewSet(viewsets.ModelViewSet):
    duplicates = (
        Word.objects.values("word_a")
        .annotate(name_count=Count("word_a"))
        .filter(name_count__gt=1)
    )
    records = (
        Word.objects.filter(word_a__in=[item["word_a"] for item in duplicates])
        .prefetch_related("level")
        .prefetch_related("level__course")
        .order_by("word_a")
    )

    queryset = records
    serializer_class = DuplicateSerializer
