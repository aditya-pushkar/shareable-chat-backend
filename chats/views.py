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


@api_view(['POST'])
def share_chat_to_public(request):
    try:
        user = request.user
        data = request.data

        chat_id = data.get('chat_id')
        
        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user!=user):
            return Response({'message': "You don't have permission to access this data"}, status=status.HTTP_401_UNAUTHORIZED)

        chat_obj.is_private = False
        chat_obj.is_public = True
        chat_obj.save()
        return Response(status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def share_chat_to_private(request):
    try:
        user = request.user
        data = request.data

        chat_id = data.get('chat_id')
        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user!=user):
            return Response({'message': "You don't have permission to access this data"}, status=status.HTTP_401_UNAUTHORIZED)
        
        chat_obj.is_private = True
        chat_obj.is_public = False
        chat_obj.save()
        return Response(status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

"""
{
"chat_id": "fcce88a3-6af1-4636-a9c7-e406e792d4cc"
}
"""

@api_view(['POST'])
def add_member_to_private_chat(request):
    try:
        user = request.user
        data = request.data

        chat_id = data.get("chat_id")
        username = data.get("username")

        chat_obj = Chat.objects.get(id=chat_id)
        if(chat_obj.user!=user):
            return Response({'message': "You don't have permission to access this data"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_obj = User.objects.get(username=username)
        except ObjectDoesNotExist:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)

        chat_obj.is_public = False
        chat_obj.is_private = True
        chat_obj.save()
        chat_obj.members.add(user_obj)
        return Response({'message': 'member added'}, status=status.HTTP_200_OK)
    except Exception as error:
        return Response({"message": "Server error, Please try again later"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def read_public_chat(request, chat_id):
    try:
        try:
            chat_obj = Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return Response({"message": "Public chat not found."}, status=status.HTTP_404_NOT_FOUND)

        if not chat_obj.is_public:
            return Response({"message": "You don't have permission to access this page."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ChatSerializer(chat_obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as error:
        return Response({"message": "server error"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def read_private_chat(request, chat_id):
    try:
        user = request.user

        try:
            chat_obj = Chat.objects.get(id=chat_id)
            serializer = ChatSerializer(chat_obj)
        except ObjectDoesNotExist:
            return Response({"message": "Public chat not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not chat_obj.is_private:
            return Response({"message": "Wrong URL"}, status=status.HTTP_404_NOT_FOUND)

        if chat_obj.user==user:
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        try:
            members_obj = chat_obj.members.get(id=user.id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "You don't have permission to access this page."}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as error:
        return Response({"message": "Server Error", "error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

# make shared chat reusable for current user //means they can copy the shared chat and make their own
@api_view(['POST'])
def fork_chat(request):
    try:
        user = request.user
        chat_id = request.data.get('chat_id')

        try:
            chat_obj = Chat.objects.get(id=chat_id)
        except ObjectDoesNotExist:
            return Response({"message": "Public chat not found."}, status=status.HTTP_404_NOT_FOUND)

        # If already folked return HTTP_226_IMUSED.
        
        if chat_obj.is_private:
            try:
                members_obj = chat_obj.members.get(id=user.id)
            except ObjectDoesNotExist:
                return Response({"message": "You don't have permission to fork this chat."}, status=status.HTTP_401_UNAUTHORIZED)

            new_chat_obj = Chat.objects.create(
                user=user, 
                title=chat_obj.title,
                chats=chat_obj.chats,
                is_forked=True
            )
            new_chat_obj.save()
            return Response({"message": "Chat Forked.", "chat_id": f"{new_chat_obj.id}"}, status=status.HTTP_201_CREATED)
        
        if chat_obj.is_public:
            new_chat_obj = Chat.objects.create(
            user=user, 
            title=chat_obj.title,
            chats=chat_obj.chats,
            is_forked=True
            )
            new_chat_obj.save()
            return Response({"message": "Chat Forked.", "chat_id": f"{new_chat_obj.id}"}, status=status.HTTP_201_CREATED)

        return Response({"message": "Server Error", "error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        return Response({"message": "Server Error", "error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

