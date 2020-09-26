from dataclasses import dataclass, field

from django.conf import settings
from websocket import WebSocket


@dataclass
class WSS:
    url: str = settings.WEB_SOCKET_SERVER
    wss: WebSocket = field(init=False)

    def __post_init__(self):
        self.wss = WebSocket()
        self.connect()

    def connect(self):
        self.wss.connect(self.url)

    def publish(self, message: str) -> None:
        self.wss.send(message)
        # self.wss.close()


wss = WSS()
