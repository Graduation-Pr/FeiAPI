from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),  # Note the 'as_asgi()' method
]
