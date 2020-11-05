from dataclasses import dataclass, field

from django.conf import settings
from websocket import WebSocket, WebSocketConnectionClosedException

from memrise import logger


@dataclass
class WSS:
    url: str = settings.WEB_SOCKET_SERVER
    wss: WebSocket = field(init=False)

    def __post_init__(self):
        self.wss = WebSocket()

    def connect(self):
        self.wss.connect(self.url)
        message = "Открываем соединение с Web Socket Server"
        logger.debug(message)
        self.wss.send(message)

    def publish(self, message: str, is_mute=False) -> None:
        is_test = settings.TEST is False
        is_debug = settings.DEBUG is False
        is_wss_mute = is_mute is False
        if is_test and is_debug and is_wss_mute:
            if self.wss.sock is None:
                self.connect()

            self.wss.send(message)

    def close(self):
        try:
            message = "Закрываем соеденение с Web Socket Server"
            self.wss.send(message)
            logger.debug(message)
            self.wss.close()
        except WebSocketConnectionClosedException:
            pass


wss = WSS()
