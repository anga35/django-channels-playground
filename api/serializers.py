
from rest_framework import serializers
from chat.models import Message

from django.contrib.auth import get_user_model
User=get_user_model()

class MessageSerializer(serializers.ModelSerializer):
    from_user=serializers.CharField(source='from_user.username')
    class Meta:
        model=Message
        fields=['from_user','text_content','date_created']