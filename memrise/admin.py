from django.contrib import admin

from memrise.models import Course, Level, Word


class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]}),
        (
            "Detail",
            {"fields": ["url", "num_things", "num_levels"], "classes": ["collapse"]},
        ),
    ]
    list_filter = ["num_levels"]


class LevelAdmin(admin.ModelAdmin):
    list_filter = ["course"]


class WordAdmin(admin.ModelAdmin):
    search_fields = ["word_a", "word_b"]
    fieldsets = [
        (None, {"fields": ["word_a", "word_b"]}),
        ("Detail", {"fields": ["thing_id", "level"], "classes": ["collapse"]},),
    ]
    list_filter = ["level__course"]


admin.site.register(Course, CourseAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Word, WordAdmin)
