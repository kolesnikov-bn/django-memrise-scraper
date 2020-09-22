import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_memrise_scraper.settings")
app = Celery("django_memrise_scraper")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
