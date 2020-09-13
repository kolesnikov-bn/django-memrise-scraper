from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import ClassVar, Dict
from urllib.parse import urljoin

import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from memrise import logger
from memrise.core.modules.api.errors import APIError
from memrise.shares.contants import DASHBOARD_URL
from memrise.shares.types import URL

GET, POST = "GET", "POST"


@dataclass
class API:
    timeout: int = 90
    retries: ClassVar[Retry] = Retry(total=5, connect=3, read=2, backoff_factor=0.1)

    def __post_init__(self) -> None:
        self._session = requests.Session()
        self._session.mount("http://", HTTPAdapter(max_retries=self.retries))
        self._session.mount("https://", HTTPAdapter(max_retries=self.retries))

    def request(
        self, method: str, endpoint: URL, params: Dict = None, data: Dict = None
    ) -> requests.Response:
        url = urljoin(settings.MEMRISE_HOST, endpoint)
        start = time()

        headers = {
            "Content-Type": "application/json",
            "User-Agent": settings.USER_AGENT,
            "charset": "utf-8",
        }

        response = self._session.request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            timeout=self.timeout,
            cookies=settings.MEMRISE_COOKIES,
        )
        duration = time() - start

        logger.debug(
            f"({duration:.3f}) SRSAPI request: {method} {url} ({params=},{data=}):{response}",
            extra={
                "method": method,
                "url": url,
                "duration": duration,
                "request": {"params": params, "data": data},
                "response": response,
            },
        )

        if response.status_code not in (200, 400):
            raise APIError(
                "Unexpected status",
                {"message": response.content, "error_code": response.status_code},
            )

        return response

    def load_dashboard_courses(self, params: Dict) -> Dict:
        """ Получение курсов из Memrise.Dashboard """
        response = self.request(GET, DASHBOARD_URL, params=params)
        return response.json()

    def get_level(self, endpoint: URL) -> str:
        """ Получение конкретного уровня из учебого курса Memrise """
        result = self.request(GET, endpoint)
        return result.text


api = API()
