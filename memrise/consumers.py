import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    channel_path_name = "update.notification"

    async def connect(self):
        await self.channel_layer.group_add(self.channel_path_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.channel_path_name, self.channel_name)

    async def receive(self, text_data):
        """Receive message from WebSocket"""
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to channel
        await self.channel_layer.group_send(
            self.channel_path_name, {"type": "chat.message", "message": message}
        )

    async def chat_message(self, event):
        """Receive message from room group"""
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
