from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Chat
from .serializers import ChatSerializer


@api_view(['GET'])
def get_chats(request):
    try:
        user = request.user
        chat_object = Chat.objects.filter(user=user)
        serializer = ChatSerializer(chat_object, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({'message': 'something went wrong in server, please try again latter', 'error': f'{error}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_chat(request):
    try:
        user = request.user
        data = request.data
        
        title = data.get('title')
        chat_obj = Chat.objects.create(user=user, title=title)
        chat_obj.save()
        serializer = ChatSerializer(chat_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_chat(request):
    try:
        user = request.user
        data = request.data

        chat_id = data.get('chat_id')
        chats = data.get('chats')

        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user!=user):
            return Response({'message': "You don't have permission to access this data"}, status=status.HTTP_401_UNAUTHORIZED)
        
        chat_obj.chats = chats
        chat_obj.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


def delete_chat(request):
    pass

@api_view(['PATCH'])
def share_chat_to_public(request):
    try:
        user = request.user
        data = request.data

        chat_id = data.get('chat_id')
        
        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user!=user):
            return Response({'message': "You don't have permission to access this data"}, status=status.HTTP_401_UNAUTHORIZED)

        chat_obj.is_public = True
        chat_obj.is_private = False
        chat_obj.save()
        return Response(status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def share_chat_to_private(request):
    pass

def read_public_chat(request):
    pass

def read_private_chat(request):
    pass

# make shared chat reusable for current user //means they can copy the shared chat and make their own
def fork_chat(request):
    # if chat private ? make sure the user is included in the members list before forking the chat 
    pass

