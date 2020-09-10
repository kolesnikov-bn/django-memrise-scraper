from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse

from memrise.models import Course, Level, Word


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        (
            "Detail",
            {"fields": ["url", "num_things", "num_levels"], "classes": ["collapse"]},
        ),
    ]
    list_filter = ["num_levels"]


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_filter = ["course"]
    list_display = ["number", "name", "course"]
    ordering = ["course", "number"]


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    search_fields = ["word_a", "word_b"]
    fieldsets = [
        (None, {"fields": ["word_a", "word_b"]}),
        ("Detail", {"fields": ["thing_id", "level"], "classes": ["collapse"]},),
    ]
    list_filter = ["level__course"]
    actions = ["export_as_json"]
    list_display = ["word_a", "word_b"]

    def export_as_json(self, request, queryset):
        response = HttpResponse(content_type="application/json")
        serializers.serialize("json", queryset, stream=response, indent=2)
        return response
