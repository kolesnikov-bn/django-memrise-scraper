from memrise.shares.types import URL
from django.conf import settings

DIFFICULT_ITEM_URL = URL("difficult-items/")


DASHBOARD_FIXTURE = settings.RESOURSES / "fixtures/dashboard_response.json"
LEVELS_FIXTURE = settings.RESOURSES / "fixtures/levels_entity.json"
