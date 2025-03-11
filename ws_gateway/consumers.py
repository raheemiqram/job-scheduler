from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json


class DashboardAnalyticsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "dashboard_analytics"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_dashboard_data(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        self.send(text_data=json.dumps({
            'message': text_data
        }))
