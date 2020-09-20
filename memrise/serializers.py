from rest_framework import serializers
from rest_framework.fields import CharField

from memrise.models import Course, Word, Level


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "name", "num_things", "num_levels"]


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

    class Meta:
        model = Word
        fields = ["word_a", "word_b", "level", "level_number"]
