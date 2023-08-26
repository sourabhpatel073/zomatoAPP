from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "notifications",
            self.channel_name
        )
        await self.accept()
        print("[WebSocket] Connection accepted.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "notifications",
            self.channel_name
        )
        print(f"[WebSocket] Disconnected with code: {close_code}.")

    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     print(f"[WebSocket] Received: {text_data}")

    #     if data['type'] == 'order_status':
    #         await self.channel_layer.group_send(
    #             "notifications",
    #             self.channel_name
    #         )
    #     else:
    #         await self.send(text_data=text_data)  # Simply echo back other messages

    async def order_status(self, event):
        # Handle the message from the group and send it to the WebSocket
        print(f"[WebSocket] Forwarding order status: {event}")
        await self.send(text_data=json.dumps(event))
