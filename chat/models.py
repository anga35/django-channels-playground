from operator import mod
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()
class ChatRoom(models.Model):
    users=models.ManyToManyField(User)
    room_name=models.CharField(max_length=100)
    

class Message(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    read_by=models.TextField(default='')
    text_content=models.TextField()
    date_created=models.DateTimeField(auto_now=True)
    chat_room=models.ForeignKey(ChatRoom,related_name='messages',on_delete=models.SET_NULL,null=True,blank=True)
