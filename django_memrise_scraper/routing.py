from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from memrise.consumers import ChatConsumer

application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "websocket": AuthMiddlewareStack(URLRouter([re_path(r"ws/", ChatConsumer)])),
    }
)
