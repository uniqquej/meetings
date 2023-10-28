import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from config.middlewarers import  WebSocketJWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

import chat.routings

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": 
            WebSocketJWTAuthMiddleware(
                URLRouter(
                    chat.routings.websocket_urlpatterns,
                )
            ),
    }
)
