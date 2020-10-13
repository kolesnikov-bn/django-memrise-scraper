from rest_framework import routers

from memrise.views import CourseViewSet, LevelViewSet, WordViewSet, DuplicateViewSet

router = routers.DefaultRouter()

router.register("course", CourseViewSet)
router.register("level", LevelViewSet)
router.register("word", WordViewSet)
router.register("duplicates", DuplicateViewSet)
