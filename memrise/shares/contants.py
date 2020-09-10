from django.conf import settings

from memrise.shares.types import URL

# <editor-fold desc="API's.">
# Endpoint для получения сложных слов.
DIFFICULT_ITEMS_URL = URL("difficult-items/")
# Endpoint для получения курстов в dashboard пользователя.
DASHBOARD_URL = URL("/ajax/courses/dashboard")
# </editor-fold>


DASHBOARD_FIXTURE = settings.RESOURSES / "fixtures/dashboard_response.json"
LEVELS_FIXTURE = settings.RESOURSES / "fixtures/levels_entity.json"
