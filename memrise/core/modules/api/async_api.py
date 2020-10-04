from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
from urllib.parse import urljoin

from aiohttp import ClientSession, ClientResponse
from django.conf import settings

from memrise import logger
from memrise.core.modules.web_socket_client import wss
from memrise.shares.types import URL

GET, POST = "GET", "POST"


@dataclass
class AsyncAPI:
    timeout: int = 90
    ssl: bool = False
    headers: Dict = field(init=False)
    cookies: Dict = field(init=False)

    def __post_init__(self) -> None:
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": settings.USER_AGENT,
            "charset": "utf-8",
        }
        self.cookies = settings.MEMRISE_COOKIES

    async def fetch(
        self, session: ClientSession, method: str, endpoint: URL
    ) -> ClientResponse:
        url = urljoin(settings.MEMRISE_HOST, endpoint)
        response = await session.request(method, url, ssl=self.ssl)
        response.raise_for_status()
        logger.debug(f"Got response [{response.status}] for URL: {url}, ({response.content=})")
        wss.publish(f"Memrise API request: {method} {url}: {response}",)
        return response

    async def get_level(self, endpoint: URL) -> str:
        """ Асинхронное получение конкретного уровня из Memrise """
        # TODO: Пересмотреть логику работы с ассинхронными запросами
        async with ClientSession(cookies=self.cookies, headers=self.headers) as session:
            response = await self.fetch(session, GET, endpoint)
            return await response.text()


async_api = AsyncAPI()
