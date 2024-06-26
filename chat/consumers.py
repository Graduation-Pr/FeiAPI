from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from accounts.models import User
from chat.models import Message, Connection
from chat.serializers import MessageSerializer, UserSerializer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import jwt


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = await self.get_user(self.scope)

        if not self.user.is_authenticated:
            await self.close()
            return

        self.username = (
            self.user.username
        )  # Set self.username to the authenticated user's username

        # Join this user to a group with their username
        await self.channel_layer.group_add(self.username, self.channel_name)
        await self.accept()

    async def get_user(self, scope):
        if "token" in scope["query_string"].decode():
            token = scope["query_string"].decode().split("token=")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await database_sync_to_async(User.objects.get)(
                    id=payload["user_id"]
                )
                return user
            except jwt.ExpiredSignatureError:
                return AnonymousUser()
            except (jwt.InvalidTokenError, User.DoesNotExist):
                return AnonymousUser()
        return AnonymousUser()

    async def disconnect(self, close_code):
        # Leave room/group
        await self.channel_layer.group_discard(self.username, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        data_source = data.get("source")
        print("Received:", json.dumps(data, indent=2))

        if data_source == "message.list":
            await self.receive_message_list(data)
        elif data_source == "message.send":
            await self.receive_message_send(data)

    async def receive_message_list(self, data):
        user = self.scope["user"]
        connection_id = data.get("connectionId")
        page = data.get("page", 0)
        page_size = 15

        try:
            connection = await sync_to_async(Connection.objects.get)(id=connection_id)
        except Connection.DoesNotExist:
            print("Error: couldn't find connection")
            return

        messages = await sync_to_async(list)(
            Message.objects.filter(connection=connection).order_by("-created")[
                page * page_size : (page + 1) * page_size
            ]
        )
        serialized_messages = MessageSerializer(
            messages, context={"user": user}, many=True
        )
        recipient = (
            connection.sender if connection.sender != user else connection.receiver
        )
        serialized_friend = UserSerializer(recipient)
        messages_count = await sync_to_async(
            Message.objects.filter(connection=connection).count
        )()
        next_page = page + 1 if messages_count > (page + 1) * page_size else None

        data = {
            "messages": serialized_messages.data,
            "next": next_page,
            "friend": serialized_friend.data,
        }
        await self.send_group(user.username, "message.list", data)

    async def receive_message_send(self, data):
        user = self.scope["user"]
        connection_id = data.get("connectionId")
        message_text = data.get("message")

        try:
            connection = await sync_to_async(Connection.objects.get)(id=connection_id)
        except Connection.DoesNotExist:
            print("Error: couldn't find connection")
            return

        message = await sync_to_async(Message.objects.create)(
            connection=connection, user=user, text=message_text
        )
        recipient = (
            connection.sender if connection.sender != user else connection.receiver
        )
        serialized_message = MessageSerializer(message, context={"user": user})
        serialized_friend = UserSerializer(recipient)

        data = {"message": serialized_message.data, "friend": serialized_friend.data}
        await self.send_group(user.username, "message.send", data)

        serialized_message = MessageSerializer(message, context={"user": recipient})
        serialized_friend = UserSerializer(user)
        data = {"message": serialized_message.data, "friend": serialized_friend.data}
        await self.send_group(recipient.username, "message.send", data)

    async def send_group(self, group, source, data):
        response = {"type": "broadcast_group", "source": source, "data": data}
        await self.channel_layer.group_send(group, response)

    async def broadcast_group(self, event):
        data = event.copy()
        data.pop("type")
        await self.send(text_data=json.dumps(data))