from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from .models import Chat

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields =  ['id', 'username']

        

class ChatSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Chat
        fields = ['id', 'user', 'title', 'chats', 'is_public', 'is_forked',  'updated_at']