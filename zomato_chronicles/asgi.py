import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import zesty_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zomato_chronicles.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(
        zesty_app.routing.websocket_urlpatterns
    ),
})
