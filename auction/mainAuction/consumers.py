from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from appdata.models import Auction, Player, AuctionPlayer

channel_layer = get_channel_layer()

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['dashboard']
        self.room_group_name = 'auction_%s' % self.room_name
        self.team = None
        
        self.auction = self.scope['url_route']['kwargs']['dashboard']
        
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
        action = text_data_json['action']
        bdata = None

        print(self.scope['session']['user'])        
        if action == 'bid' and self.scope['session']['user'] == 2:
            print(self.scope)
            bdata = {'team':team, 'player':player, 'amount': amount}

        elif action == 'getrandom' and self.scope['session']['user'] == 3:
            auction = AuctionPlayer.objects.filter(auctionId=self.auction)
            bdata = {'player':player}
            
            print("Admin Get Random")
        
        elif action == 'sold' and self.scope['session']['user'] == 3:
            team = text_data_json.team
            bid = text_data_json.bid
            player = text_data_json.player
            bdata = {'team':team, 'player':player, 'amount': bid}


            print("Player Sold")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'messagefun',
                'message':json.dumps(bdata)
            },
        )

    async def messagefun(self, event):

        message = event["message"]

        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message

        }))

