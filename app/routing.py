from channels.routing import ProtocolTypeRouter
from .asgi import application


application = ProtocolTypeRouter({
    "http": application,
    # Just HTTP for now. (We can add other protocols later.)
})