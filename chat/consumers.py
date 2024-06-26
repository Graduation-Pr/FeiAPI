import json
import base64
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected: ", close_code)