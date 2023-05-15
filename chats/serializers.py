from rest_framework.serializers import ModelSerializer

from .models import Chat

class ChatSerializer(ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'user', 'title', 'chats', 'is_private', 'is_public', 'is_forked',  'updated_at']