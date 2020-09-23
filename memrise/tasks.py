from django_memrise_scraper.celery import app
from memrise import logger


@app.task(bind=True)
def debug_task(self) -> None:
    """Проверочная задача"""
    logger.debug(self.request.id)
