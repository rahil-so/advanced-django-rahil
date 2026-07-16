from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(
            text_data=json.dumps({
                'message': 'Welcome to the chat',
            })
        )

    def disconnect(self, close_code):
        self.send(
            text_data=json.dumps({
                'message': 'You have been disconnected',
            })
        )

    def receive(self, text_data=None):
        data = json.loads(text_data)
        print(data)
        self.send(
            text_data= json.dumps({
                "echo": data['message'],
            })
        )


class UploadProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.job_id = self.scope['url_route']['kwargs']['job_id']
        self.group_name = self.scope['url_route']['kwargs']['group_id']
        await self.channel_layer.group_add(self.group_name, self.channel_name )
        await self.accept()

