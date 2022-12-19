# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import numpy as np
import random

class ChatConsumer(AsyncWebsocketConsumer):

    
    async def connect(self):
        print('connected')

        # Join room group
        #print("Channel_layer ",self.channel_layer,'\n','Channel Name ',self.channel_name)
        # await self.channel_layer.group_add(
        #     # self.room_group_name,
        #     "Room_1",
        #     self.channel_name

        # )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            #self.room_group_name,
            "Room_1",
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        content = text_data_json['content']
        print('reciving')
        if action == 'join_room':
            # Send message to room group
            print('group_created ',content)
            await self.channel_layer.group_add(
            content,
            self.channel_name,
        )
        
        if action == 'chat_message':
            print('Message_recieved')
            await self.channel_layer.group_send(
                content['roomName'],
                {
                    type:action,
                    content:content['message'],
                }
            )
        #Send message to room group
        # await self.channel_layer.group_send(
        #     'Room_1',
        #     {
        #         'type': 'chat_message',
        #         'message': content
        #     }
        # )

    # Receive message from room group
    async def chat_message(self, event):
        print('message shared')
        content = event['content']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': content
        }))











class HomeConsumer(AsyncWebsocketConsumer):
    all_users = {}
    async def connect(self):
        
        randomNum = random.randint(0,22)
        self.all_users[randomNum] = self.channel_name
        print(self.all_users)
        # Join room group
        #print("Channel_layer ",self.channel_layer,'\n','Channel Name ',self.channel_name)
        # await self.channel_layer.group_add(
        #     # self.room_group_name,
        #     "Room_1",
        #     self.channel_name

        # )


        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            #self.room_group_name,
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        print(text_data)
        text_data_json = json.loads(text_data)
        action = text_data_json['action']
        content = text_data_json['content']
        print('reciving')
        if action == 'join_room':
            self.room_name = content
            # Send message to room group
            print('group_created ',content)
            await self.channel_layer.group_add(
            content,
            self.channel_name,
        )
        
        if action == 'chat_message':
            print("-"*50,'Chat Message','-'*50)
            print('Message_recieved')
            print('Message: ',content)

            #Loops over every socket in the given room and self.send is going to run for each members.
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type':action,
                    'content':content,
                }
            )

    # Receive message from room group
    async def chat_message(self, event):
        print('message shared')
        content = event['content']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': content
        }))