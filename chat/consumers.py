from email import message
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message,ChatRoom
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async


User=get_user_model()
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name=f'chat_{self.room_name}'

        #Join group to enable communication between all channels in group
        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json=json.loads(text_data)
        print(text_data_json)
        if 'read_pk' in text_data_json:
            pk=text_data_json['read_pk']
            
            user_name=text_data_json['user_name']

            print(f'THIS IS PK {pk} {user_name}')
            await self.read_message(pk=pk,user_name=user_name)

            

        elif 'persist_username' in text_data_json :
            self.username=text_data_json['persist_username']
            print(self.username)
        else:
            message=text_data_json['message']

            user_name=text_data_json['user_name']
        

        #Create Message for the user sending message

            print("HIIII")
            message_obj=await self.save_message(username=user_name,
            text_content=message)
            await(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'from_user':user_name,
                'message_pk':message_obj.pk
            }
        )


    
    async def chat_message(self,event):
        message=event['message']
        from_user=event['from_user']
        pk=event['message_pk']



        #send the message to group
        await self.send(text_data=json.dumps({
            'message':message,
            'from_user':from_user,
            'pk':pk
        }))

    @database_sync_to_async
    def save_message(self,username,text_content):
            user=User.objects.get(username=username)
            chat_room=ChatRoom.objects.get(room_name=self.room_name)
            message_obj=Message.objects.create(from_user=user,text_content=text_content,chat_room=chat_room)
            message_obj.save()      
            return message_obj  

    @database_sync_to_async
    def read_message(self,pk,user_name):
            message=Message.objects.get(pk=pk)
            message.read_by=f'{message.read_by}{user_name},'
            message.save()