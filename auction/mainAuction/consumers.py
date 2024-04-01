from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['dashboard']
        print(self.room_name)
        self.room_group_name = 'auction_%s' % self.room_name

        print("Conncted")
        # print(get_channel_layer())

        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
    )

        await self.accept()
        await self.send(text_data=json.dumps({
            'message':'connected',
            'type':'log'
        }))


    async def disconnect(self, close_code):
            # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        amount = text_data_json['amount']
        sender = text_data_json["sender"]

        print(amount, sender)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'messagefun',
                'message':amount
            },
        )

    async def messagefun(self, event):

        message = event["message"]

        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message

        }))


    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'type': 'messagefun',
    #             'message': message
    #         }
    #     )


        # await self.send(text_data=json.dumps({
        #     'message': message,
        #     'sender': sender
        # }))
