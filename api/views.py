from tokenize import Token
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from chat.models import Message
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import MessageSerializer


User=get_user_model()
# Create your views here.

class GetUnreadMessages(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        username=user.username
        print(username)

        chat_room=user.chatroom_set.all().first()
        print(chat_room)
        messages=Message.objects.order_by('date_created').exclude(from_user=user
        ).exclude(read_by__contains=username).filter(chat_room=chat_room)#'-' annotates reverse order_by
        
        for message in messages:
            message.read_by=f'{message.read_by}{username},'
            message.save()

        serializer=MessageSerializer(messages,many=True)
        data=serializer.data
        return Response(data={'messages':data},status=200)

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


