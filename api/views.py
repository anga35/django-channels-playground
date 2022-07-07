from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from chat.models import Message
from rest_framework.response import Response
from rest_framework import serializers


User=get_user_model()
# Create your views here.

class GetUnreadMessages(APIView):
    def post(self,request):
        data=request.data
        username=data['username']
        print(username)
        user=User.objects.get(username=username)
        print(user)
        chat_room=user.chatroom_set.all().first()
        print(chat_room)
        messages=Message.objects.order_by('date_created').exclude(from_user=user
        ).exclude(read_by__contains=username).filter(chat_room=chat_room)#'-' annotates reverse order_by
        
        for message in messages:
            message.read_by=f'{message.read_by}{username},'
            message.save()
        print(messages)

        return Response(status=200)

class MessagesRead(APIView):
    def post(self,request):
        data=request.data
        username=data['username']
        message_pks=data['pk']
        if(type(message_pks)==list):
            for pk in message_pks:
                if(type(pk)==int):
                    message=get_object_or_404(Message,pk=pk)
                    message.read_by=f'{message.read_by}{username},'
                    message.save()
        else:
            raise serializers.ValidationError('')


