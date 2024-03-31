import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auction.settings")

djnago_asgi_app = get_asgi_application()

import  mainAuction.routing

application = ProtocolTypeRouter(
    {
        "http": djnago_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(mainAuction.routing.websocket_urlpatterns))
        )
    }
)