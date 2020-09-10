from rest_framework import viewsets

from memrise.models import Course, Level, Word
from memrise.serializers import CourseSerializer, LevelSerializer, WordSerializer


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
