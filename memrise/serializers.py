from django.conf import settings
from rest_framework import serializers
from rest_framework.fields import CharField

from memrise.models import Course, Word, Level


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "num_things", "num_levels", "is_disable"]


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = "__all__"


class LevelRelatedCourseField(serializers.RelatedField):
    def to_representation(self, value):
        return value.course.name


class WordSerializer(serializers.ModelSerializer):
    level = LevelRelatedCourseField(read_only=True)
    level_number = CharField(source="level.number")
    course_url = CharField(source="level.course.url")

    host = serializers.SerializerMethodField()

    def get_host(self, obj):
        return settings.MEMRISE_HOST

    class Meta:
        model = Word
        fields = ["word_a", "word_b", "level", "level_number", "course_url", "host"]


class DuplicateSerializer(serializers.ModelSerializer):
    course_name = CharField(source="level.course.name")
    level_number = CharField(source="level.number")
    course_url = CharField(source="level.course.url")

    host = serializers.SerializerMethodField()

    def get_host(self, obj):
        return settings.MEMRISE_HOST

    class Meta:
        model = Word
        fields = [
            "pk",
            "word_a",
            "word_b",
            "level",
            "level_number",
            "course_name",
            "course_url",
            "host",
        ]
