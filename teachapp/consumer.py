# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels import layers
import asyncio

class TestingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'teachapp_%s' % self.room_name
        print("room_name connected : ",self.room_group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("msg from websocket ", message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'listen_msg',
                'message': message
            }
        )

    # Receive message from room group
    async def listen_msg(self, event):
        message = event['message']
        print("msg from room ", message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def sendLogTraining(RoomCode ,Log):
        channles = layers.get_channel_layer()
        await channles.group_send(
            RoomCode,
            {
                'type': 'listen_msg',
                'message': Log
            }
        )


async def doSendLogTraining(RoomCode ,Log):
    res = await asyncio.gather(TestingConsumer.sendLogTraining(RoomCode=RoomCode, Log=Log))
    return res
    
