# from channels.routing import ProtocolTypeRouter, URLRouter
# from zesty_app import routing

# application = ProtocolTypeRouter({
#     'websocket': URLRouter(
#         routing.websocket_urlpatterns
#     ),
# })

from channels.routing import ProtocolTypeRouter, URLRouter
import zesty_app.routing

application = ProtocolTypeRouter({
    "websocket": URLRouter(zesty_app.routing.websocket_urlpatterns)
})
